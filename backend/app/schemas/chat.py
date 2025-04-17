from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

class ChatBase(BaseModel):
    name: Optional[str] = None
    is_group: bool = False
    participant_ids: List[int]

class ChatCreate(ChatBase):
    pass

class ChatUpdate(ChatBase):
    pass

class ChatInDB(ChatBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class MessageBase(BaseModel):
    content: str

class MessageCreate(MessageBase):
    pass

class MessageUpdate(MessageBase):
    pass

class MessageAttachmentBase(BaseModel):
    file_name: str
    file_type: str
    file_url: str
    file_size: int

class MessageAttachmentInDB(MessageAttachmentBase):
    id: int
    message_id: int
    created_at: datetime

    class Config:
        from_attributes = True

class MessageInDB(MessageBase):
    id: int
    chat_id: int
    sender_id: int
    is_read: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    attachments: List[MessageAttachmentInDB] = []

    class Config:
        from_attributes = True

class ChatWithMessages(ChatInDB):
    messages: List[MessageInDB] = []
    participants: List[int] = [] 