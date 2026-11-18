
    def test030_pylint(self):
        # Pylint base command
        cmd = [
            'pylint',
            '--output-format=colorized`,
            # Storing results in a pickle file is unnecessary
            '--persistent=n',
            # autodetec number of parallel jobs
            '--jobs=0',
            # Disable scoring  ("Your code has been rated at xx/10")
            '--score=n',
            # PEP8 conform line length (see PyLint Issue #3078)
            f'--max-line-length={PEP8_MAX_LINE_LENGTH}',
            # prevent false-positive no-module-member errors
            '--extension-pkg-whitelist=lxml',
            # List of members which are set dynamically and missed by pylint
            # inference system, and so shouldn't trigger E1101 when accessed.
            '--generated-members=WD_ALIGN_PARAGRAPH,WD_ORIENT,PARAGRAPH',
            # Allowlist variable names
            '--good-names=idx,fp,df',
            # Allow fstrings when logging
            '--disable=logging-fstring-interpolation',
        ]
        # Add py files
        cmd.extend(self.collected_py_files[6:7])

        # subprocess.run(cmd, check=True)
        r = subprocess.run(
            cmd,
            check=False,
            universal_newlines=True,
            capture_output=True)

        print(f'!!!!!!!!!!!!!!!! {r.stdout=}')
        print(f'!!!!!!!!!!!!1!! {r.stderr=}')
        print(f'ÖÖÖÖÖÖÖÖÖÖÖÖÖÖ {r.returncode=}')

        self.assertEqual(0, r.returncode)
