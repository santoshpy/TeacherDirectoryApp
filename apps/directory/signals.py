from django.core.exceptions import ValidationError
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

from apps.directory.models import Teacher


@receiver(m2m_changed, sender=Teacher.subjects.through)
def subject_changed(sender, **kwargs):
    total_subjects = kwargs["instance"].subjects.count()
    if total_subjects > 5 and kwargs.get("action") == "pre_add":
        raise ValidationError(
            _(
                f"A teacher can teach no more than 5 subject, found {total_subjects} subject"
            )
        )
