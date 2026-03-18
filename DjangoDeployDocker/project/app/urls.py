# from django.urls import path
# # from django.conf import settings
# # from django.conf.urls.static import static
# # from .views import (
# #     index,
# #     ProfileDetailView,
# #     ProfileCreateView,
# #     ProfileEditView,
# #     Homepage,
# #     ChatDetailView,
# #     ChatCreateView,
# #     RegisterPage,
# #     LoginPage,
# #     UserLogoutView,
# # )
# #
# # urlpatterns = [
# #     # Главная страница / тестовая
# #     path("test/", index, name="index"),
# #
# #     # Страница всех чатов пользователя
# #     path("homepage/", Homepage.as_view(), name="homepage"),
# #
# #     # Детали чата
# #     path("chats/<int:pk>/", ChatDetailView.as_view(), name="chat_detail"),
# #
# #     # Создание нового чата
# #     path("chat/create/", ChatCreateView.as_view(), name="chat_create"),
# #
# #     # Регистрация / логин / логаут
# #     path("", RegisterPage.as_view(), name="register"),
# #     path("login/", LoginPage.as_view(), name="login"),
# #     path("logout/", UserLogoutView.as_view(), name="logout"),
# #
# #     # Профиль
# #     path("profile/create/", ProfileCreateView.as_view(), name="profile_create"),
# #     path("profile/edit/", ProfileEditView.as_view(), name="profile_edit"),
# #     path("user/<slug:username>/", ProfileDetailView.as_view(), name="profile_detail"),
# # ]

# # if settings.DEBUG:
# #     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, ProfileDetailUpdateView, ChatViewSet, MessageViewSet

router = DefaultRouter()
router.register(r"users", UserViewSet, basename="user")
router.register(r"chats", ChatViewSet, basename="chat")
router.register(r"messages", MessageViewSet, basename="message")

urlpatterns = [
    path("profile/", ProfileDetailUpdateView.as_view(), name="profile-detail"),
    path("api/", include(router.urls)),
]