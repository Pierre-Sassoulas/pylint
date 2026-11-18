            paths = [cwd, "/custom_pythonpath1", "/custom_pythonpath2", cwd, *default_paths]
            sys.path = copy(paths)
            with _test_environ_pythonpath(f"/custom_pythonpath1:/custom_pythonpath2:{cwd}:"):
                modify_sys_path()
            assert sys.path == paths[1:3] + paths[4:]   # Not sure about that, it might be paths[1:]. The important part is that 2 must be present
