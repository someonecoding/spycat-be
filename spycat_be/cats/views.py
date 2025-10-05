from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import SpyCat
from .serializers import SpyCatSerializer


class SpyCatViewSet(viewsets.ModelViewSet):
    queryset = SpyCat.objects.all().order_by("id")
    serializer_class = SpyCatSerializer

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        if "salary" not in request.data:
            return Response(
                {"detail": "Only salary updates are allowed via PATCH."},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = self.get_serializer(
            instance, data={"salary": request.data["salary"]}, partial=True
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
