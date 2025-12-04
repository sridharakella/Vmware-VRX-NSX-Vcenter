#--------------------------------------------------------#
#                     Spas Kaloferov                     #
#                   www.kaloferov.com                    #
# bit.ly/The-Twitter      Social     bit.ly/The-LinkedIn #
# bit.ly/The-Gitlab        Git         bit.ly/The-Github #
# bit.ly/The-BSD         License          bit.ly/The-GNU #
#--------------------------------------------------------#

  #
  #       VMware Cloud Assembly ABX Code Sample          
  #
  # [Description] 
  #   - Auto deletes failed or canceled deployments:
  #   - Allows secrets and passwords to be provided via action inputs , AWS Secrets Manager secrets or user context  
  #   - Further guidance can be found here: ABX Action to Sync Blueprints from Assembly to Gitlab (http://kaloferov.com/blog/skkb1050)
  # [Inputs]
  #   - deleteDelayIn (Integer): Delete delay in seconds after which the deployment is deleted. Max 480 seconds (8 min)      
  #   - deploymentIdABXIn (String): Deployment ID when testing the actoin via the TEST button, otherwize not needed.
  #   - actionOptionTokenProviderIn (String): Select the token provider for the action. This is from where the tokens will be read
  #      - awssm: Use AWS Secrets Manager. Requires Faas Provider: Amazon Web Services (AWS) 
  #         - awsSmRegionNameIn (String): AWS Secrets Manager Region Name e.g. us-west-2
  #         - awsSmCspTokenSecretIdIn (String): AWS Secrets Manager CSP Token Secret ID
  #      - inputs: Use action inputs for secrets
  #         - cspRefreshTokenIn (String): CSP Token
  #      - context: Use User context. User must have permissoins to delete the dpeloyment. This will work from vRA 8.3 or vRA Cloud Oct/2020 release. 
  # [Dependency]
  #   - Requires: pyyaml,boto3,requests
  # [Subscription]
  #   - Event Topics:
  #      - deployment.request.post: Supports CREATE_DEPLOYMENT and UPDATE_DEPLOYMENT
  #   - Condition Filter: The abx_autoDeleteDeployment can optionaly be inserted in the Blueprint to allow us to exclude some deployments from the filter on a per deployment basis
  #      - event.data.requestInputs.abx_autoDeleteDeployment == "Yes"
  # [Blueprint]
  #   - Inputs (Optional) : When set to No in the Blueprint the actoin will not trigger based on the above Subscription Condition Filter
  #      - abx_autoDeleteDeployment:
  #          type: string
  #          description: Auto Delete Failed Deployment using casAutoDeleteDeployment-py ABX Action.
  #          default: 'No'
  #          title: Auto Delete (ABX)
  #          #format: hidden
  #          enum:
  #            - 'Yes'
  #            - 'No'
  # [Thanks]
  #


import json
import boto3
import requests
import urllib3
import time



# ----- Global ----- #  

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)   # Warned when making an unverified HTTPS request.
urllib3.disable_warnings(urllib3.exceptions.DependencyWarning)   # Warned when an attempt is made to import a module with missing optional dependencies. 
cspBaseApiUrl = "https://api.mgmt.cloud.vmware.com"    # CSP portal base url
cspApiVersion = "?$select=*&apiVersion=2019-09-12"  # CSP API Version

# ----- Functions  ----- # 

