from typing import List

from ninja import NinjaAPI, Schema

from src.crm.models import Message

api = NinjaAPI(urls_namespace="crm_api", title="API Кабінету Мешканця")


class DeleteMessagesIn(Schema):
    message_ids: List[int]


@api.post("/messages/delete-many")
def cabinet_message_delete_api(request, payload: DeleteMessagesIn):
    if not request.user.is_authenticated:
        return {"status": "error", "message": "Не авторизовано"}

    if payload.message_ids:
        Message.objects.filter(
            id__in=payload.message_ids, recipient=request.user
        ).delete()

    return {"status": "success"}
