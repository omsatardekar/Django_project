from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .tasks import scrape_coin_data
from .models import ScrapeJob, CoinData
import json
import logging

logger = logging.getLogger(__name__)


class StartScrapingView(APIView):
    def post(self, request):
        coins = request.data.get("coins", [])
        if not coins:
            return Response({"error": "No coins provided"}, status=status.HTTP_400_BAD_REQUEST)

        job = ScrapeJob.objects.create()
        job_id = job.job_id

        for coin in coins:
            scrape_coin_data.delay(job_id, coin)

        return Response({"job_id": str(job_id)}, status=status.HTTP_202_ACCEPTED)


class ScrapingStatusView(APIView):
    def get(self, request, job_id):
        try:
            job = ScrapeJob.objects.get(job_id=job_id)
            coin_data = CoinData.objects.filter(job=job)
            tasks = []
            for data in coin_data:
                try:
                    output = json.loads(data.data)
                except json.JSONDecodeError as e:
                    logger.error(f"Error decoding JSON for coin {data.coin}: {e}")
                    output = {"error": "Invalid data format"}

                tasks.append({
                    "coin": data.coin,
                    "output": output
                })

            return Response({"job_id": str(job_id), "tasks": tasks}, status=status.HTTP_200_OK)
        except ScrapeJob.DoesNotExist:
            return Response({"error": "Job not found"}, status=status.HTTP_404_NOT_FOUND)
