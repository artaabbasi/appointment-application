from typing import Optional

from pydantic import BaseModel


class ServiceInSchema(BaseModel):
    main_service_id: str
    name: str
    duration: int