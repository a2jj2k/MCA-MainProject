from django.db import models
from django.contrib.auth.models import User
from PIL import Image

class Department(models.Model):
    dept_name = models.CharField(max_length=100)
    dept_full_name = models.CharField(max_length=100)

    def __str__(self):
        return self.dept_name

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dept_id = models.ForeignKey(Department, on_delete=models.CASCADE)
    is_student = models.BooleanField(default=False)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, **kwargs):
        super().save()

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)