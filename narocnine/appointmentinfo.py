# narocnine/appointment_info.py

from narocnine.models import Appointment

def get_appointment_info(session, location_id):
    """
    Returns a dict with appointment + location info for a user at a location.
    Uses session to get current user id.
    """
    user_id = session.get('current_user_id')
    if not user_id:
        return None

    appointment = Appointment.objects.filter(
        user_id=user_id,
        location_id=location_id,
        type='appointment'
    ).first()  # None if no appointment

    if not appointment:
        return None

    location = appointment.location

    return {
        'appointment_id': appointment.appointment_id,
        'date': appointment.appointment_start_date,
        'time': appointment.start_time,
        'status': appointment.status,
        'location_name': location.name,
        'location_address': getattr(location, 'address', ''),
        'location_city': getattr(location, 'city', ''),
    }
