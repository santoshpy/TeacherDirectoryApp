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

        return super().clean(value, row=None, *args, **kwargs)


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
        image_path = row["profile_picture"]
        path = Path(image_path)
        if not path.exists():
            image_name = image_path.split("/")[-1]
            image_path = settings.BASE_DIR / "teachers" / image_name

        if image_path.exists():
            tmp_file = tempfile.NamedTemporaryFile(
                delete=True, dir=f"{settings.MEDIA_ROOT}"
            )
            with open(image_path, "rb") as f:
                tmp_file.write(f.read())
            tmp_file.flush()
            row["profile_picture"] = File(tmp_file, image_name)
        else:
            row["profile_picture"] = None
