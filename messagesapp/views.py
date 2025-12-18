import json

from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt

from .models import Message

# Demo-only password for POST requests (not real security)
DEMO_POST_PASSWORD = "letmein"


@csrf_exempt
def messages(request):
    if request.method == "GET":
        items = list(Message.objects.order_by("-id").values_list("text", flat=True))
        return JsonResponse({"messages": items})

    if request.method == "POST":
        try:
            payload = json.loads(request.body.decode("utf-8") or "{}")
        except json.JSONDecodeError:
            return HttpResponseBadRequest("Invalid JSON body")

        # Demo password check
        if payload.get("password") != DEMO_POST_PASSWORD:
            return JsonResponse({"error": "invalid password"}, status=403)

        msg = (payload.get("message") or "").strip()
        if not msg:
            return HttpResponseBadRequest("'message' is required")

        Message.objects.create(text=msg)
        return JsonResponse({"status": "ok"}, status=201)

    return JsonResponse({"detail": "Method not allowed"}, status=405)
