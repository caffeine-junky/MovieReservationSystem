
def seconds_to_time(seconds: int | float) -> str:
    """
    Convert seconds to time format: HH:MM:SS
    if seconds are equal or greater than an hour
    else MM:SS.
    """
    hours = int(seconds // 3600)
    seconds %= 3600
    minutes = int(seconds // 60)
    seconds %= 60
    return f"{hours:02}:{minutes:02}:{seconds:02}" if hours > 0 else f"{minutes:02}:{seconds:02}"
