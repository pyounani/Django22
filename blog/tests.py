from django.test import TestCase, Client
from bs4 import BeautifulSoup
from .models import Post, Category
from django.contrib.auth.models import User

# Create your tests here.
class TestView(TestCase):

    def setUp(self):
        # test.py 작성할시 우선 작성(클라이언트 전달)
        self.client = Client()

        self.user_park = User.objects.create_user(username="park", password="password")
        self.user_you = User.objects.create_user(username="you", password="password")  #밑에 author 추가하기

        self.category_com = Category.objects.create(name="computer", slug="computer")
        self.category_edu = Category.objects.create(name="education", slug="education")

        self.post_001 = Post.objects.create(title="첫번째 포스트", content="첫번째 포스트입니다", author=self.user_park, category=self.category_com)
        self.post_002 = Post.objects.create(title="두번째 포스트", content="두번째 포스트입니다", author=self.user_you, category=self.category_edu)
        self.post_003 = Post.objects.create(title="세번째 포스트", content="세번째 포스트입니다", author=self.user_you)

    def nav_test(self, soup):  # test의 이름을 절대로 가지면 안돼(내가 실행해야 하는 test인가 우리는 그게 아니라 test쪽에서 부르게 하고 싶을 때 부를거임)
        navbar = soup.nav
        # navbar안에 BLOG가 있는가
        self.assertIn('BLOG', navbar.text)  # 원래는 soup.nav.text 반복 귀찮아 => navbar 변수 설정
        self.assertIn('ABOUT ME', navbar.text)

        # 링크 확인하기
        home_btn = navbar.find('a', text="Home")  #Home에 만약에 span같은 것들이 있으면 삭제 필요!
        self.assertEqual(home_btn.attrs['href'], '/')

        blog_btn = navbar.find('a', text="BLOG")
        self.assertEqual(blog_btn.attrs['href'], '/blog/')

        about_btn = navbar.find('a', text="ABOUT ME")
        self.assertEqual(about_btn.attrs['href'], '/about_me/')

    def category_test(self, soup):
        category_card = soup.find('div', id='category_card')
        self.assertIn('Categories', category_card.text)
        self.assertIn(f'{self.category_com.name} ({self.category_com.post_set.count()})', category_card.text)
        self.assertIn(f'{self.category_edu.name} ({self.category_edu.post_set.count()})', category_card.text)
        self.assertIn(f'미분류 (1)', category_card.text)

    def test_post_list(self):
        # test.py 작성할시 우선 작성(클라이언트 전달)
        response = self.client.get('/blog/')
        # 만약 301 오류가 나면 response = self.client.get('/blog/', follow=True)

        # response 결과가 정상적으로 보이는지(성공에 대한 번호가 200)
        self.assertEqual(response.status_code, 200)

        #HTML을 분석을 해야하는데 BeautifulSoup 이용하기 위해 써줘 parser는 분석하겠다라는 의미
        soup = BeautifulSoup(response.content, 'html.parser')

        # title이 정상적으로 보이는지 태그와 함꼐 전달하기 때문에 text 태그안에 있는 문자를 전달한다는 의미
        self.assertEqual(soup.title.text, ' BLOG ')

        # navbar가 정상적으로 보이는지
        # nav_test를 이용해서 detail쪽에서도 같은 것 사용 함수로 처리
        self.nav_test(soup)
        self.category_test(soup)


        #붙임 2->3 self 추가
        self.assertEqual(Post.objects.count(), 3)

        response = self.client.get('/blog/')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')
        main_area = soup.find('div', id="main-area")
        self.assertIn(self.post_001.title, main_area.text)
        self.assertIn(self.post_002.title, main_area.text)
        self.assertNotIn("아직 게시물이 없습니다", main_area.text)

        self.assertIn(self.post_001.author.username.upper(), main_area.text)
        self.assertIn(self.post_002.author.username.upper(), main_area.text)

        # post가 정상적으로 보이는지
        # 여기서는 admin에 있는 것을 가져올 수가 없기에 model에서 가져옴 즉 저장되어 있는 데이터를 확인하는 것이 아니라 그 구성(구조)을 확인..?

        # 1. 맨 처음에는 Post가 없음
        # self.assertEqual(Post.objects.count(), 0)
        # main_area = soup.find('div', id="main_area") # main_area에서 찾겠다
        # self.assertIn("아직 게시물이 없습니다", main_area.text) # => list쪽에서 if문으로 exists()

        Post.objects.all().delete()
        self.assertEqual(Post.objects.count(), 0)

        response = self.client.get('/blog/')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')

        main_area = soup.find('div', id="main-area")
        self.assertIn("아직 게시물이 없습니다", main_area.text)

        # 2. Post가 추가  다른 필드를 넣어도 되는데 blank=True이니 굳이 안 넣어도 됨 blank=True가 아니라면 꼭 넣어줘야함(문자열로 date는 "2022-12-14"형태로)

        # post_001 = Post.objects.create(title="첫번째 포스트", content="첫번째 포스트입니다", author=self.user_park)
        # post_002 = Post.objects.create(title="두번째 포스트", content="두번째 포스트입니다", author=self.user_you)
        # self.assertEqual(Post.objects.count(), 2)

        # 위에 과정은 admin에 넣어준 것 뿐 클라이언트한테 아직 전달 못했기에 다시 전달
        # response = self.client.get('/blog/')
        # self.assertEqual(response.status_code, 200)
        # soup = BeautifulSoup(response.content, 'html.parser')
        # main_area = soup.find('div', id="main_area")
        # self.assertIn(post_001.title, main_area.text)
        # self.assertIn(post_002.title, main_area.text)
        # self.assertNotIn("아직 게시물이 없습니다", main_area.text)

        # self.assertIn(post_001.author.username.upper(), main_area.text)
        # self.assertIn(post_002.author.username.upper(), main_area.text)


    def test_post_detail(self):
        # 테스트를 할 때는 하나도 데이터가 없는 상태를 테스트를 하기에 임의로 만들어줘
        post_001 = Post.objects.create(title="첫번째 포스트", content="첫번째 포스트입니다", author=self.user_park)
        self.assertEqual(post_001.get_absolute_url(), '/blog/1/')

        response = self.client.get(post_001.get_absolute_url(), follow=True)  # '/blog/1/' = post_001.get_absolute_url()
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')

        # navbar가 정상적으로 보이는지
        self.nav_test(soup)

        self.assertIn(post_001.title, soup.title.text)
        # 밑에 post-area을 보겠다는 것이고 이것은 전체적인 title에 포함이 되어져있는가를 확인하는 것

        # main_area와 post_area comment_area를 id를 주자(detail쪽)
        main_area = soup.find('div', id='main-area')
        post_area = main_area.find('div', id='post-area') # main_area안에 post_area가 있음
        self.assertIn(post_001.title, post_area.text)
        self.assertIn(post_001.content, post_area.text)
        self.assertIn(post_001.author.username.upper(), post_area.text)

