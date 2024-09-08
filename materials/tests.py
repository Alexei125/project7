from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse


from materials.models import Course, Lesson, Subscription
from users.models import User


class LessonTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email="admin1@localhost")
        self.course = Course.objects.create(title="Програмного обеспечения")
        self.lesson = Lesson.objects.create(
            title="Основы программирования", course=self.course, owner=self.user
        )
        self.client.force_authenticate(user=self.user)

    def test_lesson_retrieve(self):
        self.url = reverse("lms:lessons_retrieve", args=(self.lesson.pk,))
        self.data = {"title": "Основы программирования", "course": self.course.id}
        response = self.client.get(self.url)
        self.data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], self.lesson.title)
        self.assertEqual(response.data["course"], self.lesson.course.id)

    def test_lesson_create(self):
        self.url = reverse("lms:lessons_create")
        self.data = {
            "title": "Основы backend-разработки",
            "course": self.lesson.course.id,
            "description": "Внутренняя часть цифрового продукта",
        }
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(response.data["title"], "Основы backend-разработки")
        self.assertEqual(response.data["course"], self.lesson.course.id)
        self.assertEqual(Lesson.objects.all().count(), 2)

    def test_lesson_update(self):
        self.url = reverse("lms:lessons_update", args=(self.lesson.pk,))
        self.data = {
            "title": "Основы backend-разработки",
            "course": self.course.id,
            "description": "Внутренняя часть цифрового продукта",
        }
        response = self.client.put(self.url, self.data)
        self.data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Основы backend-разработки")
        self.assertEqual(response.data["course"], self.course.id)

    def test_lesson_delete(self):
        self.url = reverse("lms:lessons_delete", args=(self.lesson.pk,))
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.all().count(), 0)


class SubscriptionTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email="admin1@localhost")
        self.course = Course.objects.create(title="Програмное обеспечение")
        self.client.force_authenticate(user=self.user)
        self.url = reverse("lms:subscription_create")

    def test_subscription_activate(self):
        """Тест подписки на курс"""
        data = {
            "user": self.user.id,
            "course": self.course.id,
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(),
            {
                "message": "Подписка добавлена",
            },
        )
        self.assertTrue(
            Subscription.objects.all().exists(),
        )

    def test_sub_deactivate(self):
        """Тест отписки с курса"""
        Subscription.objects.create(user=self.user, course=self.course)
        data = {
            "user": self.user.id,
            "course": self.course.id,
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(
            response.json(),
            {
                "message": "Подписка удалена",
            },
        )
        self.assertFalse(
            Subscription.objects.all().exists(),
        )
