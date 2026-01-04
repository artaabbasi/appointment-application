import asyncio
import io
from typing import Union, List, Optional

from common.exceptions import NotFoundException
from common.form_manager.schema.form_change_log_schema import FormChangeLogSchema
from common.form_manager.schema.user_form_answer_create_schema import UserFormAnswerCreateSchema
from common.form_manager.schema.user_form_answer_schema import UserFormAnswerSchema
from common.form_manager.schema.user_form_change_log_schema import UserFormChangeLogSchema
from common.form_manager.schema.user_form_field_answer_create_schema import UserFormFieldAnswerCreateSchema
from common.form_manager.schema.user_form_schema import UserFormSchema
from common.form_manager.schema.user_form_with_user_schema import UserFormWithUserSchema
from common.lib.base_service import BaseService
from common.form_manager.enum.form_field_type_enum import FormFieldTypeEnum
from common.form_manager.schema.form_create_schema import FormCreateSchema
from common.form_manager.schema.form_field_choice_create_schema import FormFieldChoiceCreateSchema
from common.form_manager.schema.form_field_choice_schema import FormFieldChoiceSchema
from common.form_manager.schema.form_field_create_schema import FormFieldCreateSchema
from common.form_manager.schema.form_field_schema import FormFieldSchema
from common.form_manager.schema.form_schema import FormSchema
from module.account.user.service import CustomerService
from module.form_manager.form_manager.entity.form_change_log_entity import FormChangeLogEntity
from module.form_manager.form_manager.entity.form_entity import FormEntity
from module.form_manager.form_manager.entity.form_field_choice_entity import FormFieldChoiceEntity
from module.form_manager.form_manager.entity.form_field_entity import FormFieldEntity
from module.form_manager.form_manager.entity.user_form_change_log_entity import UserFormChangeLogEntity
from module.form_manager.form_manager.entity.user_form_entity import UserFormEntity
from module.form_manager.form_manager.entity.user_form_field_answer_entity import UserFormFieldAnswerEntity
from module.form_manager.form_manager.repository.form_change_log_repository import FormChangeLogRepository
from module.form_manager.form_manager.repository.form_field_choice_repository import \
    FormFieldChoiceRepository
from module.form_manager.form_manager.repository.form_field_repository import FormFieldRepository
from module.form_manager.form_manager.repository.form_repository import FormRepository
from module.form_manager.form_manager.repository.user_form_change_log_repository import UserFormChangeLogRepository
from module.form_manager.form_manager.repository.user_form_field_answer_repository import UserFormFieldAnswerRepository
from module.form_manager.form_manager.repository.user_form_repository import UserFormRepository
from util.excel_export_util import ExcelExportUtil
from util.timestamp import DatetimeUtil


