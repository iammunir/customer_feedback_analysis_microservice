from django.db import models

class Feedback(models.Model):
    id = models.CharField(max_length=36, unique=True, editable=False, default="", primary_key=True)
    customer_id = models.IntegerField()
    feedback_text = models.TextField()
    timestamp = models.DateTimeField()

class ProcessedFeedback(models.Model):
    feedback = models.OneToOneField(Feedback, on_delete=models.CASCADE, related_name='processed')
    sentiment = models.CharField(max_length=50)
    keywords = models.JSONField()
    processed_at = models.DateTimeField(auto_now_add=True)
