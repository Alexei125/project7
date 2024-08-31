from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from materials import models
from materials.models import Course, Lesson
from users.models import Payment


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"


class CourseDetailSerializer(ModelSerializer):
    count_lessons = SerializerMethodField()
    lesson = LessonSerializer(many=True, read_only=True)
    subscription = serializers.SerializerMethodField()

    def get_subscription(self, obj):
        return obj.subscription.filter(user=self.context.get('request').user).exists()

    def get_count_lessons(self, course):
        return Lesson.objects.filter(course=course).count()

    class Meta:
        model = Course
        fields = ["id", "title", "description", "count_lessons", "lesson", "subscription"]


class CourseSerializer(ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"


class PaymentsSerializer(ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"
