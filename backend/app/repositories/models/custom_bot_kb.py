from app.routes.schemas.bot_kb import (
    type_kb_chunking_strategy,
    type_kb_embeddings_model,
    type_kb_search_type,
    type_os_character_filter,
    type_os_token_filter,
    type_os_tokenizer,
)
from pydantic import BaseModel


class SearchParamsModel(BaseModel):
    max_results: int
    search_type: type_kb_search_type


class AnalyzerParamsModel(BaseModel):
    character_filters: list[type_os_character_filter]
    tokenizer: type_os_tokenizer
    token_filters: list[type_os_token_filter]


class OpenSearchParamsModel(BaseModel):
    analyzer: AnalyzerParamsModel | None


class BedrockKnowledgeBaseModel(BaseModel):
    embeddings_model: type_kb_embeddings_model
    open_search: OpenSearchParamsModel
    chunking_strategy: type_kb_chunking_strategy
    search_params: SearchParamsModel
    max_tokens: int | None = None
    overlap_percentage: int | None = None
    knowledge_base_id: str | None = None
    data_source_ids: list[str] | None = None
