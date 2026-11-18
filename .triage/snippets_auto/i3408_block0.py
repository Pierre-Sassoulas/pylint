try:
    old_contents, _, _ = yapflib.yapf_api.ReadFile(filename)
    style_config = ('{{based_on_style: chromium, '
                    'indent_width: {}, '
                    'split_before_named_assigns: True, '
                    'column_limit: {}}}'.format(indent_width, max_line_length))
    new_contents, _ = yapf_api.FormatCode(
            old_contents, style_config=style_config, verify=False)
    operations_group = difflib.SequenceMatcher(
            None, old_contents.splitlines(), new_contents.splitlines())
except Exception:  # pylint: disable=broad-except
    # formatters are not perfect and can explode, don't block lint on that.
    # TODO log the error.
    operations_group = []

# We have a function just return operations_group above; this loop to check it for
# line-to-long is another function called by the fixer making that API call:
for i1, i2, old_longest_line, new_longest_line in operations_group:
    # 'line' is 1-indexed, the diff offsets are 0-indexed.
    if i1 < line <= i2 and old_longest_line > new_longest_line:
        return False  # the original line would have been made shorter.
return True  # the formatter can fix the line, emit the lint warning.
