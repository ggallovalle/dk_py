import typing
import pydantic
from typing import TypeAlias, Union, Set, Dict, Any, Optional, Literal


# should be `set[int] | set[str] | dict[int, IncEx] | dict[str, IncEx] | None`, but mypy can't cope
IncEx: TypeAlias = Union[Set[int], Set[str], Dict[int, Any], Dict[str, Any], None]

TSelf = typing.TypeVar("TSelf", bound="pydantic.BaseModel")
last_field = object()


class RowModelMixin:
    __pydantic_row_model_index__: typing.ClassVar[set[str]] = None

    @classmethod
    def __pydantic_init_subclass__(cls: typing.Type[TSelf], **kwargs):
        last_field_indexes = []
        required_after_last_field = False
        model_index = []

        for index, (field_name, field) in enumerate(cls.model_fields.items()):
            if last_field in field.metadata:
                last_field_indexes.append(index)

            if (
                len(last_field_indexes) > 0
                and last_field_indexes[0] != index
                and field.is_required
            ):
                required_after_last_field = True

            model_index.append(field_name)

        if len(last_field_indexes) == 0:
            raise pydantic.PydanticUserError(
                "No field with metadata 'last_field' found"
            )
        elif len(last_field_indexes) > 1:
            raise pydantic.PydanticUserError(
                "Multiple fields with metadata 'last_field' found"
            )

        if required_after_last_field:
            raise pydantic.PydanticUserError(
                "Required field found after field with metadata 'last_field'"
            )

        cls.__pydantic_row_model_index__ = model_index

    @classmethod
    def model_validate_row(
        cls: typing.Type[TSelf],
        row: list[typing.Any],
        *,
        index: typing.Optional[list[str]] = None,
        strict: typing.Optional[bool] = None,
        context: typing.Optional[dict[str, typing.Any]] = None,
    ):
        if index is not None:
            set_index = set(index)
            index = cls.__pydantic_row_model_index__
            if set_index == index:
                index = set_index

        index = index or cls.__pydantic_row_model_index__
        data = dict(zip(index, row))
        return cls.model_validate(data, strict=strict, context=context)

    def model_dump_row(
        self: TSelf, 
        *, 
        index: typing.Optional[list[str]] = None,
        mode: typing.Literal["json", "python"] | str = "python",
        include: IncEx = None,
        exclude: IncEx = None,
        context: Optional[dict[str, Any]] = None,
        exclude_unset: bool = False,
        exclude_defaults: bool = False,
        exclude_none: bool = False,
        warnings: Optional[bool] | Literal["none", "warn", "error"] = True,
    ) -> list[typing.Any]:
        dump_dict = self.model_dump(
            mode=mode,
            include=include,
            exclude=exclude,
            context=context,
            exclude_unset=exclude_unset,
            exclude_defaults=exclude_defaults,
            exclude_none=exclude_none,
            warnings=warnings,
        )
        index = index or self.__pydantic_row_model_index__
        return [dump_dict.get(field, None) for field in index]
