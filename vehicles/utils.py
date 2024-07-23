


def get_total_parking_duration(parking_session):
    total_parking_duration = 0

    for session in parking_session:
        total_parking_duration += session.parking_duration

    return total_parking_duration
