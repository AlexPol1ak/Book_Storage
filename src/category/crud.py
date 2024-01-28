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
    async def get_category(session: AsyncSession, name_or_id: str | int) -> Category | None:
        """
        Get a category by name or id.
        :param session: Instance AsyncSession.
        :param name_or_id: Category name or category id.
        :return: Category or None.
        :raises TypeError: If type argument  not str or int.
        """

        if isinstance(name_or_id, int):
            category = await session.get(Category, name_or_id)
            return category
        elif isinstance(name_or_id, str):
            if name_or_id.isdigit():
                category = await session.get(Category, int(name_or_id))
            else:
                stmt = select(Category).where(Category.name == name_or_id)
                category = await session.scalar(stmt)
            return category
        else:
            raise TypeError

    @staticmethod
    async def update_category(session: AsyncSession, name_or_id: str | int, *, new_description: str | None = None,
                              new_name: str | None = None) -> Category | None:
        """
        Updates a category by name or id . Updates the category name or description.
        :param session: Instance AsyncSession.
        :param name_or_id: Category name or id.
        :param new_description: New description.
        :param new_name: New name.
        :return: Category instance.
        :raises TypeError: If new_name type argument not str or int.
        :raises NotADirectoryError: If the category does not exist.
        :raises ValueError: If a category with that new_name already exists.
        """
        category = await CategoryCRUD.get_category(session, name_or_id)
        if not category:
            raise NotADirectoryError

        if new_description or new_name:
            if new_name:
                if await CategoryCRUD.check_category(session, new_name):
                    raise ValueError(f"Category {new_name} exist")
                else:
                    category.name = new_name

            if new_description:
                category.description = new_description

            session.add(category)
            await session.commit()

        return category

    @staticmethod
    async def delete_category(session: AsyncSession, name_or_id_or_obj: str | int | Category) -> None:
        """
        Removes a category by name or id or database object.
        :param session: AsyncSession instance.
        :param name_or_id_or_obj:  Category name or id or object Category
        :return: None.
        :raises TypeError: If the argument is not a string, integer or Category object
        :raises NotADirectoryError: If Category not found.
        """

        if isinstance(name_or_id_or_obj, (int, str)):
            category_obj = await CategoryCRUD.get_category(session, name_or_id_or_obj)
        elif isinstance(name_or_id_or_obj, Category):
            category_obj = name_or_id_or_obj
        else:
            raise TypeError("The argument must be a string, an integer, or a Category object.")

        if not category_obj:
            raise NotADirectoryError("Category not found.")

        await session.delete(category_obj)
        await session.commit()

    @staticmethod
    async def all_category(session: AsyncSession):
        """
        Returns a sequence of all categories.
        :param session: AsyncSession instance.
        :return: All categories
        """
        stmt = select(Category)
        categories = await session.scalars(stmt)
        return categories.all()

