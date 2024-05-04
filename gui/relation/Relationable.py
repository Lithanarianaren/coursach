from abc import ABC, abstractmethod


class Relationable(ABC):

    @staticmethod
    @abstractmethod
    def get_relation_attributes() -> tuple[str]:
        """
        Возвращает имена атрибутов отношения
        """
        raise NotImplementedError

    @abstractmethod
    def get_relation_object(self) -> tuple[str]:
        """
        Для каждого объекта возвращает строковые значения его атрибутов
        """
        raise NotImplementedError
