from typing import Optional

from pydantic import BaseModel


class PaginationSchema(BaseModel):
    page: Optional[int] = 1
    size: Optional[int] = 10
