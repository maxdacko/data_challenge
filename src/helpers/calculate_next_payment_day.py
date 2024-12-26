from datetime import datetime, timedelta

def calculate_next_payment_day(row):
    """
    Calculates the day of the next allowance, based on the event timestamp, 
    payment frequency, and specified day.
    Args:
        row (Series): A row from the DataFrame containing event timestamp, 
                      frequency, and scheduled day.
    Returns:
        int: The day of the month for the next payment.
    """
    timestamp = row['event.timestamp']
    frequency = row['allowance.scheduled.frequency']
    day = row['allowance.scheduled.day'].lower()

    if frequency == "daily":
        next_date = timestamp + timedelta(days=1)
    elif frequency == "weekly":
        days_to_next = {
            "monday": 0, "tuesday": 1, "wednesday": 2, "thursday": 3,
            "friday": 4, "saturday": 5, "sunday": 6
        }
        current_weekday = timestamp.weekday()
        target_weekday = days_to_next.get(day, 0)
        delta_days = (target_weekday - current_weekday + 7) % 7
        if delta_days == 0:
            delta_days = 7
        next_date = timestamp + timedelta(days=delta_days)
    elif frequency == "biweekly":
        days_to_next = {
            "monday": 0, "tuesday": 1, "wednesday": 2, "thursday": 3,
            "friday": 4, "saturday": 5, "sunday": 6
        }
        current_weekday = timestamp.weekday()
        target_weekday = days_to_next.get(day, 0)
        delta_days = (target_weekday - current_weekday + 14) % 14
        if delta_days == 0:
            delta_days = 14
        next_date = timestamp + timedelta(days=delta_days)
    elif frequency == "monthly":
        if day == "first_day":
            next_date = timestamp.replace(day=1) + timedelta(days=(1 if timestamp.day > 1 else 0))
        elif day == "fifteenth_day":
            next_date = timestamp.replace(day=15) + timedelta(days=(15 if timestamp.day > 15 else 0))
    else:
        return None

    return next_date.day