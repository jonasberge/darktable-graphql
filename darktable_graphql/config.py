import json
import os
import pathlib
import sys

import jsonschema


CONFIG_SCHEMA_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'schema', 'config.json')
CONFIG_SCHEMA = json.loads(pathlib.Path(CONFIG_SCHEMA_PATH).read_text())


def read_config(filepath):
    cwd = os.getcwd() or os.path.dirname(os.path.abspath(sys.argv[0]))
    config_path = os.path.abspath(os.path.join(cwd, filepath))
    config = json.loads(pathlib.Path(config_path).read_text())
    try:
        jsonschema.validate(instance=config, schema=CONFIG_SCHEMA)
    except jsonschema.ValidationError as error:
        print("configuration error:", str(error), file=sys.stderr)
        sys.exit(-1)
    return config
