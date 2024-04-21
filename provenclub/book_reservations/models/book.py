from book_reservations.models.reservation import Reservation
from django.db import models
from django.utils import timezone


class Book(models.Model):
    book_id = models.PositiveBigIntegerField(
        primary_key=True, unique=True, db_index=True
    )
    book_name = models.CharField(max_length=512, unique=True, db_index=True)
    number_of_copies = models.PositiveBigIntegerField(
        default=0, help_text="Number of available/remaining copies of a book"
    )

    def can_be_checked_out_by_member(self, member_id: int):
        """"""
        unfulfilled_reservation_by_this_member: Reservation = (
            Reservation.objects.filter(
                book_id=self.book_id, member_id=member_id, fulfilled_by__isnull=True
            )
        )  # Unfufilled reservations
        if (
            unfulfilled_reservation_by_this_member.exists()
            and self.number_of_copies > 0
        ):
            return True

        existing_book_reservations_by_other_members = (
            Reservation.objects.filter(
                book=self.book_id, fulfilled_by__isnull=True
            )  # Unfufilled reservations
            .exclude(member_id=member_id)  # By other members
            .count()
        )

        # If number of copies > number of existing book reservations by other members
        return self.number_of_copies > existing_book_reservations_by_other_members

    def fulfill_reservation(
        self, member_id: int, circulation_id: int = None, datetime=None
    ):
        _ = Reservation.objects.filter(
            book=self.book_id, member=member_id, fulfilled_by__isnull=True
        ).update(
            fulfilled_by=circulation_id,
            is_fulfilled=True,
            fulfilled_at=datetime or timezone.now(),
        )

    class Meta:
        db_table = "books"
