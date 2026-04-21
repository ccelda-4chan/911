import unittest
from core.engine import Engine
from services.bomber_services import get_default_services

class TestEngine(unittest.TestCase):
    def test_engine_init(self):
        services = get_default_services()
        engine = Engine(services)
        self.assertEqual(len(engine.services), 13)
        self.assertIsNone(engine._session)

    def test_engine_services_list(self):
        services = get_default_services()
        engine = Engine(services)
        service_names = [s.name for s in engine.services]
        self.assertIn("CUSTOM_SMS", service_names)
        self.assertIn("CALL_BOMB", service_names)

if __name__ == '__main__':
    unittest.main()
