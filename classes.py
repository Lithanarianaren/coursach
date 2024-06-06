from tkinter import messagebox

from gui.form.blueprints import *
from gui.relation.Relationable import *
from gui.utilities import get_datetime


class Item(Addable, Editable, Deletable):
    def __init__(self, name="item", quantity=1, cost=0):
        self.name = name
        self.cost = cost
        self.quantity = quantity

    def __str__(self):
        return "name={}, cost={}, quantity={}".format(self.name, self.cost, self.quantity)

    @staticmethod
    def get_relation_attributes() -> list[str]:
        return ["Наименование", "Цена", "Количество"]

    @staticmethod
    def add_form_blueprint() -> FormBlueprint:
        form = FormBlueprint()
        name_input = TextElem("Наименование", str_constraint)
        quantity_input = TextElem("Количество", unsigned_int_constraint)
        cost_input = TextElem("Цена", unsigned_int_constraint)
        form.add(name_input).add(quantity_input).add(cost_input)
        return form

    @staticmethod
    def add(parent: HasInternalRelations, attributes: list):
        item = Item(*attributes)
        parent.add_relation(item)

    def edit_form_blueprint(self) -> FormBlueprint:
        form = FormBlueprint()
        name_input = TextElem("Наименование", str_constraint, self.name)
        quantity_input = TextElem("Количество", str_constraint, self.quantity)
        cost_input = TextElem("Цена", unsigned_int_constraint, self.cost)
        form.add(name_input).add(quantity_input).add(cost_input)
        return form

    def edit(self, attributes: list):
        self.name = attributes[0]
        self.quantity = attributes[1]
        self.cost = attributes[2]

    def delete(self, parent: HasInternalRelations):
        parent.del_relation(self)

    def get_relation_object(self) -> list[str]:
        return [self.name, str(self.cost), str(self.quantity)]

    def get_json(self):
        d = {
            "name": self.name,
            "quantity": self.quantity,
            "cost": self.cost,
        }
        return d


class BaseTransaction(HasInternalRelations, Addable, Editable, ABC):
    def add_relation(self, item):
        self.add_items([item])

    def del_relation(self, item):
        self.del_items([item])

    def __init__(self, parent, inward, completed=False, items=None, desc=''):
        self.inward = inward
        self.parent: Warehouse = parent
        self.completed = completed
        if items is None:
            items = []
        self.desc = desc
        self.items = items

    def can_be_edited(self):
        return not self.completed

    def complete(self):
        raise NotImplementedError

    def add_items(self, items):  # ожидает список предметов
        for i in items:
            flag = 0
            for j in self.items:
                if i.name == j.name:
                    j.quantity += i.quantity
                    flag = 1
                    break
            if not flag:
                self.items.append(i)

    def del_items(self, items):  # передаются товары, из товаров в транзакции удаляются товары с тем же названием
        error_flag = 0
        items_to_del = []
        for i in items:
            flag = 0
            for j in self.items:
                if i.name == j.name:
                    flag = 1
                    items_to_del.append(j)
            if not flag:
                print("Ошибка при удалении товара: в ТРАНЗАКЦИИ нет товара с таким названием: ", i.name)
                error_flag = 1

        if error_flag:
            return 0

        # удаление своих item-ов
        for i in range(len(items)):
            self.items.remove(items_to_del[i])
        return 1


