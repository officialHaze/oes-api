from rest_framework.response import Response
from rest_framework.decorators import api_view
from collections import deque
import requests
import requests.exceptions


@api_view(["POST"])
def scrap_email(req, *args, **kwargs):
    url = req.data.get("url")

    return Response({"detail": "hi!"})
