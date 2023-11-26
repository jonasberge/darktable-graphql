import os

from flask import Flask
from flask import request, jsonify
from flask_cors import CORS
from ariadne import load_schema_from_path, make_executable_schema, \
    graphql_sync, snake_case_fallback_resolvers, ObjectType
from ariadne.explorer import ExplorerGraphiQL

from .queries import types
from .db import create_session


GRAPHQL_SCHEMA_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'schema', 'api.graphql')

app = Flask(__name__)
CORS(app)

type_defs = load_schema_from_path(GRAPHQL_SCHEMA_PATH)
schema = make_executable_schema(
    type_defs, *types, snake_case_fallback_resolvers
)

# Retrieve HTML for the GraphiQL.
# If explorer implements logic dependant on current request,
# change the html(None) call to the html(request)
# and move this line to the graphql_explorer function.
explorer_html = ExplorerGraphiQL().html(None)


@app.route('/', methods=['GET'])
def graphql_playground():
    return explorer_html, 200


@app.route('/', methods=['POST'])
def graphql_server():
    data = request.get_json()
    with create_session() as session:
        success, result = graphql_sync(
            schema,
            data,
            context_value={
                'request': request,
                'session': session
            },
            debug=app.debug
        )
    status_code = 200 if success else 400
    return jsonify(result), status_code
