from datetime import (
    date,
    datetime,
)

from dateutil.relativedelta import relativedelta
from pydantic import (
    BaseModel,
    EmailStr,
    computed_field,
    field_validator,
)


class User(BaseModel):
    first_name: str
    last_name: str
    birth_date: date
    email: EmailStr

    @computed_field
    @property
    def age(self) -> int:
        return relativedelta(datetime.now(), self.birth_date).years

    @field_validator('email')
    def validate_domain_zone(cls, value):
        if '.ru' in value:
            raise ValueError('We do not accept ru domains!')

        return value


if __name__ == '__main__':
    # Створення інстансу моделі за допомогою іменованих аргументів
    user1 = User(
        first_name='Іван',
        last_name='Петрович',
        birth_date='1990-01-15',
        email='ivan.petrovich@example.com',
    )

    # Створення інстансу моделі передавши словником
    attrs = {
        'first_name': 'Олена',
        'last_name': 'Сергіївна',
        'birth_date': '1985-05-20',
        'email': 'olena.sergiivna@example.com',
    }

    user2 = User(**attrs)

    # Вивести модель у вигляді словника і як JSON
    print(user1.model_dump())
    print(user1.model_dump_json())

    print(user2.model_dump())
    print(user2.model_dump_json())
