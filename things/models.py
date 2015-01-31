from uuid import uuid4
import os

from django.db import models


def get_image_path(instance, filename):
    filename = os.path.basename(filename)
    return os.path.join('things/pictures', str(uuid4())[:8], filename)


class Taker(models.Model):
    name = models.CharField(max_length=255)
    token = models.CharField(max_length=100, default=uuid4, unique=True)

    def __unicode__(self):
        return self.name


class Thing(models.Model):
    name = models.CharField(max_length=255)
    picture = models.ImageField(upload_to=get_image_path, blank=True)
    taken_by = models.ForeignKey(Taker, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def give_to(self, taker):
        if self.taken_by:
            raise ValueError("Cannot give the same thing twice")
        self.taken_by = taker
        self.save()

    def give_back(self, taker):
        if self.taken_by == taker:
            self.taken_by = None
            self.save()

    def __unicode__(self):
        return self.name
