def django_models_base(fields):
    prefetched_objects_cache = {}
    # Line 694 of django.db.models.base.py:
    for field in fields:
        if field in prefetched_objects_cache:
            del prefetched_objects_cache[field]
            fields.remove(field)  # [modified-iterating-list]


def django_compilemessages(is_ignored_path, ignore_patterns):
    # Test for common os.walk dirnames list mutation.
    basedirs = []
    # From line 93 of django/core/management/commands/compilemessages.py:
    for dirpath, dirnames, filenames in os.walk(".", topdown=True):  # [unused-variable]
        for dirname in dirnames:
            if is_ignored_path(
                    os.path.normpath(os.path.join(dirpath, dirname)), ignore_patterns
            ):
                dirnames.remove(dirname)  # [modified-iterating-list]
            elif dirname == "locale":
                basedirs.append(os.path.join(dirpath, dirname))
