import unittest

if __name__ == "__main__":
    # Add the project root directory to sys.path
    import os
    import sys
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "app")))

    # Discover and run tests using unittest
    loader = unittest.TestLoader()
    test_suite = loader.discover("tests")
    test_runner = unittest.TextTestRunner()
    test_runner.run(test_suite)
