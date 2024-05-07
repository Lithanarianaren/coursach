from abc import ABC, abstractmethod

from gui.relation.Relationable import Relationable


class HasInternalRelations(ABC):

    @staticmethod
    @abstractmethod
    def get_relation_names() -> list[str]:
        """
        Возвращает имена таблиц, которыми обладает объект.

        Пример:

        Объект класса "Магазин" будет обладать таблицами "Кадры", "Опись", "Дневник закупок", "Дневник продаж",
        "Дневник перемещений".

        """
        raise NotImplementedError

    @abstractmethod
    def get_relation_data(self) -> list[list[Relationable]]:
        """
        Возвращает списки объектов, которые можно положить в таблицу.

        Пример:

        Объект класса "Магазин" будет обладать списком работников, списком товаров, несколькими списками транзакций.

        """
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def get_relation_classes() -> list[type[Relationable]]:
        """
        Возвращает классы объектов, которые можно положить в таблицу.

        Пример:

        Объект класса "Магазин" вернёт классы "работник", "товар", несколько раз "транзакция".

        """
        raise NotImplementedError
