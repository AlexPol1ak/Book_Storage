import asyncio
import os
from typing import Literal

import aiofiles.os as a_os
import aioshutil as a_shutil
from asyncstdlib import any_iter

from NEW_FileStorage.storage.storage_base import BaseStorage


# Расширяет базовое хранилище. Добавляет функционал создания, удаления, получения категорий
# Получения размера категории и количества файлов в ней, получения всех файлов в категории
class StorageCategories(BaseStorage):

    @property
    async def categories(self):
        return tuple(sorted(os.listdir(self.path)))

    @categories.setter
    def categories(self, value):
        raise ValueError("Attribution is not allowed")

    async def all_categories(self) -> dict[str, str]:
        """
        Returns all available categories.
        :return: All categories.
        """
        categories = await a_os.listdir(self.path)
        if len(categories) == 0:
            return dict()
        categories = any_iter(categories)
        categories_dict = {}

        async for cat_name in categories:
            categories_dict[cat_name] = os.path.join(self.path, cat_name)
        return categories_dict

    async def check_category(self, category: str) -> bool:
        """Checks if the category exists."""
        cats = await self.all_categories()
        return category in cats

    async def get_category_path(self, category: str) -> str:
        """
        Returns the absolute path to the category.
        :param category: Category name
        :return: Category absolute path.
        :raise NotADirectoryError: If category not found.
        :raises TypeError: If argument type not string.
        """
        if not isinstance(category, str):
            raise TypeError("A string was expected as an argument.")

        cats: dict = await self.all_categories()
        if category not in cats:
            raise NotADirectoryError(f"Category {category} is not found.")
        return cats[category]

    async def create_category(self, name: str) -> dict[str, str]:
        """
        Creates a directory on the file system if it does not exist.
        :return: None
        :raises IsADirectoryError: If the specified category already exists in the repository.
        :raises TypeError: If the argument is not a valid storage instance.
        """

        if await self.check_category(name):
            raise IsADirectoryError(f"The category {name} already exists")
        if not isinstance(name, str):
            raise TypeError('Incorrect argument type.Expected str')

        cat_path = os.path.join(self.path, name)
        await a_os.mkdir(cat_path)
        return {name: cat_path}

    async def files_transfer(self, old_category: str, new_category: str) -> dict:
        """
        Moves all files from the old category to the new category.
        :param old_category: The name of the category from which you want to move all files.
        :param new_category: The category name to which you want to move files.
        :return: Name and absolute path to the category to which the files were moved.
        :raises NotADirectoryError: If categories not found.
        :raises IsADirectoryError: If old_category is empty.
        :raises TypeError: If the arguments are not strings.

        """
        if not isinstance(old_category, str) or not isinstance(new_category, str):
            raise TypeError('Incorrect arguments type. Expected str.')

        old_category_path = await self.get_category_path(old_category)
        new_category_path = await self.get_category_path(new_category)

        files_list_old_category = await a_os.listdir(old_category_path)  # содержит только имена файлов
        if len(files_list_old_category) == 0:
            raise IsADirectoryError(f"Category {old_category} is empty")
        files_list_old_category = any_iter(files_list_old_category)  # Асинхронный итератор.

        async with asyncio.TaskGroup() as tg:
            async for file in files_list_old_category:
                src_file = os.path.join(old_category_path, file)
                dst_file = os.path.join(new_category_path, file)
                await tg.create_task(a_os.replace(src_file, dst_file))

        return {new_category: new_category_path}

    async def delete_category(self, category: str,
                              mode: Literal['empty', 'all', 'moveFiles'] = 'empty',
                              new_category: str = None) -> None:
        """
        Removes a category by name.
        :param category: Name of the category to be deleted.
        :param mode: Deletion Mode.
                     Mode 'empty'- delete only empty, if not empty throw IsADirectoryError or NotADirectoryError
                     if the directory does not exist.
                     Mode 'all' - Delete in any case.
                     Mode 'moveFiles'- move all files to a new category and delete the old category.
        :param new_category: Name new category to which files from the deleted category should be moved.
                             The parameter is considered only in mode='moveFiles'.
        :return: None
        :raises NotADirectoryError: If category does not exist.
        :raises ValueError: Incorrect literal mode.
        :raises IsADirectoryError: If category is not empty and mode is 'empty'.
        :raises TypeError: Incorrect type of category names. A string is waiting.
        """

        deleted_category_path: str = await self.get_category_path(category)

        match mode:
            case str('empty'):
                try:
                    await a_os.rmdir(deleted_category_path)
                except FileNotFoundError:
                    raise NotADirectoryError(f"Category {category} is not exist.")
                except OSError:
                    raise IsADirectoryError(f"Category {category} is not empty.")

            case str('all'):
                await a_shutil.rmtree(deleted_category_path)

            case str('moveFiles'):
                if new_category is None:
                    raise ValueError("For 'moveFiles' mode, a new category must be specified ")
                if not isinstance(new_category, str):
                    raise TypeError("Expected argument type 'new_category' - str.")

                await self.files_transfer(category, new_category)
                await self.delete_category(category, mode='all')
            case _:
                raise ValueError(f"Incorrect {mode}")

    async def count_files(self, category: str) -> int:
        """Returns the number of files in the category. If the category is not created it will return -1"""

        category_path = await self.get_category_path(category)
        files = await a_os.listdir(category_path)
        return len(files)

    async def get_all_files(self, category: str) -> dict[str: str | int] | None:
        """
        Returns all files in the specified category.
        :param category: Category name.
        :return: All files format tuple(dict(), ...) or None
        :raises NotADirectoryError: If category not found.
        :raises TypeError: If argument type not string.
        """
        category_path = await self.get_category_path(category)

        all_names_files = await a_os.listdir(category_path)
        if len(all_names_files) == 0:
            return None
        all_names_files = any_iter(all_names_files)

        all_files = []
        async for name in all_names_files:
            file_path = os.path.join(category_path, name)
            if await a_os.path.isfile(file_path):
                size = await a_os.path.getsize(file_path)
                file_info = {
                    'name': name,
                    'type': os.path.splitext(file_path)[1],
                    'category': category,
                    'path': file_path,
                    'size': size
                }
                all_files.append(file_info)

        return tuple(all_files)

    async def size(self, category: str) -> int:
        """
        Returns the total size of the category in bytes.
        The category size is the total size of all files in the category.
        :return: If the category is not created it will return -1
        """
        files = await self.get_all_files(category)

        if not files:
            return 0
        size = 0
        files = any_iter(files)
        async for file_dict in files:
            size += file_dict.get('size')
        return size
