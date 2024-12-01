from rest_framework.test import APITestCase
from unittest.mock import patch
from tasks.tasks import sentiment_analysis, keyword_extraction, handle_failure, process_feedback_task

class ChildTask():
    def __init__(self, id):
        self.id = id

class TasksTests(APITestCase):

    @patch('tasks.tasks.analyze')
    def test_sentiment_analysis(self, mock_analyze):
        feedback = {
            "customer_id": 87,
            "feedback_text": "Great service!",
        }

        mock_analyze.return_value = "Positive"

        result = sentiment_analysis(feedback)
        self.assertEqual(result["sentiment"], "Positive")

    @patch('tasks.tasks.analyze')
    def test_sentiment_analysis_failure(self, mock_analyze_feedback):
        feedback = {
            "customer_id": 87,
            "feedback_text": "Great service!",
        }

        mock_analyze_feedback.side_effect = ValueError("Random failure in sentiment analysis.")  # Simulate failure

        result = sentiment_analysis(feedback)

        self.assertIn("error_sentiment", result)
        self.assertEqual(result["error_sentiment"], "Random failure in sentiment analysis.")

    @patch('tasks.tasks.extract_keywords')
    def test_keyword_extraction(self, mock_extract_keywords):
        feedback = {
            "customer_id": 87,
            "feedback_text": "Great service!",
        }

        mock_result_extract = ["example", "mock", "keywords"]
        mock_extract_keywords.return_value = mock_result_extract # Mock successful keyword extraction

        result = keyword_extraction(feedback)

        self.assertEqual(result["keywords"], mock_result_extract)  # Check if keywords are added to feedback

    @patch('tasks.tasks.extract_keywords')
    def test_keyword_extraction_failure(self, mock_extract_keywords):
        feedback = {
            "customer_id": 87,
            "feedback_text": "Great service!",
        }

        mock_extract_keywords.side_effect = ValueError("Random failure in keyword extraction.")  # Simulate failure

        result = keyword_extraction(feedback)

        self.assertIn("error_extract", result)
        self.assertEqual(result["error_extract"], "Random failure in keyword extraction.")

    @patch('tasks.tasks.group')
    @patch('tasks.tasks.chain')
    def test_process_feedback_task(self, mock_chain, mock_group):
        feedback = {
            "customer_id": 87,
            "feedback_text": "Great service!",
        }
        feedback_list = [feedback] * 20  # 20 feedback items
        mock_children_result = [ChildTask('task1'), ChildTask('task2'), ChildTask('task3'), ChildTask('task4')]
        mock_group.return_value.apply_async.return_value.children = mock_children_result

        result = process_feedback_task(feedback_list)

        self.assertEqual(len(result), len(mock_children_result))
        mock_group.assert_called_once()  # Ensure group was called
        mock_chain.assert_called()  # Ensure chain was called for each feedback item
 