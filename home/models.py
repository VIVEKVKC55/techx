from django.db import models
from cloudinary.models import CloudinaryField

class PromotionBanner(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    subtitle = models.CharField(max_length=500, blank=True, null=True)
    image = CloudinaryField('promotion_banner', null=True, blank=True)
    link = models.URLField(max_length=500, blank=True, null=True)
    is_active = models.BooleanField(default=True)  # Manually activate/deactivate

    def __str__(self):
        return self.title if self.title else "Promotion Banner"

    class Meta:
        db_table = 'promotion_banner'
