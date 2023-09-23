import unittest
# Now, import the 'microservice_gui' module from the 'app' directory
from app import microservice_gui


class TestWebGui(unittest.TestCase):

    def test_is_empty(self):
        result = microservice_gui.is_empty('')       
        self.assertTrue(result)

        result = microservice_gui.is_empty(' ')       
        self.assertTrue(result)
    
        result = microservice_gui.is_empty('Hello, World!')
        self.assertFalse(result)

    # True if at the same time not empty, integer and positive
    def test_is_not_empty_integer(self):
        result = microservice_gui.is_not_empty_integer('5')
        self.assertTrue(result)

        result = microservice_gui.is_not_empty_integer('007')
        self.assertTrue(result)
        
        result = microservice_gui.is_not_empty_integer('0')
        self.assertFalse(result)

        result = microservice_gui.is_not_empty_integer('6U')
        self.assertFalse(result)

        result = microservice_gui.is_not_empty_integer('0.7')
        self.assertFalse(result)

        result = microservice_gui.is_not_empty_integer('-6')
        self.assertFalse(result)

        result = microservice_gui.is_not_empty_integer('')
        self.assertFalse(result)

        result = microservice_gui.is_not_empty_integer(' ')
        self.assertFalse(result)

        result = microservice_gui.is_not_empty_integer('Hello, World!')
        self.assertFalse(result)


    # True if at the same time not empty, float and positive
    def test_is_not_empty_float(self):
        result = microservice_gui.is_not_empty_float('5.5')
        self.assertTrue(result)

        result = microservice_gui.is_not_empty_float('5')
        self.assertTrue(result)

        result = microservice_gui.is_not_empty_float('007.7')
        self.assertTrue(result)
        
        result = microservice_gui.is_not_empty_float('0')
        self.assertFalse(result)

        result = microservice_gui.is_not_empty_float('6U')
        self.assertFalse(result)

        result = microservice_gui.is_not_empty_float('0.7')
        self.assertTrue(result)

        result = microservice_gui.is_not_empty_float('-6.5')
        self.assertFalse(result)

        result = microservice_gui.is_not_empty_float('')
        self.assertFalse(result)

        result = microservice_gui.is_not_empty_float(' ')
        self.assertFalse(result)

        result = microservice_gui.is_not_empty_float('Hello, World!')
        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()
