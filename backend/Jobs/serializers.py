from rest_framework import serializers
from .models import JobModel


class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobModel
        fields = '__all__'


class JobCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobModel
        fields = ('url',)


class JobListSerializer(serializers.ModelSerializer):
    link = serializers.HyperlinkedIdentityField(view_name="jobmodel-detail")

    class Meta:
        model = JobModel
        fields = '__all__'
