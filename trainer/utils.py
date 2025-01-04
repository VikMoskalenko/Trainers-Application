import booking


def available_time_offer(trainer, service_id, date):
    trainer_schedule = trainer.models.TrainerSchedule.objects.filter(trainer=trainer, datetime_start__date=date)
    trainer_bookings = booking.models.Booking.objects.filter(trainer=trainer, datetime_start__date=date)
    desired_service = trainer.models.Service.objects.get(pk=service_id)
    search_window = desired_service.duration
