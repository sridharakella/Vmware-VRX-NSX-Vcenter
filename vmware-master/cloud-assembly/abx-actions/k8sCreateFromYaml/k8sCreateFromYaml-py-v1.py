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
  #   - Runs a kubernetes yaml deployment form a yaml document(s):
  #   - Gives choice to use Namespace or Admin kubeconfig 
  #   - Further guidance can be found here: ABX Action to Deploy Kubernetes YAML Document via Cloud Template in Cloud Assembly (http://kaloferov.com/blog/skkb1058)
  #   - This uses the k8s-create-from-yaml Assembly Cloud Template from this repo. 
  # [Inputs]
  #   - cspRefreshTokenIn (String): VMware Cloud Service Portal (CSP) Token
  #   - actionOptionKubeconfigIn (String): Select the token provider for the action. This is from where the tokens will be read
  #      - admin: This uses an admin kubeconfig to authenticate to the Kubernetes cluster and run the YAML document. 
  #      - namespace: This uses an namespace kubeconfig to authenticate to the Kubernetes cluster and run the YAML document. This kubeconfig is limited to the scope of the namespace that was created as part of the blueprint deployment.
  # [Dependency]
  #   - Requires: requests,pyyaml,kubernetes
  # [Subscription]
  #   - Event Topics:
  #      - kubernetes.namespace.provision.post 
  # [Blueprint]
  #   - Requires a Blueprint that can be found with the Action
  #   - Inputs (Optional) : When set to No in the Blueprint the actoin will not trigger based on the above Subscription Condition Filter
  #      - yaml (Yaml): This provides the yaml document , or documents to be run by the ABX Action. 
  #      - actionOptionKubeconfig: (String): Select the kubeconfig to be used for the action. 
  #         - admin: This uses an admin kubeconfig to authenticate to the Kubernetes cluster and run the YAML document. 
  #         - namespace: This uses an namespace kubeconfig to authenticate to the Kubernetes cluster and run the YAML document. This kubeconfig is limited to the scope of the namespace that was created as part of the blueprint deployment.
  #         - abx: This uses the kubeconfig specified in the  actionOptionKubeconfigIn input property in the ABX Action. This allows the Cloud Template Editor to let the ABX Extensibility Editor to choose the kubeconfig file.
  # [Thanks]
  #   - Special Thanks to the following people for their work in the product and for providing me the skeleton  and idea for this action 
  #      - Lazarin Lazarov 
  #      - Teodor Raykov (https://www.linkedin.com/in/tedraykov/)
  #


import json
import requests
import urllib3
import uuid 
import yaml
import time
from kubernetes import client, config, utils
from kubernetes.utils import create_from_dict
from kubernetes.client import Configuration
from kubernetes.client.api import core_v1_api
#from kubernetes.client.rest import ApiException


# ----- Global ----- #  

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)   # Warned when making an unverified HTTPS request.
urllib3.disable_warnings(urllib3.exceptions.DependencyWarning)   # Warned when an attempt is made to import a module with missing optional dependencies. 
apiCspBaseUrl = 'https://api.mgmt.cloud.vmware.com'    # CSP portal base url
apiQueryParamsVersion = '&apiVersion=2020-01-30'    # API query param Version 
apiQueryParamsExpandResources = '?expand=resources'    # API query param to expand resoruces 


# ----- Functions  ----- # 

