from django.db import DefaultConnectionProxy, models
from django.db.models.fields import DateField
from login_registeration_app.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.
class Music(models.Model):
    song_name=models.CharField(max_length=45)
    writer=models.CharField(max_length=45)
    composer = models.CharField(max_length=45)
    duration = models.CharField(max_length=45)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    lyrics=models.TextField()
    music = models.FileField(upload_to='audio/', blank=True)
    uploaded_by=models.ForeignKey(User,related_name="songs",on_delete=models.CASCADE)
    

class Rate(models.Model):
    music=models.ForeignKey(Music,related_name="rates",on_delete=models.CASCADE)
    user=models.ForeignKey(User,related_name="rates",on_delete=models.CASCADE)
    score = models.IntegerField(default=0,
        validators=[
            MaxValueValidator(5),
            MinValueValidator(0),
        ]
    )


