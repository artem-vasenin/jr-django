# accounts/test_graphql.py
import pytest

from django.contrib.auth.models import User


@pytest.fixture
def user(db):
    user = User.objects.create_user(username="testuser", password="12345")
    user.profile.city = 'Tver'
    user.profile.save(update_fields=['city'])
    return user


@pytest.fixture
def token(client, user):
    mutation = f"""
        mutation {{
          tokenAuth(username: "{user.username}", password: "12345") {{
            token
          }}
        }}
        """
    token_response = client.post("/graphql/", data={"query": mutation}, content_type="application/json")
    return token_response.json()["data"]["tokenAuth"]["token"]


def test_all_users_query(client, token):
    all_users_query = """
        query {
          allUsers {
            id
            username
            profile {
              city
            }
          }
        }
        """

    response = client.post(
        "/graphql/",
        data={"query": all_users_query},
        content_type="application/json",
        HTTP_AUTHORIZATION=f"JWT {token}",
    )

    json_data = response.json()
    assert "errors" not in json_data
    data = json_data["data"]["allUsers"]
    assert len(data) == 1
    assert data[0]["username"] == "testuser"
    assert data[0]["profile"]["city"] == "Tver"


def test_registration_mutation(db, client):
    mutation = f"""
    mutation {{
        registration(
            username: "newUser",
            email: "new@user.ru",
            password1: "111111",
            password2: "111111",
        ) {{
            result {{
                username
                email
            }}
        }}
    }}
    """

    response = client.post("/graphql/", {"query": mutation}, content_type="application/json")
    json_data = response.json()
    assert "errors" not in json_data, json_data.get("errors")

    data = json_data["data"]["registration"]["result"]
    assert data["username"] == "newUser"
    assert data["email"] == "new@user.ru"
