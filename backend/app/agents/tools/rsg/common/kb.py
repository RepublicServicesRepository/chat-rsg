"""Provides the KB class for interacting with the Bedrock Knowledgebase service."""

import boto3

class KB():

    """Class for interacting with the Bedrock Knowledgebase service."""

    def __init__(self, region, kb_id,kb_params,max_search_results=10):
        """Initialize the KB class with region, kb_id, kb_model_id, and kb_params.

        :param region: AWS region for Bedrock service
        :param kb_id: Knowledge base ID
        :param kb_model_id: Knowledge base model ID
        :param kb_params: Parameters for the knowledge base model
        :param max_search_results: max no. of search reseutls to retrrieve from KB
        """
        self.region = region
        self.kb_id = kb_id
        
        self.kb_params = kb_params
        self.max_search_results = max_search_results
    
    def filter_and_retrieve(self, input, metaDataFilter):
        """Retrieve text from the knowledge base.

        :param input: User input text to search for in the knowledge base
        :param metaDataFilter: Metadata filter for the retrieval
        :return: Response from the Bedrock agent runtime client
        """
        bedrock_agent_runtime_client = boto3.client("bedrock-agent-runtime", 
                                                    region_name=self.region)  

        return bedrock_agent_runtime_client.retrieve(
            knowledgeBaseId=self.kb_id,
            retrievalQuery={
                    'text': input
            },
            retrievalConfiguration={
                'vectorSearchConfiguration':{
                    'numberOfResults': self.max_search_results,
                    'filter': metaDataFilter
                    }
                }
        )
    
    def retrieve(self, input):
        """Retrieve text from the knowledge base.

        :param input: User input text to search for in the knowledge base
        :return: Response from the Bedrock agent runtime client
        """
        bedrock_agent_runtime_client = boto3.client("bedrock-agent-runtime", 
                                                    region_name=self.region)  

        return bedrock_agent_runtime_client.retrieve(
            knowledgeBaseId=self.kb_id,
            retrievalQuery={
                    'text': input
            },
            retrievalConfiguration={
                'vectorSearchConfiguration':{
                    'numberOfResults': self.max_search_results
                    }
                }
        )

