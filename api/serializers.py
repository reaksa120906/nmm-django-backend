from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile, Expense, Income, Savings


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)
    gender   = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model  = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name', 'gender']

    def create(self, validated_data):
        gender   = validated_data.pop('gender', '')
        password = validated_data.pop('password')
        user     = User(**validated_data)
        user.set_password(password)
        user.save()
        UserProfile.objects.create(user=user, gender=gender)
        return user


class UserSerializer(serializers.ModelSerializer):
    gender      = serializers.SerializerMethodField()
    date_joined = serializers.DateTimeField(read_only=True)

    class Meta:
        model  = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'gender', 'date_joined']

    def get_gender(self, obj):
        try:
            return obj.profile.gender
        except UserProfile.DoesNotExist:
            return ''


class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model        = Expense
        fields       = '__all__'
        read_only_fields = ['user', 'created_at']


class IncomeSerializer(serializers.ModelSerializer):
    class Meta:
        model        = Income
        fields       = '__all__'
        read_only_fields = ['user']


class SavingsSerializer(serializers.ModelSerializer):
    progress_pct = serializers.ReadOnlyField()

    class Meta:
        model        = Savings
        fields       = '__all__'
        read_only_fields = ['user', 'progress_pct']
