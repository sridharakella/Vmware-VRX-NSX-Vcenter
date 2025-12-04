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
  # [Info] 
  #   - Gets secret stored in AWS Secrets Manager
  # [Inputs]
  #   - awsRegionNameIn (String): AWS Secrets Manager Region Name e.g. us-west-2
  #   - awsSecretIdIn (String): AWS Secrets Manager Secret ID
  # [Outputs]
  #   - The AWS Secret Manager Secret
  #

import boto3
import json

def handler(context, inputs):  # Retrieves AWS Secrets Manager Secrets
    # Ref: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/secretsmanager.html
    fn = "handler -"    # Holds the funciton name. 
    print("[ABX] "+fn+" Function started.")
    
    
    # ----- Action Inputs  ----- #   
    
    awsSecretId = inputs['awsSecretIdIn'] # AWS Secrets Manager Secret ID
    awsRegionName = inputs['awsRegionNameIn']   # AWS Region where the Secret is stored e.g. "us-west-2"


    # ----- Script ----- #
        
    # Create a Secrets Manager client
    session = boto3.session.Session()
    sm_client = session.client(
        service_name='secretsmanager',
        region_name=awsRegionName
    )

    # Get Secrets
    print("[ABX] "+fn+" AWS Secrets Manager - Getting secret(s)...")
    resp_awsSecret = sm_client.get_secret_value(
            SecretId=awsSecretId
        )

    # Cleanup the response to get just the secret
    awsSecret = json.dumps(resp_awsSecret['SecretString']).replace(awsSecretId,'').replace("\\",'').replace('"{"','').replace('"}"','').replace('":"','')
    print(awsSecret)


    # ----- Outputs ----- #

    #resp_awsSecret = json.dumps(str(awsSecret))

    outputs = {   # Set action outputs
      "awsSecret": awsSecret
    }

    print("[ABX] "+fn+" Function completed.")  
    print("[ABX] "+fn+" Action completed.")     
    print("[ABX] "+fn+" P.S. Spas Is Awesome !!!")
    
    return response    # Return response 
    # End Function  
