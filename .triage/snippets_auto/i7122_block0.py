#!/usr/bin/python3
# pylint: disable=missing-docstring

import os

import apt

src_records = apt.apt_pkg.SourceRecords()
assert not hasattr(src_records, "binaries")
src_records.lookup("bash")
assert hasattr(src_records, "binaries")
print(f"type(src_records.binaries) = {type(src_records.binaries)}")
print(f"src_records.binaries = {src_records.binaries!r}")
pkgs = [p for p in src_records.binaries if not p.endswith("-doc")]
print(f"pkgs = {pkgs!r}")

fetcher = apt.apt_pkg.Acquire(apt.progress.text.AcquireProgress())
cache = apt.Cache(rootdir=os.getcwd())
cache.fetch_archives(fetcher=fetcher)
for i in fetcher.items:
    print(i)
