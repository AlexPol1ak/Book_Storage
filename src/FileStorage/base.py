import os
import shutil


class BaseStorage:
    def __init__(self, storage_path: str, storage_name: str):
        """
        Storage Initializer.
        :param storage_path: Path to the directory where the repository should be created.
        :param storage_name: Storage directory name .
        """
        self.__path = self.__create_storage(storage_path, storage_name)
        self.__name = storage_name

    def __create_storage(self, storage_path: str, storage_name: str) -> str:
        """
        Creates a storage directory if it does not exist. If it exists, connects to it.
        :param storage_path: Path to the directory where the repository should be created.
        :param storage_name: Storage directory name .
        :return: Full path to the storage directory.
        """
        full_path = self.__validate_path(storage_path)
        storage_path = os.path.join(full_path, storage_name)
        try:
            os.mkdir(storage_path)
        except FileExistsError:
            pass
        return storage_path

    @staticmethod
    def __validate_path(storage_path: str) -> str:
        """
        Checks whether the path exists, whether the path points to a directory,
        whether the path is absolute or relative.
        Returns absolute path.
        """
        if not os.path.exists(storage_path):
            raise NotADirectoryError
        else:
            if not os.path.isdir(storage_path):
                raise NotADirectoryError
            else:
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
        """
        if os.path.isdir(self.__path):
            if not all_files:
                try:
                    os.rmdir(self.__path)
                except FileNotFoundError:
                    raise FileNotFoundError("Directory not found.")
                except OSError:
                    raise OSError("The directory is not empty. If you really want to delete the repository and files "
                                  "use the flag all_files=True")
            elif all_files:
                shutil.rmtree(self.__path)
        else:
            raise FileNotFoundError("Directory not found.")

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

    def __repr__(self):
        return f"Storage:\nName: {self.name}\nPath: {self.path}"

