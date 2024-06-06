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

    @abstractmethod
    def get_json(self):
        """
        преобразовывает объект в словарь со всей инфой о нем
        :return: словарь, отображающий структуру объекта
        """
        raise NotImplementedError


class HasInternalRelations(Relationable):

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


    def add_relation(self, item):
        """
        чтобы добавить Relationable элемент надо вызвать эту функцию у его родителя
        """
        raise NotImplementedError


    def del_relation(self, item):
        """
        При удалении элемента надо знать откуда он удаляется, так что сделал так
        """
        raise NotImplementedError

    @staticmethod
    def get_class_name():
        raise NotImplementedError

    @abstractmethod
    def get_json(self):
        """
        преобразовывает объект в словарь со всей инфой о нем
        :return: словарь, отображающий структуру объекта
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

    @staticmethod
    def add(parent: HasInternalRelations, attributes: list):
        """
        :param parent: HasInternalRelations, из которого была вызвана форма создания
        :param attributes: список атрибутов, соответствующий чертежу формы (если надо словарь, пиши)
        """
        raise NotImplementedError


class Editable(Relationable, ABC):
    """
    класс, от которого наследуют все Relationable, к которым прикручена форма редактирования
    """

    def can_be_edited(self):
        return True

    # сделал метод не статическим потому что в форму надо подставлять значения конкретного элемента
    def edit_form_blueprint(self) -> FormBlueprint:
        """
        возвращает чертёж формы редактирования.
        """
        raise NotImplementedError

    def edit(self, attributes: list):
        """
        :param attributes: список атрибутов, соответствующий чертежу формы (если надо словарь, пиши)
        """
        raise NotImplementedError


class Deletable(Relationable, ABC):
    """
    класс, от которого наследуют все Relationable, к которым прикручена кнопка удаления. полиморфизм на максималках.
    """

    def can_be_deleted(self):
        return True

    def delete(self, parent: HasInternalRelations):
        """
        :return: удаление объекта из базы данных и все (каскадные?) вытекающие
        """
        raise NotImplementedError
