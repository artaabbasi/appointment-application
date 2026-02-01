from typing import Optional

from pydantic import BaseModel

from common.lib.base_output_model import BaseOutputModel


class ServiceSchema(BaseOutputModel):
    main_service_id: str
    name: str
    duration: int