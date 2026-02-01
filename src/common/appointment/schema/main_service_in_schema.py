from typing import Optional

from pydantic import BaseModel


class MainServiceInSchema(BaseModel):
    name: str