from typing import Optional

from pydantic import BaseModel


class DefaultSchema(BaseModel):
    customer_id: Optional[str] = None