from typing import Optional, List

from fastapi import (APIRouter,
                     status,
                     Body,
                     Path, Depends, UploadFile, File
                     )
from fastapi.params import Query
from common.account.enum.user_group_enum import UserGroupEnum
from common.file_manager.enum.folder_access_type import FolderAccessType
from common.file_manager.schema.file_info_schema import FileInfoSchema
from common.file_manager.schema.file_meta_data_schema import FileMetaDataSchema
from common.file_manager.schema.file_upload_schema import FileUploadSchema
from common.file_manager.schema.folder_access_accesses_schema import FolderAccessAccessesSchema
from common.file_manager.schema.folder_access_in_schema import FolderAccessInSchema, FolderAccessInListSchema
from common.file_manager.schema.folder_access_schema import FolderAccessSchema
from common.file_manager.schema.folder_schema import FolderSchema
from common.schema.pagination_schema import PaginationSchema
from common.schema.response_base_schema import GenericResponseSingleSchema, GenericResponseListSchema
from common.settings import get_settings
from module.file_manager.bucket.entity.folder_access_entity import FolderAccessEntity

from module.file_manager.bucket.service.file_service import FileService
from module.file_manager.bucket.service.folder_access_service import FolderAccessService
from module.gateway.access_management.schema import ActionEnum
from module.gateway.schema.jwt_user_schema import JWTUserSchema
from module.gateway.util.current_user_util import CurrentUserUtil

settings = get_settings()

router = APIRouter(prefix='/file-manager',
                   tags=['File Manager'],
                   responses={
                   }
                   )


@router.post('/upload', response_model=GenericResponseSingleSchema[FileInfoSchema])
async def upload_file(
        current_user: Optional[JWTUserSchema] = Depends(
            CurrentUserUtil(action=ActionEnum.file_manager__upload, optional=True)),
        file: UploadFile = File(...),
        file_data: FileUploadSchema = Depends()
):
    if current_user is not None:
        user_id = current_user.user_id
    else:
        user_id = None
    result = await FileService().upload_file_for_user(file, file_data, user_id)
    return GenericResponseSingleSchema[FileInfoSchema].return_response(result)


@router.post('/admin-upload', response_model=GenericResponseSingleSchema[FileInfoSchema])
async def admin_upload_file(
        current_user: JWTUserSchema = Depends(
            CurrentUserUtil(action=ActionEnum.file_manager__upload)),
        file: UploadFile = File(...),
        file_data: FileUploadSchema = Depends()
):
    result = await FileService().upload_file(file, file_data, current_user.user_id, current_user.roles[0])
    return GenericResponseSingleSchema[FileInfoSchema].return_response(result)


@router.get('/get_info/{file_id}', response_model=GenericResponseSingleSchema[FileInfoSchema])
async def get_file_info(
        current_user: Optional[JWTUserSchema] = Depends(
            CurrentUserUtil(action=ActionEnum.file_manager__upload, optional=True)),
        file_id: str = Path(...),
):
    result = await FileService().get_file_info(file_id)
    return GenericResponseSingleSchema[FileInfoSchema].return_response(result)


@router.get('/download/{file_id}')
async def download_file(
        current_user: Optional[JWTUserSchema] = Depends(
            CurrentUserUtil(action=ActionEnum.file_manager__upload, optional=True)),
        file_id: str = Path(...),
):
    if current_user is not None:
        user_id = current_user.user_id
    else:
        user_id = None
    result = await FileService().get_file_for_user(file_id, user_id)
    return result


@router.delete('/delete/{file_id}')
async def delete_file(
        current_user: JWTUserSchema = Depends(CurrentUserUtil(action=ActionEnum.file_manager__upload)),
        file_id: str = Path(...),
):
    if current_user.group == UserGroupEnum.admin:
        result = await FileService().delete_file_for_admin(file_id, current_user.user_id, current_user.roles[0])
    else:
        result = await FileService().delete_file(file_id, current_user.user_id)
    return result


@router.post('/folder', response_model=GenericResponseSingleSchema[FolderSchema])
async def create_folders(
        current_user: JWTUserSchema = Depends(
            CurrentUserUtil(action=ActionEnum.file_manager__upload)),
        title: str = Body(...),
        folder_id: Optional[str] = Body(None),
):
    result = await FileService().create_folder(current_user.user_id, current_user.roles[0], title, folder_id)
    return GenericResponseSingleSchema[FolderSchema].return_response(result)


@router.get('/folder/{folder_id}', response_model=GenericResponseListSchema[FolderSchema])
async def get_folders(
        current_user: JWTUserSchema = Depends(
            CurrentUserUtil(action=ActionEnum.file_manager__upload)),
        folder_id: Optional[str] = Path(...),
        meta_data_is_null: Optional[bool] = Query(None),
        search: Optional[str] = Query(None),
):
    result = await FileService().get_folders_list(folder_id, search, current_user.user_id, current_user.roles[0], meta_data_is_null)
    return GenericResponseListSchema[FolderSchema].return_response(result)


@router.post('/file/meta-data/{file_id}', response_model=GenericResponseSingleSchema[FileInfoSchema])
async def create_file_meta(
        current_user: JWTUserSchema = Depends(
            CurrentUserUtil(action=ActionEnum.file_manager__upload)),
        file_id: Optional[str] = Path(...),
        data_in: FileMetaDataSchema = Body(...)
):
    result = await FileService().create_meta_data_for_file(current_user.user_id, current_user.roles[0], file_id, data_in)
    return GenericResponseSingleSchema[FileInfoSchema].return_response(result)


