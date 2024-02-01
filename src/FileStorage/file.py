import os.path
from datetime import datetime
import aiofiles.os as a_os
import aioshutil as a_shutil

from FileStorage.storage import Storage
from FileStorage.сategory import CategoryManager


class FileManager(CategoryManager):
    """File and category management manager."""

    def __init__(self, storage: Storage, allowed_extensions: list):
        """
        Initialization of the storage and the list of file extensions the manager will be allowed to work with.
        :param storage: Storage, an instance of the Storage class.
        :param allowed_extensions: List of valid file extensions.
        :raises ValueError:If the list of valid file extensions is empty.
        :raises TypeError: If the objects in the list of valid file extensions are not strings.
        """
        super().__init__(storage)
        if len(allowed_extensions) == 0:
            raise ValueError("Empty list 'allowed_extensions'.")
        for ext in allowed_extensions:
            if not isinstance(ext, str):
                raise TypeError(f"{ext} - invalid file extension type. Extensions should be a string.")
        self.allowed_extensions = tuple(allowed_extensions)

    async def add_file(self, file_path: str, category: str, only_copy: bool = False, add_unique_name: bool = True) \
            -> dict:
        """
        Checks if the file is correct and adds it to the category.
        :param file_path: Path to the file to be added.
        :param category: The name of the category to which you want to add the file.
        :param only_copy: Determines whether the file should be remixed or copied.
                          If True, the file is copied.
                          If False, the file is moved to the specified category and deleted in the original category.
                          Default False.
        :param add_unique_name: Whether you need to add unique characters to the file name. Default is True.
        :return: Dictionary with data about the added file.
        :raises NotADirectoryError: If category not found.
        :raises FileNotFoundError: If the file is not found
        :raises TypeError: If it is not a file or working with a file of this type is not allowed.
        """

        category_path = await self.get_category_path(category)
        file_info: dict = await self.__parse_file_info(file_path)
        await self.__validate_ext(file_info.get('ext'))  # Is it permissible to add a file of this type.

        # Adding unique literals from the current date and time to the file name.
        if add_unique_name:
            name = await self.__get_unique_name(file_info.get('name'))
        else:
            name = file_info.get('name')

        src = file_path  # The starting point of the file.
        dst = os.path.join(category_path, name + file_info.get('ext'))  # File Endpoint.

        """Move a file or copy a file."""
        if not only_copy:
            dst = await a_shutil.move(src, dst)
        else:
            await a_shutil.copy2(src, dst)

        return await self.__parse_file_info(dst)

    async def get_file(self):
        pass

    async def delete_file(self):
        pass

    async def __parse_file_info(self, file_path: str) -> dict:
        """
        Returns information about the file: Full path, folder path, file, file name, file extension, file size in bytes.
        :param file_path: File Path.
        :return: A dictionary with data about the file.
        :raises FileNotFoundError: If the file is not found.
        :raises TypeError: If it is not a file.
        """

        if not await a_os.path.exists(file_path):
            raise FileNotFoundError(f"File {file_path} not found")
        if not await a_os.path.isfile(file_path):
            raise TypeError(f"{file_path} is not file!")

        path, file = os.path.split(file_path)
        name, ext = os.path.splitext(file)
        size = await a_os.path.getsize(file_path)

        result = {
            'full_path': os.path.abspath(file_path),
            'path_folder': path,
            'file': file,
            'name': name,
            'ext': ext,
            'size': size
        }
        return result

    async def __check_ext(self, ext: str) -> bool:
        """
        Checks whether work with the file .
        :param ext: File Extension.
        :return: True if the operation is enabled. False if the file is not supported.
        """
        if '.' in ext:
            ext = ext.replace('.', '', 1)
        return ext in self.allowed_extensions

    async def __validate_ext(self, ext: str) -> None:
        """
        Checks whether work with the file .
        :param ext: File Extension.
        :return: None
        :raises TypeError: If working with a file of this type is not allowed.
        """
        if not await self.__check_ext(ext):
            raise TypeError(f"File with the extension '{ext}' is not allowed")

    @classmethod
    async def __get_unique_name(cls, name: str) -> str:
        """
        Generates a unique string based on the submitted string with the addition of the current date and time
        string without delimiters.
        """
        return name + '_' + await cls.__get_datetime_now()

    @classmethod
    async def __get_datetime_now(cls) -> str:
        """Returns the current date and time as a string of numbers with no delimiters."""
        return datetime.now().strftime('%d%m%Y%H%M%S')
