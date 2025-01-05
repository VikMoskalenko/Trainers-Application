import datetime
import booking

# def available_time_offer(trainer, service_id, date, booking=None):
#     trainer_schedule = trainer.models.TrainerSchedule.objects.filter(trainer=trainer, datetime_start__date=date)
#     trainer_bookings = booking.models.Booking.objects.filter(trainer=trainer, datetime_start__date=date)
#     desired_service = trainer.models.Service.objects.get(pk=service_id)
#     search_window = desired_service.duration
#     available_slots=[]
#     for schedule in trainer_schedule:
#         current_time = schedule.datetime_start__date
#         end_time = schedule.datetime_end__date
#
#         while current_time + timedelta(minutes=search_window) <= end_time:
#             is_booked = False
#             for booking in trainer_bookings:
#                 booking_start = booking.datetime_start
#                 booking_end = booking_start + timedelta(minutes=booking.duration)
#
#                 if not(
#                     current_time + timedelta(minutes=search_window) <= booking_start
#                     or current_time >= booking_end
#                 ):
#                     is_booked = True
#                     break
#             if not is_booked:
#                 available_slots.append(current_time)
#             current_time += timedelta(minutes=15)
#     return available_slots

def booking_time(trainer_schedule, bookings, cur_date, **kwargs):
    return [cur_date.replace(hour=8),cur_date.replace(hour=10) ]

