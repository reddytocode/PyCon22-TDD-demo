def suma(a, b):
    return a + b


# tests
from unittest import TestCase, main


class TestSuma(TestCase):
    def test_success(self):
        expected = 3
        result = suma(1, 2)
        self.assertEqual(result, expected)

    def test_fail(self):
        result = suma(1, "2")
        self.assertEqual(3, expected)




if __name__ == "__main__":
    main()
