from django.db import models

from users.models import User

class Article(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    images = models.ImageField(upload_to='articles/', blank=True, null=True)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='articles')
    created_at = models.DateTimeField(auto_now_add=True)

    def whatsapp_link(self):
        if self.seller.whatsapp_number:
            return f"https://wa.me/{self.seller.whatsapp_number}"
        return None

    def __str__(self):
        return self.title
