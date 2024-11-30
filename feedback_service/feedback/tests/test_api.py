import json
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse, resolve
from unittest.mock import patch

class FeedbackAPITests(APITestCase):

    @patch('feedback.tasks.process_feedback_task.apply_async')
    def test_valid_feedback_submission(self, mock_task):
        url = reverse('feedback-process')
        mock_task.return_value.id = "mock-task-id"
        feedback_data = [
            {"customer_id": 1, "feedback_text": "Great product!", "timestamp": "2024-11-30T10:00:00Z"},
            {"customer_id": 2, "feedback_text": "Needs improvement.", "timestamp": "2024-11-30T11:00:00Z"}
        ]
        response = self.client.post(url, data=json.dumps(feedback_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)

    def test_malformed_json(self):
        url = reverse('feedback-process')
        malformed_data = "invalid-json"  # Invalid JSON
        response = self.client.post(url, data=malformed_data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
