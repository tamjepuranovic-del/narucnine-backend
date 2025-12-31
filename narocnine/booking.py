from .datumi import *
from datetime import datetime, timedelta, time
from narocnine.models import Appointment


class Booking:


    @staticmethod
    def is_location_available(location_id, date_, start_time):
        svi_datumi = SviDatumi()
        blackout_slots = svi_datumi.get_blackout_dates_by_location().get(location_id, [])

        booking_start = datetime.combine(date_, start_time)
        booking_end = booking_start + timedelta(hours=1)

        for b_start_date, b_end_date, _, _ in blackout_slots:
            blackout_start = datetime.combine(b_start_date, time.min)
            blackout_end = datetime.combine(b_end_date, time.max)

            if booking_start < blackout_end and booking_end > blackout_start:
                return False

        return True

    @staticmethod
    def reserve(user_id, location_id, date, start_time):
        """
        Reserve appointment with end_time automatically set to 1 hour after start_time.
        """
        if not Booking.is_location_available(location_id, date, start_time):
            raise ValueError("Location not available at this date/time")

        # Compute end_time as 1 hour after start_time
        start_dt = datetime.combine(date, start_time)
        end_dt = start_dt + timedelta(hours=1)
        end_time = end_dt.time()

        return Appointment.objects.create(
            location_id=location_id,
            user_id=user_id,
            appointment_start_date=date,
            appointment_end_date=date,
            start_time=start_time,
            end_time=end_time,
            type='appointment',
            status='active',
        )