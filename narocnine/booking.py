from datetime import timedelta
from datumi import *

class Booking():

    def is_location_available(location_id, start_date, end_date):
        svi_datumi = SviDatumi()
        blackout_dates_by_location = svi_datumi.get_blackout_dates_by_location()

        # Get blackout dates for the location
        blackout_dates = blackout_dates_by_location.get(location_id, set())

    # Check if any requested date overlaps a blackout
        current_date = start_date
        while current_date <= end_date:
            if current_date in blackout_dates:
                return False
            current_date += timedelta(days=1)

        return True
