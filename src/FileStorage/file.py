from FileStorage.storage import Storage
from FileStorage.сategory import CategoryManager


class FileManager(CategoryManager):
    """File and category management manager."""
    def __init__(self, storage: Storage):
        super().__init__(storage)