def handler(context, inputs):   # Action entry function.

    fn = " handler - "    # Funciton name 
    print("[ABX]"+fn+"Action started.")
    print("[ABX]"+fn+"Function started.")
    

    # ----- Action Options  ----- # 
    
    # General action options
    actionOptionTokenProvider = inputs['actionOptionTokenProviderIn'].lower()    # Values: inputs / context / awssm
    awsSmCspTokenSecretId = inputs['awsSmCspTokenSecretIdIn']   # TODO: Set in actin inputs if actionOptionUseAwsSecretsManagerIn=True  
    awsSmRegionName = inputs['awsSmRegionNameIn']   # TODO: Set in actin inputs if actionOptionUseAwsSecretsManagerIn=True    
    cspRefreshToken = inputs['cspRefreshTokenIn']    # TODO: Set in actin inputs if actionOptionUseAwsSecretsManagerIn=False
    eventType = ""  # Event Type for which aciton is running
    eventTopicId = ""   # Event Topic for which the aciton is running
    deploymentStatus = "" #
    
    # ----- Inputs  ----- #     
    deploymentId = inputs['deploymentIdABXIn']    #
    deleteDelay = inputs['deleteDelayIn']    #
    casBaseApiCallUrl = "/deployment/api/deployments/"    #


    # eventType 
    if (str(inputs).count('CREATE_DEPLOYMENT') == 1):
        eventType = "CREATE_DEPLOYMENT"
    elif (str(inputs).count('UPDATE_DEPLOYMENT') == 1):
        eventType = "UPDATE_DEPLOYMENT"
    elif (str(inputs).count("eventType") == 0):
        eventType = "TEST"
    else:
        eventType = "UNSUPPORTED"
    # End Loop
    
    # eventTopicId 
    if (str(inputs).count('deployment.request.post') == 1):
        eventTopicId = "deployment.request.post"
    elif (str(inputs).count("eventTopicId") == 0):
        eventTopicId = "TEST"
    else:
        eventTopicId = "UNSUPPORTED"
    # End Loop
    
    # deploymentStatus 
    if (str(inputs).count('FAILED') == 1):
        deploymentStatus = "FAILED"
    elif (str(inputs).count('CANCELED') == 1):
        deploymentStatus = "CANCELED"
    elif (str(inputs).count("status") == 0):
        deploymentStatus = "TEST"
    else:
        deploymentStatus = "UNSUPPORTED"
    # End Loop
    

    # actionInputs Hashtable
    actionInputs = {}  
    actionInputs['actionOptionTokenProvider'] = actionOptionTokenProvider
    actionInputs['awsSmCspTokenSecretId'] = awsSmCspTokenSecretId 
    actionInputs['awsSmRegionName'] = awsSmRegionName 
    actionInputs['cspRefreshToken'] = cspRefreshToken
    actionInputs['eventType'] = eventType
    actionInputs['eventTopicId'] = eventTopicId
    actionInputs['deploymentId'] = deploymentId
    actionInputs['deleteDelay'] = deleteDelay
    actionInputs['casBaseApiCallUrl'] = casBaseApiCallUrl
    actionInputs['casApiCallUrl'] = actionInputs['casBaseApiCallUrl']+actionInputs['deploymentId']
    actionInputs['deploymentStatus'] = deploymentStatus
    actionInputs['runOnEventTopic'] = ""
    

    # ----- Auth Provider ----- #     
    
    # Get Auth Provider
    if (actionInputs['actionOptionTokenProvider'] == "AWSSM".lower()):
        # AWS Secrets Manager
        print("[ABX]"+fn+"Auth/Secrets source: AWS Secrets Manager")
        awsRegionName = awsSmRegionName
        awsSecretId_csp = awsSmCspTokenSecretId
        awsSecrets = awsSessionManagerGetSecret (context, inputs, awsSecretId_csp, awsRegionName)  # Call function
        actionInputs['cspRefreshToken'] = awsSecrets['awsSecret_csp']
    elif (actionInputs['actionOptionTokenProvider'] == "context".lower()):
        # Request Context
        print("[ABX]"+fn+"Auth/Secrets source: Request Context")
    elif (actionInputs['actionOptionTokenProvider'] == "inputs".lower()):
        # Action Inputs
        print("[ABX]"+fn+"Auth/Secrets source: Action inputs")
    else:
        print("[ABX]"+fn+"Auth/Secrets source: UNDETERMINED")
    # End Loop
    

    # ----- CSP Token  ----- #     
    
    # Get Token
    if (actionInputs['actionOptionTokenProvider'] != "context".lower()):

        getAccessToken_apiUrl = cspBaseApiUrl + "/iaas/api/login"  # Set API URL
        body = {    # Set call body
            "refreshToken": actionInputs['cspRefreshToken']
        }
        print("[ABX]"+fn+"Getting CSP Access Token.")
        getAccessToken_postCall = requests.post(url = getAccessToken_apiUrl, data=json.dumps(body))   # Call 
        getAccessToken_responseJson = json.loads(getAccessToken_postCall.text)    # Get call response
        accessToken = getAccessToken_responseJson["token"]   # Set response
        requestsHeaders= {
            'Accept':'application/json',
            'Content-Type':'application/json',
            'Authorization': 'Bearer {}'.format(accessToken),
            # 'encoding': 'utf-8'
        }
        
        actionInputs['cspAccessToken'] = accessToken
        actionInputs['cspRequestsHeaders'] = requestsHeaders

    else:
        print("[ABX]"+fn+"Not using CSP Token due to actionOptionTokenProviderIn choice.")
        actionInputs['cspAccessToken'] = ""
        actionInputs['cspRequestsHeaders'] = ""
    # End Loop



    # replace any emptry , optional, "" or '' inputs with empty value 
    for key, value in actionInputs.items(): 
        if (("Optional".lower() in str(value).lower()) or ("empty".lower() in str(value).lower()) or ('""' in str(value).lower())  or ("''" in str(value).lower())):
            actionInputs[key] = ""
        else:
            print('')
    # End Loop
    
    
    # runOn Event Topic Inputs
    if (((actionInputs['eventType'] == "CREATE_DEPLOYMENT") or (actionInputs['eventType'] == "UPDATE_DEPLOYMENT")) and (actionInputs['eventTopicId'] == "deployment.request.post") and ((actionInputs['deploymentStatus'] == "FAILED") or (actionInputs['deploymentStatus'] == "CANCELED"))):
        actionInputs['runOnEventTopic'] = "true"
        
        actionInputs['deploymentId'] = inputs['deploymentId']
        actionInputs['casApiCallUrl'] = actionInputs['casBaseApiCallUrl']+actionInputs['deploymentId']
        
    elif ((actionInputs['eventType'] == "TEST") or (actionInputs['eventTopicId'] == "TEST") or (actionInputs['deploymentStatus'] == "TEST")):
        actionInputs['runOnEventTopic'] = "true"
        # use action inputs
    else:  
        actionInputs['runOnEventTopic'] = "false"
    # End Loop
        


    # Print actionInputs
    for key, value in actionInputs.items(): 
        if (("cspRefreshToken".lower() in str(key).lower()) or ("cspBearerToken".lower() in str(key).lower()) or ("cspAccessToken".lower() in str(key).lower()) or ("cspRequestsHeaders".lower() in str(key).lower()) or ("runOnPorpertyMatch".lower() in str(key).lower()) or ("runOnBlueprintOptionMatch".lower() in str(key).lower()) or ("cspApiTokenIn".lower() in str(key).lower())   ):
            print("[ABX]"+fn+"actionInputs[] - "+key+": OMITED")
        else:
            print("[ABX]"+fn+"actionInputs[] - "+key+": "+str(actionInputs[key]))
    # End Loop
    

    # ----- Evals ----- # 
    
    evals = {}  # Holds evals values
    
    # runOnEventTopic eval loop
    if (actionInputs['runOnEventTopic'] == "true"):
        evals['runOnEventTopic_eval'] = "true"
    elif (actionInputs['runOnEventTopic'] == "false"):
        evals['runOnEventTopic_eval'] = "false"
    else:
        evals['runOnEventTopic_eval'] = "Not Evaluated"
    # End Loop

    print("[ABX]"+fn+"runOnEventTopic_eval: " + evals['runOnEventTopic_eval'])        


    # ----- Function Calls  ----- # 
    
    if (evals['runOnEventTopic_eval'] == 'true'): 
        print("[ABX]"+fn+"Running myActionFunction...")
        resp_myActionFunction = myActionFunction (context, inputs, actionInputs, evals)     # Call function
    else:
        print("[ABX]"+fn+"runOn condition(s) NOT matched. Skipping action run.")
        resp_myActionFunction = ""
     
        
    # ----- Outputs ----- #
    
    resp_handler = {}   # Set function response 
    resp_handler = evals
    outputs = {   # Set action outputs
       "actionInputs": actionInputs,
       "resp_handler": resp_handler,
       "resp_myActionFunction": resp_myActionFunction,
    }
    print("[ABX]"+fn+"Function return: \n" + json.dumps(resp_handler))    # Write function responce to console  
    print("[ABX]"+fn+"Function completed.")     
    #print("[ABX]"+fn+"Action return: \n" +  json.dumps(outputs))    # Write action output to console     
    print("[ABX]"+fn+"Action completed.")     
    print("[ABX]"+fn+"P.S. Spas Is Awesome !!!")

    return outputs    # Return outputs 



