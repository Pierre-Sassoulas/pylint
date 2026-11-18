class SourceRecords:
    def lookup(self, name: str) -> bool: ...
    def restart(self) -> None: ...
    def step(self) -> bool: ...
    binaries: List[str]
    version: str
    files: List[SourceRecordFiles]
    index: IndexFile
    package: str
    section: str
