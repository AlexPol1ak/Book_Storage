from NEW_FileStorage.storage.storage_categories import StorageCategories


# Добавляет к хранилищу функционал проверки расширений файлов разрешенных для хранения.
class StorageAllowedExtensions(StorageCategories):

    def __init__(self, storage_path: str, storage_name: str, allowed_extensions: list, temporary: bool = False, ):
        super().__init__(storage_path, storage_name, temporary)

        if len(allowed_extensions) == 0:
            raise ValueError("Empty list 'allowed_extensions'.")
        for ext in allowed_extensions:
            if not isinstance(ext, str):
                raise TypeError(f"{ext} - invalid file extension type. Extensions should be a string.")

        self.__allowed_extensions = set(allowed_extensions)

    @property
    def allowed_extensions(self):
        return tuple(self.__allowed_extensions)

    @allowed_extensions.setter
    def allowed_extensions(self, value):
        raise ValueError("The tuple of allowed extensions cannot be modified by assigning . "
                         "Use the methods 'add_allowed_ext' and 'del_allowed_ext'.")

    async def add_allowed_ext(self, ext: str) -> None:
        ext = await self.__reformat_ext(ext)
        self.__allowed_extensions.add(ext)

    async def del_allowed_ext(self, ext: str) -> None:
        ext = await self.__reformat_ext(ext)
        self.__allowed_extensions.discard(ext)

    async def check_ext(self, ext: str) -> bool:
        """
        Checks whether work with the file .
        :param ext: File Extension.
        :return: True if the operation is enabled. False if the file is not supported.
        """
        ext = await self.__reformat_ext(ext)
        return ext in self.allowed_extensions

    async def validate_ext(self, ext: str) -> None:
        """
        Checks whether work with the file .
        :param ext: File Extension.
        :return: None
        :raises TypeError: If working with a file of this type is not allowed.
        """
        if not await self.check_ext(ext):
            raise TypeError(f"File with the extension '{ext}' is not allowed")

    @classmethod
    async def __reformat_ext(cls, ext: str) -> str:
        if not isinstance(ext, str):
            raise TypeError("The 'ext' argument must be a string type.")
        if ext.startswith('.'):
            ext = ext.replace('.', '', 1)
        return ext
