from django.db import models
from django.utils import timezone


class Reservation(models.Model):
    member_id = models.ForeignKey(
        "book_reservations.Member",
        on_delete=models.CASCADE,
        help_text="The member who reserved the book",
        db_index=True,
    )
    book_id = models.ForeignKey(
        "book_reservations.Book",
        on_delete=models.CASCADE,
        help_text="The reserved book",
        db_index=True,
    )
    reserved_at = models.DateTimeField(default=timezone.now)
    fulfilled_by = models.ForeignKey(
        "book_reservations.Circulation",
        on_delete=models.CASCADE,
        help_text="The circulation which fulfilled the book",
        null=True,
    )
    is_fulfilled = models.BooleanField(default=False)
    fulfilled_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "reservations"
        unique_together = (
            "member_id",
            "book_id",
        )  # One book cannot be reserved more than once by one member
