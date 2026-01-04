import asyncio
import mimetypes
import os
import shutil
from asyncio import gather
from io import BytesIO
from os import access
from typing import Optional, Union, List
from uuid import uuid4

from PIL.Image import Image, open as PIL_open, new as PIL_new
from fastapi import UploadFile
from fastapi.responses import FileResponse

from common.account.enum.admin_roles_enum import AdminRolesEnum
from common.exceptions import ForbiddenException, BadRequestException, NotFoundException
from common.file_manager.enum.file_access_type_enum import FileAccessTypeEnum
from common.file_manager.enum.folder_accesses_enum import FolderAccessesEnum
from common.file_manager.schema.file_info_schema import FileInfoSchema
from common.file_manager.schema.file_meta_data_schema import FileMetaDataSchema
from common.file_manager.schema.file_upload_schema import FileUploadSchema
from common.file_manager.schema.folder_schema import FolderSchema
from common.lib.base_service import BaseService
from module.account.user.service import CustomerService
from module.file_manager.bucket.entity.file_entity import FileEntity
from module.file_manager.bucket.entity.file_meta_data_entity import FileMetaDataEntity
from module.file_manager.bucket.entity.folder_entity import FolderEntity
from module.file_manager.bucket.enum.error_code_enum import FileErrorCodeEnum
from module.file_manager.bucket.repository.file_meta_data_repository import FileMetaDataRepository
from module.file_manager.bucket.repository.file_repository import FileRepository
from module.file_manager.bucket.repository.folder_access_repository import FolderAccessRepository
from module.file_manager.bucket.repository.folder_repository import FolderRepository
from module.file_manager.bucket.service.folder_access_service import FolderAccessService
from util.timestamp import DatetimeUtil
from util.yaml_util import YamlUtil
from util.logger import get_custom_logger

logger = get_custom_logger(__name__)


