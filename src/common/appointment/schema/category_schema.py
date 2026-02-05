from typing import Optional

from pydantic import BaseModel

from common.lib.base_output_model import BaseOutputModel


class CategorySchema(BaseOutputModel):
    name: str