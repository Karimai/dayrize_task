import json
from unittest.mock import patch

import requests_mock
from django.conf import settings
from django.test import RequestFactory, TestCase

from dayrizer_task.views import fetch_post, fizzbuzz_detail, fizzbuzz_list

settings.DEBUG = True


class FizzBuzzDetailTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_fizzbuzz_detail(self):
        request = self.factory.get("/fizzbuzz_detail/?number=15")
        response = fizzbuzz_detail(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            json.loads(response.content),
            {
                "number": 15,
                "fizzbuzz": "FizzBuzz",
                "placeholder_post": {
                    "title": "eveniet quod temporibus",
                    "body": "reprehenderit quos placeat\n"
                    "velit minima officia dolores impedit repudiandae molestiae nam\n"
                    "voluptas recusandae quis delectus\n"
                    "officiis harum fugiat vitae",
                },
            },
        )


class FizzBuzzListTestCase(TestCase):
    maxDiff = None

    def setUp(self):
        self.factory = RequestFactory()

    def test_fizzbuzz_list(self):
        request = self.factory.get("/fizzbuzz_list/?from_number=17&to_number=19")
        response = fizzbuzz_list(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            json.loads(response.content),
            [
                {
                    "number": 17,
                    "fizzbuzz": "Null",
                    "placeholder_post": {
                        "title": "fugit voluptas sed molestias voluptatem provident",
                        "body": "eos voluptas et aut odit natus earum\n"
                        "aspernatur fuga molestiae ullam\n"
                        "deserunt ratione qui eos\n"
                        "qui nihil ratione nemo velit ut aut id quo",
                    },
                },
                {
                    "number": 18,
                    "fizzbuzz": "Fizz",
                    "placeholder_post": {
                        "title": "voluptate et itaque vero tempora molestiae",
                        "body": "eveniet quo quis\nlaborum totam consequatur non dolor\n"
                        "ut et est repudiandae\nest voluptatem vel debitis et magnam",
                    },
                },
            ],
        )


class FetchPostTestCase(TestCase):
    @patch("dayrizer_task.views", fetch_post)
    def test_fetch_post_success(self):
        number = 12
        with requests_mock.Mocker() as mock:
            mock.get(
                f"https://jsonplaceholder.typicode.com/posts/{number}",
                status_code=200,
                json={"title": "test title", "body": "test body"},
            )
            title, body = fetch_post(number)
            self.assertEqual(title, "test title")
            self.assertEqual(body, "test body")

    @patch("dayrizer_task.views", fetch_post)
    def test_fetch_post_failure(self):
        number = 12
        with requests_mock.Mocker() as mock:
            mock.get(
                f"https://jsonplaceholder.typicode.com/posts/{number}", status_code=404
            )
            title, body = fetch_post(number)
            self.assertEqual(title, "")
            self.assertEqual(body, "")
