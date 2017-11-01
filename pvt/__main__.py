##################################################
# Copyright (C) 2017, All rights reserved.
##################################################

from __future__ import print_function
import argparse
import os
import sys

from pyprelude.file_system import make_path

from pvt import __description__, __project_name__, __version__
from pvt.config import Config
from pvt.exceptions import Informational
from pvt.project import Project

def _do_init(config, args):
    project = Project.find(config, args.search_dir)
    project.initialize(force=args.force)
    print("Initialized virtual environment for {} in {}".format(project.project_dir, project.env_dir))

def _do_exec(config, args):
    project = Project.find(config, args.search_dir)
    project.execute_command(args.command)

def _add_search_dir_arg(parser, default):
    parser.add_argument(
        "--search-dir",
        "-d",
        type=make_path,
        default=make_path(default),
        help="Location from which to search for project")

def _main(argv=None):
    if argv is None:
        argv = sys.argv[1:]

    config_dir = make_path(os.path.expanduser(os.environ.get("PVT_DIR", "~/.pvt")))
    config = Config(config_dir)

    default_search_dir = os.getcwd()

    parser = argparse.ArgumentParser(prog=__project_name__, description=__description__)
    parser.add_argument(
        "--version",
        action="version",
        version="{} version {}".format(__project_name__, __version__))

    subparsers = parser.add_subparsers(help="subcommand help")

    init_parser = subparsers.add_parser("init", help="Initialize virtual environment for current project")
    init_parser.set_defaults(func=_do_init)
    _add_search_dir_arg(init_parser, default_search_dir)
    init_parser.add_argument(
        "--force",
        "-f",
        action="store_true",
        help="Force overwrite of virtual environment directory if it already exists")

    exec_parser = subparsers.add_parser("exec", help="Execute command line in virtual environment context")
    exec_parser.set_defaults(func=_do_exec)
    _add_search_dir_arg(exec_parser, default_search_dir)
    exec_parser.add_argument(
        "command",
        nargs=argparse.REMAINDER,
        help="Command line to execute")

    args = parser.parse_args(argv)
    try:
        args.func(config, args)
    except Informational as e:
        print(e.message)
        sys.exit(1)

if __name__ == "__main__":
    _main()