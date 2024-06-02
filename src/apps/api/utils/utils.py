from datetime import datetime


def convert_to_datetime(date_string):
    if date_string is None:
        return None
    date_formats = ["%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M", "%Y-%m-%d %H", "%Y-%m-%d", "%Y.%m.%d", "%Y/%m/%d", "%Y.%m.%d %H:%M:%S", "%Y/%m/%d %H:%M:%S"]
    for fmt in date_formats:
        try:
            return datetime.strptime(date_string, fmt)
        except ValueError:
            continue
    raise ValueError(f"Date string '{date_string}' does not match any known format.")