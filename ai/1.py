import grpc

# from proto import ai_pb2, ai_pb2_grpc
import proto.ai_pb2 as ai_pb2
import proto.ai_pb2_grpc as ai_pb2_grpc

channel = grpc.insecure_channel("localhost:50051")

client = ai_pb2_grpc.AIServiceStub(channel)

response = client.Summarize(
    ai_pb2.SummaryRequest(
        text="This is a long text that needs to be summarized. It contains multiple sentences and should be truncated to the first 100 characters." 
    )
)

# print(response.result)

from transformers import AutoTokenizer

# Load the tokenizer for the model
tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased-finetuned-sst-2-english")

text = "I love coding FastAPI!"

# 1. Split into tokens
tokens = tokenizer.tokenize(text)
print(f"Tokens: {tokens}")

# 2. Convert tokens to IDs (Numbers)
input_ids = tokenizer.convert_tokens_to_ids(tokens)
print(f"IDs: {input_ids}")      