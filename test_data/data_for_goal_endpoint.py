from faker import Faker
fake = Faker()

class GoalTestData:
    valid_body = [
        (fake.name(), fake.sentence(), fake.color()),
        (fake.name(), " ", " ")
    ]

    invalid_data_for_id = [
        (0),
        (),
        ("&($(*$$*@)@*$"),
        (-10000000000000000),
        (133.200010122),
        ("fkfkfkdgklvdv"),
        (True)
    ]

    invalid_body = [
        ("", ""),
        (fake.sentence(), fake.color())
    ]

    invalid_token = [
        (""),
        ("&&^&%*%$*$"),
        ("000000000000000000")
    ]