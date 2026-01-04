from pydantic import BaseModel


class ApiTokenResponseSchema(BaseModel):
    token: str
