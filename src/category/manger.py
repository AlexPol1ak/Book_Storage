# Manage categories in the file system and database.

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

    async def create(self, session: AsyncSession, name: str, description: str, creator: int) -> Category:
        """
        :param session: Instance AsyncSession.
        :param name: Name of the new category.
        :param description: Description of the new category.
        :param creator: d of the privileged user who created the category.
        :return: Category db object.
        :raises FileExistsError: If category exists in file system.
        :raises ValueError: If category exists in database.
        """

        frmt_name = await self.text_frmt.name_formatter(name, punctuation_del=True)
        category_system_name = await self.text_frmt.name_formatter(frmt_name, translit_text='ru-en',
                                                                   replace_space="_")

        category_path = await self.storage.add_category(category_system_name)
        category_obj = await self.category_crud.create_category(session, frmt_name, category_system_name, description,
                                                                category_path, creator)

        return category_obj
