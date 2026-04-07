from src.house.models import Apartment


def cabinet_menu_data(request):
    if request.user.is_authenticated and "/cabinet/" in request.path:
        user_flats = Apartment.objects.filter(owner=request.user).select_related(
            "house"
        )

        return {
            "user_flats": user_flats,
        }

    return {}
