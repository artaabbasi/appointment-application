from datetime import datetime, timezone, date, timedelta
from persiantools.jdatetime import JalaliDate, JalaliDateTime
import pytz

tehran_tz = pytz.timezone('Asia/Tehran')


class DatetimeUtil:
    @staticmethod
    def utc_now_datetime() -> datetime:
        utc_now = datetime.utcnow().replace(tzinfo=pytz.utc)
        tehran_now = utc_now.astimezone(tehran_tz)
        return tehran_now

    @staticmethod
    def utc_now_datetime_addition_days(days: int) -> datetime:
        utc_now = datetime.utcnow().replace(tzinfo=pytz.utc)
        tehran_now = utc_now.astimezone(tehran_tz)
        return tehran_now + timedelta(days=days)

    @staticmethod
    def utc_now_timestamp() -> float:
        """Returns utcnow second based timestamp."""
        return DatetimeUtil.utc_now_datetime().timestamp()

    @classmethod
    def utc_datetime_from_timestamp(cls, timestamp: float) -> datetime:
        """Gets a second based timestamp and converts it to python datetime object."""
        timestamp = cls.convert_milliseconds_timestamp_to_seconds_timestamp_if_required(timestamp)
        return datetime.utcfromtimestamp(timestamp)

    @staticmethod
    def utc_timestamp_from_utc_datetime(date: datetime) -> float:
        """Gets a python datetime sets it timezone to utc, and returns second timestamp in utc."""
        return date.replace(tzinfo=timezone.utc).timestamp()

    @classmethod
    def convert_milliseconds_timestamp_to_seconds_timestamp_if_required(cls, timestamp: float) -> float:
        """
        Convert 13 digit timestamp to 10 digit timestamp a.k.a: from milliseconds to seconds.
        """
        if len(str(int(timestamp))) == 13:
            timestamp /= 1000
        return timestamp

    @staticmethod
    def jalali_date_today_str() -> str:
        return JalaliDate.today().strftime("%Y/%m/%d")

    @staticmethod
    def jalali_date_today_str_addition_days(days: int) -> str:
        """Gets jalali today addition to days"""
        today_date = date.today() + timedelta(days=days)
        return (JalaliDate.to_jalali(today_date.year, today_date.month, today_date.day)
                .strftime("%Y/%m/%d"))

    @staticmethod
    def utc_to_jalali_date(input_date: date) -> JalaliDate:
        return JalaliDate.to_jalali(input_date.year, input_date.month, input_date.day)

    @staticmethod
    def utc_to_jalali_date_str(input_date: date) -> str:
        return DatetimeUtil.utc_to_jalali_date(input_date).strftime("%Y/%m/%d")

    @staticmethod
    def utc_to_jalali_date_time(input_date: datetime) -> JalaliDateTime:
        # print(input_date.year, input_date.month, input_date.day,
        #                                 input_date.hour, input_date.minute, input_date.second,)
        return JalaliDateTime.to_jalali(input_date.year, input_date.month, input_date.day,
                                        input_date.hour, input_date.minute, input_date.second,
                                        input_date.microsecond, input_date.tzinfo)

    @staticmethod
    def utc_to_jalali_date_time_str(input_date: datetime) -> str:
        return DatetimeUtil.utc_to_jalali_date_time(input_date).strftime("%Y/%m/%d %H:%M:%S")

    @staticmethod
    def utc_datetime_str_to_jalali_date_time_str(input_date: str) -> str:
        date_time = datetime.strptime(input_date, "%Y/%m/%d %H:%M:%S")
        return DatetimeUtil.utc_to_jalali_date_time(date_time).strftime("%Y/%m/%d %H:%M:%S")

    @staticmethod
    def utc_datetime_str_to_jalali_date_str(input_date: str) -> str:
        date_time = datetime.strptime(input_date, "%Y/%m/%d %H:%M:%S")
        return DatetimeUtil.utc_to_jalali_date_time(date_time).strftime("%Y/%m/%d")

    @staticmethod
    def utc_date_str_to_jalali_date_str(input_date: str) -> str:
        date_time = datetime.strptime(input_date, "%Y-%m-%d")
        return DatetimeUtil.utc_to_jalali_date_time(date_time).strftime("%Y/%m/%d")

    @staticmethod
    def utc_datetime_str_to_jalali_datetime_str(input_date: str) -> str:
        date_time = datetime.strptime(input_date, "%Y-%m-%d %H:%M")
        return DatetimeUtil.utc_to_jalali_date_time(date_time).strftime("%Y/%m/%d %H:%M")

    @staticmethod
    def str_jalali_to_utc_date(input_date: str) -> datetime:
        _datetime = JalaliDateTime.strptime(input_date, "%x").to_gregorian()
        return _datetime.astimezone(tehran_tz)

    @staticmethod
    def str_jalali_date_addition_days(input_date: str, days: int) -> str:
        _datetime = JalaliDateTime.strptime(input_date, "%x").to_gregorian()
        _datetime += timedelta(days=days)
        return (JalaliDate.to_jalali(_datetime.year, _datetime.month, _datetime.day)
                .strftime("%Y/%m/%d"))


    @staticmethod
    def str_jalali_datetime_addition_days(input_date: str, days: int) -> str:
        _datetime = JalaliDateTime.strptime(input_date, "%X").to_gregorian()
        _datetime += timedelta(days=days)
        return (JalaliDate.to_jalali(_datetime.year, _datetime.month, _datetime.day)
                .strftime("%Y/%m/%d %H:%M:%S"))
