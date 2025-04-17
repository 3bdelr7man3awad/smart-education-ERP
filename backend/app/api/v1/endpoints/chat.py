from typing import List
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user
from app.services.chat_service import ChatService
from app.schemas.chat import (
    ChatCreate,
    ChatInDB,
    ChatWithMessages,
    MessageCreate,
    MessageInDB
)
from app.models.user import User

router = APIRouter()

@router.post("/", response_model=ChatInDB)
async def create_chat(
    chat_data: ChatCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new chat"""
    return await ChatService.create_chat(db, chat_data, current_user)

@router.get("/", response_model=List[ChatInDB])
async def get_chats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all chats for the current user"""
    return await ChatService.get_user_chats(db, current_user)

@router.get("/{chat_id}", response_model=ChatWithMessages)
async def get_chat(
    chat_id: int,
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get a specific chat with its messages"""
    chat = await ChatService.get_chat_messages(db, chat_id, current_user, skip, limit)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    return chat

@router.post("/{chat_id}/messages", response_model=MessageInDB)
async def send_message(
    chat_id: int,
    message_data: MessageCreate,
    files: List[UploadFile] = File(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Send a message in a chat"""
    message = await ChatService.send_message(db, chat_id, message_data, current_user, files)
    if not message:
        raise HTTPException(status_code=404, detail="Chat not found")
    return message

@router.post("/{chat_id}/read")
async def mark_messages_as_read(
    chat_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Mark all messages in a chat as read"""
    success = await ChatService.mark_messages_as_read(db, chat_id, current_user)
    if not success:
        raise HTTPException(status_code=404, detail="Chat not found")
    return {"status": "success"}

@router.delete("/messages/{message_id}")
async def delete_message(
    message_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a message"""
    success = await ChatService.delete_message(db, message_id, current_user)
    if not success:
        raise HTTPException(status_code=404, detail="Message not found")
    return {"status": "success"} 