import unittest
from uc3m_travel.storage.reservation_json_store import ReservationJsonStore
from uc3m_travel.hotel_manager import HotelManager
from uc3m_travel.storage.stay_json_store import JsonStoreCheckin
from uc3m_travel.storage.checkout_json_store import JsonStoreCheckout


class MyTestCase(unittest.TestCase):
    def test_singleton(self):
        first_instance = HotelManager()
        second_instance = HotelManager()

        self.assertEqual(first_instance, second_instance)  # add assertion here

    def test_singleton2(self):
        first_instance = ReservationJsonStore()
        second_instance = ReservationJsonStore()

        self.assertEqual(first_instance, second_instance)

    def test_singleton3(self):
        first_instance = JsonStoreCheckin()
        second_instance = JsonStoreCheckin()

        self.assertEqual(first_instance, second_instance)  # add assertion here

    def test_singleton4(self):
        first_instance = JsonStoreCheckout()
        second_instance = JsonStoreCheckout()

        self.assertEqual(first_instance, second_instance)


if __name__ == '__main__':
    unittest.main()
