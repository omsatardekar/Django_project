from rest_framework import serializers
from .models import ScrapeJob, CoinData


class ScrapeJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScrapeJob
        fields = ['job_id', 'created_at', 'updated_at']


class CoinDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoinData
        fields = ['job', 'coin', 'data']
