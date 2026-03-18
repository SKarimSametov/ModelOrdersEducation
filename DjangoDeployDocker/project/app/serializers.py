from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Profile, Chat, Message

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email"]


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = ["user", "display_name", "age", "avatar"]


class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    receiver = serializers.SerializerMethodField()  # вычисляем через chat

    class Meta:
        model = Message
        fields = ["id", "chat", "sender", "receiver", "content", "file", "is_read", "created_at"]

    def get_receiver(self, obj):
        participants = obj.chat.participants.exclude(id=obj.sender.id)
        return UserSerializer(participants.first()).data if participants.exists() else None


class ChatSerializer(serializers.ModelSerializer):
    participants = serializers.SerializerMethodField()
    last_message = serializers.SerializerMethodField()
    unread_count = serializers.SerializerMethodField()

    class Meta:
        model = Chat
        fields = ["id", "participants", "created_at", "last_message", "unread_count"]

    def get_participants(self, obj):
        profiles = Profile.objects.filter(user__in=obj.participants.all())
        return ProfileSerializer(profiles, many=True).data

    def get_last_message(self, obj):
        last_msg = obj.messages.order_by("-created_at").first()
        return MessageSerializer(last_msg).data if last_msg else None

    def get_unread_count(self, obj):
        user = self.context["request"].user
        return obj.messages.filter(is_read=False).exclude(sender=user).count()