def handler(context, inputs):   # Action entry function.

    fn = " handler - "    # Funciton name 
    print("[ABX]"+fn+"Action started.")
    print("[ABX]"+fn+"Function started.")
    

    # ----- Inputs  ----- #    
    actionInputs = {}   # Hashtable holds variables and inputs
    actionInputs['cspRefreshToken'] = inputs['cspRefreshTokenIn']    # CSP Refresh Token
    actionInputs['actionOptionKubeconfig'] = inputs['actionOptionKubeconfigIn']     # Holds the choice for the kubeconfig file
    actionInputs['deploymentId'] = inputs['deploymentId']   # Deployment ID
    actionInputs['k8sYaml'] = ""    # K8s YAML document to be run
    actionInputs['k8skubeConfigNamespace'] = inputs['kubeConfig']   # Namespace Kubeconfig
    actionInputs['k8sNamespace'] = inputs['namespaceName']      # K8s Namespace
    actionInputs['uuid'] = uuid.uuid1()     # UUID based on the host ID and current time
    actionInputs['doNotihng'] = 0    # Used to close empty elif/else loops. 
    
    # Print actionInputs and ommit sensetive data
    for key, value in actionInputs.items(): 
        if (("cspRefreshToken".lower() in str(key).lower()) or 
            ("cspBearerToken".lower() in str(key).lower()) or 
            ("cspAccessToken".lower() in str(key).lower()) or 
            ("cspRequestsHeaders".lower() in str(key).lower()) or 
            ("runOnPorpertyMatch".lower() in str(key).lower()) or 
            ("runOnBlueprintOptionMatch".lower() in str(key).lower()) or 
            ("cspApiToken".lower() in str(key).lower())   ):
            print("[ABX]"+fn+"actionInputs[] - "+key+": OMITTED")
        else:
            print("[ABX]"+fn+"actionInputs[] - "+key+": "+str(actionInputs[key]))
    # End Loop
    
    
    # ----- Parameters  ----- #

    parameters = {}     # Parameters are used in Blueprints and replaced with values in ABX 
    parameters['ABX-Parameter-K8sNamespace'] = actionInputs['k8sNamespace']     # Namespace parametre and value to be replaced in payload/blueprint


    # ----- CSP Token  ----- #     
    
    # Get Access Token
    getAccessToken_apiUrl = apiCspBaseUrl + "/iaas/api/login"  # Set API URL
    body = {    # Set Call Body
        "refreshToken": actionInputs['cspRefreshToken']
    }
    print("[ABX]"+fn+"Getting CSP Access Token.")
    getAccessToken_postCall = requests.post(url = getAccessToken_apiUrl, data=json.dumps(body))   # Call 
    getAccessToken_responseJson = json.loads(getAccessToken_postCall.text)    # Get Call Response
    actionInputs['cspAccessToken'] = getAccessToken_responseJson["token"]   # Get Access Token
    actionInputs['cspRequestsHeaders'] = {      # Set Request Headers
        'Accept':'application/json',
        'Content-Type':'application/json',
        'Authorization': 'Bearer {}'.format(actionInputs['cspAccessToken']),
        # 'encoding': 'utf-8'
    }


    # ----- Function Calls  ----- # 

    print("[ABX]"+fn+"Running Functions...")
    resp_k8sCreateFromYamlFunction = k8sCreateFromYamlFunction (context, inputs, actionInputs, parameters)     # Call Function
    resp_k8sGetPodStatusFunction = k8sGetPodStatusFunction (context, inputs, actionInputs, parameters)     # Call Function
    resp_patchDeploymentFunction = patchDeploymentFunction (context, inputs, actionInputs, parameters)     # Call Function


    # ----- Outputs ----- #

    resp_json =  ''     # Holds function responce 

    outputs = {    # Set action outputs
         "resp_k8sCreateFromYamlFunction": resp_k8sCreateFromYamlFunction,
         "resp_k8sGetPodStatusFunction": resp_k8sGetPodStatusFunction,
         "resp_patchDeploymentFunction": resp_patchDeploymentFunction
    }
    
    #print("[ABX]"+fn+"Function return: \n" + json.dumps(response))    # Write function responce to console  
    print("[ABX]"+fn+"Function completed.")   

    return outputs    # Function Return 
    # End Function    