class FileService(BaseService):

    def __init__(self):
        self.file_repository = FileRepository()
        self.folder_repository = FolderRepository()
        self.file_meta_data_repository = FileMetaDataRepository()
        self.folder_access_service = FolderAccessService()
        self.file_storage_path = self._get_settings().MEDIA_DIRECTORY
        self.acceptable_mime_types = self.load_mime_types()

    async def _aggregate_schema(self, schema: Union[FolderSchema, list[FolderSchema], any],
                                meta_data_is_null: Optional[bool] = None):
        if not schema:
            return schema
        if isinstance(schema, list):
            schema = await asyncio.gather(
                *[
                    self._aggregate_schema(item, meta_data_is_null) for item in schema
                ]
            )
        else:
            folders, files, file_count = await asyncio.gather(self.get_folders_list(schema.id,
                                                                                    meta_data_is_null=meta_data_is_null),
                                                              self.get_folder_files_info(schema.id,
                                                                                         meta_data_is_null
                                                                                         ),
                                                              self.get_folder_files_count(schema.id,
                                                                                          meta_data_is_null
                                                                                          )
                                                              )
            schema.folders = folders
            schema.files = files
            schema.file_count = file_count
        return schema

    async def _aggregate_file_schema(self, schema: Union[FileInfoSchema, list[FileInfoSchema], any]):
        if not schema:
            return schema
        if isinstance(schema, list):
            schema = await asyncio.gather(
                *[
                    self._aggregate_file_schema(item) for item in schema
                ]
            )
        else:
            meta_data = await self.file_meta_data_repository.get_by_file_id(schema.id)
            if meta_data is not None:
                meta_data = meta_data.convert_to_schema()
                (meta_data.producer_user, meta_data.controller_user,
                 meta_data.confirmer_user, meta_data.approver_user) = await gather(
                    CustomerService().get_not_detailed_user_by_id(meta_data.producer_user_id),
                    CustomerService().get_not_detailed_user_by_id(meta_data.controller_user_id),
                    CustomerService().get_not_detailed_user_by_id(meta_data.confirmer_user_id),
                    CustomerService().get_not_detailed_user_by_id(meta_data.approver_user_id),
                )
                schema.meta_data = meta_data
        return schema

    def load_mime_types(self) -> list:
        config = YamlUtil.get_value(self._get_settings().MIME_TYPES_FILE, 'acceptable_mime_types')
        return config

    async def is_mime_type_acceptable(self, mime_type: str) -> bool:
        return mime_type in self.acceptable_mime_types

    async def save_file_for_user(self,
                                 file: bytes,
                                 file_data: FileUploadSchema,
                                 user_id: str
                                 ):
        if user_id is None:
            user_id = 'unknown'
        folder_names = []
        if file_data.folder_names:
            folder_names = file_data.folder_names.split('/')
        folder = await self.folder_repository.fetch_by_names_and_user_id([user_id] + folder_names, user_id)
        return await self.save_file(
            file=file,
            file_name=file_data.file_name,
            folder_id=folder.id,
            user_id=user_id,
            access_type=file_data.access_type,
            reduce_quality=file_data.reduce_quality,
        )

    async def upload_file_for_user(self, file: UploadFile, file_data: FileUploadSchema,
                                   user_id: Optional[str]) -> FileInfoSchema:
        if user_id is None:
            user_id = 'unknown'
        folder_names = []
        if file_data.folder_names:
            folder_names = file_data.folder_names.split('/')
        folder = await self.folder_repository.fetch_by_names_and_user_id(["USER_FILES", user_id] + folder_names, user_id)
        return await self.save_file(
            file=await file.read(),
            file_name=file_data.file_name or file.filename,
            folder_id=folder.id,
            user_id=user_id,
            access_type=file_data.access_type,
            reduce_quality=file_data.reduce_quality,
        )

    async def upload_file(self, file: UploadFile, file_data: FileUploadSchema, user_id: str, staff_role: AdminRolesEnum) -> FileInfoSchema:
        if staff_role == AdminRolesEnum.supporter:
            folder = await self.folder_repository.fetch_by_id(file_data.folder_id)
            if folder.user_id != user_id:
                if not await self.folder_access_service.user_has_access_to_folder(
                        FolderAccessesEnum.CREATE_FILE,
                        user_id,
                        file_data.folder_id
                ):
                    raise ForbiddenException(FileErrorCodeEnum.FOLDER_NOT_FOR_USER)
        return await self.save_file(
            file=await file.read(),
            file_name=file_data.file_name or file.filename,
            folder_id=file_data.folder_id,
            user_id=user_id,
            access_type=file_data.access_type,
            reduce_quality=file_data.reduce_quality,
        )

    async def get_file_info(self, file_id: str) -> FileInfoSchema:
        file_entity = await self.file_repository.fetch_by_id(file_id)
        return file_entity.get_info_schema()

    async def get_folder_files_info(self,
                                    folder_id: str,
                                    meta_data_is_null: Optional[bool] = None) -> List[FileInfoSchema]:
        file_entities = await self.file_repository.get_by_folder_id(folder_id, meta_data_is_null)
        return await self._aggregate_file_schema([file_entity.get_info_schema() for file_entity in file_entities])

    async def get_folder_files_count(self,
                                     folder_id: str,
                                     meta_data_is_null: Optional[bool] = None) -> int:
        count = await self.file_repository.get_count_by_folder_id(folder_id, meta_data_is_null)
        return count

    async def get_folder_folders_info(self,
                                      user_id: str, staff_role: AdminRolesEnum,
                                      folder_id: str,
                                      meta_data_is_null: Optional[bool] = None) -> List[FolderSchema]:
        folder_ids = None
        if staff_role == AdminRolesEnum.supporter:
            access_folder_ids = await self.folder_access_service.get_folder_ids_for_user(user_id)
            user_folders = await self.folder_repository.get_by_user_id(user_id)
            folder_ids = access_folder_ids + [user_folder.id for user_folder in user_folders]
        folder_entities = await self.folder_repository.get_by_parent_folder_id(folder_id, folder_ids)
        folder_schemas = []
        for folder_schema in [folder_entity.convert_to_schema() for folder_entity in folder_entities]:
            count = await self.get_folder_files_count(folder_schema.id, meta_data_is_null)
            folder_schema.file_count = count
            folder_schemas.append(folder_schema)
        return folder_schemas

    async def get_file_for_user(self, file_id: str, user_id: Optional[str] = None) -> FileResponse:
        file_entity = await self.file_repository.fetch_by_id(file_id)

        if file_entity.access_type == FileAccessTypeEnum.PUBLIC:
            pass
        elif file_entity.access_type == FileAccessTypeEnum.PRIVATE:
            if file_entity.user_id != user_id:
                raise ForbiddenException(FileErrorCodeEnum.FILE_IS_PRIVATE)
        else:
            if user_id is None:
                raise ForbiddenException(FileErrorCodeEnum.FILE_IS_LOCAL)
        return await self.get_file_response(file_entity)

    async def get_file_for_admin(self, file_id: str) -> FileResponse:
        file_entity = await self.file_repository.fetch_by_id(file_id)
        return await self.get_file_response(file_entity)

    async def get_file_response_from_file_id(self, file_id: str) -> FileResponse:
        file_entity = await self.file_repository.fetch_by_id(file_id)
        return await self.get_file_response(file_entity)

    async def get_file_response(self, file_entity: FileEntity) -> FileResponse:
        return FileResponse(path=file_entity.file_path,
                            media_type=file_entity.mime_type,
                            filename=file_entity.name)

    async def save_file(
            self,
            file: bytes,
            file_name: str,
            folder_id: str,
            access_type: str,
            reduce_quality: bool = True,
            user_id: Optional[str] = None,
    ) -> FileInfoSchema:
        folder_entity = await self.folder_repository.fetch_by_id(folder_id)
        folder_path = await self.build_folder_path(folder_entity)
        full_path = os.path.join(self.file_storage_path, folder_path)
        os.makedirs(full_path, exist_ok=True)
        file_path = os.path.join(full_path, f"{file_name}?{DatetimeUtil.utc_now_timestamp()}")

        mime_type, _ = mimetypes.guess_type(file_name)
        if mime_type is None:
            mime_type = "application/octet-stream"  # Default MIME type if unknown

        if not await self.is_mime_type_acceptable(mime_type):
            raise BadRequestException(FileErrorCodeEnum.FILE_TYPE_NOT_ALLOWED)

        if await self.is_image(mime_type) and reduce_quality:
            try:
                file = await self.reduce_image_quality(file)
            except Exception as e:
                logger.error(f"Error in reducing image quality: {e}")

        with open(file_path, "wb") as f:
            f.write(file)

        size = os.path.getsize(file_path)

        file_entity = FileEntity(
            folder_id=folder_id,
            user_id=user_id,
            access_type=access_type,
            name=file_name,
            file_path=str(file_path),
            size=size,
            mime_type=mime_type
        )

        await self.file_repository.create(file_entity)

        return file_entity.get_info_schema()

    async def build_folder_path(self, folder_entity: FolderEntity) -> str:
        if folder_entity.parent_folder_id is not None:
            try:
                parent_folder = await self.folder_repository.fetch_by_id(folder_entity.parent_folder_id)
                parent_path = await self.build_folder_path(parent_folder)
                return os.path.join(parent_path, folder_entity.name)
            except NotFoundException:
                pass
        return folder_entity.name

    async def is_image(self, mime_type: str) -> bool:
        return mime_type.startswith("image/")

    async def reduce_image_quality(self, file: bytes, quality: Optional[int] = None) -> bytes:
        image = PIL_open(BytesIO(file))
        buffer = BytesIO()
        image = image.convert('RGB')
        if image.mode in ('RGBA', 'LA'):
            background = PIL_new(image.mode[:-1], image.size, '#fff')
            background.paste(image, image.split()[-1])
            image = background
        file_size = len(file)
        if quality is None:
            if file_size <= 500000:
                quality = 50
            elif 500000 < file_size <= 1000000:
                quality = 40
            else:
                quality = 20
        image.save(buffer, format='JPEG', quality=quality)
        return buffer.getvalue()

    async def delete_file(self, file_id: str, user_id: Optional[str] = None) -> None:
        file_entity = await self.file_repository.fetch_by_id(file_id)
        if file_entity.user_id != user_id:
            raise ForbiddenException(FileErrorCodeEnum.FILE_IS_PRIVATE)
        try:
            os.remove(file_entity.file_path)
        except Exception as e:
            logger.error(
                f"Trying to remove file from server failed: path={file_entity.file_path}, error:{str(e)}")
            pass
        await self.file_repository.delete(file_entity)

    async def delete_file_for_admin(self, file_id: str, user_id: str, staff_role: AdminRolesEnum) -> None:
        file_entity = await self.file_repository.fetch_by_id(file_id)
        if file_entity.user_id != user_id and staff_role == AdminRolesEnum.supporter:
            if not await self.folder_access_service.user_has_access_to_folder(
                FolderAccessesEnum.DELETE_FILE,
                user_id,
                file_entity.folder_id
            ):
                raise ForbiddenException(FileErrorCodeEnum.FILE_NOT_FOR_USER)
        try:
            os.remove(file_entity.file_path)
        except Exception as e:
            logger.error(
                f"Trying to remove file from server failed: path={file_entity.file_path}, error:{str(e)}")
            pass
        await self.file_repository.delete(file_entity)

    async def get_folders_list(self,
                               folder_id: str,
                               search: Optional[str] = None,
                               user_id: Optional[str] = None,
                               staff_role: Optional[AdminRolesEnum] = None,
                               meta_data_is_null: Optional[bool] = None,
                               ) -> List[FolderSchema]:
        filters = {}
        if staff_role == AdminRolesEnum.supporter:
            filters.update({'folder_ids': await self.folder_access_service.get_folder_ids_for_user(user_id)})
        filters.update({FolderEntity.parent_folder_id: folder_id})
        folders = await self.folder_repository.fetch_paginated_list_by_filters(page=1, size=-1,
                                                                               filters=filters,
                                                                               search=search)
        return await self._aggregate_schema([folder.convert_to_schema() for folder in folders], meta_data_is_null)

    async def create_folder(self,
                            user_id: str, staff_role: AdminRolesEnum,
                            title: str,
                            folder_id: Optional[str] = None,
                            ) -> FolderSchema:
        if staff_role == AdminRolesEnum.supporter:
            folder = await self.folder_repository.fetch_by_id(folder_id)
            if folder.user_id != user_id:
                if not await self.folder_access_service.user_has_access_to_folder(
                        FolderAccessesEnum.CREATE_FOLDER,
                        user_id,
                        folder_id
                ):
                    raise ForbiddenException(FileErrorCodeEnum.FOLDER_NOT_FOR_USER)
        new_folder_id = str(uuid4())
        folder = await self.folder_repository.create(
            FolderEntity(
                id=new_folder_id,
                parent_folder_id=folder_id,
                name=new_folder_id,
                title=title,
            )
        )
        return await self._aggregate_schema(folder.convert_to_schema())

    async def update_folder(self,
                            user_id: str, staff_role: AdminRolesEnum,
                            folder_id: Optional[str] = None,
                            title: Optional[str] = None,
                            ) -> FolderSchema:
        folder = await self.folder_repository.fetch_by_id(folder_id)
        if folder.user_id != user_id and staff_role == AdminRolesEnum.supporter:
            if not await self.folder_access_service.user_has_access_to_folder(
                    FolderAccessesEnum.DELETE_FOLDER,
                    user_id,
                    folder.parent_folder_id
            ):
                raise ForbiddenException(FileErrorCodeEnum.FOLDER_NOT_FOR_USER)
        if title is not None:
            folder.title = title
            await self.folder_repository.update(folder)
        return await self._aggregate_schema(folder.convert_to_schema())

    async def delete_folder(self, user_id: str, staff_role: AdminRolesEnum, folder_id: str) -> None:
        folder = await self.folder_repository.fetch_by_id(folder_id)
        if folder.user_id != user_id and staff_role == AdminRolesEnum.supporter:
            if not await self.folder_access_service.user_has_access_to_folder(
                    FolderAccessesEnum.DELETE_FOLDER,
                    user_id,
                    folder.parent_folder_id
            ):
                raise ForbiddenException(FileErrorCodeEnum.FOLDER_NOT_FOR_USER)
        folder_path = await self.build_folder_path(folder)
        full_path = os.path.join(self.file_storage_path, folder_path)
        try:
            shutil.rmtree(full_path)
        except Exception as e:
            logger.error(
                f"Trying to remove folder from server failed: path={full_path}, error:{str(e)}")
        await self.file_repository.delete(folder)

    async def create_meta_data_for_file(self, user_id: str, staff_role: AdminRolesEnum, file_id: str, data_in: FileMetaDataSchema) -> FileInfoSchema:
        file_entity = await self.file_repository.fetch_by_id(file_id)
        if file_entity.user_id != user_id and staff_role == AdminRolesEnum.supporter:
            raise ForbiddenException(FileErrorCodeEnum.FILE_NOT_FOR_USER)
        file_meta_data = await self.file_meta_data_repository.get_by_file_id(file_id)
        if file_meta_data is None:
            await self.file_meta_data_repository.create(
                FileMetaDataEntity(
                    file_id=file_id,
                    code=data_in.code,
                    name=data_in.name,
                    description=data_in.description,
                    approval_date=data_in.approval_date,
                    producer_user_id=data_in.producer_user_id,
                    controller_user_id=data_in.controller_user_id,
                    confirmer_user_id=data_in.confirmer_user_id,
                    approver_user_id=data_in.approver_user_id,
                )
            )
        else:
            await self.file_meta_data_repository.update(
                FileMetaDataEntity(
                    id=file_meta_data.id,
                    file_id=file_id,
                    code=data_in.code,
                    name=data_in.name,
                    description=data_in.description,
                    approval_date=data_in.approval_date,
                    producer_user_id=data_in.producer_user_id,
                    controller_user_id=data_in.controller_user_id,
                    confirmer_user_id=data_in.confirmer_user_id,
                    approver_user_id=data_in.approver_user_id,
                )
            )
        return await self._aggregate_file_schema(file_entity)
