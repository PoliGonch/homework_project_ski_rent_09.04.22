from pydantic import BaseModel
from typing import TypeAlias
import random
import json
import pickle

T_EQUIP_PRICE: TypeAlias = int


class Base:
    def __init__(self, name):
        self.name = name
        self.warehouse: list['Equipment'] = []
        self.debtor_list = []

    def __repr__(self):
        return self.name

    def add_to_warehouse(self, outfit: 'Equipment'):
        if outfit.base is None:
            outfit.base = self
            self.warehouse.append(outfit)
            return True
        print('Eto ne baza')
        return False

    def give_equipment(self, human: 'Human'):
        random.shuffle(self.warehouse)
        if self.warehouse:
            self.debtor_list.append(human)
            self.write_to_file()
            return self.warehouse.pop()
        return False

    def take_back(self, outfit: 'Equipment', human: 'Human'):
        if outfit.base == self:
            self.warehouse.append(outfit)
            self.debtor_list.remove(human)
            self.write_to_file()

    def check_total_price(self):
        return sum(item.current_price for item in self.warehouse)

    def write_to_file(self):
        with open(f'{self.name}', 'wb') as file_object:
            pickle.dump(self, file_object)

    @staticmethod
    def read_from_file(file_name):
        with open(f'{file_name}', 'rb') as file_object:
            return pickle.load(file_object)

class Equipment:
    regular_amort = 0.01
    extra_amort = 0.1
    risk = 0
    type = None

    def __init__(self, base_price: T_EQUIP_PRICE):
        self.base = None
        self.base_price = base_price
        self.current_price = base_price

    def roll_down(self):
        if random.randint(1, 100) <= self.risk:
            self.current_price -= self.extra_amort * self.base_price
        else:
            self.current_price -= self.regular_amort * self.base_price

    def __repr__(self):
        return f'{self.__class__.__name__}, {self.base}, {self.base_price}, {self.current_price}'



class Ski(Equipment):
    risk = 0.08


class Helmet(Equipment):
    ...


class Sled(Equipment):
    risk = 0.02


class Snowboard(Equipment):
    risk = 0.13


class Human:

    def __init__(self, name):
        self.name = name,
        self.outfit = []

    def print_outfit(self):
        for item in self.outfit:
            print(item)

    def take_outfit(self, item):
        if item:
            self.outfit.append(item)

    def return_outfit(self, base: Base):
        for item in self.outfit:
            if item.base == base:
                base.take_back(outfit=item, human=self)
                self.outfit.remove(item)


class Drag_lift:
    success_tuple = ((Sled.__name__,), (Helmet.__name__, Ski.__name__), (Helmet.__name__, Snowboard.__name__))

    def check_outfit(self, human: Human):
        allowed = False

        for combination in self.success_tuple:
            if set(combination) == set(item.__class__.__name__ for item in human.outfit) & set(combination):
                allowed = True
                break

        if allowed:
            print(f'{human.name} allowed to ride')
            for item in human.outfit:
                item.roll_down()

def fill_database(base):
    base.add_to_warehouse(Sled(250))
    base.add_to_warehouse(Sled(350))
    base.add_to_warehouse(Sled(150))
    base.add_to_warehouse(Sled(280))

    for i in range(21):
        base.add_to_warehouse(Helmet(random.randint(100, 1000)))
    for i in range(10):
        base.add_to_warehouse(Ski(random.randint(100, 500)))
    for i in range(15):
        base.add_to_warehouse(Snowboard(random.randint(1000, 5000)))


def main():
    base_1 = Base('Sunny')
    base_2 = Base('Wow')
    base_3 = Base('Albatros')

    drag = Drag_lift()

    base_list = [base_1, base_2, base_3]

    for base in base_list:
        fill_database(base)

    human_1 = Human('Ivan')
    human_2 = Human('Katya')

    for base in base_list:
        equip = base.give_equipment(human_1)
        human_1.take_outfit(equip)

    human_2.take_outfit(Ski(100))
    human_2.take_outfit(Helmet(100))
    human_2.take_outfit(Ski(100))

    # human_1.print_outfit()
    human_2.print_outfit()

    # drag.check_outfit(human_1)
    drag.check_outfit(human_2)

    # human_1.return_outfit(base_1)


if __name__ == '__main__':
    main()