class Transaction(BaseTransaction):

    @staticmethod
    def get_class_name():
        return "Транзакция купли/продажи"

    @staticmethod
    def get_relation_classes() -> list[type[Relationable]]:
        return [Item]

    def get_relation_object(self) -> list[str]:
        return [self.desc,
                "Закупка" if self.inward else "Продажа",
                str(self.count_cost()),
                "Проведено" if self.completed else "В работе"]

    @staticmethod
    def get_relation_names() -> list[str]:
        return ["Товары"]

    def get_relation_data(self) -> list[list[Relationable]]:
        return [self.items]

    @staticmethod
    def get_relation_attributes() -> list[str]:
        return ["Описание", "Тип", "Сумма", "Состояние"]

    def add_relation(self, item):
        self.add_items([item])

    def del_relation(self, item):
        self.del_items([item])

    @staticmethod
    def add_form_blueprint() -> FormBlueprint:
        return FormBlueprint() \
            .add(TextElem("Описание транзакции", str_constraint)) \
            .add(ListElem("Статус", ["Продажа", "Закупка"]))

    @staticmethod
    def add(parent: HasInternalRelations, attributes: list):
        if isinstance(parent, Store):
            trn = Transaction(parent, attributes[1] == "Закупка", attributes[0])
            parent.add_relation(trn)

    def edit_form_blueprint(self) -> FormBlueprint:
        return FormBlueprint() \
            .add(TextElem("Описание транзакции", str_constraint, self.desc)) \
            .add(ListElem("Статус", ["Продажа", "Закупка"], self.inward))

    def edit(self, attributes):
        self.desc = attributes[0]
        self.inward = attributes[1] == "Закупка"

    def complete(self):
        if self.parent.complete_monetary_transaction(self):
            self.completed = True

    def get_json(self):
        items_list = []
        for i in self.items:
            items_list.append(i.get_json())
        d = {
            'inward': self.inward,
            'desc': self.desc,
            'completed': self.completed,
            'items': items_list,
            'cost': self.cost
        }
        return d

    def __init__(self, parent, inward, desc='', completed=False, items=None, cost=0):
        super().__init__(parent, inward, completed, items, desc)
        self.parent: Store = parent
        self.cost = cost

    def count_cost(self):  # считает цену транзакции исходя из цены и кол-ва ее item-ов, не вызывать при перемещении
        self.cost = 0
        for i in self.items:
            self.cost += i.cost * i.quantity
        return self.cost


class MoveTransaction(BaseTransaction):

    @staticmethod
    def get_class_name():
        return "Движение товара"

    def complete(self):
        if self.parent.complete_move_transaction(self):
            self.completed = True

    @staticmethod
    def get_relation_classes() -> list[type[Relationable]]:
        return [Item]

    def get_relation_object(self) -> list[str]:
        return [self.desc,
                "Приход" if self.inward else "Отгрузка",
                self.uncle.str_address(),
                "Проведено" if self.completed else "В работе"]

    @staticmethod
    def get_relation_names() -> list[str]:
        return ["Товары"]

    def get_relation_data(self) -> list[list[Relationable]]:
        return [self.items]

    @staticmethod
    def get_relation_attributes() -> list[str]:
        return ["Описание", "Тип", "Адрес склада", "Состояние"]

    def add_relation(self, item):
        self.add_items([item])

    def del_relation(self, item):
        self.del_items([item])

    @staticmethod
    def add_form_blueprint() -> FormBlueprint:
        return FormBlueprint() \
            .add(TextElem("Описание транзакции", str_constraint)) \
            .add(ListElem("Отгрузка на", Warehouse.get_all_addresses(), 0, True))

    @staticmethod
    def add(parent: HasInternalRelations, attributes: list):
        if isinstance(parent, Store):
            trn = MoveTransaction(parent, False, Warehouse.find_warehouse_by_address(attributes[1]),
                                  False, None, attributes[0])
            parent.add_relation(trn)

    def edit_form_blueprint(self) -> FormBlueprint:
        all_addresses: list[str] = Warehouse.get_all_addresses()
        uncle_index = all_addresses.index(self.uncle.str_address())
        return FormBlueprint() \
            .add(TextElem("Описание транзакции", str_constraint, self.desc)) \
            .add(ListElem("Отгрузка на", Warehouse.get_all_addresses(), uncle_index, True))

    def edit(self, attributes):
        self.desc = attributes[0]
        self.uncle = Warehouse.find_warehouse_by_address(attributes[1])

    def get_json(self):
        items_list = []
        for i in self.items:
            items_list.append(i.get_json())
        d = {
            'uncle': self.uncle.address,
            'inward': self.inward,
            'desc': self.desc,
            'completed': self.completed,
            'items': items_list
        }
        return d

    def __init__(self, parent, inward, uncle, completed=False, items=None, desc=''):
        super().__init__(parent, inward, completed, items, desc)
        self.uncle: Warehouse = uncle


