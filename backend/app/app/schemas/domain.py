from typing import Optional

from pydantic import BaseModel


# Shared properties
class DomainBase(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None


# Properties to receive on item creation
class DomainCreate(DomainBase):
    title: str


# Properties to receive on item update
class DomainUpdate(DomainBase):
    pass


# Properties shared by models stored in DB
class DomainInDBBase(DomainBase):
    id: int
    title: str
    owner_id: int

    class Config:
        orm_mode = True


# Properties to return to client
class Domain(DomainInDBBase):
    pass


# Properties properties stored in DB
class DomainInDB(DomainInDBBase):
    pass
