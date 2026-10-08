    # Update the entry ID
    if str(record.id) != entry['Entry-ID']:   # here, pylint complains about record.id
        del entry['Entry-ID']
        entry['Entry-ID'] = str(record.id)   # but pylint doesn't complain here
        fixup_needed = True