def k8sCreateFromYamlFunction (context, inputs, actionInputs, parameters):  # Create K8s deployment from Yaml

    fn = " k8sCreateFromYamlFunction - "    # Holds funciton name. 
    print("[ABX]"+fn+"Function started.")

    
    # ----- Script ----- #

    # Get Deployemt Info
    body = {}   # Set Call Body
    getDeployment_ApiUrl = apiCspBaseUrl + '/deployment/api/deployments/' + actionInputs['deploymentId'] + apiQueryParamsExpandResources + apiQueryParamsVersion    # Call 
    resp_getDeployment_call = requests.get(getDeployment_ApiUrl, data=json.dumps(body), verify=False, headers=(actionInputs['cspRequestsHeaders']))     # Get Call Response
    resp_getDeployment_json = json.loads(resp_getDeployment_call.text)      # Convert to JSON

    # Replace parameters in Deployment inputs
    print("[ABX]"+fn+"Updating Deployment Parameters...")
    #print(resp_getDeployment_json['inputs']['yaml'])
    getDeploymentInputsYaml_str = str(resp_getDeployment_json['inputs']['yaml'])
    for key, value in parameters.items(): 
        if (str(key) in getDeploymentInputsYaml_str):
            getDeploymentInputsYaml_str = getDeploymentInputsYaml_str.replace(key,value)
            break
        else:
            actionInputs['doNotihng']+=1
    # End Loop    
    resp_getDeployment_json['inputs']['yaml'] = json.dumps(getDeploymentInputsYaml_str.replace("'",'"'))    # Convert to YAML
    #resp_getDeployment_json = json.loads(resp_getDeployment_str.replace("'",'"'))      # Convert to JSON
    #print(resp_getDeployment_json)


    actionInputs['k8sYaml'] = resp_getDeployment_json['inputs']['yaml']
    actionInputs['k8sClusterId'] = resp_getDeployment_json['resources'][0]['properties']['clusterId']       # Cluster ID
    actionInputs['deploymentName'] = resp_getDeployment_json['name']        # Deployment Name
    
    # Check to see if triggered from Serice Broker. Description may be missing. 
    if (str(resp_getDeployment_json).count('description') == 1):
        actionInputs['deploymentDescription'] = resp_getDeployment_json['description']
    else:
        actionInputs['deploymentDescription'] = ''
    # End Loop

    # Get Admin kubeconfig
    actionInputs['cspRequestsHeaders_yaml'] = {     # Set Request Headers
        'Accept':'application/yaml',
        'Content-Type':'application/json',
        'Authorization': 'Bearer {}'.format(actionInputs['cspAccessToken']),
        # 'encoding': 'utf-8'
    }
    
    getKubeconfigForACluster_ApiUrl = apiCspBaseUrl + '/cmx/api/resources/k8s/clusters/' + actionInputs['k8sClusterId'] + '/kube-config?includeCredentials=true' + apiQueryParamsVersion    # Call
    resp_getKubeconfigForACluster_call = requests.get(getKubeconfigForACluster_ApiUrl, data=json.dumps(body) , verify=False, headers=(actionInputs['cspRequestsHeaders_yaml']))     # Call Response 
    resp_getKubeconfigForACluster_json = yaml.safe_load(resp_getKubeconfigForACluster_call.text)    # Convert to JSON
    actionInputs['k8skubeConfigAdmin_dict'] = resp_getKubeconfigForACluster_json    # Convert to Dict
    actionInputs['k8skubeConfigNamespace_dict'] = yaml.load(actionInputs['k8skubeConfigNamespace'], Loader=yaml.FullLoader) # Convert to Dict


    # Choose which kubeconfig to use based on bluepirnt and action inputs  
    if (str(resp_getDeployment_json['inputs']).count('actionOptionKubeconfig') == 1):
        print("[ABX]"+fn+"actionOptionKubeconfig found in blueprint.")        
        
        
        if (resp_getDeployment_json['inputs']['actionOptionKubeconfig'].lower() == 'admin'.lower()):
            actionInputs['k8skubeConfig_dict'] = actionInputs['k8skubeConfigAdmin_dict']
            print("[ABX]"+fn+"Using Blueprint actionOptionKubeconfig:"+resp_getDeployment_json['inputs']['actionOptionKubeconfig'])
        elif (resp_getDeployment_json['inputs']['actionOptionKubeconfig'].lower() == 'namespace'.lower()):
            actionInputs['k8skubeConfig_dict'] = actionInputs['k8skubeConfigNamespace_dict']
            print("[ABX]"+fn+"Using Blueprint actionOptionKubeconfig:"+resp_getDeployment_json['inputs']['actionOptionKubeconfig'])
        elif (resp_getDeployment_json['inputs']['actionOptionKubeconfig'].lower() == 'abx'.lower()):
            # Use ABX action inputs
            print("[ABX]"+fn+"Blueprint actionOptionKubeconfig:"+resp_getDeployment_json['inputs']['actionOptionKubeconfig'])
            print("[ABX]"+fn+"Using Action actionOptionKubeconfigIn action input: "+ actionInputs['actionOptionKubeconfig']) 
            
            if (actionInputs['actionOptionKubeconfig'].lower() == 'admin'.lower()):
                actionInputs['k8skubeConfig_dict'] = actionInputs['k8skubeConfigAdmin_dict']
            elif (actionInputs['actionOptionKubeconfig'].lower() == 'namespace'.lower()):
                actionInputs['k8skubeConfig_dict'] = actionInputs['k8skubeConfigNamespace_dict']
            else:
                print("[ABX]"+fn+"actionOptionKubeconfig actin input NOT valid") 
            # End Loop
            
        else:
            # Use ABX action inputs
            print("[ABX]"+fn+"Using Action actionOptionKubeconfigIn action input: "+ actionInputs['actionOptionKubeconfig']) 
        # End Loop
        
    elif (str(resp_getDeployment_json['inputs']).count('actionOptionKubeconfig') == 0):
        # Use ABX action inputs
        print("[ABX]"+fn+"Blueprint actionOptionKubeconfig NOT found.") 
        print("[ABX]"+fn+"Using Action actionOptionKubeconfigIn action input: "+ actionInputs['actionOptionKubeconfig']) 
        
        if (actionInputs['actionOptionKubeconfig'].lower() == 'admin'.lower()):
            actionInputs['k8skubeConfig_dict'] = actionInputs['k8skubeConfigAdmin_dict']
        elif (actionInputs['actionOptionKubeconfig'].lower() == 'namespace'.lower()):
            actionInputs['k8skubeConfig_dict'] = actionInputs['k8skubeConfigNamespace_dict']
        else:
            print("[ABX]"+fn+"actionOptionKubeconfig actin input NOT valid") 
        # End Loop
        
    else:
        actionInputs['doNotihng']+=1
    # End Loop


    # Load kubeconfig and create k8sClient
    config.load_kube_config_from_dict(actionInputs['k8skubeConfig_dict'])   # Load Kubeconfig
    k8sClient = client.ApiClient()      # Create API Client


    # Run Crete From YAML for each YAML Document. 
    k8sYamlDoc_array = yaml.safe_load(actionInputs['k8sYaml']).split("---")     # Split yaml documents into array mambers     
    for k8sYamlDoc in k8sYamlDoc_array:
      # actionInputs['k8sYamlDoc_dict'] = yaml.load(k8sYamlDoc, Loader=yaml.FullLoader) 
      actionInputs['k8sYamlDoc_dict'] = yaml.safe_load(k8sYamlDoc) 
      create_from_dict(k8sClient, actionInputs['k8sYamlDoc_dict'], namespace=actionInputs['k8sNamespace'])
      # alternative way to create from yaml
      #utils.create_from_yaml(k8sClient, actionInputs['k8sYaml'], namespace=actionInputs['k8sNamespace'])
    # End Loop
    
    
    # ----- Outputs ----- #
    
    resp_json = ''
    
    response = {   # Set function outputs
        "response" : resp_json
        }
        
    print("[ABX]"+fn+"Function completed.")  
    
    return response    # Function Return 
    # End Function  



