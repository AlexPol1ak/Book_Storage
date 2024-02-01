import asyncio
import os

from FileStorage.file import FileManager
from FileStorage.storage import Storage


class StorageManager(FileManager):
    def __init__(self, storage_path: str, storage_name: str, allowed_extensions: list, temporary: bool = False):
        super().__init__(Storage(storage_path, storage_name, temporary),
                         allowed_extensions
                         )

    async def delete_storage(self, all_files: bool = False) -> None:
        self.storage.delete_storage(all_files)

    def __repr__(self):
        return self.storage.__repr__()


if __name__ == '__main__':
    async def main():
        from pprint import pprint

        exts = ['txt', 'pdf']

        file1 = r'Storage\Cat0\testfile.txt'
        cat1 = 'Cat4'

        dr = os.path.dirname(os.path.abspath(__file__))
        st = StorageManager(dr, "Storage", exts)

        r = await st.add_file(file1, cat1, only_copy=True)
        pprint(r)



    asyncio.run(main())

