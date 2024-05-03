class Item:
    def __init__(self, name="item", cost=0, quantity=1):
        self.name = name
        self.cost = cost
        self.quantity = quantity

    def __str__(self):
        return "name={}, cost={}, quantity={}".format(self.name, self.cost, self.quantity)


class Transaction:
    def __init__(self, items):
        self.desc = ''
        self.cost = 0
        if isinstance(items, list):
            self.items = items
        else:
            self.items = []

    def add_items(self, items):  #ожидает список предметов
        for i in items:
            flag = 0
            for j in self.items:
                if i.name == j.name:
                    j.quantity += i.quantity
                    flag = 1
                    break
            if not flag:
                self.items.append(i)

    def count_cost(self):  #считает цену транзакции исходя из цены и кол-ва ее item-ов, не вызывать при перемещении
        for i in self.items:
            self.cost += i.cost * i.quantity
        return self.cost


class Warehouse:
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

    def set_address(self, country, city, street, house):
        self.address.country = country
        self.address.city = city
        self.address.street = street
        self.address.house = house
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

    def accept_transaction(self, transaction): #если транзакция есть в списке активных транзакций - принять
        if transaction in self.active_trans:
            self.active_trans.remove(transaction)
            self.add_items(transaction.items)
        else:
            print("Транзакция не была заявлена")
            return

    def add_transaction(self, transaction):
        self.active_trans.append(transaction)

    def transfer_items(self, items, warehouse): #перемещение товаров на другой склад
        #удаление своих item-ов
        for i in items:
            for j in self.stored_items:
                if i.name == j.name:
                    if i.quantity < j.quantity:
                        j.quantity -= i.quantity
                    elif i.quantity == j.quantity:
                        self.stored_items.remove(j)
                    break
        #добавление новой транзакции переданному складу
        tr = Transaction(items)
        warehouse.add_transaction(tr)

    def hire(self, worker):
        self.workers.append(worker)

    def fire(self, worker):  #удаляет работника по его id
        self.workers.remove(worker)


class Store(Warehouse):
    def __init__(self, id, cash=0):
        super().__init__(id)
        self.cash = cash

    def sell_items(self, items):
        for i in items:
            for j in self.stored_items:
                if i.name == j.name:
                    if i.quantity < j.quantity:
                        j.quantity -= i.quantity
                    elif i.quantity == j.quantity:
                        self.stored_items.remove(j)
                    break

    def buy_items(self, items):
        tr = Transaction(items)
        self.active_trans.append(tr)

        tr.count_cost()
        self.cash -= tr.cost


class Worker:
    def __init__(self, id=-1, name='', salary=0, phone=''):
        self.id = id
        self.name = name
        self.salary = salary
        self.phone = phone


#тесты

item1 = Item("moloko", 100, 3)
item2 = Item("sapog", 1000, 13)
item3 = Item("karandash", 35, 50)

wh1 = Warehouse()
wh1.id = 1
wh1.add_items([item1, item2])

whSev = Warehouse()
whSev.id = 2
whSev.add_items([item3])

itemToTrans = Item("moloko", 100, 2)

wh1.transfer_items([itemToTrans], whSev)

print(whSev.active_trans[0])