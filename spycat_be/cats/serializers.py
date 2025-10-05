from rest_framework import serializers
from .models import SpyCat
from integrations.cats_api.api import get_all_breeds, CatAPIError


class SpyCatSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpyCat
        fields = ["id", "name", "years_of_experience", "breed", "salary"]
        read_only_fields = ["id"]

    def validate_years_of_experience(self, value):
        if value < 0:
            raise serializers.ValidationError("years_of_experience must be >= 0")
        return value

    def validate_breed(self, value):
        try:
            breeds = get_all_breeds()
        except CatAPIError:
            raise serializers.ValidationError("Could not validate breed (TheCatAPI unreachable).")
        if value.lower() not in breeds:
            raise serializers.ValidationError("Breed is not valid according to TheCatAPI.")
        return value
