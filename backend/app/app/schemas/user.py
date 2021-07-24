from datetime import datetime
from app.core.products import Plan
from typing import Optional

from pydantic import BaseModel, EmailStr


# Shared properties
class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = True
    is_superuser: bool = False
    full_name: Optional[str] = None


# Properties to receive via API on creation
class UserCreate(UserBase):
    email: EmailStr
    password: str


# Properties to receive via API on update
class UserUpdate(UserBase):
    password: Optional[str] = None


class UserStripeInfoUpdate(BaseModel):
    stripe_customer_id: str
    active_plan: Optional[Plan]
    stripe_subscription_ref: Optional[str]
    last_paid: Optional[datetime]


class UserInDBBase(UserBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


# Additional properties to return via API
class User(UserInDBBase):
    active_plan: Plan


# Additional properties stored in DB
class UserInDB(UserInDBBase):
    hashed_password: str