def k8sGetPodStatusFunction (context, inputs, actionInputs, parameters):  # Get Pod Status

    fn = " k8sGetPodStatusFunction - "    # Holds funciton name. 
    print("[ABX]"+fn+"Function started.")

    
    # ----- Script ----- #

    # Elevate with Admin Kubeconfig to get pod status
    config.load_kube_config_from_dict(actionInputs['k8skubeConfigAdmin_dict'])   # Load Kubeconfig
    k8sClientV1 = client.CoreV1Api()      # Create API Client
    
    time.sleep(30)      # Sleep to give time to the pods to power up
    
    ret = k8sClientV1.list_pod_for_all_namespaces(watch=False)      # Ref https://raw.githubusercontent.com/kubernetes-client/python/master/kubernetes/docs/CoreV1Api.md
    actionInputs['k8sPod_status'] = {}      # holds status dor the pod(s)


    # Get Pod(s) Status
    print("[ABX]"+fn+"Listing pods with their IPs:")
    podCount_int = 0
    for item in ret.items:
        if (item.metadata.namespace == actionInputs['k8sNamespace']):
            actionInputs['k8sPod_status'].update({
                str(item.metadata.name): str(item.status.phase)
            })

            print(
            "%s\t%s\t%s\t%s" %
            (item.metadata.namespace,
             item.metadata.name,
             item.status.pod_ip,
             item.status.phase,))
            #print(str(item))
            podCount_int +=1
        else:
            actionInputs['doNotihng']+=1
        # End Loop    
    # End Loop    
    
    
    # Get total Pod(s) count
    actionInputs['k8sPod_status'].update({
        'podCount' : (podCount_int)
    })
    
    # Get overral Pod(s) health 
    if (str(actionInputs['k8sPod_status']).count('Running') == actionInputs['k8sPod_status']['podCount'] ):
        actionInputs['k8sPod_status'].update({
            'totalStatus' : 'Running'
        })
    else:
        actionInputs['k8sPod_status'].update({
            'totalStatus' : 'NOT_HEALTHY'
        })
    # End Loop
    
    print(actionInputs['k8sPod_status'])    

    # List Services for All namespaces and filter those for our namespace
    print("[ABX]"+fn+"Listing services for the namespace:")
    ret2 = k8sClientV1.list_service_for_all_namespaces()
    for item in ret2.items:
        if ((item.metadata.namespace == actionInputs['k8sNamespace']) and (item.spec.type == 'LoadBalancer')):
            actionInputs['k8sPodLb_hostname'] = item.status.load_balancer.ingress[0].hostname
            print(
            "%s\t%s" %
            (item.metadata.name,
             item.status.load_balancer.ingress[0].hostname))
        else:
            actionInputs['doNotihng']+=1
        # End Loop    
    # End Loop    

        
    # ----- Outputs ----- #

    response = {   # Set function outputs
        "totalStatus" : actionInputs['k8sPod_status']['totalStatus']
        }

    print("[ABX]"+fn+"Function completed.")  
    
    return response    # Function Return 
    # End Function  



