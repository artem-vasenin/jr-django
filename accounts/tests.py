# import pytest
# from accounts.models import Profile
#
# @pytest.mark.django_db
# def test_product_creation():
#     category = Category.objects.create(name="Pytest Cat")
#     product = Product.objects.create(
#         name="Pytest",
#         unit="1l",
#         price=100,
#         category=category,
#     )
#     assert product.name == "Pytest"
#     assert Product.objects.count() == 1