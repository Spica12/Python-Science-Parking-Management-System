from datetime import timedelta


def get_total_parking_duration(parking_sessions):
    total_parking_duration = sum(
        (session.parking_duration for session in parking_sessions),
        timedelta()
    )

    days = total_parking_duration.days
    hours, remainder = divmod(total_parking_duration.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    result = []
    if days > 0:
        result.append(f"{days} д.")
    if hours > 0:
        result.append(f"{hours} год.")
    if minutes > 0:
        result.append(f"{minutes} хв.")
    if seconds > 0:
        result.append(f"{seconds} сек.")

    return ", ".join(result)
