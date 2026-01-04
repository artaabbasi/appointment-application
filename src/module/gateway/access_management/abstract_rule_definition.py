import abc
from typing import List, Union, Literal, Optional

from common.account.enum.auth_action_enum import AuthActionEnum
from common.account.enum.user_group_enum import UserGroupEnum
from .schema import (ActionEnum,
                     RestrictionEnum,
                     )
from common.account.enum.admin_roles_enum import AdminRolesEnum


class AbstractAccessRuleDefinition(abc.ABC):
    """
    Abstract base class for access rule definitions

    Subclasses must define following properties as class attributes.

    `action`: Must be one of actions defined in `ActionEnum`.
    `authorized_groups`: Must be one of groups defined `UserGroupEnum`.
    `authorized_admin_roles`: Must be one of groups defined `AdminGroupRolesEnum`.
    `module`
    `sub_module`
    `auth_action`
    Note that `authorized_groups` and `authorized_admin_roles` can have a special value which
    indicate all of possible role and groups has access to that action.
    """

    @property
    @abc.abstractmethod
    def action(self) -> ActionEnum:
        raise Exception("Defining `action` is required.")

    @property
    @abc.abstractmethod
    def module(self) -> Optional[str]:
        return None

    @property
    @abc.abstractmethod
    def sub_module(self) -> Optional[str]:
        return None

    @property
    @abc.abstractmethod
    def auth_action(self) -> Optional[AuthActionEnum]:
        return None

    @property
    @abc.abstractmethod
    def authorized_groups(self) -> List[Union[UserGroupEnum, Literal['__all__']]]:
        raise Exception("Defining `authorized_groups` is required.")

    @property
    @abc.abstractmethod
    def authorized_admin_roles(self) -> List[Union[AdminRolesEnum, Literal['__all__']]]:
        raise Exception("Defining `authorized_roles` is required.")

    @authorized_admin_roles.setter
    def authorized_admin_roles(self, value):
        self.authorized_admin_roles = value

    @authorized_groups.setter
    def authorized_groups(self, value):
        self.authorized_groups = value

    @property
    @abc.abstractmethod
    def restricted_statuses(self) -> List[RestrictionEnum]:
        raise Exception("Defining `restricted_statuses` is required.")

    @restricted_statuses.setter
    def restricted_statuses(self, value):
        self.authorized_admin_roles = value

    def __str__(self):
        action = self.action
        groups = self.authorized_groups
        roles = self.authorized_admin_roles
        return f'{self.__name__}(action={action}, groups={groups}, roles={roles})'