def myActionFunction (context, inputs, actionInputs, evals):   # Main Function. 
    fn = " myActionFunction - "    # Holds the funciton name. 
    print("[ABX]"+fn+"Action started.")
    print("[ABX]"+fn+"Function started.")
    
    
    # ----- Script ----- #

    # ----- Execution ----- #
    print("[ABX]"+fn+"Sleeping for "+str(actionInputs['deleteDelay'])+" seconds...")  

    # Limit deleteDelay to 8 minutes    
    if (actionInputs['deleteDelay'] > 480):
        actionInputs['deleteDelay'] = 480
    else:
        print("")
        
    time.sleep(actionInputs['deleteDelay']) # Sleep 
    
    print("[ABX]"+fn+"Executing call ...")
    
    # Execute call
    if (actionInputs['actionOptionTokenProvider'] != "context".lower()):
        resp_callUrl = cspBaseApiUrl + actionInputs['casApiCallUrl'] + cspApiVersion
        resp_call = requests.delete(resp_callUrl, verify=False, headers=(actionInputs['cspRequestsHeaders']) )
        resp_json = json.loads(resp_call.text)
    elif (actionInputs['actionOptionTokenProvider'] == "context".lower()):
        resp_callUrl = actionInputs['casApiCallUrl']
        resp_call = context.request(resp_callUrl, 'DELETE', '') 
        resp_json = resp_call['content'] # also resp_call['headers']
    else:
        print("")
    
    print("[ABX]"+fn+"Call executed.")
    print("[ABX]"+fn+"Call responce:")
    print(resp_json)


    # ----- Outputs ----- #

    response = {    # Set action outputs
         "response_content": resp_json
    }
    #print("[ABX]"+fn+"Function return: \n" + json.dumps(response))    # Write function responce to console  
    print("[ABX]"+fn+"Function completed.")   
    
    return response    # Return response 
    # End Function    



