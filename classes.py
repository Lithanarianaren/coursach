from gui.relation.Relationable import HasInternalRelations
from gui.relation.Relationable import Relationable


class Item(Relationable):
    def __init__(self, name="item", quantity=1, cost=0):
        self.name = name
        self.cost = cost
        self.quantity = quantity

    def __str__(self):
        return "name={}, cost={}, quantity={}".format(self.name, self.cost, self.quantity)

    @staticmethod
    def get_relation_attributes() -> list[str]:
        return ["Наименование", "Цена", "Количество"]

    def get_relation_object(self) -> list[str]:
        return [self.name, str(self.cost), str(self.quantity)]


class Transaction(HasInternalRelations):
    @staticmethod
    def get_relation_classes() -> list[type[Relationable]]:
        return [Item]

    def get_relation_object(self) -> list[str]:
        return [self.desc, str(self.cost)]

    @staticmethod
    def get_relation_names() -> list[str]:
        return ["Товары"]

    def get_relation_data(self) -> list[list[Relationable]]:
        return [self.items]

    @staticmethod
    def get_relation_attributes() -> list[str]:
        return ["Описание", "Сумма"]

    def __init__(self, items=None, desc='', cost=0):
        if items is None:
            items = []
        self.desc = desc
        self.cost = cost
        if isinstance(items, list):
            self.items = items
        else:
            self.items = []

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

    def count_cost(self):  # считает цену транзакции исходя из цены и кол-ва ее item-ов, не вызывать при перемещении
        self.cost = 0
        for i in self.items:
            self.cost += i.cost * i.quantity
        return self.cost

    def __str__(self):
        return "description={}, cost={}, items={}".format(self.desc, self.cost, self.items)


class Warehouse(HasInternalRelations):
    @staticmethod
    def get_relation_attributes() -> list[str]:
        return ["№","Адрес"]

    def get_relation_object(self) -> list[str]:
        addr_denom=["country","city","street","house"]
        addr=', '.join([self.address[i] for i in addr_denom])
        return [str(self.id),addr]

    @staticmethod
    def get_relation_names() -> list[str]:
        return ["Кадры","Опись","Дневник","Текущие транзакции"]

    @staticmethod
    def get_relation_classes() -> list[type[Relationable]]:
        return [Worker,Item,Transaction,Transaction]

    def get_relation_data(self) -> list[list[Relationable]]:
        return [self.workers,self.stored_items,self.diary,self.active_trans]

    def __init__(self, id=-1):
        self.id = id
        self.stored_items = []
        self.workers = []
        self.address = {
            "country": "",
            "city": "",
            "street": "",
            "house": ""
        }
        self.diary = []
        self.active_trans = []

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

    def accept_transaction(self, transaction):  # если транзакция есть в списке активных транзакций - принять
        if transaction in self.active_trans:
            self.active_trans.remove(transaction)
            self.add_items(transaction.items)

            diary_note = Transaction(transaction.items, "принята поставка")
            self.diary.append(diary_note)
            return 1
        else:
            print("Ошибка при принятии транзакции: транзакция не была заявлена")
            return 0

    def add_transaction(self, transaction):
        if transaction not in self.active_trans:
            self.active_trans.append(transaction)
            return 1
        else:
            print("Ошибка при добавлении транзакции: транзакция уже заявлена")
            return 0

    def del_transaction(self, transaction):
        if transaction in self.active_trans:
            self.active_trans.remove(transaction)
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
        tr = Transaction(items)
        warehouse.add_transaction(tr)

        # добавление записи в журнал
        diary_note = Transaction(items, "перемещение товара на склад c id={}".format(warehouse.id))
        self.diary.append(diary_note)
        return 1

    def hire(self, worker):
        if worker not in self.workers:
            self.workers.append(worker)
            diary_note = Transaction([], "нанят {}, id={}".format(worker.name, worker.id))
            self.diary.append(diary_note)
            return 1
        else:
            print("Ошибка при найме: рабочий уже нанят")
            return 0

    def fire(self, worker):
        if worker in self.workers:
            self.workers.remove(worker)
            diary_note = Transaction([], "уволен {}, id={}".format(worker.name, worker.id))
            self.diary.append(diary_note)
            return 1
        else:
            print("Ошибка при увольнении: выбранный рабочий не нанят")
            return 0


class Store(Warehouse):
    def __init__(self, id, cash=0):
        super().__init__(id)
        self.cash = cash

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

        # добавление записи в дневник
        diary_note = Transaction(items, "продажа товара")
        diary_note.count_cost()
        self.diary.append(diary_note)
        return 1

    def buy_items(self, items):
        tr = Transaction(items)
        tr.count_cost()

        if tr.cost > self.cash:
            print("Ошибка при покупке товара: недостаточно денег")
            return 0

        self.active_trans.append(tr)
        self.cash -= tr.cost

        # добавление записи в дневник
        diary_note = Transaction(items, 'покупка товара')
        diary_note.count_cost()
        self.diary.append(diary_note)
        return 1


class Worker(Relationable):
    @staticmethod
    def get_relation_attributes() -> list[str]:
        return ["№","Имя","Оклад","Номер телефона"]

    def get_relation_object(self) -> list[str]:
        return [str(self.id),self.name,str(self.salary),self.phone]

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
            # добавление записи в дневник магазина
            diary_note = Transaction([], "выдана зарплата работнику {}, id={}".format(self.name, self.id), self.salary)
            store.diary.append(diary_note)
            return 1
        else:
            print("Ошибка при выдаче зарплаты: в магазине с id={} недостаточно денег "
                  "(cash={}, требуемая сумма = {})".format(store.id, store.cash, self.salary))
            return 0


# тесты, чекать по желанию
item1 = Item("moloko", 100, 3)
item2 = Item("sapog", 1000, 13)
item3 = Item("karandash", 35, 50)

wh1 = Warehouse()
wh1.id = 1
wh1.add_items([item1, item2])

whSev = Warehouse()
whSev.id = 2
whSev.add_items([item3])

# count_cost
tr1 = Transaction([item1, item3], "new purchase")

print(tr1.count_cost())

# transfer_items & add_transaction & accept_transaction & add_items
itemToTrans = Item("moloko", 100, 2)
wh1.transfer_items([itemToTrans], whSev)
whSev.accept_transaction(whSev.active_trans[0])

# hire и fire
wrk = Worker(1, "loh", 350, "88005553555")
whSev.hire(wrk)
whSev.fire(wrk)

# del_items
tr = Transaction([item1, item2])
tr.del_items([Item("sapog")])
whSev.del_items([Item("moloko")])

for i in whSev.stored_items:
    print(i)

# del_transaction
whSev.add_transaction(tr)
whSev.del_transaction(tr)

# sell_items & buy_items
sevStore = Store(1, 3000)
sevStore.buy_items([item1])
sevStore.accept_transaction(sevStore.active_trans[0])

print(sevStore.stored_items[0], sevStore.cash)

sevStore.sell_items([Item("moloko", 90)])

print(sevStore.cash)

# get_salary
wrk.salary += 300
wrk.get_salary(sevStore)

print(sevStore.cash)

for i in sevStore.diary:
    print(i)