class Warehouse(HasInternalRelations, Addable, Editable):

    @staticmethod
    def get_class_name():
        return "Склад"

    @staticmethod
    def get_all_addresses() -> list[str]:
        return System.all_addresses()

    @staticmethod
    def add_form_blueprint() -> FormBlueprint:
        return FormBlueprint() \
            .add(TextElem("Страна", str_constraint)) \
            .add(TextElem("Город", str_constraint)) \
            .add(TextElem("Улица", str_constraint)) \
            .add(TextElem("Дом", str_constraint))

    @staticmethod
    def add(parent: HasInternalRelations, attributes: list):
        house = Warehouse(*attributes)
        house_address = house.str_address()
        if house_address not in Warehouse.get_all_addresses():
            parent.add_relation(house)
        else:
            messagebox.showerror("Ошибка в создании склада", "Адрес уже используется")

    def edit_form_blueprint(self) -> FormBlueprint:
        return FormBlueprint() \
            .add(TextElem("Страна", str_constraint, self.address["country"])) \
            .add(TextElem("Город", str_constraint, self.address["city"])) \
            .add(TextElem("Улица", str_constraint, self.address["street"])) \
            .add(TextElem("Дом", str_constraint, self.address["house"]))

    def edit(self, attributes: list):
        house_address = ', '.join(attributes)
        if house_address not in Warehouse.get_all_addresses():
            address_denomination = ["country", "city", "street", "house"]
            for i in range(4):
                self.address[address_denomination[i]] = attributes[i]
        else:
            messagebox.showerror("Ошибка в изменении адреса", "Адрес уже используется")

    @staticmethod
    def get_relation_attributes() -> list[str]:
        return ["Адрес", "Хранится товаров"]

    def str_address(self):
        address_denomination = ["country", "city", "street", "house"]
        return ', '.join([self.address[i] for i in address_denomination])

    def get_relation_object(self) -> list[str]:

        return [self.str_address(), sum([item.quantity for item in self.stored_items])]

    @staticmethod
    def get_relation_names() -> list[str]:
        return ["Опись", "Перемещения"]

    @staticmethod
    def get_relation_classes() -> list[type[Relationable]]:
        return [Item, Transaction]

    def get_relation_data(self) -> list[list[Relationable]]:
        return [self.stored_items, self.movements]

    def add_relation(self, item):
        res: int = -1
        if isinstance(item, Item):
            res = self.add_items([item])
        elif isinstance(item, BaseTransaction):
            res = self.add_transaction(item)
        return res

    def del_relation(self, item):
        res: int = -1
        if isinstance(item, Item):
            res = self.del_items([item])
        elif isinstance(item, BaseTransaction):
            res = self.del_transaction(item)
        return res

    def get_json(self):
        stored_items_json = []
        for i in self.stored_items:
            stored_items_json.append(i.get_json())
        movements_json = []
        for i in self.movements:
            movements_json.append(i.get_json())
        d = {
            'address': self.address,
            'items': stored_items_json,
            'movements': movements_json
        }
        return d

    def __init__(self, country, city, street, house):
        self.stored_items = []

        self.address = {
            "country": country,
            "city": city,
            "street": street,
            "house": house
        }
        self.movements = []

    def set_address(self, country='не указано', city='не указано', street='не указано', house='не указано'):
        self.address["country"] = country
        self.address["city"] = city
        self.address["street"] = street
        self.address["house"] = house
        return self.address

    def add_items(self, items):
        for i in items:
            flag = 0
            for j in self.stored_items:
                if i.name == j.name:
                    j.quantity += i.quantity
                    flag = 1
                    break
            if not flag:
                self.stored_items.append(i)
        return 1

    def del_items(self, items):  # передаются товары, из товаров на складе удаляются товары с тем же названием
        error_flag = 0
        items_to_del = []
        for i in items:
            flag = 0
            for j in self.stored_items:
                if i.name == j.name:
                    flag = 1
                    items_to_del.append(j)
            if not flag:
                print("Ошибка при удалении товара: на СКЛАДЕ нет товара с таким названием: ", i.name)
                error_flag = 1

        if error_flag:
            return 0

        # удаление своих item-ов
        for i in range(len(items)):
            self.stored_items.remove(items_to_del[i])
        return 1

    def add_transaction(self, transaction: BaseTransaction):
        if not isinstance(transaction, MoveTransaction): return
        if transaction not in self.movements:
            self.movements.append(transaction)
            return 1
        else:
            print("Ошибка при добавлении транзакции: транзакция уже заявлена")
            return 0

    def del_transaction(self, transaction: BaseTransaction):
        if not isinstance(transaction, MoveTransaction): return
        if transaction in self.movements:
            self.movements.remove(transaction)
            return 1
        else:
            print("Ошибка при удалении транзакции: нет такой транзакции")
            return 0

    def transfer_items(self, items, warehouse):  # перемещение товаров на другой склад
        # проверка, есть ли такие товары в нужном количестве на складе
        error_flag = 0
        items_to_transf = []
        for i in items:
            flag = 0
            for j in self.stored_items:
                if i.name == j.name:
                    flag = 1
                    items_to_transf.append(j)
                    if i.quantity > j.quantity:
                        print("Ошибка при перемещении: нет такого количества товара: ", i.name, i.quantity)
                        print("Актуальное количество товара: ", j.quantity)
                        error_flag = 1
                    break
            if not flag:
                print("Ошибка при перемещении: нет товара с таким названием: ", i.name)
                error_flag = 1

        if error_flag:
            return 0

        # удаление своих item-ов
        for i in range(len(items)):
            if items[i].quantity == items_to_transf[i].quantity:
                self.stored_items.remove(items_to_transf[i])
            else:
                items_to_transf[i].quantity -= items[i].quantity

        # добавление новой транзакции переданному складу
        tr = MoveTransaction(warehouse, inward=True, uncle=self, completed=False, items=items,
                             desc=f'Привоз: {self.str_address()} от {get_datetime()}')
        warehouse.add_transaction(tr)
        return 1



    def complete_move_transaction(self, transaction: MoveTransaction):
        if transaction.inward:
            self.add_items(transaction.items)
        else:
            self.transfer_items(transaction.items, transaction.uncle)

    @staticmethod
    def find_warehouse_by_address(strad):
        return System.address_to_warehouse(strad)


