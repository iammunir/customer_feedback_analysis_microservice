import pytest
from unittest import mock
from feedback.tasks import sentiment_analysis, keyword_extraction, handle_failure, process_feedback_task

class ChildTask():
    def __init__(self, id):
        self.id = id

@pytest.fixture
def feedback():
    return {
        "customer_id": 1,
        "feedback_text": "Great service!",
    }

# Mock the external functions (analyze_feedback and extract_keywords)
@pytest.fixture
def mock_analyze_feedback():
    with mock.patch('feedback.tasks.analyze_feedback') as mock_func:
        yield mock_func

@pytest.fixture
def mock_extract_keywords():
    with mock.patch('feedback.tasks.extract_keywords') as mock_func:
        yield mock_func

# Test for sentiment_analysis task
def test_sentiment_analysis(mock_analyze_feedback, feedback):
    mock_analyze_feedback.return_value = "positive"  # Mock successful sentiment analysis

    result = sentiment_analysis(feedback)

    assert result["sentiment"] == "positive"  # Check if sentiment is added to feedback

# Test for failure in sentiment_analysis task
def test_sentiment_analysis_failure(mock_analyze_feedback, feedback):
    mock_analyze_feedback.side_effect = ValueError("Random failure in sentiment analysis.")  # Simulate failure

    result = sentiment_analysis(feedback)

    assert "error_sentiment" in result  # Ensure error message is added to feedback
    assert result["error_sentiment"] == "Random failure in sentiment analysis."

# Test for keyword_extraction task
def test_keyword_extraction(mock_extract_keywords, feedback):
    mock_extract_keywords.return_value = ["example", "mock", "keywords"]  # Mock successful keyword extraction

    result = keyword_extraction(feedback)

    assert result["keywords"] == ["example", "mock", "keywords"]  # Check if keywords are added to feedback

# Test for failure in keyword_extraction task
def test_keyword_extraction_failure(mock_extract_keywords, feedback):
    mock_extract_keywords.side_effect = ValueError("Random failure in keyword extraction.")  # Simulate failure

    result = keyword_extraction(feedback)

    assert "error_extract" in result  # Ensure error message is added to feedback
    assert result["error_extract"] == "Random failure in keyword extraction."

# Test for handle_failure task
def test_handle_failure(feedback):
    result = handle_failure(None, None, None, feedback, "sentiment_analysis")

    assert "error" in result  # Ensure error message is added to feedback
    assert result["error"] == "sentiment_analysis failed."

# Test for process_feedback_task
@mock.patch('feedback.tasks.group')
@mock.patch('feedback.tasks.chain')
def test_process_feedback_task(mock_chain, mock_group, feedback):
    feedback_list = [feedback] * 20  # 20 feedback items
    mock_group.return_value.apply_async.return_value.children = [ChildTask('task1'), ChildTask('task2'), ChildTask('task3'), ChildTask('task4')]

    result = process_feedback_task(feedback_list)

    assert len(result) == 4  # Ensure the result contains 4 task IDs
    mock_group.assert_called_once()  # Ensure group was called
    mock_chain.assert_called()  # Ensure chain was called for each feedback item
