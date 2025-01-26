# Migration Guide (v1 to v2)

## Overview

The v2 update introduces a significant change by replacing pgvector on Aurora Serverless and ECS-based embedding with [Amazon Bedrock Knowledge Bases](https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base.html). This change is not backward compatible. If you want to continue using pgvector, avoid upgrading to v2. If you plan to transition, start by updating to v1.3.0 and enabling the Knowledge Bases option in cdk.json. This will make your existing bots read-only, allowing a gradual shift to the new system. Note that **upgrading to v2 will result in the deletion of all Aurora-related resources.** Future updates will focus exclusively on v2, with v1 being deprecated.

## Key Changes and Migration Steps

### v2 brings a major architectural shift

Replacement of pgvector and ECS Embedding: The previous system using pgvector on Aurora Serverless and ECS for embedding is replaced by Amazon Bedrock Knowledge Bases, which utilize an OpenSearch backend. This offers a fully managed solution, improving reliability and ease of maintenance.

### Migration Process

- Update to v1.3.0: Ensure you are using version 1.3.0 or later.
- Enable Knowledge Bases: Set `useBedrockKnowledgeBasesForRag` to `true` in [cdk.json](../../cdk/cdk.json). **Be aware that enabling Knowledge Bases will incur charges for both Aurora and Knowledge Bases.**
- Read-Only Mode: Once enabled, your existing pgvector-based bots become read-only, preventing further edits but allowing continued use.
- Re-create Bots: Open the bot creation screen and re-create your bots with the same definitions as those using pgvector, but now utilizing Knowledge Bases. **Note that some feature is not available on KnowledgeBases e.g. web crawling and youtube transcript.**

![](../imgs/v1_to_v2_readonly_bot.png)

- Upgrade to v2: Once you have successfully transitioned to using Knowledge Bases, proceed with the full upgrade to v2.

### Important Note

Migration of existing vector data from Aurora to the new Knowledge Bases is complex and not supported by this sample. If you rely on pgvector, consider staying with v1.
