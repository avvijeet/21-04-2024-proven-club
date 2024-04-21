from book_reservations.models import Circulation
from book_reservations.serializers import BookViewSetSerializer
from dateutil.parser import parser
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import ViewSet

# Create your views here.
# API Endpoint(s) for handling book checkouts, returns, reservations and reservation fulfillments


class BooksViewSet(ViewSet):
    # - Check out/Issue a book when a copy is available in case of a ‘checkout’ request
    serializer_class = BookViewSetSerializer

    @action(methods=["POST"], detail=False)
    def checkout(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        book_pk = serializer.data.get("book_id")
        member_pk = serializer.data.get("member_id")

        err = Circulation.checkout_book(book_id=book_pk, member_id=member_pk)
        if err is not None:
            return Response(data={"error": err}, status=status.HTTP_400_BAD_REQUEST)

        return Response(
            data={
                "message": f"Book({book_pk}) Checked Out By {member_pk} Successfully"
            },
            status=status.HTTP_200_OK,
        )

    # - Return a book on a ‘return’ request
    @action(methods=["PUT"], detail=False)
    def return_book(self, request):
        # - Fulfill request from the reservation queue once a book is returned and a copy becomes available
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        book_pk = serializer.data.get("book_id")
        member_pk = serializer.data.get("member_id")

        err = Circulation.return_book(book_id=book_pk, member_id=member_pk)
        if err is not None:
            return Response(data={"error": err}, status=status.HTTP_400_BAD_REQUEST)

        return Response(
            data={"message": f"Book({book_pk}) Returned By {member_pk} Successfully"},
            status=status.HTTP_200_OK,
        )

    # - Reserve a book and move to reservation queue when a particular book has no copies available in case of a ‘checkout’ request.
    @action(methods=["PUT"], detail=False)
    def reserve(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        book_pk = serializer.data.get("book_id")
        member_pk = serializer.data.get("member_id")

        err = Circulation.reserve_book(book_id=book_pk, member_id=member_pk)
        if err is not None:
            return Response(data={"error": err}, status=status.HTTP_400_BAD_REQUEST)

        return Response(
            data={"message": f"Book({book_pk}) Reserved By {member_pk} Successfully"},
            status=status.HTTP_200_OK,
        )

    @action(methods=["PUT"], detail=False)
    def fulfill(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        book_pk = serializer.data.get("book_id")
        member_pk = serializer.data.get("member_id")

        err = Circulation.fulfill_book(
            book_id=book_pk, member_id=member_pk, circulation_id=None
        )
        if err is not None:
            return Response(data={"error": err}, status=status.HTTP_400_BAD_REQUEST)

        return Response(
            data={"message": f"Book({book_pk}) Fulfilled For {member_pk} Successfully"},
            status=status.HTTP_200_OK,
        )

    @action(methods=["POST"], detail=False)
    def handle_event(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        book_pk = serializer.data.get("book_id")
        member_pk = serializer.data.get("member_id")
        event_type = serializer.data.get("eventtype")
        datetime = parser.parse(serializer.data.get("date"))

        if event_type == "checkout":
            Circulation.checkout_book(
                book_id=book_pk, member_id=member_pk, datetime=datetime
            )

        elif event_type == "return":
            Circulation.return_book(
                book_id=book_pk, member_id=member_pk, datetime=datetime
            )

        elif event_type == "reserve":
            Circulation.reserve_book(
                book_id=book_pk, member_id=member_pk, datetime=datetime
            )

        elif event_type == "fulfill":
            Circulation.fulfill_book(
                book_id=book_pk, member_id=member_pk, datetime=datetime
            )

        return Response(status=status.HTTP_200_OK)
