from bd.filesInterfaces import *
from classes import *
import json

# для сохранения просто вызываем SaveJSON.save_system(System)
# для загрузки просто вызываем LoadJSON.load_system(), вернет готовую систему

class SavingJSON(SavingInterface):
    @staticmethod
    def save_system(system: System):
        system_json = system.get_json()
        with open('../json/system.json', 'w') as f:
            json.dump(system_json, f, indent=4)


class LoadJSON(LoadInterface):
    @staticmethod
    def load_system() -> System:
        with open('../json/system.json') as f:
            data = json.load(f)
            movements_pairs = []
            # в movements_pairs стакаем пары Warehouse (или Store) - MoveTransaction,
            # после того как распарсятся все склады
            # начинаем парсить перемещения
            # так надо, потому что о дядюшках мы знаем только адреса
            stores = []
            for i in data["stores"]:
                stores.append(LoadJSON.parseStore(i, movements_pairs))
            warehouses = []
            for i in data["warehouses"]:
                warehouses.append(LoadJSON.parseWarehouse(i, movements_pairs))

            sys = System()
            for i in stores:
               sys.add_relation(i)
            for i in warehouses:
                sys.add_relation(i)

            for i in movements_pairs:
                movement = LoadJSON.parseMoveTransaction(i[0], i[1], sys)
                i[1].add_relation(movement)

            return sys

    @staticmethod
    def parseStore(store, movements_pairs) -> Store:
        address = store["address"]
        cash = store["cash"]

        res = Store(address["country"], address["city"], address["street"], address["house"], cash)

        for i in store["workers"]:
            res.add_relation(LoadJSON.parseWorker(i))
        for i in store["items"]:
            res.add_relation(LoadJSON.parseItem(i))
        for i in store["diary"]:
            res.add_relation(LoadJSON.parseTransaction(i, res))

        mv = store["movements"]
        for i in mv:
            movements_pairs.append((i, res))
        return res

    @staticmethod
    def parseWarehouse(wh, movements_pairs) -> Warehouse:
        address = wh["address"]
        stored_items = wh["items"]
        res = Warehouse(address["country"], address["city"], address["street"], address["house"])
        for i in stored_items:
            res.add_relation(LoadJSON.parseItem(i))

        mv = wh["movements"]
        for i in mv:
            movements_pairs.append((i, res))

        return res

    @staticmethod
    def parseWorker(worker):
        id = worker["id"]
        name = worker["name"]
        salary = worker["salary"]
        phone = worker["phone"]
        res = Worker(id, name, salary, phone)
        return res

    @staticmethod
    def parseItem(item):
        name = item["name"]
        qty = item["quantity"]
        cost = item["cost"]
        res = Item(name, qty, cost)
        return res

    @staticmethod
    def parseTransaction(tr, parent):
        inward = tr["inward"]
        desc = tr["desc"]
        completed = tr["completed"]
        cost = tr["cost"]
        items = []
        for i in tr["items"]:
            items.append(LoadJSON.parseItem(i))
        res = Transaction(parent, inward, desc, completed, items, cost)
        return res

    @staticmethod
    def parseMoveTransaction(tr, parent, system):
        inward = tr["inward"]
        completed = tr["completed"]
        desc = tr["desc"]
        items = []
        for i in tr["items"]:
            items.append(LoadJSON.parseItem(i))

        uncle_address = tr["uncle"]
        address_denomination = ["country", "city", "street", "house"]
        uncle_address = ', '.join([uncle_address[i] for i in address_denomination])
        uncle = system.address_to_warehouse(uncle_address)

        res = MoveTransaction(parent, inward, uncle, completed, items, desc)
        return res