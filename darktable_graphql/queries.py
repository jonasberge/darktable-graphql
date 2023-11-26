from ariadne import ObjectType, load_schema_from_path, make_executable_schema, snake_case_fallback_resolvers, convert_kwargs_to_snake_case
from graphql import GraphQLResolveInfo
from sqlalchemy import func
from sqlalchemy.orm import Session, Query
from sqlalchemy.engine.row import Row

from .orm import data, library


def row_to_dict(row):
    if type(row) == Row:
        return row._mapping
    return dict((col, getattr(row, col)) for col in row.__table__.columns.keys())

def rows_to_dict(rows):
    return [ row_to_dict(row) for row in rows ]


query = ObjectType("Query")
image = ObjectType("Image")
tag = ObjectType("Tag")
film_roll = ObjectType("FilmRoll")

types = [query, image, tag, film_roll]


@query.field("listImages")
@convert_kwargs_to_snake_case
def listImages_resolver(obj: dict, info: GraphQLResolveInfo, limit: int = None):
    sess: Session = info.context['session']
    query: Query = sess.query(library.Images)
    if limit is not None:
        query = query.limit(limit)
    return rows_to_dict(query.all())


@image.field("tags")
def image_tags_resolver(obj: dict, info: GraphQLResolveInfo):
    sess: Session = info.context['session']


    rows = sess.query(
        library.TaggedImages.tagid.label('id'),
        library.TaggedImages.position.label('position'),
    ).join(
        data.Tags,
        library.TaggedImages.tagid == data.Tags.id
    ).filter(
        library.TaggedImages.imgid == obj['id']
    ).all()

    """
    sess.query(
        library.TaggedImages.imgid,
        library.TaggedImages.tagid,
        data.Tags.name.label('tag_name')
    ).join(data.Tags, library.TaggedImages.tagid == data.Tags.id)
    """


    d = rows_to_dict(rows)
    d = [
        {
            'tag': {
                'id': t.id
            },
            'position': t.position
        }
        for t in d
    ]

    return d
    return [
        {
            "id": 1,
            "position": 0
        }
    ]
