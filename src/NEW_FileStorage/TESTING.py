import asyncio
import os

from NEW_FileStorage.storage.storage import Storage

if __name__ == '__main__':
    async def main():
        dir = os.path.dirname(os.path.abspath(__file__))
        st = Storage(dir, 'STRORAGE_draft')

        print(await st.get_all_files('cat2'))
        print(await st.size('cat2'))




    asyncio.run(main())