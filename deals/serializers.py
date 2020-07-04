from rest_framework import serializers
from .models import Deal


class DealSerializer(serializers.ModelSerializer):
    '''
    Сериалайзер для работы с БД.
    '''
    class Meta:
        model = Deal
        fields = ['username', 'item', 'total', 'quantity', 'date']


class DealGetSerializer(serializers.Serializer):
    '''
    Сериалайзер для отображения в GET.
    '''
    username    = serializers.CharField(max_length=200)
    spent_money = serializers.IntegerField()
    gems        = serializers.ListField(
        child = serializers.CharField(max_length=200)
    )