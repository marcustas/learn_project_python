from abc import ABC, abstractmethod


#  Абстракція
class AbstractPiglet(ABC):
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def build_house(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def house_material(self):
        raise NotImplementedError


class Piglet(AbstractPiglet):
    def __init__(self, name, material: str = 'солома'):
        super().__init__(name)
        self.__house_material = material  # Інкапсуляція
        self._strategy = 'Врятуватися від вовка.'

    @property
    def house_material(self):
        return self.__house_material

    def print_strategy(self):
        print(self._strategy)

    def build_house(self):
        print(f'{self.name} побудував будинок з {self.house_material}!')


#  Наслідування
class ImprovedPiglet(Piglet):
    def __init__(self, name: str, material: str = 'цегла'):
        super().__init__(name=name, material=material)


class Wolf:
    def __init__(self, name: str = 'Вова'):
        self.name = name

    def huff_and_puff(self, piglet: AbstractPiglet):
        if piglet.house_material == 'солома':
            print(f'Вовк {self.name} він здув будинок!')
        else:
            print(f'Вовк {self.name} не зміг здути будинок.')


if __name__ == '__main__':
    first_piglet = Piglet(name='Хрю')
    first_piglet.build_house()
    first_piglet.print_strategy()

    second_piglet = ImprovedPiglet(name='Хря')
    second_piglet.build_house()
    second_piglet.print_strategy()

    big_bad_wolf = Wolf()
    #  Поліморфізм
    big_bad_wolf.huff_and_puff(piglet=first_piglet)
    big_bad_wolf.huff_and_puff(piglet=second_piglet)
