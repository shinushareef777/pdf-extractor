from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound
from django.http import JsonResponse


def error_404(request, exception):
    message = f"404 Not found: {exception}"

    response = JsonResponse(data={'error':message, 'status_code':404})
    return response

def error_500(request):
    message = "Internal server error"

    response = JsonResponse(data={'error':message, 'status_code':500})
    return response

def error_400(request, exception):
    message = f"Bad request: {exception}"

    response = JsonResponse(data={'error':message, 'status_code':400})
    return response