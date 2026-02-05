from typing import Optional

from pydantic import BaseModel


class CategoryInSchema(BaseModel):
    name: str