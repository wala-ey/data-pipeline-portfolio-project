import unittest
from path import Path
import sys
sys.path.append(Path("src/pipeline"))
from db_utilities import SQLite3DatabaseConnection

class Testdb_utilities(unittest.TestCase):
    def __init__(self):
        self.contextmanager = SQLite3DatabaseConnection