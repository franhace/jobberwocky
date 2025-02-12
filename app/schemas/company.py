from pydantic import BaseModel


class CompanyBase(BaseModel):
    name: str

class Company(CompanyBase):
    id: int

    class Config:
        orm_mode = True
        from_attributes = True