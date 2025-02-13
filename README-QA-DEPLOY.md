# QA Deployment 
The curreent deployment is very manual and this file outlines the steps.
!!! Important: chat-rsg is deployed in us-east-1

### Code Repo:
Since the code for QA has some hard-code values for QA environemnt, a seprate repo for QA is maintained
repo name: chatRSG-v1-QA
url: https://github.com/RepublicServicesRepository/chat-rsg/tree/chatRSG-v1-QA

### Deployment
````
git clone https://github.com/RepublicServicesRepository/chat-rsg/tree/chatRSG-v1-QA
cd chatRSG-v1-QA
npm install
./bin.sh --bedrock-region us-east-1 --allowed-signup-email-domains "republicservices.com,repsrv.com" --ipv4-ranges "10.0.0.0/8,172.16.0.0/12,192.168.0.0/16" --version "1.2.6"
````

# Important Debug Info
#### Agent/Tools
- Custom rsg agent/tools are under /chat-rsg/backend/app/agents/tools/rsg
- Add the tools in : /chat-rsg/backend/app/agents/utils.py

#### Cloudwatch Logs (in us-east-1)
- General chat-rsg backend log: /aws/lambda/BedrockChatStack-BackendApiHandlerXXXXX
- Agent/tool specific  logs are with : /aws/lambda/BedrockChatStack-WebSocketHandlerXXXXXX


# !!!!! Important Info on changes done for QA. 

### /chat-rsg/cdk/lib/bedrock-chat-stack.ts  (line #52)
````
const vpc = ec2.Vpc.fromLookup(this, "VPC", {
      vpcName: 'ai-platfrom-vpc-qa',
      ownerAccountId: process.env.CDK_DEFAULT_ACCOUNT,
      region: process.env.CDK_DEFAULT_REGION,
    });
````

### /chat-rsg/cdk/cdk.json  (line #66)
````
 "userPoolDomainPrefix": "chat-rsg-qa",
````

### /chat-rsg/deploy.yml  (line #144)
````
  "git clone --branch chatRSG-v1-QA https://github.com/RepublicServicesRepository/chat-rsg.git",
````

### /chat-rsg/deploy.yml  (line #146)
````
  "export CDK_DEFAULT_ACCOUNT=339712742482",
  "export CDK_DEFAULT_REGION=us-east-1",
````  

### /chat-rsg/backend/requirements.txt  (line #20)
````
  httpx==0.27.2
````

### on AWS CodeBuild Project: FrontendReactBuildProjectXXXXX
`````
set these environemnt vars specific to QA.
VITE_APP_REDIRECT_SIGNIN_URL:  https://chat-rsg.aiservicesqa.awsext.repsrv.com
VITE_APP_REDIRECT_SIGNOUT_URL: https://chat-rsg.aiservicesqa.awsext.repsrv.com
VITE_APP_USER_POOL_ID: us-east-1_1SVzQwRZS
VITE_APP_USER_POOL_CLIENT_ID: hq3059ti1o1g6vh60nb3ukf7h
VITE_APP_COGNITO_DOMAIN: chat-rsg-qa.auth.us-east-1.amazoncognito.com
`````

### on AWS Lambda: BedrockChatStack-WebSocketHandlerXXXXXX
`````
set these environemnt vars specific to QA.
ACCOUNT=339712742482
ASK_JEFF_KB_ID=3OQ0M8CJD4
ASK_JEFF_KB_MAX_SEARCH_RESULTS=5
ASK_JEFF_KB_MAX_TOKENS=1000
ASK_JEFF_KB_REGION=us-east-1
ASK_JEFF_KB_TEMPERATURE=0.4
ASK_JEFF_KB_TOP_P=0.5
ASK_KM_KB_ID=3OQ0M8CJD4
ASK_KM_KB_MAX_SEARCH_RESULTS=5
ASK_KM_KB_MAX_TOKENS=512
ASK_KM_KB_REGION=us-east-1
ASK_KM_KB_TEMPERATURE=0.4
ASK_KM_KB_TOP_P=0.5
ASK_SOP_KB_ID=VAQDRMH36A
ASK_SOP_KB_MAX_SEARCH_RESULTS=5
ASK_SOP_KB_MAX_TOKENS=1000
ASK_SOP_KB_REGION=us-east-1
ASK_SOP_KB_TEMPERATURE=0.4
ASK_SOP_KB_TOP_P=0.5
BEDROCK_REGION=us-east-1
CLIENT_ID=hq3059ti1o1g6vh60nb3ukf7h
ES_API_HOST=https://api.republicservices.com
ES_API_HOST_HEADER=internal.api.republicservices.com
ES_API_KEY=XXXXXXXX
GIS_API_HOST=https://api.republicservices.com/utilityservices
GIS_API_KEY=XXXXXXXXX
REGION=us-east-1
USER_POOL_ID=us-east-1_1SVzQwRZS
`````