class Store(Warehouse):

    @staticmethod
    def get_class_name():
        return "Магазин"

    @staticmethod
    def get_relation_attributes() -> list[str]:
        return ["Адрес", "Хранится товаров", "Баланс"]

    def get_relation_object(self) -> list[str]:
        return [self.str_address(),
                sum([item.quantity for item in self.stored_items]),
                self.cash]

    @staticmethod
    def add_form_blueprint() -> FormBlueprint:
        return FormBlueprint() \
            .add(TextElem("Страна", str_constraint)) \
            .add(TextElem("Город", str_constraint)) \
            .add(TextElem("Улица", str_constraint)) \
            .add(TextElem("Дом", str_constraint)) \
            .add(TextElem("Баланс", int_constraint, "0"))

    @staticmethod
    def add(parent: HasInternalRelations, attributes: list):
        house = Store(*attributes)
        house_address = house.str_address()
        if house_address not in Warehouse.get_all_addresses():
            parent.add_relation(house)
        else:
            messagebox.showerror("Ошибка в создании склада", "Адрес уже используется")

    def edit_form_blueprint(self) -> FormBlueprint:
        return FormBlueprint() \
            .add(TextElem("Страна", str_constraint, self.address["country"])) \
            .add(TextElem("Город", str_constraint, self.address["city"])) \
            .add(TextElem("Улица", str_constraint, self.address["street"])) \
            .add(TextElem("Дом", str_constraint, self.address["house"])) \
            .add(TextElem("Баланс", int_constraint, str(self.cash)))

    def edit(self, attributes: list):
        house_address = ', '.join(attributes)
        if house_address not in Warehouse.get_all_addresses():
            address_denomination = ["country", "city", "street", "house"]
            for i in range(4):
                self.address[address_denomination[i]] = attributes[i]
            self.cash = attributes[4]
        else:
            messagebox.showerror("Ошибка в изменении адреса", "Адрес уже используется")

    @staticmethod
    def get_relation_classes() -> list[type[Relationable]]:
        return [Worker, Item, Transaction, MoveTransaction]

    def get_relation_data(self) -> list[list[Relationable]]:
        return [self.workers, self.stored_items, self.diary, self.movements]

    @staticmethod
    def get_relation_names() -> list[str]:
        return ["Кадры", "Опись", "Дневник", "Перемещения"]

    def get_json(self):
        workers_json = []
        for i in self.workers:
            workers_json.append(i.get_json())
        diary_json = []
        for i in self.diary:
            diary_json.append(i.get_json())
        items_json = []
        for i in self.stored_items:
            items_json.append(i.get_json())
        movements_json = []
        for i in self.movements:
            movements_json.append(i.get_json())
        d = {
            "address": self.address,
            "cash": self.cash,
            "workers": workers_json,
            "diary": diary_json,
            "items": items_json,
            "movements": movements_json
        }
        return d

    def __init__(self, country, city, street, house, cash=0):
        super().__init__(country, city, street, house)
        self.cash = cash
        self.workers: list[Worker] = []
        self.diary = []

    def add_relation(self, item):
        res: int = -1
        if isinstance(item, Item):
            res = self.add_items([item])
        elif isinstance(item, BaseTransaction):
            res = self.add_transaction(item)
        elif isinstance(item, Worker):
            res = self.hire(item)
        return res

    def del_relation(self, item):
        res: int = -1
        if isinstance(item, Item):
            res = self.del_items([item])
        elif isinstance(item, BaseTransaction):
            res = self.del_transaction(item)
        elif isinstance(item, Worker):
            res = self.fire(item)
        return res

    def add_transaction(self, transaction: BaseTransaction):
        if isinstance(transaction, MoveTransaction):
            if transaction not in self.movements:
                self.movements.append(transaction)
                return 1
            else:
                print("Ошибка при добавлении транзакции: транзакция уже заявлена")
                return 0
        if isinstance(transaction, Transaction):
            if transaction not in self.diary:
                self.diary.append(transaction)
                return 1
            else:
                print("Ошибка при добавлении транзакции: транзакция уже заявлена")
                return 0

    def del_transaction(self, transaction: BaseTransaction):
        if isinstance(transaction, MoveTransaction):
            if transaction in self.movements:
                self.movements.remove(transaction)
                return 1
            else:
                print("Ошибка при удалении транзакции: нет такой транзакции")
                return 0
        if isinstance(transaction, Transaction):
            if transaction in self.diary:
                self.diary.remove(transaction)
                return 1
            else:
                print("Ошибка при удалении транзакции: нет такой транзакции")
                return 0

    def sell_items(self, items):
        # проверка, есть ли такие товары в нужном количестве на складе
        error_flag = 0
        items_to_sell = []
        for i in items:
            flag = 0
            for j in self.stored_items:
                if i.name == j.name:
                    flag = 1
                    if i.quantity > j.quantity:
                        print("Ошибка при продаже: нет такого количества товара: ", i.name, i.quantity)
                        print("Актуальное количество товара: ", j.quantity)
                        error_flag = 1
                    else:
                        items_to_sell.append(j)
                    break
            if not flag:
                print("Ошибка при продаже: нет товара с таким названием: ", i.name)
                error_flag = 1

        if error_flag:
            return 0

        # удаление своих item-ов и начисление деняк
        for i in range(len(items)):
            if items[i].quantity == items_to_sell[i].quantity:
                self.stored_items.remove(items_to_sell[i])
            else:
                items_to_sell[i].quantity -= items[i].quantity
            self.cash += items[i].cost * items[i].quantity

        return 1

    def complete_monetary_transaction(self, transaction: Transaction):
        if transaction.inward:
            self.cash -= transaction.cost
            self.add_items(transaction.items)
            return 1
        else:
            self.cash += transaction.cost
            return self.sell_items(transaction.items)

    def pay_all_workers(self):
        sum_ = sum([worker.salary for worker in self.workers])
        if sum_ < self.cash:
            messagebox.showerror("Ошибка оплаты", "Баланс магазина меньше, чем зарплата всех работников.")
            return
        for wrk in self.workers:
            wrk.get_salary(self)

    def hire(self, worker):
        if worker not in self.workers:
            self.workers.append(worker)
            return 1
        else:
            print("Ошибка при найме: рабочий уже нанят")
            return 0

    def fire(self, worker):
        if worker in self.workers:
            self.workers.remove(worker)
            return 1
        else:
            print("Ошибка при увольнении: выбранный рабочий не нанят")
            return 0


