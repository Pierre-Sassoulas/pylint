import dataclasses


@dataclasses.dataclass
class MockTiming:
    def patch(self, monkeypatch) -> None:
        from shadok import MagicFaucet  # noqa: PLW0406
        print(MagicFaucet)
