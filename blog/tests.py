from django.test import TestCase, Client
from bs4 import BeautifulSoup
from .models import Post

# Create your tests here.
class TestView(TestCase):

    def setUp(self):
        self.client = Client()


    def test_post_list(self):
        response = self.client.get('/blog/')
        # response 결과가 정상적으로 보이는지
        self.assertEqual(response.status_code, 200)

        soup = BeautifulSoup(response.content, 'html.parser')
        # title이 정상적으로 보이는지
        self.assertEqual(soup.title.text, 'BLOG')

        # navbar가 정상적으로 보이는지
        navbar = soup.nav
        self.assertIn('BLOG', soup.nav.text)
        self.assertIn('ABOUT ME', navbar.text)

        # post가 정상적으로 보이는지
        # 여기서는 admin에 있는 것을 가져올 수가 없기에 model에서 가져옴 즉 값을 확인하는 것이 아니라 그 구성(구조)을 확인..?

        # 1. 맨 처음에는 Post가 없음
        self.assertEqual(Post.objects.count(), 0)
        main_area = soup.find('div', id="main-area")
        self.assertIn("아직 게시물이 없습니다", main_area.text)

        # 2. Post가 추가
        post_001 = Post.objects.create(title="첫번째 포스트", content="첫번째 포스트입니다")
        post_002 = Post.objects.create(title="두번째 포스트", content="두번째 포스트입니다")
        self.assertEqual(Post.objects.count(), 2)

        response = self.client.get('/blog/')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')
        main_area = soup.find('div', id="main-area")
        self.assertIn(post_001.title, main_area.text)
        self.assertIn(post_002.title, main_area.text)
        self.assertNotIn("아직 게시물이 없습니다", main_area.text)