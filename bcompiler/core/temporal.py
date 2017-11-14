import datetime


class Quarter:

    start_months = {
        1: (4, 'April'),
        2: (7, 'July'),
        3: (10, 'October'),
        4: (1, 'January')
    }

    end_months = {
        1: (6, 'June', 30),
        2: (9, 'September', 30),
        3: (12, 'December', 31),
        4: (3, 'March', 31),
    }

    def __init__(self, quarter: int, year: int):


        if isinstance(quarter, int) and (quarter >= 1 and quarter <= 4):
            self.quarter = quarter
        else:
            raise ValueError("A quarter must be either 1, 2, 3 or 4")

        if isinstance(year, int) and (year in range(1950, 2100)):
            self.year = year
        else:
            raise ValueError("Year must be between 1950 and 2100 - surely that will do?")

        self.start_date = self._start_date(self.quarter, self.year)
        self.end_date = self._end_date(self.quarter, self.year)

    def _start_date(self, q, y):
        return datetime.date(y, Quarter.start_months[q][0], 1)

    def _end_date(self, q, y):
        return datetime.date(y, Quarter.end_months[q][0], Quarter.end_months[q][2])
