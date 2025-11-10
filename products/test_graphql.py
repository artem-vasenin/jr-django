# products/test_graphql.py
import pytest
from django.contrib.auth.models import User

from products.models import Product, Category


@pytest.fixture
def category(db):
    """Добавляем фикстуру с категорией товара"""
    return Category.objects.create(name="Test cat 1")


@pytest.fixture
def product(db, category):
    """Добавляем фикстуру с товаром"""
    return Product.objects.create(
        name='Test prod 1',
        unit='1l',
        price=100,
        category=category,
    )


@pytest.fixture
def superuser(db):
    """Добавляем суперюзера"""
    return User.objects.create_superuser(username="superuser", email="super@user.ru", password="12345")


@pytest.fixture
def user(db):
    """Добавляем обычного пользователя"""
    return User.objects.create_user(username="testuser", password="12345")


@pytest.fixture
def token(client, user):
    """Добавляем токен"""
    mutation = f"""
        mutation {{
          tokenAuth(username: "{user.username}", password: "12345") {{
            token
          }}
        }}
        """
    token_response = client.post("/graphql/", data={"query": mutation}, content_type="application/json")
    return token_response.json()["data"]["tokenAuth"]["token"]


@pytest.fixture
def super_token(client, superuser):
    """Добавляем токен админа"""
    mutation = f"""
        mutation {{
          tokenAuth(username: "{superuser.username}", password: "12345") {{
            token
          }}
        }}
        """
    token_response = client.post("/graphql/", data={"query": mutation}, content_type="application/json")
    return token_response.json()["data"]["tokenAuth"]["token"]


def test_all_products_query(db, client, product):
    """Тест получения всех товаров"""
    query = """
        query {
          allProducts {
            name
          }
        }
    """

    response = client.post("/graphql/", data={"query": query}, content_type="application/json")
    json_data = response.json()
    assert "errors" not in json_data
    data = json_data["data"]["allProducts"]
    assert len(data) > 0


def test_do_not_create_cat_mutation(db, client, token):
    """Проверка на невозможность создавать категорию не админом"""
    mutation = f"""
    mutation {{
        createCategory(name: "New Cat") {{
            result {{
              name
            }}
        }}
    }}
    """

    response = client.post(
        "/graphql/",
        {"query": mutation},
        content_type="application/json",
        HTTP_AUTHORIZATION=f"JWT {token}",
    )
    json_data = response.json()
    assert "errors" in json_data, json_data.get("errors")


def test_create_and_delete_product_mutation(db, client, category, super_token):
    """Проверка создания и удаления товара"""
    mutation = f"""
    mutation {{
        createProduct(categoryId: {category.pk}, name: "New Prod", price: "111.11", unit: "1t") {{
            result {{
                id
                name
                price
                category {{
                    name
                }}
            }}
        }}
    }}
    """

    response = client.post(
        "/graphql/",
        {"query": mutation},
        content_type="application/json",
        HTTP_AUTHORIZATION=f"JWT {super_token}",
    )
    json_data = response.json()
    assert "errors" not in json_data, json_data.get("errors")

    data = json_data["data"]["createProduct"]["result"]
    assert data["id"] is not None
    assert data["name"] == "New Prod"
    assert data["price"] == "111.11"
    assert data["category"]["name"] == "Test cat 1"
    product_pk = data["id"]

    del_mutation = f"""
        mutation {{
            deleteProduct(pk: {product_pk}) {{
                ok
            }}
        }}
    """

    response2 = client.post(
        "/graphql/",
        {"query": del_mutation},
        content_type="application/json",
        HTTP_AUTHORIZATION=f"JWT {super_token}",
    )
    json_data = response2.json()
    assert "errors" not in json_data, json_data.get("errors")
    ok = json_data["data"]["deleteProduct"]["ok"]
    assert ok


def test_update_product_mutation(db, client, product, super_token):
    """Проверка изменения товара"""
    mutation = f"""
    mutation {{
        updateProduct(pk: {product.pk}, name: "Changed Prod", price: "555.11", stock: 20) {{
            result {{
                id
                name
                price
                stock
            }}
        }}
    }}
    """

    response = client.post(
        "/graphql/",
        {"query": mutation},
        content_type="application/json",
        HTTP_AUTHORIZATION=f"JWT {super_token}",
    )
    json_data = response.json()
    assert "errors" not in json_data, json_data.get("errors")

    data = json_data["data"]["updateProduct"]["result"]
    assert data["id"] == str(product.pk)
    assert data["name"] == "Changed Prod"
    assert data["price"] == "555.11"
    assert data["stock"] == 20


def test_add_review_mutation(db, client, product, user, token):
    """Проверка добавления рейтинга для товара"""
    mutation = f"""
    mutation {{
        createReview(productId: {product.pk}, comment: "La-la-la", userId: {user.pk}, rating: 5) {{
            result {{
                comment
                rating
                product {{
                    id
                }}
                user {{
                    id
                }}
            }}
        }}
    }}
    """

    response = client.post(
        "/graphql/",
        {"query": mutation},
        content_type="application/json",
    )
    json_data = response.json()
    assert "errors" in json_data, json_data.get("errors")

    response = client.post(
        "/graphql/",
        {"query": mutation},
        content_type="application/json",
        HTTP_AUTHORIZATION=f"JWT {token}",
    )
    json_data = response.json()
    assert "errors" not in json_data, json_data.get("errors")

    data = json_data["data"]["createReview"]["result"]
    assert data["comment"] == "La-la-la"
    assert data["rating"] == 5
    assert data["user"]["id"] == str(user.pk)
    assert data["product"]["id"] == str(product.pk)

