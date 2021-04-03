from datetime import datetime
from pathlib import Path


def get_upload_path(instance, filename):
    folder_name = datetime.now().date().strftime("%Y/%m/%d")
    return Path("profile/picture/") / folder_name / filename
