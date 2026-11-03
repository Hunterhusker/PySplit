import unittest
from pathlib import Path

if __name__ == '__main__':
    loader = unittest.TestLoader()
    HERE = Path(__file__).resolve().parent
    suite = loader.discover(start_dir=HERE, pattern='Test*.py')

    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
