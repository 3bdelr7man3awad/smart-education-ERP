from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import UploadFile
from app.models.chat import Chat, Message, MessageAttachment
from app.models.user import User
from app.core.security import get_current_user
from app.schemas.chat import ChatCreate, MessageCreate
from app.core.storage import save_file

class ChatService:
    @staticmethod
    async def create_chat(db: Session, chat_data: ChatCreate, current_user: User) -> Chat:
        chat = Chat(
            name=chat_data.name,
            is_group=chat_data.is_group
        )
        chat.participants.append(current_user)
        for participant_id in chat_data.participant_ids:
            participant = db.query(User).filter(User.id == participant_id).first()
            if participant:
                chat.participants.append(participant)
        
        db.add(chat)
        db.commit()
        db.refresh(chat)
        return chat

    @staticmethod
    async def get_user_chats(db: Session, current_user: User) -> List[Chat]:
        return db.query(Chat).filter(Chat.participants.contains(current_user)).all()

    @staticmethod
    async def get_chat_messages(
        db: Session,
        chat_id: int,
        current_user: User,
        skip: int = 0,
        limit: int = 50
    ) -> List[Message]:
        chat = db.query(Chat).filter(Chat.id == chat_id).first()
        if not chat or current_user not in chat.participants:
            return []
        
        return db.query(Message).filter(
            Message.chat_id == chat_id
        ).order_by(Message.created_at.desc()).offset(skip).limit(limit).all()

    @staticmethod
    async def send_message(
        db: Session,
        chat_id: int,
        message_data: MessageCreate,
        current_user: User,
        files: List[UploadFile] = None
    ) -> Message:
        chat = db.query(Chat).filter(Chat.id == chat_id).first()
        if not chat or current_user not in chat.participants:
            return None

        message = Message(
            chat_id=chat_id,
            sender_id=current_user.id,
            content=message_data.content
        )
        db.add(message)
        db.commit()
        db.refresh(message)

        if files:
            for file in files:
                file_url = await save_file(file)
                attachment = MessageAttachment(
                    message_id=message.id,
                    file_name=file.filename,
                    file_type=file.content_type,
                    file_url=file_url,
                    file_size=file.size
                )
                db.add(attachment)
            db.commit()

        return message

    @staticmethod
    async def mark_messages_as_read(
        db: Session,
        chat_id: int,
        current_user: User
    ) -> bool:
        messages = db.query(Message).filter(
            Message.chat_id == chat_id,
            Message.sender_id != current_user.id,
            Message.is_read == False
        ).all()
        
        for message in messages:
            message.is_read = True
        
        db.commit()
        return True

    @staticmethod
    async def delete_message(
        db: Session,
        message_id: int,
        current_user: User
    ) -> bool:
        message = db.query(Message).filter(Message.id == message_id).first()
        if not message or message.sender_id != current_user.id:
            return False
        
        db.delete(message)
        db.commit()
        return True 