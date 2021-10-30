from django.core import validators
from django.db import models

class Customer(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.CharField(max_length=255)
    age = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Product(models.Model):
    CATEGORY = (
            ('daily', '日用品'),
            ('child', '子供向け'),
            ('sports', 'スポーツ'),
            )

    name = models.CharField(max_length=100)
    price = models.FloatField()
    category = models.CharField(max_length=50, choices=CATEGORY)
    description = models.CharField(max_length=2000, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.name


class Order(models.Model):
    STATUS = (
            ('processing', '処理中'),
            ('delivering', '配送中'),
            ('canceled', '配送中止'),
            ('Done', '配送済'),
            )

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=STATUS)

from django.core import validators
from django.db import models

class Author(models.Model):
    """著者"""
    name = models.CharField(max_length=255)
    add_name = models.CharField(max_length=255, blank=True, verbose_name='additional name')
    memo = models.TextField(blank=True)
    books = models.ManyToManyField('Book', related_name='books', blank=True)
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["name", "add_name"],
                name="author_unique"
            ),
        ]
    def __str__(self):
        return self.name

class Book(models.Model):
    """書籍"""
    title = models.CharField(max_length=255)
    authors = models.ManyToManyField(Author, related_name='authors')
    pub_date = models.DateField(null=True, blank=True, verbose_name='date published')
    publisher = models.CharField(max_length=255, blank=True)
    series = models.CharField(max_length=255, blank=True)
    price = models.IntegerField(null=True, blank=True)
    evaluation = models.IntegerField(null=True, blank=True, validators=[validators.MinValueValidator(0), validators.MaxValueValidator(100)])
    memo = models.TextField(blank=True)
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["title", "publisher", "series"],
                name="book_unique"
            ),
        ]
    def __str__(self):
        return self.title