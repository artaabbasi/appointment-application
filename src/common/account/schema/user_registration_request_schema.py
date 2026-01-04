from pydantic import BaseModel


class UserRegistrationRequestSchema(BaseModel):
    phone_number: str = None
