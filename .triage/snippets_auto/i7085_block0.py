# tests that all the conditions to get coverage are met
import os
import typing
from pathlib import Path


def _dir_has_any_pyfile(
    start_dir: str,
) -> typing.Union[bool, typing.List[str]]:  # pragma: no cover
    for _dir_name, _subdirs, file_list in os.walk(start_dir):
        subdir_pyfiles = [
            filename for filename in file_list if filename.endswith(".py")
        ]
        if subdir_pyfiles:
            return subdir_pyfiles

    # not found
    return False


def test_all_dirs_have_inits() -> None:
    dirs_with_no_init = []
    dirs_with_no_init_but_subdir_pys = []
    dirs_with_only_init = []

    base_path = (Path(os.path.dirname(__file__)) / ".." / "..").resolve()
    paths_to_test = (base_path / "mdgm", base_path / "tests")

    for start_dir in paths_to_test:
        for dir_name, subdirs, file_list in os.walk(start_dir):
            # strip out known util dirs
            subdirs[:] = [
                dname
                for dname in subdirs
                if dname not in ("__pycache__", ".pytest_cache")
            ]

            if str(Path(dir_name).relative_to(base_path)) == "tests/data":
                subdirs[:] = []
                continue

            pyfiles = [filename for filename in file_list if filename.endswith(".py")]
            subdir_pyfiles = None
            rel_to_root = str(Path(dir_name).relative_to(base_path))

            if not pyfiles:  # pragma: no cover
                subdir_pyfiles = _dir_has_any_pyfile(rel_to_root)
                if not subdir_pyfiles:
                    # we may or may not have a dir without python files
                    continue  # skip as no python files

            if "__init__.py" not in file_list:  # pragma: no cover
                if pyfiles:
                    dirs_with_no_init.append(rel_to_root)
                else:
                    assert subdir_pyfiles, (
                        "if we get here, one of pyfiles *or* "
                        "subdir_pyfiles should contain files as "
                        "we should have 'continued' otherwise"
                    )
                    dirs_with_no_init_but_subdir_pys.append(rel_to_root)
            else:
                single_file_no_dirs = (len(file_list) == 1) and (len(subdirs) == 0)
                if single_file_no_dirs:  # pragma: no cover
                    dirs_with_only_init.append(rel_to_root)

    assert not dirs_with_no_init, (
        "We have directories with missing '__init__.py' file\n"
        f"\t{dirs_with_no_init}\n"
    )

    assert not dirs_with_only_init, (
        "We have directories that _only_ contain an __init__.py file and"
        f"nothing else!\n\t{dirs_with_only_init}"
    )

    assert not dirs_with_no_init_but_subdir_pys, (
        "We have directories with missing '__init__.py' file but "
        ".py files in subdirs\n"
        f"\t{dirs_with_no_init_but_subdir_pys}\n"
    )

