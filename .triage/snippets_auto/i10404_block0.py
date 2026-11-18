all(None)

any(None)


def create_list():
    if error_case():
      return None
    return [1, 2, 3]

all(create_list())
any(create_list())
for _ in create_list():
    pass
