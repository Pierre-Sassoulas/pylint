def from_db(self):
    instance = super().from_db()
    instance.save(custom_arg=whatever). # unexpected-keyword-arg
