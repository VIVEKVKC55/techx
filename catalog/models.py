from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField


class Category(models.Model):
    """This is the Category Django Model for the pim_category database table."""

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=250)
    include_in_home = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    image_url = CloudinaryField('category', null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,  # Sets upcreated_by to NULL instead of deleting the record
        related_name='category_created',
        db_column='created_by',
        null=True,
        blank=True  # Allows empty values in forms
    )
    updated = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,  # Sets updated_by to NULL instead of deleting the record
        related_name='category_updated',
        db_column='updated_by',
        null=True,
        blank=True  # Allows empty values in forms
    )

    def __str__(self):
        """Override string method and return custom data.
        Returns:
            str: It returns category name
        """
        return str(self.name)

    class Meta:
        """Provide database table name explicitly."""
        db_table = 'category'