class Worker(Addable, Editable, Deletable):
    @staticmethod
    def get_relation_attributes() -> list[str]:
        return ["№", "Имя", "Оклад", "Номер телефона"]

    def get_relation_object(self) -> list[str]:
        return [str(self.id), self.name, str(self.salary), self.phone]

    @staticmethod
    def add_form_blueprint() -> FormBlueprint:
        form = FormBlueprint()
        # блин прописать бы ограничение на уникальный id, но хз как
        id_input = TextElem("id", unsigned_int_constraint)
        name_input = TextElem("Имя", str_constraint)
        salary_input = TextElem("Зарплата", unsigned_int_constraint)
        phone_input = TextElem("телефонный номер", str_constraint)
        form.add(id_input).add(name_input).add(salary_input).add(phone_input)
        return form

    @staticmethod
    def add(parent: HasInternalRelations, attributes: list):
        wrk = Worker(*attributes)
        parent.add_relation(wrk)

    def edit_form_blueprint(self) -> FormBlueprint:
        form = FormBlueprint()
        # id неизменяемый, навсякий
        name_input = TextElem("Имя", str_constraint, self.name)
        salary_input = TextElem("Зарплата", unsigned_int_constraint, self.salary)
        phone_input = TextElem("телефонный номер", str_constraint, self.phone)
        form.add(name_input).add(salary_input).add(phone_input)
        return form

    def edit(self, attributes):
        self.name = attributes[0]
        self.salary = attributes[1]
        self.phone = attributes[2]

    def delete(self, parent: HasInternalRelations):
        parent.del_relation(self)

    def get_json(self):
        d = {
            "id": self.id,
            "name": self.name,
            "salary": self.salary,
            "phone": self.phone
        }
        return d

    def __init__(self, id=-1, name='', salary=0, phone=''):
        self.id = id
        self.name = name
        self.salary = salary
        self.phone = phone

    def __str__(self):
        return "name={}, id={}, salary={}, phone={}".format(self.name, self.id, self.salary, self.phone)

    def get_salary(self, store):
        if self.salary <= store.cash:
            store.cash -= self.salary
            return 1
        else:
            print("Ошибка при выдаче зарплаты: в магазине с id={} недостаточно денег "
                  "(cash={}, требуемая сумма = {})".format(store.id, store.cash, self.salary))
            return 0


