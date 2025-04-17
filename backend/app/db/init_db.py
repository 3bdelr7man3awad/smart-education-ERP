from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.base import Base
from app.db.session import engine
from app.models.user import User, UserRole
from app.core.security import get_password_hash

def init_db(db: Session) -> None:
    # Create tables
    Base.metadata.create_all(bind=engine)

    # Create default admin user if it doesn't exist
    user = db.query(User).filter(User.email == "admin@example.com").first()
    if not user:
        user = User(
            email="admin@example.com",
            hashed_password=get_password_hash("admin123"),
            full_name="System Admin",
            role=UserRole.ADMIN,
            is_superuser=True
        )
        db.add(user)
        db.commit()
        db.refresh(user) 