"""
Send Data Email Tool

Sends a configurable set of data fields — extracted by the AI during the call —
to a recipient email address. Fields, recipient, subject, and description are
all defined in ai-agent.yaml, making this tool reusable for any data-collection
use case without code changes.

Example use cases:
  - Machine identifier + city  → maintenance team
  - Client ID + Gmail address  → registration team
  - Order number + complaint   → support team

Config (ai-agent.yaml):
  tools:
    send_data_email:
      enabled: true
      description: "Send the machine ID and city collected during the call."
      recipient_email: "team@company.com"
      from_email: "agent@company.com"
      from_name: "AI Voice Agent"
      subject: "Call Data Report"
      provider: auto          # auto | resend | smtp
      fields:
        - name: machine_id
          description: "The machine identifier mentioned by the caller."
          required: true
        - name: city
          description: "The city where the machine is located."
          required: false
"""

import asyncio
import html
from typing import Any, Dict, List, Optional

import structlog

from src.tools.base import Tool, ToolCategory, ToolDefinition, ToolParameter
from src.tools.business.email_dispatcher import resolve_context_value, send_email
from src.tools.business.email_templates import DEFAULT_SEND_DATA_EMAIL_HTML_TEMPLATE
from src.tools.business.template_renderer import render_html_template_with_fallback
from src.tools.context import ToolExecutionContext

logger = structlog.get_logger(__name__)

_TOOL_NAME = "send_data_email"


def _load_tool_config() -> Dict[str, Any]:
    """Load this tool's config section without relying on self.definition (avoids recursion)."""
    try:
        from src.config import load_config

        config = load_config()
        return config.get("tools", {}).get(_TOOL_NAME, {})
    except Exception as e:
        logger.warning("Failed to load send_data_email config", error=str(e))
        return {}


class SendDataEmailTool(Tool):
    """
    Generic in-call tool that emails data collected during a conversation.

    The set of fields the AI collects (and their descriptions) is defined
    entirely in ai-agent.yaml, so the same tool class handles different
    data-collection scenarios with no code changes.
    """

    @property
    def definition(self) -> ToolDefinition:
        config = _load_tool_config()
        field_defs: List[Dict[str, Any]] = config.get("fields", [])

        parameters: List[ToolParameter] = []
        for f in field_defs:
            name = str(f.get("name", "")).strip()
            if not name:
                continue
            parameters.append(
                ToolParameter(
                    name=name,
                    type=str(f.get("type", "string")),
                    description=str(f.get("description", f"Value for {name}")),
                    required=bool(f.get("required", True)),
                )
            )

        # Fallback when no fields are configured: accept a plain data string.
        if not parameters:
            parameters = [
                ToolParameter(
                    name="data",
                    type="string",
                    description="The data to include in the email.",
                    required=True,
                )
            ]

        description = str(
            config.get(
                "description",
                "Send the data collected during the call to the configured email address.",
            )
        )

        return ToolDefinition(
            name=_TOOL_NAME,
            description=description,
            category=ToolCategory.BUSINESS,
            parameters=parameters,
        )

    async def execute(
        self,
        parameters: Dict[str, Any],
        context: ToolExecutionContext,
    ) -> Dict[str, Any]:
        call_id = context.call_id

        try:
            config = context.get_config_value(f"tools.{_TOOL_NAME}", {})

            if not config.get("enabled", False):
                logger.info("send_data_email disabled, skipping", call_id=call_id)
                return {"status": "skipped", "message": "Data email tool is disabled."}

            # Resolve context_name for per-context overrides (admin_email_by_context, etc.)
            session = await context.get_session()
            context_name: Optional[str] = (
                getattr(session, "context_name", None) if session else context.context_name
            )

            email_data = self._build_email(parameters, config, context_name, call_id)

            # Fire-and-forget — do not block the AI response.
            asyncio.create_task(self._send_async(email_data, call_id, config))

            logger.info(
                "Data email scheduled",
                call_id=call_id,
                recipient=email_data["to"],
                fields=list(parameters.keys()),
            )

            return {
                "status": "success",
                "message": "The data has been sent by email.",
            }

        except Exception as e:
            logger.error(
                "Failed to schedule data email",
                call_id=call_id,
                error=str(e),
                exc_info=True,
            )
            return {"status": "error", "message": f"Failed to send data email: {e}"}

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _build_email(
        self,
        fields: Dict[str, Any],
        config: Dict[str, Any],
        context_name: Optional[str],
        call_id: str,
    ) -> Dict[str, Any]:
        """Build the email payload from collected fields and config."""

        recipient = resolve_context_value(
            tool_config=config,
            key="recipient_email",
            context_name=context_name,
            default="admin@company.com",
        )
        from_email = resolve_context_value(
            tool_config=config,
            key="from_email",
            context_name=context_name,
            default=config.get("from_email", "agent@company.com"),
        )
        from_name = config.get("from_name", "AI Voice Agent")
        subject = resolve_context_value(
            tool_config=config,
            key="subject",
            context_name=context_name,
            default="Data from call",
        )

        # fields_list lets the default template iterate with autoescape intact.
        # Individual field values are also available as top-level variables so
        # custom html_template overrides can reference them directly, e.g. {{ machine_id }}.
        variables: Dict[str, Any] = {
            "call_id": call_id,
            "context_name": context_name or "",
            "subject": subject,
            "fields_list": list(fields.items()),
            **{k: v for k, v in fields.items()},
        }

        html_content = render_html_template_with_fallback(
            template_override=config.get("html_template"),
            default_template=DEFAULT_SEND_DATA_EMAIL_HTML_TEMPLATE,
            variables=variables,
            call_id=call_id,
            tool_name=_TOOL_NAME,
        )

        return {
            "to": recipient,
            "from": f"{from_name} <{from_email}>",
            "subject": subject,
            "html": html_content,
        }

    async def _send_async(
        self,
        email_data: Dict[str, Any],
        call_id: str,
        config: Dict[str, Any],
    ) -> None:
        try:
            await send_email(
                email_data=email_data,
                tool_config=config,
                call_id=call_id,
                log_label="Data email",
                recipient=str(email_data.get("to") or ""),
            )
        except Exception as e:
            logger.error(
                "Failed to send data email",
                call_id=call_id,
                recipient=email_data.get("to"),
                error=str(e),
                exc_info=True,
            )
