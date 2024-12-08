START_WEEK = 1
START_YEAR = 2024


def to_greenhouse_time(week: int, year: int):
	greenhouse_time = (week - START_WEEK) * (year - START_YEAR + 1)
	return greenhouse_time
