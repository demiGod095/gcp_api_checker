# Create your views here.
from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from .models import JobModel
from .serializers import JobSerializer, JobCreateSerializer, JobListSerializer


class JobViewSet(viewsets.ModelViewSet):
    queryset = JobModel.objects.all()
    permission_classes = (AllowAny,)

    def get_serializer_class(self):
        if self.action == 'create':
            return JobCreateSerializer
        if self.action == 'list':
            return JobListSerializer
        else:
            return JobSerializer

