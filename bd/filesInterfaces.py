from classes import System


# класс, определяющий методы для всех ссохрраняющих классов, которые можно написать
class SavingInterface:
    @staticmethod
    def save_system(system: System):
        """
        передаем че сохранять и вот готово
        """
        raise NotImplementedError


class LoadInterface:
    @staticmethod
    def load_system() -> System:
        """
        возвращает готовый экземпляр класса System
        """
        raise NotImplementedError
