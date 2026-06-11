import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import grpc
from concurrent import futures

from proto import ai_pb2, ai_pb2_grpc


class AI(ai_pb2_grpc.AIServiceServicer):

    def Summarize(self, request, context):
        text = request.text
        result = text[:10]
        print(f"Received text: {text}")
        print(f"Generated summary: {result}")

        return ai_pb2.SummaryResponse(result=result)


server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

ai_pb2_grpc.add_AIServiceServicer_to_server(AI(), server)

server.add_insecure_port("[::]:50051")
server.start()
print("AI Service is running on port 50051...")

server.wait_for_termination()
