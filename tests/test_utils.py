import unittest
from core.base_service import BaseService

class DummyService(BaseService):
    async def send(self, session, phone):
        return True

class TestUtils(unittest.TestCase):
    def setUp(self):
        self.service = DummyService("test")

    def test_normalize_ph_09(self):
        self.assertEqual(self.service.normalize_phone("09123456789"), "+639123456789")

    def test_normalize_ph_9(self):
        self.assertEqual(self.service.normalize_phone("9123456789"), "+639123456789")

    def test_normalize_ph_63(self):
        self.assertEqual(self.service.normalize_phone("639123456789"), "+639123456789")

    def test_normalize_ph_plus63(self):
        self.assertEqual(self.service.normalize_phone("+639123456789"), "+639123456789")

    def test_normalize_with_spaces(self):
        self.assertEqual(self.service.normalize_phone("0912 345 6789"), "+639123456789")

if __name__ == '__main__':
    unittest.main()
