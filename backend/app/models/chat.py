from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime, Boolean, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base_class import Base

# Association table for chat participants
chat_participants = Table(
    'chat_participants',
    Base.metadata,
    Column('chat_id', Integer, ForeignKey('chats.id'), primary_key=True),
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True)
)

class Chat(Base):
    __tablename__ = "chats"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=True)  # For group chats
    is_group = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    participants = relationship("User", secondary=chat_participants, backref="chats")
    messages = relationship("Message", back_populates="chat")

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    chat_id = Column(Integer, ForeignKey("chats.id"), nullable=False)
    sender_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    content = Column(Text, nullable=False)
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    chat = relationship("Chat", back_populates="messages")
    sender = relationship("User", backref="sent_messages")
    attachments = relationship("MessageAttachment", back_populates="message")

class MessageAttachment(Base):
    __tablename__ = "message_attachments"

    id = Column(Integer, primary_key=True, index=True)
    message_id = Column(Integer, ForeignKey("messages.id"), nullable=False)
    file_name = Column(String, nullable=False)
    file_type = Column(String, nullable=False)
    file_url = Column(String, nullable=False)
    file_size = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    message = relationship("Message", back_populates="attachments") 