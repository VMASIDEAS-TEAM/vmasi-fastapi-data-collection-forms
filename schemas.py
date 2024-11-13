from pydantic import BaseModel, EmailStr

class FormData(BaseModel):
    action: str
    name: str
    phone: str
    email: EmailStr
    privacyCheck: bool
    city: str
    campaign: int
