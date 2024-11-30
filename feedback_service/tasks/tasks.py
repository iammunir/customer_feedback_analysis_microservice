from celery import shared_task, chain, group
from sentiment.analysis import analyze, extract_keywords

@shared_task(autoretry_for=(Exception,), retry_kwargs={'max_retries': 3}, retry_backoff=True)
def sentiment_analysis(feedback):
    try:
        sentiment = analyze(feedback)
        feedback["sentiment"] = sentiment
        return feedback
    except Exception as e:
        feedback["error_sentiment"] = str(e)        
        return feedback

@shared_task(autoretry_for=(Exception,), retry_kwargs={'max_retries': 3}, retry_backoff=True)
def keyword_extraction(feedback):
    try:
        feedback["keywords"] = extract_keywords(feedback)
        return feedback
    except Exception as e:
        feedback["error_extract"] = str(e)      
        return feedback

@shared_task
def handle_failure(request, exc, traceback, feedback, task_name):
    feedback["error"] = f"{task_name} failed."
    return feedback

@shared_task
def process_feedback_task(feedback_list):
    batch_size = 10
    batches = [feedback_list[i:i + batch_size] for i in range(0, len(feedback_list), batch_size)]

    task_group = group(
        [
            chain(
                sentiment_analysis.s(feedback).on_error(handle_failure.s(feedback, "sentiment_analysis")),
                keyword_extraction.s().on_error(handle_failure.s(feedback, "keyword_extraction"))
            )
            for batch in batches for feedback in batch
        ]
    )

    group_result = task_group.apply_async()
    return [result.id for result in group_result.children]  # Return child task IDs


