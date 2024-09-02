from django.core.management import BaseCommand

from materials.models import Lesson, Course
from users.models import Payment, User


class Command(BaseCommand):
    def handle(self, *args, **options):
        payment_list = [
            {
                "user": "User1",
                "date_of_payment": "2022-01-01",
                "lesson": "Lesson1",
                "course": "Course1",
                "payment_status": "Paid",
                "amount": 1000,
                "method": "Card"
            },
            {
                "user": "User2",
                "date_of_payment": "2022-01-02",
                "lesson": "Lesson2",
                "course": "Course2",
                "payment_status": "Not Paid",
                "amount": 500,
                "method": "Cash"
            },

        ]
        payment_for_create = []
        for payment_item in payment_list:
            payment_for_create.append(
                Payment(**payment_item)
            )

        Payment.objects.bulk_create(payment_for_create)
