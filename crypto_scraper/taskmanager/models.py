from django.db import models
import uuid


class ScrapeJob(models.Model):
    job_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.job_id)


class CoinData(models.Model):
    job = models.ForeignKey(ScrapeJob, related_name='coin_data', on_delete=models.CASCADE)
    coin = models.CharField(max_length=50)
    data = models.JSONField()

    def __str__(self):
        return self.coin
