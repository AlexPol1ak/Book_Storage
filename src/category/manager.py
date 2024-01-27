# Manage categories in the file system and database.

from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from FileStorage import StorageManager
from category.crud import CategoryCRUD
from category.models import Category
from utils.text_formatter import TextFormatter


class BaseCategoryManager:
    """The base class of the category manager."""

    def __init__(self, storage: StorageManager):
        """Initialization of storage object, text formatting object, CRUD operations object."""
        if not isinstance(storage, StorageManager):
            raise TypeError

        self.storage = storage
        self.text_frmt = TextFormatter()
        self.category_crud = CategoryCRUD()

    def __repr__(self):
        return (f"Object of management category."
                f"Storage name: {self.storage.storage.name}. Storage location: {self.storage.storage.path}")


class CategoryManager(BaseCategoryManager):
    """
    Manages categories at the database and file system level.
    Combines category management in the file system and in the database.
    """

    async def create(self, session: AsyncSession, name: str, description: str, creator: int) -> dict[str, Any]:
        """
        :param session: Instance AsyncSession.
        :param name: Name of the new category.
        :param description: Description of the new category.
        :param creator: d of the privileged user who created the category.
        :return: A dictionary with category data. {'id':int, 'description': int, 'data_joined': datetime, 'creator':int}
        :raises FileExistsError: If category exists in file system.
        :raises ValueError: If category exists in database.
        """

        frmt_name = await self.text_frmt.name_formatter(name, punctuation_del=True)
        category_system_name = await self.text_frmt.name_formatter(frmt_name, translit_text='ru-en',
                                                                   replace_space="_")

        category_path = await self.storage.add_category(category_system_name)
        category_obj = await self.category_crud.create_category(session, frmt_name, category_system_name, description,
                                                                category_path, creator)

        return await self.__to_dict(category_obj)

    async def update(self, session: AsyncSession, category_name_or_id: str | int, *,
                     new_name: str = None, new_description: str = None) -> dict[str, Any]:
        """
        Updates a category by name or id . Updates the category name or description.
        :param session: Instance AsyncSession.
        :param  category_name_or_id: Category name or id.
        :param new_description: New description. Default None.
        :param new_name: New name. Default None.
        :return: A dictionary with category data. {'id':int, 'description': int, 'data_joined': datetime,
                'creator':int, path: str}.
        :raises TypeError: If new_name type argument not str or int.
        :raises NotADirectoryError: If the category does not exist.
        :raises ValueError: If a category with that new_name already exists.
                """
        category_obj = await self.category_crud.update_category(session, category_name_or_id,
                                                                new_name=new_name, new_description=new_description)
        return await self.__to_dict(category_obj)

    async def delete(self, session: AsyncSession, category_name_or_id: str | int):
        """
        Deletes a category from storage and from the database. If the category does not contain any files.
        :param session: AsyncSession instance.
        :param category_name_or_id: Category name or id.
        :return: None.
        :raises TypeError: Incorrect type argument category_name_or_id.
        :raises NotADirectoryError: If category is not exist or not found.
        :raises IsADirectoryError: If category is not empty.
        """

        category_obj = await CategoryCRUD.get_category(session, category_name_or_id)
        if not category_obj:
            raise NotADirectoryError

        await self.storage.delete_category(category_obj.system_name, mode='empty')
        await CategoryCRUD.delete_category(session, category_obj)

    async def __to_dict(self, category_obj: Category) -> dict[str, Any]:
        """Converts a database object into a dictionary."""
        result = {'id': category_obj.id,
                  'name': category_obj.name,
                  'description': category_obj.description,
                  'date_joined': category_obj.data_joined,
                  'creator': category_obj.creator,
                  'path': category_obj.path,
                  }
        return result
