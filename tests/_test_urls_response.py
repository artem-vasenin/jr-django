import pytest
from django.urls import reverse, resolve
from accounts.tests.urls_accounts_data import urls as accounts_urls
from management.tests.urls_admin_data import urls as management_urls
from orders.tests.urls_orders_data import urls as orders_urls
from products.tests.urls_products_data import urls as products_urls


@pytest.mark.django_db
@pytest.mark.parametrize("url_name, view_func, kwargs, expected_status",
                         accounts_urls + management_urls + orders_urls + products_urls)
def test_url_response_and_view(client, url_name, view_func, kwargs, expected_status):
    """
    Проверяет:
    1) URL корректно реверсится (с kwargs если нужно)
    2) URL резолвится в ожидаемую view
    3) Сервер отвечает ожидаемым статус-кодом
    """
    # Реверс с/без kwargs
    if isinstance(kwargs, dict):
        url = reverse(url_name, kwargs=kwargs)
    else:
        url = reverse(url_name)

    # Проверяем, что resolve(url) → правильная View
    resolved = resolve(url)
    assert resolved.func.view_class == view_func, (
        f"{url_name}: ожидалась View {view_func.__name__}, "
        f"получена {resolved.func.view_class.__name__}"
    )

    # Проверка ответа
    response = client.get(url)
    assert response.status_code == expected_status, (
        f"{url_name}: ожидался статус {expected_status}, "
        f"получен {response.status_code}"
    )