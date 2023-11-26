from sqlalchemy import Column, Float, ForeignKey, Index, Integer, LargeBinary, String, Table
from sqlalchemy.orm import declarative_base

Base = declarative_base()
metadata = Base.metadata


class DbInfo(Base):
    __tablename__ = 'db_info'
    __table_args__ = {'schema': 'data'}

    key = Column(String, primary_key=True)
    value = Column(String)


t_presets = Table(
    'presets', metadata,
    Column('name', String),
    Column('description', String),
    Column('operation', String),
    Column('op_version', Integer),
    Column('op_params', LargeBinary),
    Column('enabled', Integer),
    Column('blendop_params', LargeBinary),
    Column('blendop_version', Integer),
    Column('multi_priority', Integer),
    Column('multi_name', String(256)),
    Column('multi_name_hand_edited', Integer),
    Column('model', String),
    Column('maker', String),
    Column('lens', String),
    Column('iso_min', Float),
    Column('iso_max', Float),
    Column('exposure_min', Float),
    Column('exposure_max', Float),
    Column('aperture_min', Float),
    Column('aperture_max', Float),
    Column('focal_length_min', Float),
    Column('focal_length_max', Float),
    Column('writeprotect', Integer),
    Column('autoapply', Integer),
    Column('filter', Integer),
    Column('def', Integer),
    Column('format', Integer),
    Index('presets_idx', 'name', 'operation', 'op_version', unique=True),
    schema='data'
)


t_style_items = Table(
    'style_items', metadata,
    Column('styleid', Integer),
    Column('num', Integer),
    Column('module', Integer),
    Column('operation', String(256)),
    Column('op_params', LargeBinary),
    Column('enabled', Integer),
    Column('blendop_params', LargeBinary),
    Column('blendop_version', Integer),
    Column('multi_priority', Integer),
    Column('multi_name', String(256)),
    Column('multi_name_hand_edited', Integer),
    Index('style_items_styleid_index', 'styleid'),
    schema='data'
)


class Styles(Base):
    __tablename__ = 'styles'
    __table_args__ = (
        Index('styles_name_index', 'name'),
        {'schema': 'data'}
    )

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    iop_list = Column(String)


class Tags(Base):
    __tablename__ = 'tags'
    __table_args__ = (
        Index('tags_name_idx', 'name', unique=True),
        {'schema': 'data'}
    )

    id = Column(Integer, primary_key=True)
    name = Column(String)
    synonyms = Column(String)
    flags = Column(Integer)


class Locations(Tags):
    __tablename__ = 'locations'
    __table_args__ = {'schema': 'data'}

    tagid = Column(ForeignKey('data.tags.id'), primary_key=True)
    type = Column(Integer)
    longitude = Column(Float)
    latitude = Column(Float)
    delta1 = Column(Float)
    delta2 = Column(Float)
    ratio = Column(Float)
    polygons = Column(LargeBinary)
