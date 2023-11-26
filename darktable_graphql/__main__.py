# from sqlalchemy import create_engine, MetaData, Table,Column,Integer,select, String, select
# from sqlalchemy.orm import mapper, sessionmaker, join
# from sqlite3 import dbapi2 as sqlite
# from sqlalchemy.engine.reflection import Inspector

# from src.dtgraphql.api import app
# from src.dtgraphql.db import data, library

import os
import sys
from argparse import ArgumentParser
from enum import Enum

from .api import app
from .config import read_config
from .generate import generate_orm


class CommandType(Enum):
    RUN = 1
    GENERATE_ORM = 2


def init_argparse() -> ArgumentParser:
    parser = ArgumentParser(
        prog=os.path.basename(os.path.dirname(os.path.abspath(__file__))),
        description='access local Darktable library images through a GraphQL interface'
    )
    parser.set_defaults(cmd=None)
    parser.add_argument(
        '-c', '--config',
        type=str,
        default='./config.json',
        help='path to the configuration file',
        metavar='CONFIG_FILE'
    )
    subparsers = parser.add_subparsers()
    run = subparsers.add_parser(
        'run',
        help='run the GraphQL server'
    )
    run.set_defaults(cmd=CommandType.RUN)
    run.add_argument(
        '--host',
        type=str,
        default='127.0.0.1',
        help='host'
    )
    run.add_argument(
        '-p', '--port',
        type=int,
        default=5000,
        help='port'
    )
    run.add_argument(
        '--debug',
        action='store_true',
        help='launch server in debug mode'
    )
    generate_orm = subparsers.add_parser(
        'generate-orm',
        help='generate ORM for the darktable version that is configured as CLI path'
    )
    generate_orm.set_defaults(cmd=CommandType.GENERATE_ORM)
    return parser


def main(args, config):
    if args.cmd == CommandType.RUN:
        app.run(host=args.host, port=args.port, debug=args.debug)
        return
    if args.cmd == CommandType.GENERATE_ORM:
        print('generating ORM source files')
        generate_orm(config['darktable']['cliPath'])
        # FIXME: how to know if the program still works with the older/newer ORM?
        # write tests that uses the ORM extensively and execute them?
        return


if __name__ == '__main__':
    parser = init_argparse()
    args = parser.parse_args()

    if args.cmd is None:
        parser.print_help()
        sys.exit(0)

    config = read_config(os.path.join(os.getcwd(), args.config))
    main(args, config)