@router.get('/folder/files/{folder_id}', response_model=GenericResponseListSchema[FileInfoSchema])
async def get_folder_files(
        current_user: JWTUserSchema = Depends(
            CurrentUserUtil(action=ActionEnum.file_manager__upload)),
        folder_id: Optional[str] = Path(...),
        meta_data_is_null: Optional[bool] = Query(None),
):
    result = await FileService().get_folder_files_info(folder_id, meta_data_is_null)
    return GenericResponseListSchema[FileInfoSchema].return_response(result)


@router.get('/folder/folders/{folder_id}', response_model=GenericResponseListSchema[FolderSchema])
async def get_folder_folders(
        current_user: JWTUserSchema = Depends(
            CurrentUserUtil(action=ActionEnum.file_manager__upload)),
        folder_id: Optional[str] = Path(...),
        meta_data_is_null: Optional[bool] = Query(None),

):
    result = await FileService().get_folder_folders_info(
        current_user.user_id,
        current_user.roles[0],
        folder_id,
        meta_data_is_null)
    return GenericResponseListSchema[FolderSchema].return_response(result)


@router.patch('/folder/{folder_id}', response_model=GenericResponseSingleSchema[FolderSchema])
async def update_folder(
        current_user: JWTUserSchema = Depends(
            CurrentUserUtil(action=ActionEnum.file_manager__upload)),
        folder_id: Optional[str] = Path(...),
        title: Optional[str] = Body(None, embed=True),
):
    result = await FileService().update_folder(current_user.user_id, current_user.roles[0], folder_id, title)
    return GenericResponseSingleSchema[FolderSchema].return_response(result)


@router.delete('/folder/{folder_id}', response_model=None, status_code=204)
async def delete_folder(
        current_user: JWTUserSchema = Depends(
            CurrentUserUtil(action=ActionEnum.file_manager__upload)),
        folder_id: Optional[str] = Path(...),
):
    result = await FileService().delete_folder(current_user.user_id, current_user.roles[0], folder_id)
    return None


@router.get('/folder-access', response_model=GenericResponseListSchema[FolderAccessSchema])
async def get_folder_accesses(
        current_user: JWTUserSchema = Depends(CurrentUserUtil(action=ActionEnum.admin_access)),
        pagination_query: PaginationSchema = Depends(),
        folder_id: Optional[str] = Query(None),
        type: Optional[FolderAccessType] = Query(None),
        instance_id: Optional[str] = Query(None),
        accesses_is_null: Optional[bool] = Query(None),
):
    filters = {}
    if folder_id is not None:
        filters[FolderAccessEntity.folder_id] = folder_id
    if type is not None:
        filters[FolderAccessEntity.type] = type
    if instance_id is not None:
        filters[FolderAccessEntity.instance_id] = instance_id
    if accesses_is_null is not None:
        filters['accesses_is_null'] = accesses_is_null

    result = await (FolderAccessService().
                    get_folder_access_list(page=pagination_query.page,
                                           size=pagination_query.size,
                                           filters=filters))
    count = await (FolderAccessService().get_count(filters=filters))
    return GenericResponseListSchema[FolderAccessSchema].return_response(result,
                                                                         page=pagination_query.page,
                                                                         size=pagination_query.size,
                                                                         count=count)


@router.post('/folder-access', response_model=GenericResponseListSchema[FolderAccessSchema])
async def create_folder_access(
        current_user: JWTUserSchema = Depends(CurrentUserUtil(action=ActionEnum.admin_access)),
        data_in: FolderAccessInListSchema = Body(...),
):
    result = await (FolderAccessService().
                    create_folder_access(current_user.user_id, current_user.roles[0], data_in))
    return GenericResponseListSchema[FolderAccessSchema].return_response(result)


@router.patch('/folder-access/{folder_access_id}', response_model=GenericResponseSingleSchema[FolderAccessSchema])
async def update_folder_access(
        current_user: JWTUserSchema = Depends(CurrentUserUtil(action=ActionEnum.admin_access)),
        folder_access_id: str = Path(...),
        data_in: FolderAccessSchema = Body(...),
):
    result = await (FolderAccessService().
                    update_folder_access(current_user.user_id, current_user.roles[0], folder_access_id, data_in))
    return GenericResponseSingleSchema[FolderAccessSchema].return_response(result)


@router.delete('/folder-access/{folder_access_id}', response_model=None, status_code=204)
async def delete_folder_access(
        current_user: JWTUserSchema = Depends(CurrentUserUtil(action=ActionEnum.admin_access)),
        folder_access_id: str = Path(...),
):
    result = await (FolderAccessService().
                    delete_folder_access(current_user.user_id, current_user.roles[0], folder_access_id))
    return None


@router.get('/folder-access/get_access/{folder_id}', response_model=GenericResponseSingleSchema[FolderAccessAccessesSchema])
async def get_user_access_to_folder(
        current_user: JWTUserSchema = Depends(CurrentUserUtil(action=ActionEnum.admin_access)),
        folder_id: str = Path(...),
):
    result = await (FolderAccessService().
                    get_by_user_id_and_folder_id(current_user.user_id, folder_id))
    return GenericResponseSingleSchema[FolderAccessAccessesSchema].return_response(result)
