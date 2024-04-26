import unittest
from uc3m_travel.storage.reservation_json_store import ReservationJsonStore
from uc3m_travel.hotel_manager import HotelManager
from uc3m_travel.storage.stay_json_store import JsonStoreCheckin
from uc3m_travel.storage.checkout_json_store import JsonStoreCheckout


class MyTestCase(unittest.TestCase):
    def test_singleton(self):
        mi_primera_instancia = HotelManager()
        mi_segunda_instancia = HotelManager()

        self.assertEqual(mi_primera_instancia, mi_segunda_instancia)  # add assertion here

    def test_singleton2(self):
        mi_primera_instancia = ReservationJsonStore()
        mi_segunda_instancia = ReservationJsonStore()

        self.assertEqual(mi_primera_instancia, mi_segunda_instancia)

    def test_singleton3(self):
        mi_primera_instancia = JsonStoreCheckin()
        mi_segunda_instancia = JsonStoreCheckin()

        self.assertEqual(mi_primera_instancia, mi_segunda_instancia)  # add assertion here

    def test_singleton4(self):
        mi_primera_instancia = JsonStoreCheckout()
        mi_segunda_instancia = JsonStoreCheckout()

        self.assertEqual(mi_primera_instancia, mi_segunda_instancia)


if __name__ == '__main__':
    unittest.main()
