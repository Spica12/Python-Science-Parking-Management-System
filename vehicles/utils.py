from datetime import timedelta

from parking_service.models import StatusParkingEnum


def get_total_parking_duration(parking_sessions):

    parking_sessions_finished = parking_sessions.filter(status=StatusParkingEnum.FINISHED.name)

    total_parking_duration = sum(
        (session.parking_duration for session in parking_sessions_finished),
        timedelta()
    )
    print(total_parking_duration)

    days = total_parking_duration.days
    hours, remainder = divmod(total_parking_duration.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    result = []
    result.append(f"{days} d")
    result.append(f"{hours} h")
    result.append(f"{minutes} m")
    result.append(f"{seconds} s")


    return " ".join(result)
