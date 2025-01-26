import json
import boto3
from app.repositories.custom_bot import (
    compose_bot_id,
    decompose_bot_id,
    find_private_bot_by_id,
)

cf_client = boto3.client("cloudformation")


def handler(event, context):
    print(event)
    pk = event["pk"]
    sk = event["sk"]

    bot_id = decompose_bot_id(sk)

    # Note: stack naming rule is defined on:
    # cdk/bin/bedrock-knowledge-base.ts
    stack_name = f"BrChatKbStack{bot_id}"

    response = cf_client.describe_stacks(StackName=stack_name)
    outputs = response["Stacks"][0]["Outputs"]

    knowledge_base_id = None
    data_source_ids = []

    for output in outputs:
        if output["OutputKey"] == "KnowledgeBaseId":
            knowledge_base_id = output["OutputValue"]
        elif output["OutputKey"].startswith("DataSource"):
            data_source_ids.append(output["OutputValue"])

    result = []
    for data_source_id in data_source_ids:
        result.append(
            {
                "KnowledgeBaseId": knowledge_base_id,
                "DataSourceId": data_source_id,
                "PK": pk,
                "SK": sk,
            }
        )

    return result
