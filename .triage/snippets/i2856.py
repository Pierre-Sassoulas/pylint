class GitError(Exception):
    pass


class InvalidGitRepositoryError(GitError):
    pass


try:
    raise InvalidGitRepositoryError()
except GitError:
    print("a")
except Exception:
    print("b")
