from typing import List, Optional, Union, Dict, Any
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.core.security import get_password_hash, verify_password
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.core.tenant import get_tenant_id

class UserService:
    @staticmethod
    def get_user(db: Session, user_id: int) -> Optional[User]:
        """
        Get a user by ID.
        """
        tenant_id = get_tenant_id()
        query = db.query(User).filter(User.id == user_id)
        
        # If tenant context is set, filter by tenant
        if tenant_id:
            query = query.filter(User.organization_id == tenant_id)
            
        return query.first()

    @staticmethod
    def get_user_by_email(db: Session, email: str) -> Optional[User]:
        """
        Get a user by email.
        """
        tenant_id = get_tenant_id()
        query = db.query(User).filter(User.email == email)
        
        # If tenant context is set, filter by tenant
        if tenant_id:
            query = query.filter(User.organization_id == tenant_id)
            
        return query.first()

    @staticmethod
    def get_users(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        active_only: bool = False
    ) -> List[User]:
        """
        Get all users.
        """
        tenant_id = get_tenant_id()
        query = db.query(User)
        
        # If tenant context is set, filter by tenant
        if tenant_id:
            query = query.filter(User.organization_id == tenant_id)
            
        if active_only:
            query = query.filter(User.is_active == True)
            
        return query.offset(skip).limit(limit).all()

    @staticmethod
    def create_user(db: Session, user_in: UserCreate) -> User:
        """
        Create a new user.
        """
        # Check if user with same email already exists
        existing_user = UserService.get_user_by_email(db, email=user_in.email)
        if existing_user:
            raise HTTPException(
                status_code=400,
                detail="User with this email already exists"
            )
        
        # Get tenant ID from context
        tenant_id = get_tenant_id()
        
        # Create user
        user = User(
            email=user_in.email,
            hashed_password=get_password_hash(user_in.password),
            full_name=user_in.full_name,
            is_active=user_in.is_active,
            is_superuser=user_in.is_superuser,
            organization_id=tenant_id or user_in.organization_id
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def update_user(
        db: Session,
        user_id: int,
        user_in: Union[UserUpdate, Dict[str, Any]]
    ) -> User:
        """
        Update a user.
        """
        user = UserService.get_user(db, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        update_data = user_in.dict(exclude_unset=True) if isinstance(user_in, UserUpdate) else user_in
        
        # Don't allow changing organization_id if tenant context is set
        tenant_id = get_tenant_id()
        if tenant_id and "organization_id" in update_data:
            del update_data["organization_id"]
        
        # Update password if provided
        if "password" in update_data:
            update_data["hashed_password"] = get_password_hash(update_data.pop("password"))
        
        for field, value in update_data.items():
            setattr(user, field, value)
        
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def delete_user(db: Session, user_id: int) -> None:
        """
        Delete a user.
        """
        user = UserService.get_user(db, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        db.delete(user)
        db.commit()

    @staticmethod
    def authenticate(db: Session, email: str, password: str) -> Optional[User]:
        """
        Authenticate a user.
        """
        user = UserService.get_user_by_email(db, email=email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user 