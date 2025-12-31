from collections import defaultdict
from datetime import timedelta

from narocnine.models import Appointment


class SviDatumi:

    @staticmethod
    def get_blackout_dates_by_location():
        blackout_slots = defaultdict(list)
        blackouts = Appointment.objects.filter(type='blackout', status='active')
        for a in blackouts:
            blackout_slots[a.location_id].append(
                (a.appointment_start_date,a.appointment_end_date, a.start_time, a.end_time)
            )
        return blackout_slots

