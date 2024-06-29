from pydantic import BaseModel
from typing import Annotated

from dkpy.extensions.pydantic_ext import RowModelMixin, last_field

class UserModel(RowModelMixin, BaseModel):
    name: str
    age: int
    is_alive: Annotated[bool, last_field]

class TestModelDump:
    def test_when_called_should_return_a_list_of_values(self):
        # Given

        model = UserModel(name="John", age=30, is_alive=True)

        # When
        result = model.model_dump_row()

        # Then
        assert result == ["John", 30, True]

    def test_when_called_with_index_should_return_a_list_of_values(self):
        # Given
        model = UserModel(name="John", age=30, is_alive=True)

        # When
        result = model.model_dump_row(index=["age", "name", "is_alive"])

        # Then
        assert result == [30, "John", True]

