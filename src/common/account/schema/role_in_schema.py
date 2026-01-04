from typing import Optional

from pydantic import BaseModel


class RoleInSchema(BaseModel):
    name: Optional[str] = None
    title: Optional[str] = None
    show_in_site: Optional[bool] = None
