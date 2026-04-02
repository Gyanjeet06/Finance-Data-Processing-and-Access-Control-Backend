from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_active_user, require_roles
from app.crud.crud_user import create_user, get_user, get_user_by_email, get_users, update_user
from app.schemas.user import UserCreate, UserRead, UserUpdate

router = APIRouter()


@router.post("/", response_model=UserRead, summary="Register a new user")
def register_user(user_in: UserCreate, db: Session = Depends(get_db)):
    if get_user_by_email(db, user_in.email):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    user_in.role = "viewer"
    return create_user(db, user_in)


@router.get("/me", response_model=UserRead, summary="Get current user")
def read_current_user(current_user=Depends(get_current_active_user)):
    return current_user


@router.get("/", response_model=list[UserRead], summary="List all users")
def list_users(db: Session = Depends(get_db), _=Depends(require_roles("admin"))):
    return get_users(db)


@router.patch("/{user_id}", response_model=UserRead, summary="Update user role or status")
def modify_user(user_id: int, updates: UserUpdate, db: Session = Depends(get_db), _=Depends(require_roles("admin"))):
    user = get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return update_user(db, user, updates)
