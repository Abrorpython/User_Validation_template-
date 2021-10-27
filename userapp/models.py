from django.core.files import File
from django.db import models
from django.contrib.auth.models import AbstractUser
from PIL import Image
from io import BytesIO
import os, datetime, random
from django.conf import settings
from pathlib import Path

def upload_file_name(instance, filname):
    _, ext = os.path.splitext(filname)

    return "profile/{}/{:%Y-%m-%d-%H-%M-%S}-{}{}".format(
        datetime.datetime.now().strftime("%Y%m"),
        datetime.datetime.now(), random.randint(1000, 999), ext)


class User(AbstractUser):
    photo = models.ImageField(upload_to=upload_file_name)

    def save(self, *args, **kwargs):
        if not self.image.closed:
            img = Image.open(self.image)
            img.thumbnail((100, 100), Image.ANTIALIAS)

            tmp = BytesIO()
            img.save(tmp, 'PNG')
            self.image = File(tmp, 't.png')

        return super().save(**kwargs)

    def save(self, *args, **kwargs):
        super(*args, **kwargs)


    @property
    def image_url(self):
        if self.image:
            return os.path.join(settings.MEDIA_URL, str(self.image))

        return Path(settings.STATIC_URL).joinpath('main/nophoto.png')
