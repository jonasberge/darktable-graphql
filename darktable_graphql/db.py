import re
from enum import Enum

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from .orm import data, library


class DatabaseType(Enum):
    DATA = 'data'
    LIBRARY = 'library'

    def db_filename(self):
        return self.value + '.db'

    def orm_filename(self):
        return re.sub(r'\W+', '_', self.value) + '.py'


def create_session():
    engine = create_engine('sqlite://')
    engine.execute("attach database 'file:/media/photography/Darktable/config-ubuntu/library.db?mode=ro' as library;")
    engine.execute("attach database 'file:/media/photography/Darktable/config-ubuntu/data.db?mode=ro' as data;")
    data.metadata.reflect(engine)
    library.metadata.reflect(engine)
    session = Session(bind=engine)
    return session
