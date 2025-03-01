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


class Product(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    # slug = models.SlugField(max_length=250, unique=True, blank=True)
    brand = models.CharField(max_length=255)
    specification = models.TextField()
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="products_created",
        db_column="created_by"  # Remove null=True, blank=True
    )

    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name="products_updated",
        db_column="updated_by",
        null=True,
        blank=True
    )
    # def save(self, *args, **kwargs):
    #     """Automatically generate a unique slug from the name."""
    #     if not self.slug:  # If slug is empty, generate from name
    #         base_slug = slugify(self.name)
    #         slug = base_slug
    #         count = 1
    #         while Product.objects.filter(slug=slug).exists():
    #             slug = f"{base_slug}-{count}"
    #             count += 1
    #         self.slug = slug
    #     super().save(*args, **kwargs)

    def default_image(self):
        """Returns all images related to this product."""
        return self.product_images.all().first()
    
    def images(self):
        """Returns all images related to this product."""
        return self.product_images.all()  

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_images")
    image = CloudinaryField('product_images', null=True, blank=True)

    def __str__(self):
        return f"Image for {self.product.name}"
