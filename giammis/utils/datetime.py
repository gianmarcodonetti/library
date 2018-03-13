from datetime import datetime, timedelta


def sum_intervals(intervals):
    """Compute the total sum of the given date intervals, handling in the proper way overlapping intervals.

    Args:
        intervals (list[tuple]): list of tuples, where each tuple contains (start_date, end_date)

    Returns:
        float: total sum of the given intervals, in seconds
    """
    start, end = 0, 1
    times = []
    for interval in intervals:
        times.append((interval[start], start))
        times.append((interval[end], end))
    times.sort()

    started = 0
    start_time = times[0][0] if times else None
    result = timedelta()
    for t, type in times:
        if type == start:
            if not started:
                start_time = t
            started += 1
        elif type == end:
            started -= 1
            if not started:
                result += (t - start_time)
    return result.total_seconds()


def xrange_datetime(start_date, end_date, delta):
    """

    Args:
        start_date (datetime): the start of the time period to bin
        end_date (datetime): the end of the time period to bin
        delta (timedelta): the delta between each time bin

    Returns:
        GeneratorType:
    """
    curr = start_date
    while curr < end_date:
        yield curr
        curr += delta


def range_datetime(start_date, end_date, delta):
    """

    Args:
        start_date (datetime): the start of the time period to bin
        end_date (datetime): the end of the time period to bin
        delta (timedelta): the delta between each time bin

    Returns:
        list:
    """
    curr = start_date
    result = []
    while curr < end_date:
        result.append(curr)
        curr += delta
    return result


def round_datetime(date, round_to=60 * 60):
    """

    Args:
        date (datetime):
        round_to (int): time unit, the granularity for the rounding, in seconds

    Returns:
        datetime:
    """
    seconds = (date.replace(tzinfo=None) - date.min).seconds
    rounding = (seconds + round_to / 2) // round_to * round_to
    return date + timedelta(0, rounding - seconds, -date.microsecond)


def floor_datetime(date, round_to=60 * 60):
    """

    Args:
        date (datetime):
        round_to (float): time unit, the granularity for the flooring, in seconds

    Returns:
        datetime:
    """
    seconds = (date.replace(tzinfo=None) - date.min).seconds
    rounding = seconds // round_to * round_to
    return date + timedelta(0, rounding - seconds, -date.microsecond)


def time_units_touched(start_date, duration_seconds, delta_seconds):
    """

    Args:
        start_date (datetime):
        duration_seconds (int): event duration, in seconds
        delta_seconds (float): time granularity, in seconds

    Returns:
        list:
    """
    first_unit = floor_datetime(start_date, delta_seconds)
    end_date = start_date + timedelta(seconds=duration_seconds)
    last_unit = floor_datetime(end_date, delta_seconds)
    result = range_datetime(first_unit, last_unit, delta=timedelta(seconds=delta_seconds))
    if last_unit != end_date:
        result.append(last_unit)
    return result
