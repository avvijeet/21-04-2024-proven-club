from django.db import models


class Member(models.Model):
    member_id = models.PositiveBigIntegerField(
        primary_key=True, unique=True, db_index=True
    )
    member_name = models.CharField(
        max_length=512,
        unique=True,
        db_index=True,
        help_text="Member name who checked out a book",
    )

    class Meta:
        db_table = "members"
