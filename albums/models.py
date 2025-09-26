from django.db import models

class Album(models.Model):
    title = models.CharField(max_length=200)
    artist = models.CharField(max_length=200)
    year = models.PositiveIntegerField()
    genre = models.CharField(max_length=100, blank=True)
    tracks = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.title} — {self.artist} ({self.year})"
