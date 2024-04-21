import json

from django.test import TestCase
from rest_framework.test import APIClient


class TestBook(TestCase):
    fixtures = ["book_reservations/test_data.json.gz"]
    api_client = APIClient()

    TEST_DATA = [
        {
            "eventtype": "checkout",
            "book_id": 1000,
            "member_id": 2003,
            "date": "2023-05-10",
        },
        {
            "eventtype": "checkout",
            "book_id": 1000,
            "member_id": 2013,
            "date": "2023-05-11",
        },
        {
            "eventtype": "checkout",
            "book_id": 1000,
            "member_id": 2000,
            "date": "2023-05-18",
        },
        {
            "eventtype": "return",
            "book_id": 1000,
            "member_id": 2013,
            "date": "2023-05-22",
        },
        {
            "eventtype": "checkout",
            "book_id": 1002,
            "member_id": 2006,
            "date": "2023-05-02",
        },
        {
            "eventtype": "checkout",
            "book_id": 1002,
            "member_id": 2018,
            "date": "2023-05-04",
        },
        {
            "eventtype": "checkout",
            "book_id": 1002,
            "member_id": 2010,
            "date": "2023-05-05",
        },
        {
            "eventtype": "return",
            "book_id": 1002,
            "member_id": 2006,
            "date": "2023-05-08",
        },
        {
            "eventtype": "return",
            "book_id": 1002,
            "member_id": 2018,
            "date": "2023-05-18",
        },
        {
            "eventtype": "checkout",
            "book_id": 1011,
            "member_id": 2019,
            "date": "2023-05-08",
        },
    ]

    FAILING_DATA = [
        {"eventtype": "fulfill", "book_id": 1000, "date": "2023-05-23"},
        {"eventtype": "fulfill", "book_id": 1002, "date": "2023-05-19"},
        {"eventtype": "fulfill", "book_id": 1002, "date": "2023-05-09"},
        {"eventtype": "fulfill", "book_id": 1000, "date": "2023-05-23"},
    ]

    def test_api(self):
        url_path = "/books/handle_event/"

        for data in self.TEST_DATA:
            with self.subTest(data=data):
                resp = self.api_client.post(
                    path=url_path,
                    data=json.dumps(data),
                    content_type="application/json",
                )
                self.assertEqual(resp.status_code, 200, f"{resp.content = }")

    def test_failure(self):
        """Assumption: Book Fulfill requires member"""
        url_path = "/books/handle_event/"

        for data in self.FAILING_DATA:
            with self.subTest(data=data):
                resp = self.api_client.post(
                    path=url_path,
                    data=json.dumps(data),
                    content_type="application/json",
                )
                self.assertEqual(resp.status_code, 400, f"{resp.content = }")
