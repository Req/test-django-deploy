from random import randint

from django.http import JsonResponse


def random_number(request):
    """Return a JSON payload with a random number between 1 and 10."""
    return JsonResponse({"number": randint(1, 10)})
