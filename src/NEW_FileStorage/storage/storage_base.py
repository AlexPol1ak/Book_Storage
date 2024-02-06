import os
import shutil


# Базовый класс хранилища. Поставляет инициализатор и служебные, вспомогательные методы для создания хранилища
# и его удаления.
# Создает и удаляет директорию хранилища в файловой системе.
# Инициализирует переменные хранящие путь к хранилищу, его имя и флаг временного хранилища

class BaseStorage:
    """Basic storage for storing files."""

    def __init__(self, storage_path: str, storage_name: str, temporary: bool = False):
        """
        Storage initialization.
        :param storage_path: Path to the directory where the repository should be created.
        :param storage_name: Storage directory name .
        """
        self.__path, self.__name = self.__get_or_create(storage_path, storage_name)
        self.__temporary = temporary

    def __del__(self):
        if self.__temporary:
            self.delete_storage(all_files=True)
        del self

    def __repr__(self):
        return f"Storage:\nName: {self.name}\nPath: {self.path}Temporary: {self.temporary}"

    @property
    def path(self):
        return self.__path

    @path.getter
    def path(self):
        return self.__path

    @path.setter
    def path(self, value):
        raise IsADirectoryError("You cannot change the path to a repository after it has been created.")

    @path.deleter
    def path(self):
        raise IsADirectoryError("You cannot delete the path to a repository it has been created. Call the method "
                                "delete_storage")

    @property
    def name(self):
        return self.__name

    @name.getter
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        raise ValueError("You cannot change the name of a repository after it has been created.")

    @name.deleter
    def name(self):
        raise NameError("You cannot change the name of a repository after it has been created. Call the method "
                        "delete_storage")

    @property
    def temporary(self):
        return self.__temporary

    @temporary.setter
    def temporary(self, value):
        raise ValueError("The storage type cannot be changed after it has been created.")

    def __get_or_create(self, storage_path: str, storage_name: str) -> tuple[str, str]:
        """
        If the storage already exists on disk - it returns the absolute path to it and its name.
        If it does not exist, it creates it and returns absolute path and name.
        :param storage_path: Path to the directory where the repository should be created.
        :param storage_name: Storage directory name .
        :return: Absolute path to storage , storage name.
        """
        storage_path = self.__validate_path(storage_path)
        full_path = os.path.join(storage_path, storage_name)
        if os.path.isdir(full_path):
            return full_path, storage_name
        else:
            return self.__create_storage(storage_path, storage_name), storage_name

    def __create_storage(self, storage_path: str, storage_name: str) -> str:
        """
        Creates a storage directory if it does not exist. If it exists, connects to it.
        :param storage_path: Path to the directory where the repository should be created.
        :param storage_name: Storage directory name .
        :return: Full path to the storage directory.
        """
        full_path = os.path.join(storage_path, storage_name)
        try:
            os.mkdir(full_path)
        except FileExistsError:
            pass
        return full_path

    @staticmethod
    def __validate_path(storage_path: str) -> str:
        """
        Checks whether the path exists, whether the path points to a directory,
        whether the path is absolute or relative.
        Returns absolute path.
        """
        if not os.path.exists(storage_path):
            raise NotADirectoryError(f"Path: {storage_path} not found")

        if not os.path.isdir(storage_path):
            raise NotADirectoryError(f"The path: {storage_path} doesn't lead to a directory.")

        if os.path.isabs(storage_path):
            return storage_path
        else:
            return os.path.abspath(storage_path)

    def delete_storage(self, all_files: bool = False) -> None:
        """
        Deletes storage.
        :param all_files: If True, it tries to delete the storage and all files in it.
                          If False - deletes the repository if it is empty or raises OSError. Default is False.
        :return: None
        :raises FileNotFoundError: If the directory is not found.
        :raises IsADirectoryError: If the directory is not empty.
        """
        if os.path.isdir(self.__path):
            if not all_files:
                try:
                    os.rmdir(self.__path)
                except FileNotFoundError:
                    raise FileNotFoundError("Directory not found.")
                except OSError:
                    raise IsADirectoryError("The directory is not empty. If you really want to delete the repository "
                                            "and fil use the flag all_files=True")
            elif all_files:
                shutil.rmtree(self.__path)
        else:
            raise FileNotFoundError("Directory not found.")




