import asyncio
import os

from FileStorage.file import FileManager
from FileStorage.storage import Storage


class StorageManager(FileManager):
    def __init__(self, storage_path: str, storage_name: str, temporary: bool = False):
        super().__init__(Storage(storage_path, storage_name, temporary))

    async def delete_storage(self, all_files: bool = False) -> None:
        self.storage.delete_storage(all_files)

    def __repr__(self):
        return self.storage.__repr__()


if __name__ == '__main__':
    async def main():
        dr = os.path.dirname(os.path.abspath(__file__))
        st = StorageManager(dr, "Storage")
        # await st.delete_category('Cat2', mode='moveFiles', new_category= 'Cat3')
        # await st.move_all_files('Cat3', 'Cat2')
        # await st.move_all_files('Cat2', 'Cat3')
        await st.delete_category('Cat2')


    asyncio.run(main())

