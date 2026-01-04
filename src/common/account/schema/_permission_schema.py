from typing import Optional

from pydantic import BaseModel


class _PermissionSchema(BaseModel):
    id: str
    had_access_to_all: Optional[bool] = False
