from django.apps import AppConfig
from django.utils.module_loading import autodiscover_modules
from django.utils.translation import ugettext_lazy as _


class DirectoryConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.directory"
    verbose_name = _("directory")

    def ready(self):
        autodiscover_modules("signals")