class System(HasInternalRelations):
    single_instance = None

    @staticmethod
    def get_class_name():
        return "Программа для управления бизнес-процессами сети магазинов электроники"

    def get_json(self):
        stores = []
        for i in self.stores:
            stores.append(i.get_json())
        warehouses = []
        for i in self.warehouses:
            warehouses.append(i.get_json())
        d = {
            "stores": stores,
            "warehouses": warehouses
        }
        return d

    def __init__(self):
        System.single_instance = self
        self.stores: list[Store] = []
        self.warehouses: list[Warehouse] = []

    @staticmethod
    def get_relation_names() -> list[str]:
        return ["Магазины", "Склады"]

    def get_relation_data(self) -> list[list[Relationable]]:
        return [System.single_instance.stores, System.single_instance.warehouses]

    @staticmethod
    def get_relation_classes() -> list[type[Relationable]]:
        return [Store, Warehouse]

    def add_relation(self, item):
        if isinstance(item, Store):
            System.single_instance.stores.append(item)
        elif isinstance(item, Warehouse):
            System.single_instance.warehouses.append(item)

    def del_relation(self, item):
        if isinstance(item, Store) and item in System.single_instance.stores:
            System.single_instance.stores.remove(item)
        elif isinstance(item, Warehouse) and item in System.single_instance.warehouses:
            System.single_instance.warehouses.remove(item)

    @staticmethod
    def get_relation_attributes() -> list[str]:
        return ["Версия"]

    def get_relation_object(self) -> list[str]:
        return ["0.3.2"]

    @staticmethod
    def all_addresses():
        return [store.str_address() for store in System.single_instance.stores] + \
               [warehouse.str_address() for warehouse in System.single_instance.warehouses]

    @staticmethod
    def address_to_warehouse(strad):
        for warehouse in System.single_instance.stores + System.single_instance.warehouses:
            if warehouse.str_address() == strad:
                return warehouse
        return None
