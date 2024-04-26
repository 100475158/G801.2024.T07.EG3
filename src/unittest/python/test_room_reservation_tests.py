"""testing room reservation based on csv file with tests"""
import csv
import json
import os.path
import hashlib
from os import remove
from unittest import TestCase
from freezegun import freeze_time
from uc3m_travel import (JSON_FILES_PATH,
                         HotelManager,
                         HotelReservation,
                         HotelManagementException)


class TestHotelReservation(TestCase):
    """Class for testing deliver_product"""

    def setUp(self):
        """ inicializo el entorno de prueba """
        fichero = "store_reservation.json"
        my_file = JSON_FILES_PATH + fichero
        if os.path.exists(my_file):
            remove(my_file)

    @staticmethod
    def read_file():
        """ this method read a Json file and return the value """
        my_file = JSON_FILES_PATH + "store_reservation.json"
        try:
            with open(my_file, "r", encoding="utf-8", newline="") as file:
                data = json.load(file)
        except FileNotFoundError as exception:
            raise HotelManagementException("Wrong file or file path") from exception
        except json.JSONDecodeError as exception:
            raise HotelManagementException("JSON Decode Error - Wrong JSON Format") from exception
        return data

    @freeze_time("2024/03/22 13:00:00")
    def test_duplicated_reservation_tests(self):
        """duplicated reservation test"""
        my_manager = HotelManager()
        credit_card_number = "5105105105105100"
        name = "JOSE LOPEZ"
        dni = "12345678Z"
        room_type = "SINGLE"
        arrival = "01/07/2024"
        days = 1
        phone_number = "+341234567"

        # first reservation
        my_manager.room_reservation(credit_card=credit_card_number,
                                    name_surname=name,
                                    id_card=dni,
                                    phone_number=phone_number,
                                    room_type=room_type,
                                    arrival_date=arrival,
                                    num_days=days)

        # we calculater the files signature before calling the second method
        reservations_file = JSON_FILES_PATH + "store_reservation.json"
        if os.path.isfile(reservations_file):
            with open(reservations_file, "r", encoding="utf-8", newline="") as file_org:
                hash_original = hashlib.md5(str(file_org).encode()).hexdigest()
        else:
            hash_original = ""
        # second reservation with same data
        with self.assertRaises(HotelManagementException) as exception_context:
            my_manager.room_reservation(credit_card=credit_card_number,
                                        name_surname=name,
                                        id_card=dni,
                                        phone_number=phone_number,
                                        room_type=room_type,
                                        arrival_date=arrival,
                                        num_days=days)
        self.assertEqual(exception_context.exception.message, "Reservation already exists")
        # now we check that the signature of the file is the same (the file didn't change
        # because the second call raised and exception)
        if os.path.isfile(reservations_file):
            with open(reservations_file, "r", encoding="utf-8", newline="") as file:
                hash_new = hashlib.md5(str(file).encode()).hexdigest()
        else:
            hash_new = ""
        self.assertEqual(hash_new, hash_original)

    def test_duplicated_id_reservation_tests(self):
        """duplicated reservation (different data but same idcard)"""
        my_manager = HotelManager()
        credit_card_number = "5105105105105100"
        name = "JOSE LOPEZ"
        dni = "12345678Z"
        room_type = "SINGLE"
        arrival = "01/07/2024"
        days = 1
        phone_number = "+341234567"

        # first reservation
        my_manager.room_reservation(credit_card=credit_card_number,
                                    name_surname=name,
                                    id_card=dni,
                                    phone_number=phone_number,
                                    room_type=room_type,
                                    arrival_date=arrival,
                                    num_days=days)

        reservations_file = JSON_FILES_PATH + "store_reservation.json"
        # we calculater the files signature bejore calling the second method
        if os.path.isfile(reservations_file):
            with open(reservations_file, "r", encoding="utf-8", newline="") as file_org:
                hash_original = hashlib.md5(str(file_org).encode()).hexdigest()
        else:
            hash_original = ""
        # second reservation with different data but same id card
        credit_card_number = "5105105105105100"
        name = "JOSE LOPEZ"
        dni = "12345678Z"
        room_type = "DOUBLE"
        arrival = "01/09/2024"
        days = 3
        phone_number = "+347654321"
        with self.assertRaises(HotelManagementException) as exception_context:
            my_manager.room_reservation(credit_card=credit_card_number,
                                        name_surname=name,
                                        id_card=dni,
                                        phone_number=phone_number,
                                        room_type=room_type,
                                        arrival_date=arrival,
                                        num_days=days)
        self.assertEqual(exception_context.exception.message, "This ID card has another reservation")
        # now we check that the signature of the file is the same (the file didn't change
        # because the second call raised and exception)
        if os.path.isfile(reservations_file):
            with open(reservations_file, "r", encoding="utf-8", newline="") as file:
                hash_new = hashlib.md5(str(file).encode()).hexdigest()
        else:
            hash_new = ""
        self.assertEqual(hash_new, hash_original)

    # pylint: disable=too-many-locals
    @freeze_time("2024/03/22 13:00:00")
    def test_parametrized_cases_tests(self):
        """Parametrized cases read from testingCases_RF1.csv"""
        my_cases = JSON_FILES_PATH + "GE2_TestCasesTemplate_2024_F1.csv"
        with open(my_cases, newline='', encoding='utf-8') as csvfile:
            param_test_cases = csv.DictReader(csvfile, delimiter=',')
            my_manager = HotelManager()
            for row in param_test_cases:
                test_id = row['ID TEST']
                dni = row["ID_CARD"]
                name = row["NAME_SURNAME"]
                room_type = row["ROOM_TYPE"]
                credit_card_number = row["CREDIT_CARD_NUMBER"]
                try:
                    days = int(row["NUM_DAYS"])
                except ValueError:
                    days = row["NUM_DAYS"]
                result = row["RESULT"]
                valid = row["VALID/INVALID"]
                arrival = row["ARRIVAL"]
                phone_number = row["PHONE_NUMBER"]
                if valid == "VALID":
                    with self.subTest(test_id + valid):
                        valor = my_manager.room_reservation(credit_card=credit_card_number,
                                                            name_surname=name,
                                                            id_card=dni,
                                                            phone_number=phone_number,
                                                            room_type=room_type,
                                                            arrival_date=arrival,
                                                            num_days=days)
                        self.assertEqual(result, valor)
                        # Check if this DNI is store in storeRequest.json
                        my_data = self.read_file()
                        my_request = HotelReservation(dni,
                                                      credit_card_number,
                                                      name,
                                                      phone_number,
                                                      room_type,
                                                      arrival, days)
                        found = False
                        for data in my_data:
                            if data["_HotelReservation__localizer"] == valor:
                                found = True
                                # this assert give me more information
                                # about the differences than assertEqual
                                self.assertDictEqual(data, my_request.__dict__)
                        # if found is False , this assert fails
                        self.assertTrue(found)
                else:
                    with self.subTest(test_id + valid):
                        reservations_file = JSON_FILES_PATH + "store_reservation.json"
                        # we calculate the files signature bejore calling the tested method
                        if os.path.isfile(reservations_file):
                            with open(reservations_file, "r", encoding="utf-8", newline=""
                                      ) as file_org:
                                hash_original = hashlib.md5(str(file_org).encode()).hexdigest()
                        else:
                            hash_original = ""
                        with self.assertRaises(HotelManagementException) as exception_context:
                            my_manager.room_reservation(credit_card=credit_card_number,
                                                        name_surname=name,
                                                        id_card=dni,
                                                        phone_number=phone_number,
                                                        room_type=room_type,
                                                        arrival_date=arrival,
                                                        num_days=days)
                        self.assertEqual(exception_context.exception.message, result)

                        # now we check that the signature of the file is the same
                        # (the file didn't change)
                        if os.path.isfile(reservations_file):
                            with open(reservations_file, "r", encoding="utf-8", newline="") as file:
                                hash_new = hashlib.md5(str(file).encode()).hexdigest()
                        else:
                            hash_new = ""
                        self.assertEqual(hash_new, hash_original)
