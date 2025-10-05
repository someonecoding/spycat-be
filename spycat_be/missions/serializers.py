from rest_framework import serializers
from .models import Mission, Target
from cats.models import SpyCat


class TargetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Target
        fields = ["id", "name", "country", "notes", "completed"]
        read_only_fields = ["id"]

    def validate(self, data):
        if self.instance:
            if (self.instance.completed or self.instance.mission.completed) and data.get("notes", self.instance.notes) != self.instance.notes:
                raise serializers.ValidationError("Cannot update notes: target or mission is completed.")
        return data


class MissionSerializer(serializers.ModelSerializer):
    targets = TargetSerializer(many=True)
    cat_id = serializers.PrimaryKeyRelatedField(queryset=SpyCat.objects.all(), source="cat", required=False)

    class Meta:
        model = Mission
        fields = ["id", "name", "cat_id", "completed", "targets"]
        read_only_fields = ["id", "completed"]

    def create(self, validated_data):
        targets_data = validated_data.pop("targets")
        mission = Mission.objects.create(**validated_data)
        for t_data in targets_data:
            Target.objects.create(mission=mission, **t_data)
        mission.update_completed_status()
        return mission

    def update(self, instance, validated_data):
        cat = validated_data.get("cat")
        if cat:
            instance.cat = cat
        instance.save()
        return instance
