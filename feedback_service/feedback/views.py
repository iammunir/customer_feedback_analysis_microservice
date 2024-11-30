from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from celery.result import AsyncResult
from tasks.tasks import process_feedback_task
from .serializers import FeedbackSerializer

class FeedbackProcessView(APIView):
    def post(self, request):
        serializer = FeedbackSerializer(data=request.data, many=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        feedback_objects = []
        for feedback_data in serializer.validated_data:
            feedback_objects.append(feedback_data)

        task = process_feedback_task.delay(feedback_objects)
        task_id = task.id
        return Response({"message": "Feedback queued for processing. Task Id: {}".format(task_id)}, status=status.HTTP_202_ACCEPTED)

class FeedbackResultView(APIView):
    def get(self, request, task_id):

        task = AsyncResult(task_id)
        if task.state != 'SUCCESS':
            return Response({"message": 'invalid task id'}, status=status.HTTP_400_BAD_REQUEST)

        results = []
        for child_id in task.result:
            task_child = AsyncResult(child_id)
            if task_child.ready():
                result = None
                try:
                    result = task_child.get()
                except Exception as e:
                    result = str(e)
                    
                results.append({'status': 'completed', 'result': result})
            else:
                results.append({'status': 'processing', 'child_task_id': task_child.id})

        return Response({"data": results}, status=status.HTTP_200_OK)
