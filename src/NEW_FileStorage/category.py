from typing import Self

from NEW_FileStorage.storage.storage import Storage


# Класс категории хранилища. Взаимодействует с хранилищем. Предоставляет функционал создания, удаления
# директории категории в хранилище.
# Предоставляет функционал перемещения файлов из одной категории в другую, размер категории и количество файлов в ней.

class Category:
    """Manage categories in the repository."""

    def __init__(self, name):

        self.__name = name
        self.__storage: Storage | None = None
        self.__path: str | None = None

    def __repr__(self):
        return f"Category: {self.name}. Path: {self.path}\n"

    def __eq__(self, other: Self):
        if self.name == other.name and self.path == other.path and self.storage is other.storage:
            return True
        else:
            return False


    @property
    def name(self):
        return self.__name

    @property
    def storage(self) -> Storage:
        return self.__storage

    @property
    def path(self):
        return self.__path


    @classmethod
    async def __validate_storage(cls, storage: Storage) -> None:
        """
        Verifies that the storage is correct.
        :param storage: Storage instance
        :return: None
        :raises TypeError: If the argument is not a valid storage instance.
        """
        if not isinstance(storage, Storage):
            raise TypeError("The argument must be an instance of the Storage class.")
