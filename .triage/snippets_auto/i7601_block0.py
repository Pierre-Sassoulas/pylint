    @validator("sender_mail", always=True, pre=True)
    # pylint: disable-next=no-self-use, no-self-argument, unused-argument
    def set_email_if_possible(
        cls, value: Any, values: dict[str, Any], extra_information_place_holder: dict[str, Any]
    ) -> Optional[NameEmail]:
        try:
            return split_name_and_mail(values.get("sender_from", ""))
        except ValueError:
            return None
