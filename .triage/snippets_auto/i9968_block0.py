"""
With the new LangChain version (0.3.0) there is support for Pydantic V2,
they changed all the models to use Pydantic V2, and some of our code is
returning a false positive specifically related to the BaseMessage class.
"""

# Error
from langchain_core.messages import BaseMessage

def my_function():
    message = BaseMessage(content="x", type="system")
    message.additional_kwargs["foo"] = "bar"


# Not error
from langchain_core.messages import BaseMessage
from langchain_core.pydantic_v1 import Field
# Note: with from pydantic.v1 import Field fails too

class MyBaseMessage(BaseMessage):
    additional_kwargs: dict = Field(default_factory=dict)

def my_function():
    message = BaseMessage(content="x", type="system")
    message.additional_kwargs["foo"] = "bar"
