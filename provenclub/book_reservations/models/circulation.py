from book_reservations.models.book import Book
from book_reservations.models.member import Member
from book_reservations.models.reservation import Reservation
from django.db import models, transaction
from django.utils import timezone

CHECKOUT = "checkout"
RETURN = "return"

EVENT_TYPE_CHOICES = (
    (CHECKOUT, CHECKOUT),
    (RETURN, RETURN),
)


class Circulation(models.Model):
    member = models.ForeignKey(
        "book_reservations.Member",
        on_delete=models.CASCADE,
        help_text="The member who reserved the book",
    )
    book = models.ForeignKey(
        "book_reservations.Book",
        on_delete=models.CASCADE,
        help_text="The reserved book",
    )
    event_type = models.CharField(
        max_length=512, choices=EVENT_TYPE_CHOICES, help_text="Checkout ? Return"
    )
    datetime = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "circulations"

    @classmethod
    def add_event(cls, member_id: int, book_id: int, status: str, datetime=None) -> int:
        obj = cls(
            member_id=member_id,
            book_id=book_id,
            event_type=status,
            datetime=datetime or timezone.now(),
        )
        obj.save()
        return obj.id

    @classmethod
    @transaction.atomic
    def checkout_book(cls, book_id: int, member_id: int, datetime=None) -> str | None:
        """
        Issue the book if a copy is available. -> reduce number of book copies by one
        """
        try:
            book: Book = Book.objects.get(pk=book_id)

        except Book.DoesNotExist:
            return f"Book({book_id}) Does Not Exist"

        try:
            member: Member = Member.objects.get(pk=member_id)

        except Member.DoesNotExist:
            return f"Member({member_id}) Does Not Exist"

        if book.can_be_checked_out_by_member(member_id=member_id):
            book.number_of_copies -= 1
            book.save()
            circulation_id = cls.add_event(
                member_id=member_id,
                book_id=book.book_id,
                status=CHECKOUT,
                datetime=datetime,
            )
            book.fulfill_reservation(
                member_id=member.member_id,
                circulation_id=circulation_id,
                datetime=datetime,
            )

        else:
            cls.reserve_book(book_id=book.book_id, member_id=member.member_id)
            return "Book Copy is not available, booked a reservation for this book"

    @classmethod
    @transaction.atomic
    def return_book(cls, book_id: int, member_id: int, datetime=None) -> str | None:
        """
        Revert Issue the book if a copy is available. -> increase number of book copies by one
        """
        try:
            book: Book = Book.objects.get(pk=book_id)

        except Book.DoesNotExist:
            return f"Book({book_id}) Does Not Exist"

        try:
            member: Member = Member.objects.get(pk=member_id)

        except Member.DoesNotExist:
            return f"Member({member_id}) Does Not Exist"

        book.number_of_copies += 1
        book.save()
        circulation_id = cls.add_event(
            member_id=member.member_id,
            book_id=book.book_id,
            status=RETURN,
            datetime=datetime,
        )

        book.fulfill_reservation(
            member_id=member.member_id,
            circulation_id=circulation_id,
            datetime=datetime,
        )

    @classmethod
    @transaction.atomic
    def reserve_book(cls, book_id: int, member_id: int, datetime=None) -> str | None:
        _ = Reservation(
            member_id=member_id, book_id=book_id, reserved_at=datetime or timezone.now()
        ).save()

    @classmethod
    @transaction.atomic
    def fulfill_book(cls, book_id: int, member_id: int, datetime=None) -> str | None:
        try:
            book: Book = Book.objects.get(pk=book_id)

        except Book.DoesNotExist:
            return f"Book({book_id}) Does Not Exist"

        try:
            member: Member = Member.objects.get(pk=member_id)

        except Member.DoesNotExist:
            return f"Member({member_id}) Does Not Exist"

        book.fulfill_reservation(
            member_id=member.member_id,
            datetime=datetime,
        )
