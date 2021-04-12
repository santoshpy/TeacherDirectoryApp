import tempfile
from pathlib import Path

from django.conf import settings
from django.core.files import File
from import_export import resources
from import_export.fields import Field
from import_export.widgets import ManyToManyWidget

from apps.directory.models import Subject, Teacher


class ManyToManyWidgetWithCreation(ManyToManyWidget):
    def __init__(
        self, model, seperator=None, field=None, create=False, *args, **kwargs
    ):
        self.create = create
        super().__init__(model, separator=seperator, field=field, *args, **kwargs)

    def clean(self, value, row=None, *args, **kwargs):
        if self.create:
            for val in value.strip().split(","):
                instance, new = self.model.objects.get_or_create(
                    **{self.field: val.strip().lower()}
                )

        return super().clean(value, row=row, *args, **kwargs)


class TeacherResource(resources.ModelResource):
    subjects = Field(
        attribute="subjects",
        column_name="subjects",
        widget=ManyToManyWidgetWithCreation(model=Subject, field="name", create=True),
    )

    class Meta:
        model = Teacher
        import_id_fields = ("email_address",)
        fields = (
            "first_name",
            "last_name",
            "profile_picture",
            "email_address",
            "phone_number",
            "room_number",
            "subjects",
        )
        export_order = (
            "first_name",
            "last_name",
            "profile_picture",
            "email_address",
            "phone_number",
            "room_number",
            "subjects",
        )

    def before_import_row(self, row, row_number=None, **kwargs):
        upload_images = kwargs.get('upload_images')
        profile_image = row.get("profile_picture")
        if upload_images and profile_image in upload_images:
            file_obj = upload_images.get(profile_image)
            profile_pic = File(file_obj)
            row["profile_picture"] = profile_pic
        else:
            row["profile_picture"] = None
