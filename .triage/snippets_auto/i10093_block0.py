def some_method(
    session: AsyncSession = Depends(get_session_read),
) -> None:
    ...
