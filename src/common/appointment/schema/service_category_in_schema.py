from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ServiceCategoryInSchema(BaseModel):
    category_id: Optional[str] = None
    service_id: Optional[str] = None
