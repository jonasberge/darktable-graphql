from sqlalchemy import CHAR, Column, Float, ForeignKey, Index, Integer, LargeBinary, String, Table, text
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql.sqltypes import NullType

Base = declarative_base()
metadata = Base.metadata


t_color_labels = Table(
    'color_labels', metadata,
    Column('imgid', Integer),
    Column('color', Integer),
    Index('color_labels_idx', 'imgid', 'color', unique=True),
    schema='library'
)


class DbInfo(Base):
    __tablename__ = 'db_info'
    __table_args__ = {'schema': 'library'}

    key = Column(String, primary_key=True)
    value = Column(String)


class FilmRolls(Base):
    __tablename__ = 'film_rolls'
    __table_args__ = (
        Index('film_rolls_folder_index', 'folder'),
        {'schema': 'library'}
    )

    folder = Column(String(1024), nullable=False)
    id = Column(Integer, primary_key=True)
    access_timestamp = Column(Integer)

    images = relationship('Images', back_populates='film')


t_legacy_presets = Table(
    'legacy_presets', metadata,
    Column('name', String),
    Column('description', String),
    Column('operation', String),
    Column('op_version', Integer),
    Column('op_params', LargeBinary),
    Column('enabled', Integer),
    Column('blendop_params', LargeBinary),
    Column('blendop_version', Integer),
    Column('multi_priority', Integer),
    Column('multi_name', String),
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
    schema='library'
)


t_meta_data = Table(
    'meta_data', metadata,
    Column('id', Integer),
    Column('key', Integer),
    Column('value', String),
    Index('metadata_index', 'id', 'key', 'value', unique=True),
    Index('metadata_index_key', 'key'),
    Index('metadata_index_value', 'value'),
    schema='library'
)


class ModuleOrder(Base):
    __tablename__ = 'module_order'
    __table_args__ = {'schema': 'library'}

    imgid = Column(Integer, primary_key=True)
    version = Column(Integer)
    iop_list = Column(String)


class SelectedImages(Base):
    __tablename__ = 'selected_images'
    __table_args__ = {'schema': 'library'}

    imgid = Column(Integer, primary_key=True)


t_sqlite_sequence = Table(
    'sqlite_sequence', metadata,
    Column('name', NullType),
    Column('seq', NullType),
    schema='library'
)


class Images(Base):
    __tablename__ = 'images'
    __table_args__ = (
        Index('image_position_index', 'position'),
        Index('images_datetime_taken_nc', 'datetime_taken'),
        Index('images_filename_index', 'filename', 'version'),
        Index('images_film_id_index', 'film_id', 'filename'),
        Index('images_group_id_index', 'group_id', 'id'),
        Index('images_latlong_index', 'latitude', 'longitude'),
        {'schema': 'library'}
    )

    id = Column(Integer, primary_key=True)
    group_id = Column(ForeignKey('library.images.id', ondelete='RESTRICT', onupdate='CASCADE'))
    film_id = Column(ForeignKey('library.film_rolls.id', ondelete='CASCADE', onupdate='CASCADE'))
    width = Column(Integer)
    height = Column(Integer)
    filename = Column(String)
    maker = Column(String)
    model = Column(String)
    lens = Column(String)
    exposure = Column(Float)
    aperture = Column(Float)
    iso = Column(Float)
    focal_length = Column(Float)
    focus_distance = Column(Float)
    datetime_taken = Column(Integer)
    flags = Column(Integer)
    output_width = Column(Integer)
    output_height = Column(Integer)
    crop = Column(Float)
    raw_parameters = Column(Integer)
    raw_denoise_threshold = Column(Float)
    raw_auto_bright_threshold = Column(Float)
    raw_black = Column(Integer)
    raw_maximum = Column(Integer)
    license = Column(String)
    sha1sum = Column(CHAR(40))
    orientation = Column(Integer)
    histogram = Column(LargeBinary)
    lightmap = Column(LargeBinary)
    longitude = Column(Float)
    latitude = Column(Float)
    altitude = Column(Float)
    color_matrix = Column(LargeBinary)
    colorspace = Column(Integer)
    version = Column(Integer)
    max_version = Column(Integer)
    write_timestamp = Column(Integer)
    history_end = Column(Integer)
    position = Column(Integer)
    aspect_ratio = Column(Float)
    exposure_bias = Column(Float)
    import_timestamp = Column(Integer, server_default=text('-1'))
    change_timestamp = Column(Integer, server_default=text('-1'))
    export_timestamp = Column(Integer, server_default=text('-1'))
    print_timestamp = Column(Integer, server_default=text('-1'))

    film = relationship('FilmRolls', back_populates='images')
    group = relationship('Images', remote_side=[id], back_populates='group_reverse')
    group_reverse = relationship('Images', remote_side=[group_id], back_populates='group')
    tagged_images = relationship('TaggedImages', back_populates='images')


t_history = Table(
    'history', metadata,
    Column('imgid', ForeignKey('library.images.id', ondelete='CASCADE', onupdate='CASCADE')),
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
    Index('history_imgid_num_index', 'imgid', 'num'),
    Index('history_imgid_op_index', 'imgid', 'operation'),
    schema='library'
)


class HistoryHash(Images):
    __tablename__ = 'history_hash'
    __table_args__ = {'schema': 'library'}

    imgid = Column(ForeignKey('library.images.id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True)
    basic_hash = Column(LargeBinary)
    auto_hash = Column(LargeBinary)
    current_hash = Column(LargeBinary)
    mipmap_hash = Column(LargeBinary)


t_masks_history = Table(
    'masks_history', metadata,
    Column('imgid', ForeignKey('library.images.id', ondelete='CASCADE', onupdate='CASCADE')),
    Column('num', Integer),
    Column('formid', Integer),
    Column('form', Integer),
    Column('name', String(256)),
    Column('version', Integer),
    Column('points', LargeBinary),
    Column('points_count', Integer),
    Column('source', LargeBinary),
    Index('masks_history_imgid_index', 'imgid', 'num'),
    schema='library'
)


class TaggedImages(Base):
    __tablename__ = 'tagged_images'
    __table_args__ = (
        Index('tagged_images_position_index', 'position'),
        Index('tagged_images_tagid_index', 'tagid'),
        {'schema': 'library'}
    )

    imgid = Column(ForeignKey('library.images.id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True)
    tagid = Column(Integer, primary_key=True)
    position = Column(Integer)

    images = relationship('Images', back_populates='tagged_images')
