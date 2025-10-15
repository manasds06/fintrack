from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from ..core.database import get_db
from ..core.security import hash_password, verify_password, create_access_token
from ..table_models.user_model import UserTable
from ..validation_schemas.users import User, UserCreate, UserLogin


# Creates a mini API
router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

# POST method at /user endpoint for user to create account
@router.post("/register", response_model=User)
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(UserTable).filter(UserTable.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username unavailable")

    hashed_pw = hash_password(user.password)
    new_user = UserTable(username=user.username, hashed_password=hashed_pw)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(UserTable).filter(UserTable.username == user.username).first()
    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    if not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    token = create_access_token({"sub": db_user.username})
    return {"access_token": token, "token_type": "bearer"}
