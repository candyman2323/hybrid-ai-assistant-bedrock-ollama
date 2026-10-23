
import boto3
from botocore.exceptions import ClientError, BotoCoreError

REGION = "us-east-1"
MODEL_ID = "amazon.nova-micro-v1:0"

try:
    client = boto3.client(
        "bedrock-runtime",
        region_name=REGION
    )

    response = client.converse(
        modelId=MODEL_ID,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "text": "Explain artificial intelligence in simple words."
                    }
                ]
            }
        ],
        inferenceConfig={
            "maxTokens": 200,
            "temperature": 0.5
        }
    )

    answer = response["output"]["message"]["content"][0]["text"]

    print("\nBedrock connection successful!")
    print("AI response:", answer)

except (ClientError, BotoCoreError) as error:
    print("AWS request failed.")
    print(error)
