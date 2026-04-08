from typing import List

from ninja import NinjaAPI, Schema

from src.crm.models import CallMaster, Message

api = NinjaAPI(urls_namespace="crm_api", title="API Кабінету Мешканця")


class DeleteMessagesIn(Schema):
    message_ids: List[int]


class DeleteCallIn(Schema):
    call_id: int


@api.post("/messages/delete-many")
def cabinet_message_delete_api(request, payload: DeleteMessagesIn):
    if not request.user.is_authenticated:
        return {"status": "error", "message": "Не авторизовано"}

    if payload.message_ids:
        Message.objects.filter(
            id__in=payload.message_ids, recipient=request.user
        ).delete()

    return {"status": "success"}


@api.post("/calls/delete")
def cabinet_call_delete_api(request, payload: DeleteCallIn):
    if not request.user.is_authenticated:
        return {"status": "error", "message": "Не авторизовано"}

    deleted, _ = CallMaster.objects.filter(
        id=payload.call_id, apartment__owner=request.user
    ).delete()

    if deleted:
        return {"status": "success"}
    return {"status": "error", "message": "Заявка не знайдена"}
