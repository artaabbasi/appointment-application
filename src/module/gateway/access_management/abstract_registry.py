from abc import ABC, abstractmethod

from .schema import ActionEnum
from .abstract_rule_definition import AbstractAccessRuleDefinition


class AbstractAccessRuleRegistry(ABC):
    @abstractmethod
    def get_access_rule_definition_by_action(self, action: ActionEnum) -> AbstractAccessRuleDefinition:
        pass

    @abstractmethod
    def check_if_access_rule_definition_is_already_registered(self, action: ActionEnum):
        pass

    @abstractmethod
    def register_access_rule(self, role_definition: AbstractAccessRuleDefinition):
        pass
