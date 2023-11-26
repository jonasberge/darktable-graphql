import os
import io
import pathlib
import re
import subprocess
import tempfile

import sqlalchemy
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import declarative_base, Session
from sqlacodegen.generators import DeclarativeGenerator

from .db import DatabaseType


ORM_GEN_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'orm')
ORM_GEN_INIT_PATH = os.path.join(ORM_GEN_DIR, '__init__.py')


def init_dt_configdir(dt_clipath: str, directory: str):
    subprocess.run([
        dt_clipath,
        'INPUT.RW2',
        'INPUT.RW2.xmp',
        'OUTPUT.jpg',
        '--core',
        '--configdir',
        directory,
        '--library',
        os.path.join(directory, DatabaseType.LIBRARY.db_filename()),
    ], capture_output=True, text=True)
    if not os.path.exists(os.path.join(directory, DatabaseType.LIBRARY.db_filename())):
        raise RuntimeError(f'{DatabaseType.LIBRARY.db_filename()} not generated')
    if not os.path.exists(os.path.join(directory, DatabaseType.DATA.db_filename())):
        raise RuntimeError(f'{DatabaseType.DATA.db_filename()} not generated')


def get_darktable_version(dt_clipath, short=True):
    result = subprocess.run([
        dt_clipath,
        '--version'
    ], capture_output=True, text=True)
    first_line = result.stdout.split('\n', 1)[0]
    if short:
        match = re.search(r'(\d+\.\d+\.\d+)', first_line)
        if match:
            version = match.group()
    else:
        match = re.search(r'\d', first_line, 0)
        if match:
            position = match.start()
            end_match = re.compile(r'[\n\r\s]|$').search(first_line, position)
            assert(end_match is not None)
            end = end_match.start()
            version = first_line[position:end]
    if not match:
        raise RuntimeError('darktable version not found in output')
    return version


def replace_file_contents(path, regex, replace):
    with open(path, 'r+') as f:
        content = f.read()
        new = re.sub(regex, replace, content, flags=re.M)
        f.seek(0)
        f.write(new)


def get_db_version(db_path):
    Base = declarative_base()

    class DbInfo(Base):
        __tablename__ = 'db_info'
        key = sqlalchemy.Column(sqlalchemy.String, primary_key=True)
        value = sqlalchemy.Column(sqlalchemy.String)

    engine = sqlalchemy.create_engine(f'sqlite:///{db_path}')
    Base.metadata.reflect(engine)

    with Session(engine) as session:
        stmt = sqlalchemy.select(DbInfo).filter_by(key='version')
        rows = session.execute(stmt).first()
        return int(rows[0].value)


def _generate_database_orm(config_dir: str, database_type: DatabaseType):
    db_path = os.path.join(config_dir, database_type.db_filename())
    out_file = os.path.join(ORM_GEN_DIR, database_type.orm_filename())
    pathlib.Path(ORM_GEN_DIR).mkdir(parents=True, exist_ok=True)
    engine = create_engine(f'sqlite://')
    engine.execute(f"attach database 'file:{db_path}?mode=ro' as {database_type.value};")
    metadata = MetaData(bind=engine, schema=database_type.value)
    metadata.reflect()
    generator = DeclarativeGenerator(metadata, engine, [])
    out_file = io.open(out_file, 'w', encoding='utf-8')
    out_file.write(generator.generate())
    out_file.close()
    db_version = get_db_version(db_path)
    replace_file_contents(ORM_GEN_INIT_PATH, f'({database_type.name}_VERSION) = \\d+', f'\\1 = {db_version}')


def generate_orm(dt_clipath):
    with tempfile.TemporaryDirectory() as tmpdir:
        init_dt_configdir(dt_clipath, tmpdir)
        _generate_database_orm(tmpdir, DatabaseType.DATA)
        _generate_database_orm(tmpdir, DatabaseType.LIBRARY)
        short_dt_version = get_darktable_version(dt_clipath, short=True)
        full_dt_version = get_darktable_version(dt_clipath, short=False)
        replace_file_contents(ORM_GEN_INIT_PATH, f'(DARKTABLE_VERSION) = [^\r\n]+', f'\\1 = "{short_dt_version}"')
        replace_file_contents(ORM_GEN_INIT_PATH, f'(DARKTABLE_VERSION_FULL) = [^\r\n]+', f'\\1 = "{full_dt_version}"')
