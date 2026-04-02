from sqlalchemy.orm import Session

from app.core.security import get_password_hash
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate


def get_user(db: Session, user_id: int) -> User | None:
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()


def get_users(db: Session) -> list[User]:
    return db.query(User).order_by(User.id).all()


def create_user(db: Session, user_in: UserCreate) -> User:
    user = User(
        email=user_in.email,
        hashed_password=get_password_hash(user_in.password),
        role=user_in.role,
        is_active=True,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def update_user(db: Session, user: User, updates: UserUpdate) -> User:
    if updates.role is not None:
        user.role = updates.role
    if updates.is_active is not None:
        user.is_active = updates.is_active
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
