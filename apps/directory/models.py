from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from apps.directory.utils import get_upload_path


class TimestampModel(models.Model):
    """
    Abstract Model for timestamp.
    """

    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)

    class Meta:
        abstract = True


class Subject(TimestampModel):
    """
    Store subject information
    """

    name = models.CharField(max_length=50, primary_key=True)

    class Meta:
        verbose_name = _("subject")
        verbose_name_plural = _("subjects")

    def __str__(self):
        return self.name

    def clean(self, *args, **kwargs) -> None:
        self.name = self.name.lower()
        return super().clean(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("subject_detail", kwargs={"pk": self.pk})


class Teacher(TimestampModel):
    """
    To store teacher information
    """

    email_address = models.EmailField(
        _("email_address"), max_length=50, primary_key=True
    )
    first_name = models.CharField(_("first name"), max_length=150)
    last_name = models.CharField(_("last name"), max_length=150)
    phone_number = models.CharField(_("phone number"), max_length=15)
    profile_picture = models.ImageField(
        _("profile picture"),
        max_length=255,
        upload_to=get_upload_path,
        null=True,
        blank=True,
    )
    room_number = models.CharField(_("room number"), max_length=5)
    subjects = models.ManyToManyField(Subject)

    class Meta:
        verbose_name = _("teacher")
        verbose_name_plural = _("teachers")

    def __str__(self):
        return self.email_address

    def get_absolute_url(self):
        return reverse("teacher_detail", kwargs={"pk": self.id})

    def get_first_letter_of_last_name(self):
        return self.last_name[0] if self.last_name else ""
