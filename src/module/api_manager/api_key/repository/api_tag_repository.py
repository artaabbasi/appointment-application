from common.lib.base_respository import BaseRepository
from module.api_manager.api_key.entity.api_tag_entity import ApiTagEntity


class ApiTagRepository(BaseRepository):
    def __init__(self):
        super().__init__(ApiTagEntity)
