import unittest
from uc3m_travel.storage.reservation_json_store import ReservationJsonStore
from uc3m_travel import HotelManager
class MyTestCase(unittest.TestCase):
    def test_singleton(self):
        mi_primera_instancia= HotelManager()
        mi_segunda_instancia= HotelManager()

        self.assertEqual(mi_primera_instancia, mi_segunda_instancia )  # add assertion here

    def test_singleton(self):
        mi_primera_instancia= ReservationJsonStore()
        mi_segunda_instancia= ReservationJsonStore()

        self.assertEqual(mi_primera_instancia, mi_segunda_instancia )
if __name__ == '__main__':
    unittest.main()
