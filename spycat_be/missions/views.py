from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Mission, Target
from .serializers import MissionSerializer, TargetSerializer


class MissionViewSet(viewsets.ModelViewSet):
    queryset = Mission.objects.all().order_by("id")
    serializer_class = MissionSerializer

    def destroy(self, request, *args, **kwargs):
        mission = self.get_object()
        if mission.cat is not None:
            return Response(
                {"detail": "Cannot delete a mission that is assigned to a cat."},
                status=status.HTTP_400_BAD_REQUEST
            )
        return super().destroy(request, *args, **kwargs)


class TargetViewSet(viewsets.ModelViewSet):
    queryset = Target.objects.all().order_by("id")
    serializer_class = TargetSerializer

    def partial_update(self, request, *args, **kwargs):
        """Allow PATCH for updating notes or marking completed"""
        target = self.get_object()
        serializer = self.get_serializer(target, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
