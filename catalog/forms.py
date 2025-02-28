from django import forms
from .models import Product, ProductImage, Category

class ProductForm(forms.ModelForm):
    images = forms.FileField(
        widget=forms.ClearableFileInput(
            attrs={
                "multiple": False,  # Allow multiple images
                "class": "custom-file-input d-none",  # Hide default input
                "id": "imageUpload"
            }
        ),
        required=True,
    )

    class Meta:
        model = Product
        fields = ['name', 'category', 'brand', 'specification', 'description', 'images']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Product Name'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'brand': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Product Brand'}),
            'specification': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Product Specification'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Product Description'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.all()