def awsSessionManagerGetSecret (context, inputs, awsSecretId_csp, awsRegionName):  # Retrieves AWS Secrets Manager Secrets
    # Ref: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/secretsmanager.html
    fn = "awsSessionManagerGetSecret -"    # Holds the funciton name. 
    print("[ABX]"+fn+"Function started.")
    
    
    # ----- Script ----- #
        
    # Create a Secrets Manager client
    print("[ABX] "+fn+" AWS Secrets Manager - Creating session...")
    session = boto3.session.Session()
    sm_client = session.client(
        service_name='secretsmanager',
        region_name=awsRegionName
    )

    # Get Secrets
    print("[ABX]"+fn+"AWS Secrets Manager - Getting secret(s)...")
    resp_awsSecret_csp = sm_client.get_secret_value(
            SecretId=awsSecretId_csp
        )
    #print(awsSecret)
    awsSecret_csp = json.dumps(resp_awsSecret_csp['SecretString']).replace(awsSecretId_csp,'').replace("\\",'').replace('"{"','').replace('"}"','').replace('":"','')   # Cleanup the response to get just the secret

    # ----- Outputs ----- #
    
    response = {   # Set action outputs
        "awsSecret_csp" : str(awsSecret_csp)
        }
    print("[ABX] "+fn+" Function completed.")  
    
    return response    # Return response 
    # End Function  
