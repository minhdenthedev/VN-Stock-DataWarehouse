from datetime import date


def transform_time_str_to_date(time_str):
    quarter = time_str[:2]
    year = int(time_str[2:])
    match quarter:
        case "Q1":
            return date(year, 3, 15)
        case "Q2":
            return date(year, 6, 15)
        case "Q3":
            return date(year, 9, 15)
        case "Q4":
            return date(year, 12, 15)
        case _:
            return None