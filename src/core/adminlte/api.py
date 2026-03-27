from datetime import date
from typing import List, Optional

from django.shortcuts import get_object_or_404
from ninja import NinjaAPI, Schema

from src.crm.models import (
    CounterReadings,
    PersonalAccount,
    Receipt,
    Service,
    TariffService,
)
from src.house.models import Apartment, Floor, Section
from src.user.models import User

api = NinjaAPI()


class ServiceUnitOut(Schema):
    unit_name: str
    currency: str


class RoleOut(Schema):
    role_name: str


class ItemOut(Schema):
    id: int
    name: str


class SectionsFloorsOut(Schema):
    sections: List[ItemOut]
    floors: List[ItemOut]


class ApartmentInfoOut(Schema):
    owner_name: str
    owner_phone: str
    account_number: str
    tariff_id: Optional[int] = None


class ReadingOut(Schema):
    service_id: int
    quantity: float


class TariffServiceOut(Schema):
    service_id: int
    price: float


class DeleteReceiptsIn(Schema):
    ids: List[int]


class ListsByHouseOut(Schema):
    sections: str
    flats: str


class AccountOwnerOut(Schema):
    owner_name: str


@api.get("/service-unit", response=ServiceUnitOut)
def get_service_unit(request, service_id: int):
    service = (
        Service.objects.filter(id=service_id)
        .select_related("measure", "currency")
        .first()
    )
    if service:
        return {
            "unit_name": service.measure.name if service.measure else "",
            "currency": service.currency.name if service.currency else "грн",
        }
    return {"unit_name": "", "currency": ""}


@api.get("/user-role", response=RoleOut)
def get_user_role(request, user_id: int):
    user = get_object_or_404(User.objects.select_related("role"), pk=user_id)
    return {"role_name": user.role.name if user.role else "Без ролі"}


@api.get("/sections-and-floors", response=SectionsFloorsOut)
def get_sections_and_floors(request, house_id: int):
    sections = list(Section.objects.filter(house_id=house_id).values("id", "name"))
    floors = list(Floor.objects.filter(house_id=house_id).values("id", "name"))
    return {"sections": sections, "floors": floors}


@api.get("/apartment-info", response=ApartmentInfoOut)
def get_apartment_info(request, apartment_id: int):
    apt = get_object_or_404(Apartment.objects.select_related("owner"), id=apartment_id)

    owner_name = (
        f"{apt.owner.first_name} {apt.owner.last_name}" if apt.owner else "Не обрано"
    )
    owner_phone = getattr(apt.owner, "phone_number", None) if apt.owner else None

    account = PersonalAccount.objects.filter(apartment=apt).first()

    return {
        "owner_name": owner_name,
        "owner_phone": owner_phone or "Немає телефону",
        "account_number": account.number if account else "Рахунок не створено",
        "tariff_id": getattr(apt, "tariff_id", None),
    }


@api.get("/counter-readings", response=List[ReadingOut])
def get_counter_readings(request, apartment_id: int, date_from: date, date_to: date):
    readings = CounterReadings.objects.filter(
        apartment_id=apartment_id, date__gte=date_from, date__lte=date_to
    ).select_related("service")

    return [{"service_id": r.service.id, "quantity": r.meter} for r in readings]


@api.get("/tariff-services", response=List[TariffServiceOut])
def get_tariff_services(request, tariff_id: int):
    services = TariffService.objects.filter(tariff_id=tariff_id)
    return [
        {"service_id": ts.service_id, "price": ts.price_per_unit} for ts in services
    ]


@api.post("/receipts/delete-many")
def receipt_delete_many(request, payload: DeleteReceiptsIn):
    if payload.ids:
        Receipt.objects.filter(id__in=payload.ids).delete()
        return {"status": "success"}
    return {"status": "error"}


@api.get("/lists-by-house", response=ListsByHouseOut)
def get_lists_by_house(
    request, house_id: Optional[int] = None, section_id: Optional[int] = None
):
    sections_html = '<option value="">Оберіть...</option>'
    flats_html = '<option value="">Оберіть...</option>'

    if house_id:
        sections = Section.objects.filter(house_id=house_id)
        for section in sections:
            sections_html += f'<option value="{section.id}">{section.name}</option>'

        flats = Apartment.objects.filter(house_id=house_id)

        if section_id:
            flats = flats.filter(section_id=section_id)

        for flat in flats:
            flats_html += f'<option value="{flat.id}">{flat.number}</option>'

    return {"sections": sections_html, "flats": flats_html}


@api.get("/account-owner", response=AccountOwnerOut)
def get_account_owner(request, account_id: int):

    try:
        account = PersonalAccount.objects.get(id=account_id)
        apt = getattr(account, "apartment", None)

        if not apt and hasattr(account, "apartment_set"):
            apt = account.apartment_set.first()

        if apt and apt.owner:
            owner_name = f"{apt.owner.first_name} {apt.owner.last_name}"
            return {"owner_name": owner_name}

    except PersonalAccount.DoesNotExist:
        pass

    return {"owner_name": "(не задано)"}