class FormService(BaseService):
    def __init__(self):
        self.form_repository = FormRepository()
        self.form_field_repository = FormFieldRepository()
        self.form_field_choice_repository = FormFieldChoiceRepository()
        self.user_form_repository = UserFormRepository()
        self.user_form_field_answer_repository = UserFormFieldAnswerRepository()
        self.form_change_log_repository = FormChangeLogRepository()
        self.user_form_change_log_repository = UserFormChangeLogRepository()

    async def _aggregate_form_schema(self, schema: Union[FormSchema, list[FormSchema], any]):
        if not schema:
            return schema
        if isinstance(schema, list):
            schema = await asyncio.gather(
                *[
                    self._aggregate_form_schema(item) for item in schema
                ]
            )
        else:
            fields = await self.get_form_fields(schema.id)
            schema.fields = fields
        return schema

    async def _aggregate_form_change_log_schema(self, schema: Union[FormChangeLogSchema, list[FormChangeLogSchema], any]):
        if not schema:
            return schema
        if isinstance(schema, list):
            schema = await asyncio.gather(
                *[
                    self._aggregate_form_change_log_schema(item) for item in schema
                ]
            )
        else:
            if schema.user_id:
                schema.user = await CustomerService().get_not_detailed_user_by_id(schema.user_id)
        return schema

    async def _aggregate_user_form_change_log_schema(self, schema: Union[UserFormChangeLogSchema, list[UserFormChangeLogSchema], any]):
        if not schema:
            return schema
        if isinstance(schema, list):
            schema = await asyncio.gather(
                *[
                    self._aggregate_user_form_change_log_schema(item) for item in schema
                ]
            )
        else:
            if schema.user_id:
                schema.user = await CustomerService().get_not_detailed_user_by_id(schema.user_id)
        return schema

    async def _aggregate_field_schema(self, schema: Union[FormFieldSchema, list[FormFieldSchema], any]):
        if not schema:
            return schema
        if isinstance(schema, list):
            schema = await asyncio.gather(
                *[
                    self._aggregate_field_schema(item) for item in schema
                ]
            )
        else:
            if schema.field_type in [FormFieldTypeEnum.CHOICE, FormFieldTypeEnum.MULTI_CHOICE,]:
                choices = await self.get_field_choices(schema.id)
                schema.choices = choices
        return schema

    async def _import_form_field_choice(self,
                                        form_field_id: str,
                                        data_in: FormFieldChoiceCreateSchema):
        try:
            form_field_choice = await self.form_field_choice_repository.fetch_by_id(data_in.id)
        except NotFoundException:
            form_field_choice = None
        if form_field_choice is None:
            form_field_choice = await self.form_field_choice_repository.create(
                FormFieldChoiceEntity(
                    field_id=form_field_id,
                    attachment_files=data_in.attachment_files,
                    description=data_in.description,
                )
            )
        else:
            update_data = data_in.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                try:
                    setattr(form_field_choice, key, value)
                except:
                    pass
            await self.form_field_choice_repository.update(form_field_choice)

    async def _import_form_field(self,
                                 form_id: str,
                                 data_in: FormFieldCreateSchema):
        try:
            form_field = await self.form_field_repository.fetch_by_id(data_in.id)
        except NotFoundException:
            form_field = None
        if form_field is None:
            form_field = await self.form_field_repository.create(
                FormFieldEntity(
                    form_id=form_id,
                    field_type=data_in.field_type,
                    attachment_files=data_in.attachment_files,
                    title=data_in.title,
                    description=data_in.description,
                    min_length=data_in.min_length,
                    max_length=data_in.max_length,
                    is_required=data_in.is_required,
                )
            )
        else:
            update_data = data_in.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                try:
                    setattr(form_field, key, value)
                except:
                    pass
            await self.form_field_repository.update(form_field)
        await self.form_field_choice_repository.delete_by_field_id_and_not_ids(form_field.id,
                                                                               [choice.id for choice in
                                                                                data_in.choices])
        for field_choice in data_in.choices:
            await self._import_form_field_choice(form_field.id, field_choice)

    async def _create_form_change_log(self, user_id: str, form_id: str, new_fields: list[dict]):
        form_fields = await self.get_form_fields(form_id)
        fields = []
        if form_fields:
            fields = [field.model_dump() if isinstance(field, FormFieldSchema) else field
                          for field in form_fields]
        await self.form_change_log_repository.create(
            FormChangeLogEntity(
                user_id=user_id,
                form_id=form_id,
                last_fields=fields,
                new_fields=new_fields,
            )
        )

    async def import_form(self, user_id: str, data_in: FormCreateSchema) -> FormSchema:
        try:
            form = await self.form_repository.fetch_by_service_id_and_service_type(
                service_id=data_in.service_id,
                service_type=data_in.service_type
            )
            form.name = data_in.name
            await self.form_repository.update(form)
        except NotFoundException:
            form = await self.form_repository.create(
                FormEntity(
                    name=data_in.name,
                    service_id=data_in.service_id,
                    service_type=data_in.service_type
                )
            )
        await self._create_form_change_log(user_id, form.id, [field.model_dump() for field in data_in.fields])
        await self.form_field_repository.delete_by_form_id_and_not_ids(form.id,
                                                                       [field.id for field in
                                                                        data_in.fields])
        for field in data_in.fields:
            await self._import_form_field(form.id, field)

        return await self._aggregate_form_schema(form.convert_to_schema())

    async def _create_user_form_field_answer(self,
                                             user_form_id: str,
                                             data_in: UserFormFieldAnswerCreateSchema):
        user_form_field_answer = await self.user_form_field_answer_repository.fetch_by_user_form_id_and_form_field_id(
            user_form_id, data_in.field_id)
        if user_form_field_answer is not None:
            await self.user_form_field_answer_repository.delete(user_form_field_answer)
        await self.user_form_field_answer_repository.create(
            UserFormFieldAnswerEntity(
                user_form_id=user_form_id,
                form_field_id=data_in.field_id,
                answer=data_in.answer,
                attachment_files=data_in.attachment_files,
            )
        )

    async def _create_user_form_change_log(self, user_id: str, user_form_id: str, new_answers: list[dict]):
        answers = []
        n_answers = []
        user_form_fields = await self.user_form_field_answer_repository.fetch_by_user_form_id(user_form_id)
        form_fields = await self.form_field_repository.fetch_all_by_ids([user_form_field.form_field_id
                                                                         for user_form_field in user_form_fields])
        for user_form_field in user_form_fields:
            for form_field in form_fields:
                if form_field.id == user_form_field.form_field_id:
                    answers.append(
                        UserFormAnswerSchema(
                            field=await self._aggregate_field_schema(form_field.convert_to_schema()),
                            answer=user_form_field.answer,
                            attachment_files=user_form_field.attachment_files,
                        ).model_dump()
                    )
        form_fields = await self.form_field_repository.fetch_all_by_ids([new_answer.get("field_id")
                                                                         for new_answer in new_answers])
        for new_answer in new_answers:
            for form_field in form_fields:
                if form_field.id == new_answer.get("field_id"):
                    n_answers.append(
                        UserFormAnswerSchema(
                            field=await self._aggregate_field_schema(form_field.convert_to_schema()),
                            answer=new_answer.get("answer"),
                            attachment_files=new_answer.get("attachment_files"),
                        ).model_dump()
                    )

        await self.user_form_change_log_repository.create(
            UserFormChangeLogEntity(
                user_id=user_id,
                user_form_id=user_form_id,
                last_answers=answers,
                new_answers=n_answers,
            )
        )

    async def _create_user_form(self, user_id: str, data_in: UserFormAnswerCreateSchema) -> UserFormEntity:
        user_form = None
        if data_in.user_form_id is not None:
            try:
                user_form = await self.user_form_repository.fetch_by_id(data_in.user_form_id)
            except NotFoundException:
                user_form = None
        if user_form is None:
            user_form = await self.user_form_repository.create(
                UserFormEntity(
                    user_id=user_id,
                    form_id=data_in.form_id,
                )
            )
        await self._create_user_form_change_log(user_id, user_form.id, [answer.model_dump() for answer in data_in.answers])
        for field in data_in.answers:
            await self._create_user_form_field_answer(user_form.id, field)
        return user_form

    async def create_form_answer(self, user_id: str, data_in: UserFormAnswerCreateSchema) -> UserFormSchema:
        user_form = await self._create_user_form(user_id, data_in)
        return await self.get_user_form_by_id(user_form.id)

    async def get_user_form_by_id(self, user_form_id: str) -> UserFormSchema:
        user_form_fields = await self.user_form_field_answer_repository.fetch_by_user_form_id(user_form_id)
        result = []
        for user_form_field in user_form_fields:
            form_field = await self.form_field_repository.fetch_by_id(user_form_field.form_field_id)
            result.append(
                UserFormAnswerSchema(
                    field=await self._aggregate_field_schema(form_field.convert_to_schema()),
                    answer=user_form_field.answer,
                    attachment_files=user_form_field.attachment_files,
                )
            )
        return UserFormSchema(field_answers=result, user_form_id=user_form_id)

    @property
    def base_column_data(self) -> list:
        return [
            (2, 'نام و نام خانوادگی', lambda x: f"{x.user.first_name} {x.user.last_name}"),
        ]

    def _convert_response_for_excel(self,
                                    answer: Optional[str] = None,
                                    field_type: FormFieldTypeEnum = None,
                                    choices: List[FormFieldChoiceSchema] = []) -> str:
        if answer is None:
            return "-"
        if field_type == FormFieldTypeEnum.DATE:
            return DatetimeUtil.utc_date_str_to_jalali_date_str(answer)
        elif field_type == FormFieldTypeEnum.DATE_TIME:
            return DatetimeUtil.utc_datetime_str_to_jalali_datetime_str(answer)
        elif field_type == FormFieldTypeEnum.FILE:
            return  "فایل آپلود شده است" if answer else "-"
        elif field_type in [FormFieldTypeEnum.CHOICE, FormFieldTypeEnum.MULTI_CHOICE]:
            result = ""
            for answer_id in answer.split(","):
                for choice in choices:
                    if choice.id == answer_id:
                        result += choice.description
                result += ", "
            return result[:-2]
        return answer

    async def get_user_form_excel_by_ids(self, form_id: str, user_form_ids: List[str]) -> io.BytesIO:
        column_data = self.base_column_data
        form = await self.get_form(form_id)
        for idx, field in enumerate(form.fields, 3):
            column_data.append(
                (idx, field.title, lambda x,
                                          field_id=field.id,
                                          field_type=field.field_type,
                                          choices=tuple(field.choices):
                    self._convert_response_for_excel(next((f.answer for f in x.field_answers if f.field.id == field_id), None),
                                                     field_type,
                                                     choices)
                )
            )
        result = []
        for user_form_id in user_form_ids:
            user_form = await self.user_form_repository.fetch_by_id(user_form_id)
            user = await CustomerService().get_not_detailed_user_by_id(user_form.user_id)
            user_form_fields = await self.user_form_field_answer_repository.fetch_by_user_form_id(user_form_id)
            field_answers = []
            for user_form_field in user_form_fields:
                form_field = await self.form_field_repository.fetch_by_id(user_form_field.form_field_id)
                field_answers.append(
                    UserFormAnswerSchema(
                        field=await self._aggregate_field_schema(form_field.convert_to_schema()),
                        answer=user_form_field.answer,
                        attachment_files=user_form_field.attachment_files,
                    )
                )
            result.append(
                UserFormWithUserSchema(
                    user=user,
                    field_answers=field_answers,
                )
            )
        return await ExcelExportUtil().get_list_export(column_data, result)

    async def delete_user_form_by_id(self, user_form_id: str) -> None:
        user_form = await self.user_form_repository.fetch_by_id(user_form_id)
        user_form_fields = await self.user_form_field_answer_repository.fetch_by_user_form_id(user_form_id)
        await self.user_form_repository.delete(user_form)
        await asyncio.gather(
            *[self.user_form_field_answer_repository.delete(user_form_field) for user_form_field in user_form_fields]
        )
        return None

    async def get_form(self, form_id: str) -> FormSchema:
        form = await self.form_repository.fetch_by_id(form_id)
        return await self._aggregate_form_schema(form.convert_to_schema())

    async def delete_form(self, form_id: str) -> None:
        form = await self.form_repository.fetch_by_id(form_id)
        return await self.form_repository.delete(form)

    async def get_form_field(self, form_field_id: str) -> FormFieldSchema:
        form = await self.form_field_repository.fetch_by_id(form_field_id)
        return await self._aggregate_field_schema(form.convert_to_schema())

    async def get_form_fields(self, form_id: str) -> list[FormFieldSchema]:
        fields = await self.form_field_repository.fetch_by_form_id(form_id)
        return await self._aggregate_field_schema([field.convert_to_schema() for field in fields])

    async def get_field_choices(self, field_id: str) -> list[FormFieldChoiceSchema]:
        choices = await self.form_field_choice_repository.fetch_by_field_id(field_id)
        return [choice.convert_to_schema() for choice in choices]

    async def get_form_changes_by_form_id(self, form_id: str) -> list[FormChangeLogSchema]:
        changes = await self.form_change_log_repository.fetch_paginated_list_by_filters(1, -1, {FormChangeLogEntity.form_id: form_id})
        return await self._aggregate_form_change_log_schema([change.convert_to_schema() for change in changes])

    async def get_user_form_changes_by_user_form_id(self, user_form_id: str) -> list[UserFormChangeLogSchema]:
        changes = await self.user_form_change_log_repository.fetch_paginated_list_by_filters(1, -1, {UserFormChangeLogEntity.user_form_id: user_form_id})
        return await self._aggregate_user_form_change_log_schema([change.convert_to_schema() for change in changes])
