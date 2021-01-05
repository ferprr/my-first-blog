from blog.models import Post
from users.models import CustomUser
from django.test import TestCase, Client
from django.urls import reverse

ADMIN = ('admin', 'senhaadmin')
AUTHOR = ('jonas.teixeira', 'senhajonas')
VISITOR = ('ana', 'senhaana')

SAMPLE_POST = {
    'title': 'First Post',
    'text': 'Lorem Ipsum Dolor',
    'created_date': '2020-12-28',
    'published_date': '2020-12-29'
}

class PostTestCase(TestCase):
    def setUp(self):
        self.client = Client()

        self.author = CustomUser.objects.create_user(
            username=AUTHOR[0],
            first_name='Jonas Teixeira',
            last_name='da Silva',
            email='jonas@gmail.com',
            is_active=True,
            is_admin=False
        )

        self.author.set_password(AUTHOR[1])

    def test_edit_post_inaccessibale_by_visitor(self):
        post = Post.objects.create(**SAMPLE_POST, author=self.author)

        self.client.login(username=VISITOR[0], password=VISITOR[1])
        response = self.client.get(reverse('post_edit', kwargs={ 'pk': post.pk }))
        self.assertNotEqual(response.status_code, 200)

    def test_new_post_inaccessibale_by_visitor(self):
        post = Post.objects.create(**SAMPLE_POST, author=self.author)

        self.client.login(username=VISITOR[0], password=VISITOR[1])
        response = self.client.get(reverse('post_new'))
        self.assertNotEqual(response.status_code, 200)

    def test_list_post_accessibale_by_unlogged_visitor(self):
        post = Post.objects.create(**SAMPLE_POST, author=self.author)

        response = self.client.get(reverse('post_list'))
        self.assertEqual(response.status_code, 200)

    def test_detail_post_accessibale_by_unlogged_visitor(self):
        post = Post.objects.create(**SAMPLE_POST, author=self.author)

        response = self.client.get(reverse('post_detail', kwargs={ 'pk': post.pk }))
        self.assertEqual(response.status_code, 200)