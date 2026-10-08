import django
from django.conf import settings
from rest_framework import serializers


class DataSerializerWithError(serializers.Serializer):
    data = serializers.JSONField()
    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class DataSerializerWithoutError(serializers.Serializer):
    payload = serializers.JSONField()
    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


def print_data():
    settings.configure()
    django.setup()

    serializer = DataSerializerWithError(data={'data': 42})
    if not serializer.is_valid():
        print("Failure!")
        return
    print(serializer.data['data'])

    serializer = DataSerializerWithoutError(data={'payload': 42})
    if not serializer.is_valid():
        print("Failure!")
        return
    print(serializer.data['payload'])
