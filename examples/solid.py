from abc import ABC, abstractmethod
from typing import List


# Single Responsibility Principle
class Engine:
    def start(self) -> str:
        return 'Двигун стартував'

    def stop(self) -> str:
        return 'Двигун зупинився'


class Radio:
    def turn_on(self) -> str:
        return 'Радіо включено'

    def turn_off(self) -> str:
        return 'Радіо виключено'


# Open/Closed Principle
class BaseSensor(ABC):
    @abstractmethod
    def read_data(self) -> str:
        pass


class TemperatureSensor(BaseSensor):
    def read_data(self) -> str:
        return 'Дані температурного датчика'


# Liskov Substitution Principle
class Bird:
    def move(self) -> str:
        return 'Птах літає'


class Ostrich(Bird):
    def move(self) -> str:
        return 'Страус біжить'


# Interface Segregation Principle
class Worker(ABC):
    @abstractmethod
    def work(self) -> str:
        pass


class Musician(Worker):
    def work(self) -> str:
        return 'Музикант грає на інструменті'


class Builder(Worker):
    def work(self) -> str:
        return 'Будівельник будує будівлю'


# Dependency Inversion Principle
class LightBulb(ABC):
    @abstractmethod
    def turn_on(self) -> str:
        pass

    @abstractmethod
    def turn_off(self) -> str:
        pass


class IncandescentBulb(LightBulb):
    def turn_on(self) -> str:
        return 'Лампочка розжарюється'

    def turn_off(self) -> str:
        return 'Лампочка гасне'


class Switch:
    def __init__(self, bulb: LightBulb):
        self.bulb = bulb

    def operate(self) -> str:
        return self.bulb.turn_on() + '\n' + self.bulb.turn_off()


if __name__ == '__main__':
    # Single Responsibility Principle
    engine = Engine()
    print(engine.start())
    radio = Radio()
    print(radio.turn_on())

    # Open/Closed Principle
    sensors: List[BaseSensor] = [TemperatureSensor()]
    for sensor in sensors:
        print(sensor.read_data())

    # Liskov Substitution Principle
    bird = Bird()
    print(bird.move())
    ostrich = Ostrich()
    print(ostrich.move())

    # Interface Segregation Principle
    musician = Musician()
    print(musician.work())
    builder = Builder()
    print(builder.work())

    # Dependency Inversion Principle
    bulb = IncandescentBulb()
    switch = Switch(bulb=bulb)
    print(switch.operate())
