"""
Business tools package.

Contains tools for business operations like email, calendar, CRM, etc.
"""

from src.tools.business.email_summary import SendEmailSummaryTool
from src.tools.business.request_transcript import RequestTranscriptTool
from src.tools.business.send_data_email import SendDataEmailTool

__all__ = [
    "SendEmailSummaryTool",
    "RequestTranscriptTool",
    "SendDataEmailTool",
]

try:
    from src.tools.business.gcal_tool import GCalendarTool
    __all__.append("GCalendarTool")
except ImportError:
    pass
