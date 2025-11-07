import pytest
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile

from products.models import Product, Category, Review


@pytest.mark.django_db
def test_product_creation():
    """ Проверка создания товара """
    category = Category.objects.create(name='Pytest Cat')
    Product.objects.create(
        name='Pytest First',
        unit='1l',
        price=100,
        category=category,
    )
    product = Product.objects.create(
        name='Pytest Second',
        unit='1l',
        price=200,
        category=category,
    )

    assert category.name == 'Pytest Cat'
    assert Category.objects.count() == 1
    assert product.name == 'Pytest Second'
    assert Product.objects.count() == 2


@pytest.mark.django_db
def test_category_edit():
    """ Проверка редактирования категории """
    Category.objects.create(name='Pytest New')

    obj = Category.objects.get(name='Pytest New')
    obj.name = 'Pytest Edited'
    obj.save(update_fields=['name'])

    assert Category.objects.count() == 1
    assert obj.name == 'Pytest Edited'


@pytest.mark.django_db
def test_product_edit():
    """ Проверка редактирования товара """
    category = Category.objects.create(name='Pytest Cat')
    Product.objects.create(
        name='Product First',
        unit='1l',
        price=100,
        category=category,
    )
    product = Product.objects.get(name='Product First')
    product.name = 'One'
    product.price = 220
    product.save(update_fields=['name', 'price'])

    assert Product.objects.count() == 1
    assert product.name == 'One'
    assert product.price == 220


@pytest.mark.django_db
def test_product_add_comment():
    """ Проверка создания комментария к товару """
    user = User.objects.create_user(username='TestUser', email='test@mail.ru')
    category = Category.objects.create(name='Pytest Cat')
    product = Product.objects.create(
        name='Product First',
        unit='1l',
        price=100,
        category=category,
    )
    Review.objects.create(
        user=user,
        product=product,
        rating=3,
        comment='Some comment'
    )
    f_product = Product.objects.get(name='Product First')
    reviews = f_product.reviews.all()

    assert reviews.count() == 1
    assert reviews[0].rating == 3
    assert reviews[0].comment == 'Some comment'


class CatalogViewTest(TestCase):
    def test_catalog_status_code(self):
        """ Проверка доступности страницы каталога """
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_details_status_code(self):
        """ Проверка доступности страницы товара """
        category = Category.objects.create(name='Pytest Cat')
        image = SimpleUploadedFile(
            name='test_image.jpg',
            content=b'\x00\x01\x02',
            content_type='image/jpeg'
        )
        Product.objects.create(
            name='One',
            slug='one',
            unit='1l',
            price=100,
            category=category,
            image=image,
        )
        response = self.client.get(reverse('products:product', kwargs={'slug': 'one'}))
        self.assertEqual(response.status_code, 200)
