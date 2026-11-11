from django.test import SimpleTestCase, Client
from django.views.generic import TemplateView
from django.utils import timezone

from . import views


class HomePageGetTests(SimpleTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        url = '/'
        client = Client()
        cls.response = client.get(url)

    def test_url_access(self):
        self.assertEqual(self.response.status_code, 200)

    def test_url_name(self):
        self.assertEqual(self.response.resolver_match.url_name, 'home')

    def test_url_namespace(self):
        self.assertEqual(self.response.resolver_match.namespace, 'blog')

    def test_view_name(self):
        self.assertEqual(self.response.resolver_match.func, views.index)

    def test_template_name(self):
        self.assertTemplateUsed(self.response, 'app_blog/index.html')

    def test_base_template_name(self):
        self.assertTemplateUsed(self.response, 'base.html')

    def test_context_var(self):
        self.assertIn('site', self.response.context)
        self.assertEqual(self.response.context['site'], 'mysite.com')

    def test_content_title(self):
        self.assertContains(self.response, '<title>Главная</title>', html=True)

    def test_content_links(self):
        self.assertContains(self.response, '<a href="/about/">О нас</a>', html=True)
        self.assertContains(self.response, '<a href="/contact/">Контакты</a>', html=True)
        self.assertNotContains(self.response, '<a href="/">Главная</a>', html=True)

    def test_content_text(self):
        self.assertContains(self.response, f'&copy; mysite.com 2023-{timezone.now().year}. All rights reserved.')


class AboutPageGetTests(SimpleTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        url = '/about/'
        client = Client()
        cls.response = client.get(url)

    def test_url_access(self):
        self.assertEqual(self.response.status_code, 200)

    def test_url_name(self):
        self.assertEqual(self.response.resolver_match.url_name, 'about')

    def test_url_namespace(self):
        self.assertEqual(self.response.resolver_match.namespace, 'blog')

    def test_view_name(self):
        self.assertIs(self.response.resolver_match.func.view_class, TemplateView)

    def test_template_name(self):
        self.assertTemplateUsed(self.response, 'app_blog/about.html')

    def test_base_template_name(self):
        self.assertTemplateUsed(self.response, 'base.html')

    def test_context_var(self):
        self.assertIn('site', self.response.context)
        self.assertEqual(self.response.context['site'], 'mysite.com')

    def test_content_title(self):
        self.assertContains(self.response, '<title>О нас</title>', html=True)

    def test_content_links(self):
        self.assertContains(self.response, '<a href="/">Главная</a>', html=True)
        self.assertContains(self.response, '<a href="/contact/">Контакты</a>', html=True)
        self.assertNotContains(self.response, '<a href="/about/">О нас</a>', html=True)

    def test_content_text(self):
        self.assertContains(self.response, 'Телефон: +12345677890')
        self.assertContains(self.response, 'Email: admin@admin.com')
        self.assertContains(self.response, f'&copy; mysite.com 2023-{timezone.now().year}. All rights reserved.')


class ContactPageGetTests(SimpleTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        url = '/contact/'
        client = Client()
        cls.response = client.get(url)

    def test_url_access(self):
        self.assertEqual(self.response.status_code, 302)

    def test_url_name(self):
        self.assertEqual(self.response.resolver_match.url_name, 'contact')

    def test_url_namespace(self):
        self.assertEqual(self.response.resolver_match.namespace, 'blog')

    def test_view_name(self):
        self.assertEqual(self.response.resolver_match.func, views.contact)