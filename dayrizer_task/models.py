from enum import Enum

from django.db import models


# Define an enum called FizzBuzzStatus that represents the possible FizzBuzz values.
class FizzBuzzStatus(Enum):
    Null = "Null"
    Fizz = "Fizz"
    Buzz = "Buzz"
    Fizzbuzz = "FizzBuzz"


# Define a model called FizzBuzz
class FizzBuzz(models.Model):
    class Meta:
        app_label = "dayrizer_task"

    id = models.AutoField(primary_key=True)
    number = models.PositiveIntegerField(unique=True)
    fizzbuzz = models.CharField(
        max_length=10, choices=[(tag, tag.value) for tag in FizzBuzzStatus]
    )
    placeholder_post = models.JSONField(default=dict, blank=True)


def determine_fizzbuzz(number) -> FizzBuzzStatus:
    """
     It takes a number as input and returns a FizzBuzzStatus.
    :param number: the input number which should be determined if is divisible
    by 15, 3, or 5 or not
    :return:
    """
    if number % 3 == 0 and number % 5 == 0:
        return FizzBuzzStatus.Fizzbuzz
    elif number % 3 == 0:
        return FizzBuzzStatus.Fizz
    elif number % 5 == 0:
        return FizzBuzzStatus.Buzz
    return FizzBuzzStatus.Null
