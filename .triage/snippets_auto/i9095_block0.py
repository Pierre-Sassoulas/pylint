class DubDependency(ExternalDependency):
    # dub program and version
    class_dubbin: T.Optional[T.Tuple[ExternalProgram, str]] = None
    class_dubbin_searched = False

    def __init__(self, name: str, environment: 'Environment', kwargs: T.Dict[str, T.Any]):

[...]

        if DubDependency.class_dubbin is None:
            if self.required:
                raise DependencyException('DUB not found.')
            self.is_found = False
            return

        (self.dubbin, dubver) = DubDependency.class_dubbin ### <<< pylint error
