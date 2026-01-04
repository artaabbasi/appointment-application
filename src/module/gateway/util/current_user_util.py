import json
from typing import Optional, Union

from common.account.enum.admin_roles_enum import AdminRolesEnum
from common.account.enum.authentication_error_code_enum import AuthenticationErrorCodeEnum
from common.account.enum.token_type_enum import TokenTypeEnum
from common.account.enum.user_group_enum import UserGroupEnum
from common.account.schema.user_permission_schema import UserPermissionSchema
from common.account.util.jwt_util import JwtUtil

from fastapi import Request

from common.config.http_method_enum import HTTPMethodEnum
from common.exceptions import (
    BadRequestException, ForbiddenException,
)
from common.account.schema.authenticated_user_schema import (
    AuthenticatedUserSchema)
from module.account.user.service import CustomerService
from module.api_manager.api_key.service.api_key_service import ApiKeyService
from module.account.user.util.redis_jwt_util import RedisJwtUtil
from module.gateway.access_management import AccessManagementService
from module.gateway.access_management.schema import ActionEnum
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from util.redis_util import RedisUtil


class CurrentUserUtil(HTTPBearer, JwtUtil):
    """
           Current user dependency.
           Acts a middleware and runs multiple validations on authenticated user.

           :param action: The action which user wants to take.
    """

    def __init__(self, action: ActionEnum, optional: Optional[bool] = False):
        super(CurrentUserUtil, self).__init__(auto_error=False)
        self.action = action
        self.optional = optional

    async def __call__(self,
                       request: Request) \
            -> Union[AuthenticatedUserSchema, None]:
        credentials: HTTPAuthorizationCredentials = await super(CurrentUserUtil, self).__call__(request)
        try:
            if not credentials and not self.optional:
                raise BadRequestException(code=AuthenticationErrorCodeEnum.INVALID_TOKEN)
            if not credentials.scheme == "Bearer":
                raise BadRequestException(code=AuthenticationErrorCodeEnum.INVALID_TOKEN)
            decoded_token = self._decode_token(credentials.credentials)
            if decoded_token.group == UserGroupEnum.admin:
                permissions =  await RedisUtil().get_key(f"user:{decoded_token.admin_id}:perms")
                if permissions:
                    permissions = json.loads(permissions)
                    decoded_token.permissions = [UserPermissionSchema(**perm) for perm in permissions]
                else:
                    decoded_token.permissions = []
            decoded_token.token = credentials.credentials
            permission = await self._run_validations(request, decoded_token, request.method)
            decoded_token.permission = permission
            if decoded_token.group == UserGroupEnum.admin:
                if customer_id := request.query_params.get("customer_id"):
                    user = await CustomerService().get_not_detailed_user_by_id(customer_id)
                    decoded_token.user_id = user.id
                else:
                    decoded_token.user_id = decoded_token.admin_id
            return decoded_token
        except Exception as err:
            if self.optional:
                return None
            raise err

    async def _run_validations(self, request: Request, user_payload: AuthenticatedUserSchema, method: str):
        if user_payload.token_type != TokenTypeEnum.api_key:
            if user_payload.token_type == TokenTypeEnum.refresh:
                if await RedisJwtUtil().is_token_blacklisted(user_payload.token):
                    raise BadRequestException(code=AuthenticationErrorCodeEnum.BLOCKED_TOKEN)

                if self.action != ActionEnum.account__auth__refresh_token:
                    raise BadRequestException(code=AuthenticationErrorCodeEnum.CAN_NOT_USE_REFRESH_TOKEN_FOR_THIS_ROUTE)
            if AdminRolesEnum.full_read in user_payload.roles and method == HTTPMethodEnum.GET:
                return None
            permission = await AccessManagementService().check_if_user_has_access_to_action(user_payload.user_id,
                                                                                            self.action,
                                                                                            user_payload.group,
                                                                                            user_payload.roles,
                                                                                            user_payload.permissions)
        else:
            permission = None
            url = request.url.path
            method = HTTPMethodEnum.get_enum_from_str(method)
            if not await ApiKeyService().api_key_has_access(url, method, user_payload.admin_id):
                raise ForbiddenException(code=AuthenticationErrorCodeEnum.DONT_HAVE_ACCESS_TO_API)

        return permission