def patchDeploymentFunction (context, inputs, actionInputs, parameters):  # Create K8s deployment from Yaml

    fn = " patchDeploymentFunction - "    # Holds funciton name. 
    print("[ABX]"+fn+"Function started.")

    
    # ----- Script ----- #

    body = {    # Call Body
        "description": str('LB: '+actionInputs['k8sPodLb_hostname']+', '+actionInputs['deploymentDescription']),
        "name": str(actionInputs['deploymentName']+'  (Pod: '+actionInputs['k8sPod_status']['totalStatus']+')')
        }
    patchDeployment_ApiUrl = apiCspBaseUrl + '/deployment/api/deployments/' + actionInputs['deploymentId']      # Call
    resp_patchDeployment_call = requests.patch(patchDeployment_ApiUrl, data=json.dumps(body), verify=False, headers=(actionInputs['cspRequestsHeaders']))    # Call Responce 
    resp_patchDeployment_json = json.loads(resp_patchDeployment_call.text)      # Convert to JSON

    print (resp_patchDeployment_json)

        
    # ----- Outputs ----- #
    resp_json = ''
    
    response = {   # Set function outputs
        "response" : resp_json
        }
        
    print("[ABX]"+fn+"Function completed.")  
    
    return response    # Function Return 
    # End Function  



