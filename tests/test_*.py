import unittest
import os
from config import load_config

class TestDevelopmentConfiguration(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.test_json_file = '/Users/Joseph/udacity-capstone-python/python-structure-template/config/test.json'
        
        # Ensuring the file exists before running tests
        if not os.path.exists(cls.test_json_file):
            raise FileNotFoundError(f"The test configuration file '{cls.test_json_file}' was not found.")

    def test_singleton_behavior(self):
        config1 = load_config(self.test_json_file)
        config2 = load_config(self.test_json_file)
        self.assertIs(config1, config2)

    def test_metadata(self):
        config = load_config(self.test_json_file)
        self.assertEqual(config.metadata['title'], 'Test Configuration')
        self.assertEqual(config.metadata['version'], '1.0.0')

    def test_database_config(self):
        config = load_config(self.test_json_file)
        self.assertEqual(config.database['host'], 'localhost')
        self.assertEqual(config.database['port'], 5432)

    def test_logging_config(self):
        config = load_config(self.test_json_file)
        self.assertEqual(config.logging['level'], 'DEBUG')
        self.assertEqual(config.logging['file']['path'], 'logs/development.log')

    def test_get_path(self):
        config = load_config(self.test_json_file)
        self.assertEqual(config.get_path('fonts', 'OpenSans-Bold.ttf'), 'tests/res/font/open-sans/OpenSans-Bold.ttf')
        self.assertEqual(config.get_path('quotes', 'SimpleLines.csv'), 'tests/res/quotes/SimpleLines.csv')
        self.assertEqual(config.get_path('images', 'xander_1.jpg'), 'tests/res/img/xander_1.jpg')
        self.assertEqual(config.get_path('default', 'default.csv'), 'tests/res/default/default.csv')

    def test_get_path_invalid_category(self):
        config = load_config(self.test_json_file)
        with self.assertRaises(ValueError):
            config.get_path('invalid_category', 'somefile.txt')

    def test_get_path_invalid_file(self):
        config = load_config(self.test_json_file)
        with self.assertRaises(ValueError):
            config.get_path('fonts', 'nonexistentfile.ttf')

if __name__ == '__main__':
    unittest.main()
