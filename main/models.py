from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    description = models.TextField()
    thumbnail = models.URLField()
    category = models.CharField(max_length=100)
    is_featured = models.BooleanField(default=False)

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='products'  
    )

    # Nampilin siapa pemilik barangnya
    def __str__(self):
        return f"{self.name} - {self.category} ({self.owner.username})"

    
