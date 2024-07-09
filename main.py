from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
from sqlalchemy import or_
from datetime import datetime
from base_models import SessionLocal, User, UserCreate, UserUpdate

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
        
# API endpoints
@app.post("/add_users")
async def create_user(user: UserCreate, db: SessionLocal = Depends(get_db)):
    # Convert dob from string to date object
    if user.dob:
        try:
            user.dob = datetime.strptime(user.dob, "%Y-%m-%d").date()
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid date format. Expected format: YYYY-MM-DD")
    else:
        user.dob = datetime.now().date()
    username = user.email if user.email else user.mobile_number if user.mobile_number else False
    check_user = db.query(User).filter(
        or_(
            User.email == username,
            User.mobile_number == username
        )
    ).all()
    if check_user:
        raise HTTPException(status_code=400, detail=f"{username} already exists")
    if not check_user:
        raise HTTPException(status_code=400, detail=f"Please provide email or mobile number to create user.")
    
    db_user = User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user


@app.get("/get_users")
async def get_users(db: SessionLocal = Depends(get_db)):
    return db.query(User).all()


@app.patch("/update_users/{user_id}")
async def update_user(user_id: int, user: UserUpdate, db: SessionLocal = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.delete("/delete_users/{user_id}")
async def delete_user(user_id: int, db: SessionLocal = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
    return {"detail": "User deleted"}