##################################################
# Copyright (C) 2017, All rights reserved.
##################################################

import hashlib
import os
import virtualenv

from pyprelude.file_system import make_path
from pysimplevcs.git import Git

from pvt.exceptions import Informational

class Project(object):
    @staticmethod
    def find(config, search_dir=None):
        git = Git(search_dir)

        setup_py_path = make_path(git.repo_dir, "setup.py")
        if not os.path.isfile(setup_py_path):
            raise Informational("Could not determine project directory from search location {}".format(search_dir))

        project_dir = os.path.dirname(setup_py_path)
        project_id = hashlib.md5(project_dir).hexdigest()
        env_dir = make_path(config.dir, "envs", project_id)
        return Project(project_dir, env_dir)

    def __init__(self, project_dir, env_dir):
        self._project_dir = project_dir
        self._env_dir = env_dir

    @property
    def project_dir(self): return self._project_dir

    @property
    def env_dir(self): return self._env_dir

    def initialize(self, force=False):
        if os.path.isdir(self._env_dir):
            if force:
                shutil.rmtree(self._env_dir)
            else:
                raise Informational("Virtual environment directory {} already exists: use --force to overwrite".format(self._env_dir))

        virtualenv.create_environment(
            self._env_dir,
            search_dirs=virtualenv.file_search_dirs(),
            download=True)
