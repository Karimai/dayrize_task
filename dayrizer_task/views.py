import json
import logging

import requests
from django.core.cache import cache
from django.http import HttpResponse, JsonResponse

from . import settings
from .models import FizzBuzz, determine_fizzbuzz

logging.getLogger().setLevel(logging.INFO)


settings.DEBUG = False


def index(request):
    endpoints = [
        "list of API endpoints:",
        "1) fizzbuzz_list/?from_number=X&to_number=Y",
        "2) fizzbuzz_detail/?number=X",
        "3) get_fizzbuzzes",
    ]
    return HttpResponse("\n".join(endpoints))


def fetch_post(number):
    """
    It fetches a post from a remote API based on the given number, extracts its title
    and body, and stores them along with a fizzbuzz value in a database.
    If the post does not exist, empty strings are returned for the title and body.
    :param number: an integer.
    :return: return a tuple (title, body) which describes the placeholder status for
    the input number
    """
    response = requests.get(f"https://jsonplaceholder.typicode.com/posts/{number}")
    if response.status_code == 200:
        post = response.json()
        title = post.get("title", "")
        body = post.get("body", "")
    else:
        title = ""
        body = ""
    fizzbuzz_value = determine_fizzbuzz(number)
    FizzBuzz.objects.update_or_create(
        number=number,
        defaults={
            "fizzbuzz": fizzbuzz_value,
            "placeholder_post": json.dumps({"title": title, "body": body}),
        },
    )
    return title, body


def fizzbuzz_list(request):
    """
    It retrieves a list of fizzbuzz entities for the specified range of numbers using
    the from_number and to_number parameters in the request. If a fizzbuzz entity
    exists in the cache for a given number, it is retrieved from the cache, otherwise,
    it is fetched from the remote API using the fetch_post function.
    The fetched data is then stored in the cache and returned as a JSON response.
    :param request: a Django HttpRequest object that contains parameters.
    :return: Returns: a JSON response that contains a list of dictionaries representing
     fizzbuzz entities.
    GET http://example.com/api/fizzbuzz?from_number=1&to_number=5
    """
    from_number = int(request.GET.get("from_number", 10))
    to_number = int(request.GET.get("to_number", 20))
    fizzbuzz_entities = []
    for number in range(from_number, to_number):
        if cache.get(number):
            fizzbuzz_entity = cache.get(number)
        else:
            title, body = fetch_post(number)
            fizzbuzz_value = determine_fizzbuzz(number)
            fizzbuzz_entity = {
                "number": number,
                "fizzbuzz": fizzbuzz_value.value,
                "placeholder_post": {
                    "title": title,
                    "body": body,
                },
            }
        cache.set(number, fizzbuzz_entity)
        fizzbuzz_entities.append(fizzbuzz_entity)
    return JsonResponse(fizzbuzz_entities, safe=False)


def fizzbuzz_detail(request):
    """
    This function retrieves a fizzbuzz entity for the specified number using the number
    parameter in the request. If a fizzbuzz entity exists in the cache for the
    specified number, it is retrieved from the cache, otherwise,
    it is fetched from the remote API using the fetch_post function,
    and its fizzbuzz value is determined using the determine_fizzbuzz function.
    The fetched data is then stored in the cache and returned as a JSON response.
    The function also logs if the cache was hit or if the data was inserted to the cache.
    Example usage: GET http://example.com/api/fizzbuzz/detail?number=3
    :param request: a Django HttpRequest object that contains parameters.
    :return: a JSON response that contains a dictionary representing a fizzbuzz entity.
    """
    number = int(request.GET.get("number"))
    if cache.get(number):
        fizzbuzz_entity = cache.get(number)
        logging.info("Hit the cache")
    else:
        title, body = fetch_post(number)
        fizzbuzz_value = determine_fizzbuzz(number)
        fizzbuzz_entity = {
            "number": number,
            "fizzbuzz": fizzbuzz_value.value,
            "placeholder_post": {
                "title": title,
                "body": body,
            },
        }
        cache.set(number, fizzbuzz_entity)
        logging.info("insert to cache.")
    return JsonResponse(fizzbuzz_entity, safe=False)


def get_fizzbuzzes(request):
    """
    API endpoint that returns all FizzBuzz objects in the database.

    :param request : HttpRequest
    :return:
        A JSON response containing a list of dictionaries representing
        the FizzBuzz objects in the database.
        Each dictionary contains the following keys:
        - id: the unique identifier for the FizzBuzz object
        - number: the integer value for the FizzBuzz object
        - fizzbuzz: the FizzBuzz status for the object
        (either "Null", "Fizz", "Buzz", or "FizzBuzz")
        - placeholder_post: a JSON object representing any additional data associated
        with the FizzBuzz object.

    Examples
    --------
    >>> # Make a GET request to the API endpoint
    >>> response = client.get('/fizzbuzzes/')
    >>>
    >>> # Verify that the response status code is 200 OK
    >>> assert response.status_code == 200
    >>>
    >>> # Verify that the response contains the expected FizzBuzz data
    >>> assert len(response.json()['fizzbuzzes']) == FizzBuzz.objects.count()
    """
    fizzbuzzes = FizzBuzz.objects.all()
    data = {"fizzbuzzes": list(fizzbuzzes.values())}
    return JsonResponse(data)
