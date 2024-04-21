from rest_framework import serializers


class BookViewSetSerializer(serializers.Serializer):
    book_id = serializers.IntegerField()
    member_id = serializers.IntegerField()
