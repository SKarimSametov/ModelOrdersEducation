# from django.contrib.auth.views import LoginView
# from django.shortcuts import render
# from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
# from .forms import RegisterForm, ChatCreateForm, MessageForm, ProfileForm
# from django.urls import reverse_lazy
# from .models import Chat, Message, Profile, User
# from django.contrib.auth.views import LogoutView
# from django.contrib.auth.mixins import LoginRequiredMixin
#
# def index(request):
#     return render(request, "index.html")
#
#
# class Homepage(ListView, LoginRequiredMixin):
#     model = Chat
#     template_name = "homepage.html"
#     context_object_name = "chats"
#     def get_queryset(self):
#         return Chat.objects.filter(participants=self.request.user)
#
#
# class ChatPage(DetailView):
#     model = Chat
#     template_name = "chatpage.html"
#     context_object_name = "chat"
#
# class RegisterPage(CreateView):
#     form_class = RegisterForm
#     template_name = "register.html"
#     success_url = reverse_lazy("login")
#
# class LoginPage(LoginView):
#     template_name = "login.html"
#     context_object_name = "login"
#     success_url = reverse_lazy("index")
#
# from django.shortcuts import redirect
# from .forms import MessageForm
#
# class ChatDetailView(LoginRequiredMixin, DetailView):
#     model = Chat
#     template_name = "chatdetail.html"
#     context_object_name = "chat"
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         chat = self.object
#         participants = chat.participants.all()
#         messages = Message.objects.filter(
#             sender__in=participants,
#             receiver__in=participants
#         ).order_by("created_at")
#         context["messages"] = messages
#         context["user"] = self.request.user
#         context["form"] = MessageForm()
#         return context
#
#     def post(self, request, *args, **kwargs):
#         self.object = self.get_object()
#         form = MessageForm(request.POST, request.FILES)
#         if form.is_valid():
#             message = form.save(commit=False)
#             message.sender = request.user
#             participants = self.object.participants.exclude(id=request.user.id)
#             if participants.exists():
#                 message.receiver = participants.first()
#             else:
#                 message.receiver = request.user
#
#             message.save()
#             return redirect("chatdetail", pk=self.object.pk)
#         context = self.get_context_data(form=form)
#         return self.render_to_response(context)
#
# class UserLogoutView(LogoutView):
#     next_page = "/login/"
#
#
# class ChatCreateView(LoginRequiredMixin, CreateView):
#     model = Chat
#     form_class = ChatCreateForm
#     template_name = "createchat.html"
#     success_url = reverse_lazy("homepage")
#
#     def form_valid(self, form):
#         chat = form.save()
#
#         user2 = form.cleaned_data["participant"]
#
#         chat.participants.add(self.request.user)
#         chat.participants.add(user2)
#
#         return super().form_valid(form)
#
#
#
# class ProfileDetailView(LoginRequiredMixin, DetailView):
#     model = User
#     template_name = "profile_detail.html"
#     context_object_name = "profile_user"
#     slug_field = "username"
#     slug_url_kwarg = "username"
#
# class ProfileEditView(LoginRequiredMixin, View):
#     template_name = "profile_edit.html"
#
#     def get(self, request):
#         profile, created = Profile.objects.get_or_create(user=request.user)
#         form = ProfileForm(instance=profile)
#         return render(request, self.template_name, {"form": form})
#
#     def post(self, request):
#         profile, created = Profile.objects.get_or_create(user=request.user)
#         form = ProfileForm(request.POST, request.FILES, instance=profile)
#         if form.is_valid():
#             form.save()
#             return redirect("profile_detail", username=request.user.username)
#         return render(request, self.template_name, {"form": form})
#
# class ProfileCreateView(LoginRequiredMixin, View):
#     template_name = "profile_create.html"
#
#     def get(self, request):
#         if hasattr(request.user, "profile"):
#             return redirect("profile_detail", username=request.user.username)
#
#         form = ProfileForm()
#         return render(request, self.template_name, {"form": form})
#
#     def post(self, request):
#         form = ProfileForm(request.POST, request.FILES)
#         if form.is_valid():
#             profile = form.save(commit=False)
#             profile.user = request.user
#             profile.save()
#             return redirect("profile_detail", username=request.user.username)
#         return render(request, self.template_name, {"form": form})



from rest_framework import viewsets, permissions, status
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from .models import Profile, Chat, Message
from .serializers import UserSerializer, ProfileSerializer, ChatSerializer, MessageSerializer

User = get_user_model()


# Пользователи (только чтение)
class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


# Профиль текущего пользователя (GET / PATCH)
class ProfileDetailUpdateView(RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        profile, created = Profile.objects.get_or_create(user=self.request.user)
        return profile


# Чаты
class ChatViewSet(viewsets.ModelViewSet):
    serializer_class = ChatSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Chat.objects.filter(participants=self.request.user)

    def perform_create(self, serializer):
        chat = serializer.save()
        chat.participants.add(self.request.user)
        other_user_id = self.request.data.get("participant_id")
        if other_user_id:
            try:
                other_user = User.objects.get(id=other_user_id)
                chat.participants.add(other_user)
            except User.DoesNotExist:
                pass
        chat.save()



class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        chat_id = self.request.query_params.get("chat_id")
        if chat_id:
            chat = get_object_or_404(Chat, id=chat_id, participants=self.request.user)
            return Message.objects.filter(chat=chat).order_by("created_at")
        return Message.objects.none()

    def perform_create(self, serializer):
        chat_id = self.request.data.get("chat_id")
        chat = get_object_or_404(Chat, id=chat_id, participants=self.request.user)
        serializer.save(sender=self.request.user, chat=chat)