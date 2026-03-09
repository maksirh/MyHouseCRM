from django.apps import AppConfig
from django.db.models.signals import post_migrate


def create_default_roles(sender, **kwargs):
    from src.user.models import Roles

    default_roles = ["Директор", "Керівник", "Бухгалтер", "Сантехнік", "Електрик"]

    for role_name in default_roles:
        if role_name == "Сантехнік" or role_name == "Електрик":
            Roles.objects.get_or_create(name=role_name, is_master=True)
        Roles.objects.get_or_create(name=role_name)


class AdminlteConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "src.core.adminlte"

    def ready(self):
        post_migrate.connect(create_default_roles, sender=self)
