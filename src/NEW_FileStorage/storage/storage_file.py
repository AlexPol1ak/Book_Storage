from datetime import datetime

from NEW_FileStorage.storage.storage_ext import StorageAllowedExtensions


class StorageFiles(StorageAllowedExtensions):
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