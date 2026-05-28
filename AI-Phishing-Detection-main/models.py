from pydantic import BaseModel, Field
from typing import List, Optional

class EmailObservation(BaseModel):
    sender: str
    subject: str
    body: str
    links: List[str]
    has_attachments: bool
    spf_record: str
    dmarc_record: str
    urgency_level: str

class PhishAction(BaseModel):
    action: str = Field(description="MARK_SAFE, MOVE_TO_SPAM, QUARANTINE, BLOCK_DOMAIN")
    reasoning: str = Field(description="Brief explanation for the security decision")