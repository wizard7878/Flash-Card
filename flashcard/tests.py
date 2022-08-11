from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

from core import models
from .serializer import WordDetailSerializer
# Create your tests here.


            
def user_url_builder(method, **kwargs):
    if kwargs is None:
        return reverse(f"user-{method}")
    else:
        return reverse(f"user-{method}", kwargs=kwargs)

def category_url_builder(method, **kwargs):
    return reverse(f'category-{method}', kwargs=kwargs)

def words_url_builder(method, categories= None, **kwargs):
    if categories is not None and method != 'detail':
        return f"{reverse(f'words-{method}',kwargs=kwargs)}?categories={categories}"
    return f"{reverse(f'words-{method}',kwargs=kwargs)}"


class PublicFlashCardApiTests(TestCase):
    """
    Testing FlashCard Api
    """
    def setUp(self):
        self.client = APIClient()
        user = models.User.objects.create(username="UserTest", telegram_user_id=555)
        user2 = models.User.objects.create(username="UserTest", telegram_user_id=333)

        self.user = user 
        self.user2 = user2

        self.category = models.Category.objects.create(title="test", user=self.user)

    def test_list_categories(self):
        """
        test list all categories
        """

        c1 = models.Category.objects.create(title="C1", user=self.user)
        c2 = models.Category.objects.create(title="C2", user=self.user)
        a2 = models.Category.objects.create(title="A2", user=self.user2)

        CATEGORY_LIST_URL = category_url_builder('list', telegram_user_id=self.user.telegram_user_id)
        categories = models.Category.objects.filter(user=self.user)
        res = self.client.get(CATEGORY_LIST_URL)

        self.assertEqual(len(res.data), categories.count())
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertNotEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


    def test_create_category(self):
        """
        test create category with given data
        """
        payload = {
            "title" : "A1",
            "user": self.user
        }
        CATEGORY_URL = category_url_builder('list', telegram_user_id=self.user.telegram_user_id)
        res = self.client.post(CATEGORY_URL, payload)

        self.assertEqual(res.data['title'], payload['title'])
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertNotEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_invalid_category(self):
        """
        test create category with invalid 
        payload (without title)
        """
        payload = {
            "user": self.user
        }

        CATEGORY_URL = category_url_builder('list', telegram_user_id=self.user.telegram_user_id)
        res = self.client.post(CATEGORY_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotEqual(res.status_code, status.HTTP_201_CREATED)

    def test_delete_category(self):
        """
        test delete a category
        """
        b2 = models.Category.objects.create(title='B2', user=self.user)
        CATEGORY_URL = category_url_builder('detail', telegram_user_id=self.user.telegram_user_id, pk=b2.id)
        res = self.client.delete(CATEGORY_URL)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertNotEqual(res.status_code, status.HTTP_200_OK)

    def test_delete_invalid_category(self):
        """
        test delete another user2's category 
        with user 1 telegram id
        """
        a1 = models.Category.objects.create(title='A1', user=self.user2)
        CATEGORY_URL = category_url_builder('detail', telegram_user_id=self.user.telegram_user_id, pk=a1.id)
        res = self.client.delete(CATEGORY_URL)

        self.assertNotEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_user(self):
        """
        test create user with given payload
        """
        payloads = {
            'telegram_user_id': 143,
            'username': 'testname',
        }
        USER_URL = user_url_builder('list') 
        res = self.client.post(USER_URL, payloads)

        self.assertEqual(res.data, payloads)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertNotEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_invalid_user(self):
        """
        test create user with invalid 
        payload (without telegram id)
        """
        payload = {
            'username': 'testname'
        }
        USER_URL = user_url_builder('list') 
        res = self.client.post(USER_URL, payload)
        self.assertNotEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_detail_user(self):
        """
        test all users and get user with telegram id
        """
        user1= models.User.objects.create(username='testname', telegram_user_id=243)
        user2 =models.User.objects.create(username='testname2', telegram_user_id=354)
        USER_URL = user_url_builder('detail', pk=user1.telegram_user_id) 
        users = models.User.objects.all()
        res = self.client.get(USER_URL)
        
        self.assertEqual(user1.username, res.data['username'])
        self.assertNotEqual(user2.username, res.data['username'])
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertNotEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


    def test_create_word(self):
        """
        test create a word with given payload
        """
        payload = {
            "english": "word",
            "persian": "کلمه",
            "category": self.category.title,
            "telegram_user_id" : self.user.telegram_user_id
        }
        create_word_url = reverse('create-word')
        res = self.client.post(create_word_url, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data['persian'], payload['persian'])
         

    def test_create_invalid_word(self):
        """
        test create invalid word with payload.
        invalid because user2 dosen't create that category
        """
        payload = {
            "english": "word",
            "persian": "کلمه",
            "category": self.category.title,
            "telegram_user_id" : self.user2.telegram_user_id
        }
        create_word_url = reverse('create-word')
        res = self.client.post(create_word_url, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotEqual(res.status_code, status.HTTP_201_CREATED)

    def test_list_words(self):
        """
        test get list of words
        by selecting categories
        """
        a1 = models.Category.objects.create(title="A1", user=self.user)
        a2 = models.Category.objects.create(title="A2", user=self.user)

        b2 = models.Category.objects.create(title="B2", user=self.user2)

        w1_a1 = models.Word.objects.create(english="simple", persian="نمونه", category=a1, user=self.user)
        w2_a1 = models.Word.objects.create(english="sunny", persian="افتابی", category=a1, user=self.user)
        w3_a1 = models.Word.objects.create(english="cloudy", persian="ابری", category=a1, user=self.user)

        w1_a2 = models.Word.objects.create(english="snow", persian="برفی", category=a2, user=self.user)

        w1_b2 = models.Word.objects.create(english="dust", persian="خاک", category=b2, user=self.user2)

        payload1 = {
            "categories" : "A1,A2"
        }

        payload2 = {
            "categories" : "B2"
        }
        
        user1_word_url = words_url_builder('list',categories=payload1["categories"], telegram_user_id=self.user.telegram_user_id)
        user2_word_url = words_url_builder('list',categories=payload2["categories"], telegram_user_id=self.user2.telegram_user_id)
        user2_word_invalid_url = words_url_builder('list',categories=payload1["categories"], telegram_user_id=self.user2.telegram_user_id)

        res1 = self.client.get(user1_word_url)
        res2 = self.client.get(user2_word_url)
        res3 = self.client.get(user2_word_invalid_url)

        self.assertEqual(res1.status_code, status.HTTP_200_OK)
        self.assertIn(WordDetailSerializer(w1_a1).data, res1.data)
        self.assertIn(WordDetailSerializer(w2_a1).data, res1.data)
        self.assertIn(WordDetailSerializer(w3_a1).data, res1.data)
        self.assertIn(WordDetailSerializer(w1_a2).data, res1.data)

        self.assertIn(WordDetailSerializer(w1_b2).data, res2.data)

        self.assertNotIn(WordDetailSerializer(w1_b2).data, res1.data)
        self.assertNotIn(WordDetailSerializer(w1_a1).data, res2.data)
        self.assertNotIn(WordDetailSerializer(w1_a2).data, res2.data)

        self.assertEqual(res3.data, [])

    def test_destory_word(self):
        """
        test delete word api
        """
        word = models.Word.objects.create(english="simple", persian="نمونه", category=self.category, user=self.user)
        word_url = words_url_builder('detail', telegram_user_id=self.user.telegram_user_id, pk=word.id)
        
        res = self.client.delete(word_url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertNotEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_destory_invalid_word(self):
        """
        test delete invalid word.
        user1 can't delete user2's word
        """
        user2_category = models.Category.objects.create(title="A", user=self.user2)
        user2_word = models.Word.objects.create(english="simple", persian="نمونه", category=user2_category, user=self.user2)
        
        word_url = words_url_builder('detail', telegram_user_id=self.user.telegram_user_id, pk=user2_word.id)
        
        res = self.client.delete(word_url)

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertNotEqual(res.status_code, status.HTTP_204_NO_CONTENT)

            