from werkzeug.datastructures import FileStorage
from typing import Union
import os


class PicturesDB:
    def __init__(self):
        self.root_path = os.path.split(os.path.abspath(__name__))[0]

        self.database_path = os.path.join(self.root_path, 'pictures')
        if not os.path.exists(self.database_path):
            os.mkdir(self.database_path)
            print('Pictures Database created!')

        self.tables = ['profile-image']
        for table in self.tables:
            table_path = os.path.join(self.database_path, table)
            if not os.path.exists(table_path):
                os.mkdir(table_path)
                print('Table', table, 'created!')

    def add_picture(self, table: str, picture: FileStorage) -> None:
        if table not in self.tables:
            print('Table', table, 'not in Tables list!')
            return

        picture.save(os.path.join(self.database_path, table))
