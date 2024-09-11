import datetime
from django_filters import rest_framework
from rest_framework import filters
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    get_object_or_404,
)
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from materials import models, serializers
from materials.models import Course, Lesson, Subscription
from materials.paginators import CustomPagination
from materials.serializers import (
    CourseSerializer,
    LessonSerializer,
    PaymentsSerializer,
    SubscriptionSerializer,
)
from materials.task import sending_mail
from users.models import Payment
from users.permissions import IsModerator, IsOwner


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = CustomPagination

    def get_serializer_class(self):
        if self.action == "retrieve":
            return CourseSerializer.CourseDetailSerializer
        return CourseSerializer

    def perform_create(self, serializer):
        course = serializer.save()
        course.owner = self.request.user
        course.save()

    def get_queryset(self):
        if self.request.user.is_superuser or self.request.user.groups.filter(
                name='Администраторы DRF').exists():
            return Course.objects.all()
        elif self.request.user.is_anonymous:
            return None
        else:
            return Course.objects.filter(owner=self.request.user)

    def get_permissions(self):
        if self.action in "create":
            self.permission_classes = (~IsModerator, IsAuthenticated)
        elif self.action in ["update", "retrieve"]:
            self.permission_classes = (IsModerator | IsOwner,)
        elif self.action == "destroy":
            self.permission_classes = (
                ~IsModerator,
                IsOwner,
            )
        return super().get_permissions()

    def get(self, request):
        queryset = Course.objects.all()
        paginated_queryset = self.paginate_queryset(queryset)
        serializer = CourseSerializer(paginated_queryset, many=True)
        return self.get_paginated_response(serializer.data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        date = instance.last_update
        instance.last_update = datetime.datetime.now()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        sending_mail.delay(instance.id, date)
        return Response(serializer.data)


class LessonCreateAPIView(CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (~IsModerator, IsAuthenticated)

    def perform_create(self, serializer):
        lesson = serializer.save()
        lesson.owner = self.request.user
        lesson.save()


class LessonListAPIView(ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    pagination_class = CustomPagination


class LessonRetrieveAPIView(RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsModerator, IsAuthenticated | IsOwner)

    def get_queryset(self):

        if self.request.user.is_superuser or self.request.user.groups.filter(
                name='Администраторы DRF').exists():
            return Lesson.objects.all()
        else:
            return Lesson.objects.filter(owner=self.request.user)


def get(self, request):
    queryset = Lesson.objects.all()
    paginated_queryset = self.paginate_queryset(queryset)
    serializer = LessonSerializer(paginated_queryset, many=True)
    return self.get_paginated_response(serializer.data)


class LessonUpdateAPIView(UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsModerator, IsAuthenticated | IsOwner)


class LessonDestroyAPIView(DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (
        IsAuthenticated,
        IsOwner,
        ~IsModerator,
    )


class PaymentListAPIView(ListAPIView):
    serializer_class = serializers.PaymentsSerializer
    queryset = Payment.objects.all()
    filter_backends = [rest_framework.DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ["course", "lesson", "method"]
    ordering_fields = ["date_of_payment"]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


class SubscriptionCreateAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def post(self, request, *args, **kwargs):
        user = self.request.user
        course_id = self.request.data.get("course")
        course = get_object_or_404(Course, pk=course_id)

        subs_item = Subscription.objects.filter(user=user, course=course)
        if subs_item.exists():
            subs_item.delete()
            message = "Подписка удалена"
        else:
            Subscription.objects.create(user=user, course=course)
            message = "Подписка добавлена"
        return Response({"message": message})
