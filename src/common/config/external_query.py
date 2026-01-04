from common.lib.base_service import BaseService


class ExternalQuery(BaseService):

    @property
    def sample_query(self) -> str:
        return "SELECT * FROM sample_db"
