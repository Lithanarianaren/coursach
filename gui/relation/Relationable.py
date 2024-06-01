from abc import ABC, abstractmethod

from gui.form.blueprints import FormBlueprint


class Relationable(ABC):

    @staticmethod
    @abstractmethod
    def get_relation_attributes() -> list[str]:
        """
        Возвращает имена атрибутов отношения
        """
        raise NotImplementedError

    @abstractmethod
    def get_relation_object(self) -> list[str]:
        """
        Для каждого объекта возвращает строковые значения его атрибутов
        """
        raise NotImplementedError


class Addable(Relationable, ABC):
    """
    класс, от которого наследуют все Relationable, к которым прикручена форма создания
    """

    @staticmethod
    def add_form_blueprint() -> FormBlueprint:
        """
        возвращает чертёж формы создания.
        """
        raise NotImplementedError


class Editable(Relationable, ABC):
    """
    класс, от которого наследуют все Relationable, к которым прикручена форма редактирования
    """

    @staticmethod
    def edit_form_blueprint() -> FormBlueprint:
        """
        возвращает чертёж формы редактирования.
        """
        raise NotImplementedError
