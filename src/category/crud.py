from typing import Literal, Type, Any, Coroutine

from sqlalchemy import update, select
from sqlalchemy.ext.asyncio import AsyncSession

from category.models import Category
from user.crud import get_user


class CategoryCRUD:
    def __init__(self):
        pass

    @staticmethod
    async def check_category(session: AsyncSession, category_name: str) -> bool:
        """
        Checks to see if the category exists.
        :param session: Instance AsyncSession.
        :param category_name: Category name/
        :return: True if the category exists, otherwise False.
        """

        category: Category | None
        stmt = select(Category).where(Category.name == category_name)
        category = await session.scalar(stmt)
        if category:
            return True
        else:
            return False

    @staticmethod
    async def create_category(session: AsyncSession, category_name: str, category_system_name: str,
                              category_description: str, category_path: str, category_creator: int) -> Category:
        """
        Creates a new category record in the table.
        :param category_system_name: Category name in Latin characters, without spaces and punctuation marks.
        :param session: Instance AsyncSession.
        :param category_name: Name of the new category.
        :param category_description: Description of the new category
        :param category_path: The path in the file system to the new category.
        :param category_creator: id of the privileged user who created the category.
        :return: Category db object.
        :raises ValueError: If a category with this name exists.
        """

        cat_flag: bool = await CategoryCRUD.check_category(session, category_name)

        if not cat_flag:
            new_category: Category = Category(name=category_name, system_name=category_system_name,
                                              description=category_description, path=category_path)
            user = await get_user(session, category_creator)

            new_category.user = user

            session.add_all([new_category, user])
            await session.commit()
            return new_category
        else:
            raise ValueError(f'Category {category_name} already exists')

    @staticmethod
    async def get_category():
        pass

    @staticmethod
    async def update_category():
        pass

    @staticmethod
    async def del_category():
        pass

    @staticmethod
    async def all_category():
        pass
