# -*- coding: utf-8 -*-

from os.path import join, dirname
from dotenv  import load_dotenv

dotenv_path = join(dirname(__file__), 'local.env')
load_dotenv(dotenv_path)