import pandas as pd
import os
from common.lib.base_service import BaseService


# TODO: composition
class DatasetImportUtil(BaseService):
    def __init__(self):
        self._base_excel_directory = self._get_settings().BASE_EXCEL_DIRECTORY

    @staticmethod
    async def _file_path(base_directory: str, file_name: str) -> str:
        return os.path.join(base_directory, file_name)

    @staticmethod
    async def get_data_frame_shape(df: pd.DataFrame) -> tuple[int, int]:
        return df.shape

    async def _get_excel_file_path(self, file_name: str) -> str:
        return await self._file_path(self._base_excel_directory, file_name)

    async def get_data_frame_from_path(self, file_path: str, sheet_name) -> pd.DataFrame:
        if ".xlsx" in file_path:
            data_frame = pd.read_excel(file_path, sheet_name=sheet_name)
        elif ".csv" in file_path:
            data_frame = pd.read_csv(file_path)
        else:
            raise FileNotFoundError
        if type(data_frame) == pd.DataFrame:
            return data_frame
        else:
            for _, data_frame in data_frame.items():
                return data_frame

    async def get_excel_dataset(self, dataset_name: str, sheet_name: str = None) -> pd.DataFrame:
        file_path = await self._get_excel_file_path(dataset_name)
        return await self.get_data_frame_from_path(file_path, sheet_name)
