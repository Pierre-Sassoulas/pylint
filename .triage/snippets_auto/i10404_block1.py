def create_list():
    if error_case():
      return None
    return [1, 2, 3]

for _ in create_list():
    pass
