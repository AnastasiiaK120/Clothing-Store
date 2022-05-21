from django.db import models
from django.urls import reverse
from django.core.validators import MaxValueValidator, MinValueValidator

class Category(models.Model):
    name = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(max_length=150, unique=True)

    class Meta:
        ordering = ('-name',)
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(max_length=150, unique=True)
    image = models.ImageField(upload_to='products/')
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def get_average_review_score(self):
        average_score = 0
        if self.reviews.count() > 0:
            total_score = sum([review.rating for review in self.reviews.all()])
            average_score = total_score/self.reviews.count()
        return round(average_score, 1)



class Review(models.Model):
    product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE)
    author = models.CharField(max_length=50)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    text = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created',)
