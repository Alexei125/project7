from django.urls import path
from rest_framework.routers import SimpleRouter

from materials.apps import MaterialsConfig
from materials.views import (CourseViewSet, LessonListAPIView, LessonCreateAPIView,
                             LessonUpdateAPIView, LessonDestroyAPIView, LessonRetrieveAPIView)

app_name = MaterialsConfig.name

router = SimpleRouter()
router.register("", CourseViewSet)

urlpatterns = [
    path("lessons/", LessonListAPIView.as_view(), name='list'),
    path("lessons/<int:pk>/", LessonRetrieveAPIView.as_view(), name='retrieve'),
    path("lessons/create/", LessonCreateAPIView.as_view(), name='create'),
    path("lessons/<int:pk>/destroy/", LessonDestroyAPIView.as_view(), name='destroy'),
    path("lessons/<int:pk>/update/", LessonUpdateAPIView.as_view(), name='update'),
]

urlpatterns += router.urls
