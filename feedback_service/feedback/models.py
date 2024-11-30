from django.db import models

class Feedback(models.Model):
    id = models.CharField(max_length=36, unique=True, editable=False, default="", primary_key=True)
    customer_id = models.IntegerField()
    feedback_text = models.TextField()
    timestamp = models.DateTimeField()
