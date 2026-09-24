from typing import TYPE_CHECKING, TypeAlias, Union

if TYPE_CHECKING:
    AuthenticationType: TypeAlias = "Authentication"
    DockerAuthenticationType: TypeAlias = "DockerAuthentication"
    AnyAuthentication = Union[AuthenticationType, DockerAuthenticationType]


class Authentication: ...


class DockerAuthentication: ...
