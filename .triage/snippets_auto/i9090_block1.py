from pydantic import Field, BaseModel


class Example2(BaseModel):
    number: int = Field(alias='n')


example = Example2(n=5)
