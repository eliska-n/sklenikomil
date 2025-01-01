START_YEAR = 2024


def to_greenhouse_time(week: int, year: int):
	greenhouse_time = week + ((year - START_YEAR) * 52)
	return greenhouse_time
