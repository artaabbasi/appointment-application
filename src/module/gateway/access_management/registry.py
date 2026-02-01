from typing import Type, Dict

from .schema import ActionEnum
from .abstract_registry import AbstractAccessRuleRegistry
from .abstract_rule_definition import AbstractAccessRuleDefinition

from .access_rule_definitions.account.admins import access_rule_definitions as account_admins_definitions
from .access_rule_definitions.account.auth import access_rule_definitions as account_auth_definitions
from .access_rule_definitions.account.customers import access_rule_definitions as account_customers_definitions
from .access_rule_definitions.file_manager.file import access_rule_definitions as file_manager_file_definitions
from .access_rule_definitions.main.main import access_rule_definitions as main_definitions


class AccessRuleDefinitionRegistry(AbstractAccessRuleRegistry):
    _registry: Dict[ActionEnum, AbstractAccessRuleDefinition] = None

    def __init__(self):
        if not self._registry:
            self._registry = dict()

    def register_access_rule(self, definition: Type[AbstractAccessRuleDefinition]):
        assert issubclass(definition, AbstractAccessRuleDefinition), 'role_definition should be subclass' \
                                                                     ' of the AbstractRoleDefinition'
        assert not self.check_if_access_rule_definition_is_already_registered(definition.action), \
            (f'The action is already registered with another role'
             f' definition: {self.get_access_rule_definition_by_action(definition.action)}')
        self._registry[definition.action] = definition

    def get_access_rule_definition_by_action(self, action: ActionEnum):
        return self._registry.get(action)

    def check_if_access_rule_definition_is_already_registered(self, action: ActionEnum):
        return action in self._registry.keys()


def register_rule_definitions(registry: AccessRuleDefinitionRegistry):
    access_rule_definitions = [
        *account_customers_definitions,
        *account_auth_definitions,
        *account_admins_definitions,
        *file_manager_file_definitions,
        *main_definitions,
    ]
    for access_role in access_rule_definitions:
        registry.register_access_rule(access_role)
    return registry


access_rule_definition_registry = AccessRuleDefinitionRegistry()
access_rule_definition_registry = register_rule_definitions(access_rule_definition_registry)
