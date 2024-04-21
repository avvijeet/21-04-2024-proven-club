from book_reservations.models import Circulation
from book_reservations.serializers import BookViewSetSerializer
from dateutil.parser import parse
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

# Create your views here.
# API Endpoint(s) for handling book checkouts, returns, reservations and reservation fulfillments


class BooksViewSet(ViewSet):
    # - Check out/Issue a book when a copy is available in case of a ‘checkout’ request
    serializer_class = BookViewSetSerializer
    parser_classes = [JSONParser]

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

        err = Circulation.fulfill_book(book_id=book_pk, member_id=member_pk)
        if err is not None:
            return Response(data={"error": err}, status=status.HTTP_400_BAD_REQUEST)

        return Response(
            data={"message": f"Book({book_pk}) Fulfilled For {member_pk} Successfully"},
            status=status.HTTP_200_OK,
        )

    @action(methods=["POST"], detail=False)
    def handle_event(self, request):
        book_pk = request.data.get("book_id")
        member_pk = request.data.get("member_id")
        event_type = request.data.get("eventtype")
        datetime = parse(timestr=request.data["date"])

        err = None
        if event_type == "checkout":
            err = Circulation.checkout_book(
                book_id=book_pk, member_id=member_pk, datetime=datetime
            )

        elif event_type == "return":
            err = Circulation.return_book(
                book_id=book_pk, member_id=member_pk, datetime=datetime
            )

        elif event_type == "reserve":
            err = Circulation.reserve_book(
                book_id=book_pk, member_id=member_pk, datetime=datetime
            )

        elif event_type == "fulfill":
            err = Circulation.fulfill_book(
                book_id=book_pk, member_id=member_pk, datetime=datetime
            )

        if err is not None:
            return Response(data={"error": err}, status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_200_OK)
