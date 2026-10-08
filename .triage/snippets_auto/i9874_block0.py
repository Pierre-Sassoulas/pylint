# pylint: disable=missing-docstring,missing-class-docstring,too-few-public-methods

from advanced_alchemy.repository import SQLAlchemyAsyncRepository
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class ExampleModel(Base):
    __tablename__ = "example_model"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]


class ExampleModelRepository(SQLAlchemyAsyncRepository[ExampleModel]):
    model_type = ExampleModel
