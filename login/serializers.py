from rest_framework import serializers
from .models import User, Book, Borrowing
from django.contrib.auth.hashers import make_password  

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_admin', 'is_member', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

class BorrowingSerializer(serializers.ModelSerializer):
    fine = serializers.SerializerMethodField()

    class Meta:
        model = Borrowing
        fields = ['id', 'user', 'book', 'borrowed_at', 'due_date', 'returned', 'fine']

    def get_fine(self, obj):
        return obj.calculate_fine()
