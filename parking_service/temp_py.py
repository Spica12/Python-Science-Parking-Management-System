    def save(self, *args, **kwargs):
        self.amount = self.calculate_amount_for_session()
        super().save(*args, **kwargs)

    def calculate_amount_for_session(self):
        current_tariff = Tariff.objects.filter(
            start_date__lte=self.started_at,
            end_date__gte=self.started_at
        ).first()
        session = ParkingSession.objects.filter(pk=self.parking_session_pk.pk).first()
        duration = session.parking_duration

        amount = current_tariff * duration
        return amount
