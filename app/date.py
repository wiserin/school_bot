from time import time, sleep, localtime
from datetime import datetime, timedelta 



class Date():
    current_time = localtime(time())
    current_date = datetime.today()

    year = current_time.tm_year
    month = current_time.tm_mon
    day = current_time.tm_mday
    hour = current_time.tm_hour
    min = current_time.tm_min
    sec = current_time.tm_sec

    def date_count(self, quantity: int):
        self.quantity = quantity
        count = 0
        days = {}

        for i in range (0, self.quantity):
            day = []
            date = self.current_date + timedelta(days=count)
            day.append(str(date.year))
            day.append(str(date.month))
            day.append(str(date.day))
            day_str = '-'.join(day)
            days[day_str] = day[2]
            count += 1
        return days




