##################################################
# Copyright (C) 2017, All rights reserved.
##################################################

import hashlib
import os
import shutil
import virtualenv

from pyprelude.file_system import make_path
from pyprelude.platform import ON_WINDOWS
from pyprelude.process import execute
from pyprelude.temp_util import temp_cwd
from pyprelude.util import unpack_args
from pysimplevcs.git import Git

from pvt.exceptions import Informational

def _make_bin_dir(env_dir):
    if ON_WINDOWS:
        return make_path(env_dir, "Scripts")
    else:
        return make_path(env_dir, "bin")

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
        self._bin_dir = _make_bin_dir(self._env_dir)

    @property
    def project_dir(self): return self._project_dir

    @property
    def env_dir(self): return self._env_dir

    @property
    def bin_dir(self): return self._bin_dir

    def initialize(self, force=False):
        if os.path.isdir(self._env_dir):
            if force:
                shutil.rmtree(self._env_dir)
            else:
                raise Informational("Virtual environment directory {} already exists: use \"--force\" to overwrite".format(self._env_dir))

        virtualenv.create_environment(
            self._env_dir,
            search_dirs=virtualenv.file_search_dirs(),
            download=True)

    def uninitialize(self):
        if os.path.isdir(self._env_dir):
            shutil.rmtree(self._env_dir)

    def execute_script(self, script_name, args):
        self._check_env_dir()
        script_path = make_path(self._bin_dir, script_name)
        os.system(" ".join([script_path] + args))

    def execute_setup_actions(self, actions):
        self._check_env_dir()
        with temp_cwd(self._project_dir):
            self.execute_script("python", ["setup.py"] + actions)

    def _check_env_dir(self):
        if not os.path.isdir(self._env_dir):
            raise Informational("Virtual environment directory does not exist for project {}: create with \"init\" command".format(self._project_dir))
