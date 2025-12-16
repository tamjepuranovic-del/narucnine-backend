from collections import defaultdict
from datetime import timedelta

from narocnine.models import Appointment


class SviDatumi:

    def get_blackout_dates_by_location(self):

        blackout_dates = defaultdict(set)

        blackouts = Appointment.objects.filter(type='blackout')
        isActive = Appointment.objects.filter(type='active')

        for appointment in blackouts:
            if appointment in isActive:
                current_date = appointment.appointment_start_date
                while current_date <= appointment.appointment_end_date:
                    blackout_dates[appointment.location_id].add(current_date)
                    current_date += timedelta(days=1)

        return blackout_dates

