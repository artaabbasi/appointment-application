class TestPhoneNumbersConfig:
    _PHONE_NUMBERS = ["09120458562"]

    @staticmethod
    def is_test_phone_number(phone_number: str) -> bool:
        if phone_number in TestPhoneNumbersConfig._PHONE_NUMBERS:
            return True
        return False
