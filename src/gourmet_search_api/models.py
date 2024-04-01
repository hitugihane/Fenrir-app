from django.db import models
from django.contrib.auth.models import User

class FavoriteShop(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    shop_id = models.CharField(max_length=255)

    def __str__(self):
        return f"Favorite shop ({self.shop_id}) for user {self.user.username}"
