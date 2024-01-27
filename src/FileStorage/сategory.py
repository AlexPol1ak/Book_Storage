import asyncio
import os
from typing import Literal
import aiofiles.os as a_os
import aioshutil as a_shutil
from asyncstdlib import any_iter

from FileStorage.storage import Storage


class CategoryManager:
    """A manager class for managing categories."""
    def __init__(self, storage: Storage):
        """
        :param storage: An instance of the Storage class.
        :raises TypeError: Incorrect instance
        """
        if isinstance(storage, Storage):
            self.storage = storage
        else:
            raise TypeError(f"{storage} invalid type.")

    @property
    async def categories(self):
        return tuple(sorted(os.listdir(self.storage.path)))

    @categories.setter
    def categories(self, value):
        raise ValueError("Attribution is not allowed")

    async def all_categories(self) -> dict[str, str]:
        """
        Returns all available categories.
        :return: All categories.
        """
        categories = await a_os.listdir(self.storage.path)
        if len(categories) == 0:
            return dict()
        categories = any_iter(categories)
        categories_dict = {}

        async for cat in categories:
            categories_dict[cat] = os.path.join(self.storage.path, cat)
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
        """
        cats = await self.all_categories()
        if category not in cats:
            raise NotADirectoryError(f"Category {category} is not found.")
        return cats[category]

    async def add_category(self, name: str) -> str:
        """
        Add new category
        :param name: Name category.
        :return: Category absolute path.
        :raises FileExistsError: If category exists.
        """
        if await self.check_category(name):
            raise FileExistsError(f"The category {name} already exists")

        cat_path = os.path.join(self.storage.path, name)
        await a_os.mkdir(cat_path)
        return cat_path

    async def delete_category(self, name: str,
                              mode: Literal['empty', 'all', 'moveFiles'] = 'empty',
                              new_category: str | None = None):
        """
        Removes a category by name.
        :param name: Category name.
        :param mode: Deletion Mode.
                     Mode 'empty'- delete only empty, if not empty throw IsADirectoryError or NotADirectoryError
                     if the directory does not exist.
                     Mode 'all' - Delete in any case.
                     Mode 'moveFiles'- move all files to a new category and delete the old category.
        :param new_category: New category to which files from the deleted category should be moved.
                             The parameter is considered only in mode='moveFiles'.
        :return: None
        :raises NotADirectoryError: If category does not exist.
        :raises ValueError: Incorrect literal mode.
        :raises IsADirectoryError: If category is not empty and mode is 'empty'.
        """

        cats = await self.all_categories()
        if name not in cats:
            raise NotADirectoryError(f"The category {name} does not exist.")

        match mode:
            case str('empty'):
                try:
                    await a_os.rmdir(cats[name])
                except FileNotFoundError:
                    raise NotADirectoryError(f"Category {name} is not exist.")
                except OSError:
                    raise IsADirectoryError(f"Category {name} is not empty.")

            case str('all'):
                await a_shutil.rmtree(cats[name])
            case str('moveFiles'):
                if new_category is None or new_category not in cats:
                    raise NotADirectoryError(f"The category {new_category} does not exist.")
                await self.move_all_files(name, new_category)
                await self.delete_category(name, mode='all')
            case _:
                raise ValueError(f"Incorrect {mode}")

    async def move_all_files(self, old_category: str, new_category: str) -> str:
        """
        Moves all files from the old category to the new category.
        :param old_category: A category with files to move.
        :param new_category: The category to which you want to move files.
        :return: Absolute path to the category to which the files were moved.
        :raises NotADirectoryError: If category does not exist.
        :raises IsADirectoryError: If old_category is empty.
        """

        cats = await self.all_categories()
        if old_category not in cats:
            raise NotADirectoryError(f"Category {old_category} is not empty.")
        if new_category not in cats:
            raise NotADirectoryError(f"Category {new_category} is not empty.")

        files_list = await a_os.listdir(cats[old_category])
        if len(files_list) == 0:
            raise IsADirectoryError(f"Category {old_category} is empty")
        files_list = any_iter(files_list)

        async with asyncio.TaskGroup() as tg:

            async for file in files_list:
                src_file = os.path.join(cats[old_category], file)
                dst_file = os.path.join(cats[new_category], file)
                await tg.create_task(a_os.replace(src_file, dst_file))

        return cats[new_category]

    async def count_files(self, category: str) -> int:
        """Returns the number of files in the category. """
        cat_path = await self.get_category_path(category)
        files = await a_os.listdir(cat_path)
        return len(files)
