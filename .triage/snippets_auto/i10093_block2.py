def some_method(
    session: typing.Annotated[AsyncSession, Depends(get_session_read)],
) -> None:
    ...
