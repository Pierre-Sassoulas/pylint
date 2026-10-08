    with SQLUnitOfWork(config) as uow:
        animal = Animal(**data).add_animal_to_db(uow)
        if not animal:
            return {'status': 'Incorrect values', 'values': body}, 405
        return animal.as_dict(), 201  # pylint: disable=no-member
