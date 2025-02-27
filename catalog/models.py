from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from cloudinary.models import CloudinaryField

class Category(models.Model):
    """This is the Category Django Model for the pim_category database table."""

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=250, unique=True, blank=True)
    image_url = CloudinaryField('category', null=True, blank=True)
    include_in_home = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='category_created',
        db_column='created_by',
        null=True,
        blank=True
    )
    updated = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='category_updated',
        db_column='updated_by',
        null=True,
        blank=True
    )

    def save(self, *args, **kwargs):
        """Automatically generate a unique slug from the name."""
        if not self.slug:  # If slug is empty, generate from name
            base_slug = slugify(self.name)
            slug = base_slug
            count = 1
            while Category.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{count}"
                count += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.name)

    class Meta:
        db_table = 'category'
