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
  #   - Action posts Cloud Assembly deployment info in a Slack channel via Webhook.
  #   - It posts IP Address and Resource Name. 
  #   - Can be tested from within the ABC Action without deployment payload
  # [Inputs]
  #   - slackHookIn (String): Slack Webhook Url
  #   - slackAttColorIn (String): color value
  #   - slackAttFallbackIn (String): fallback value
  #   - slackAttAuthorIconIn (String): Author icon value (e.g http://gitlab.elasticskyholdings.com/class-delivery/lab-files/raw/master/images/tito-v2-app-icon.png)
  #   - slackAttAuthorLinkIn (String): Author link value (e.g http://gitlab.elasticskyholdings.com/class-delivery/tito)
  #   - slackAttAuthorNameIn (String): Author name value 
  # [Outputs]
  # [Dependency]
  #   - requests,datetime
  # [Subscription]
  #   - Event Topics:
  #      - compute.provision.post  
  # [Thanks]
  #

import requests
import json
import datetime

# ----- Global ----- # 
# ----- Functions  ----- # 

def handler(context, inputs):   # Function posts to Slack

    fn = "handler -"    # Holds the funciton name. 
    print("[ABX] "+fn+" Action started.")
    print("[ABX] "+fn+" Function started.")
   
    # ----- Inputs ----- #
    
    slackHook = inputs["slackHookIn"]   # Slack Webhook Url
    slackAttFallback = inputs["slackAttFallbackIn"]   # fallback value
    slackAttColor = inputs["slackAttColorIn"]   # color value
    slackAttAuthorName = inputs["slackAttAuthorNameIn"]   # Author name value
    slackAttAuthorLink = inputs["slackAttAuthorLinkIn"]   # Author link value (e.g http://gitlab.elasticskyholdings.com/class-delivery/tito)
    slackAttAuthorIcon = inputs["slackAttAuthorIconIn"]   # Author link value (e.g http://gitlab.elasticskyholdings.com/class-delivery/lab-files/raw/master/images/tito-v2-app-icon.png)
    
    actionInputs = {}
    actionInputs['slackHook'] = slackHook
    actionInputs['slackAttFallback'] = slackAttFallback
    actionInputs['slackAttColor'] = slackAttColor
    actionInputs['slackAttAuthorName'] = slackAttAuthorName
    actionInputs['slackAttAuthorLink'] = slackAttAuthorLink
    actionInputs['slackAttAuthorIcon'] = slackAttAuthorIcon
    
    # replace any <emptry> or <optional> inputs with empty value 
    for key, value in actionInputs.items(): 
        if (("Optional".lower() in value.lower()) or ("empty".lower() in value.lower()) or ('""'.lower() in value.lower())  or ("''".lower() in value.lower())):
            actionInputs[key] = ""
        else:
            print('')
    
    # ----- Script ----- #
        
    now = datetime.datetime.now()   # Gets Date & time 
    
    if ( (str(inputs).count("resourceNames") != 0) and (str(inputs).count("addresses") != 0) ):
        slackMsg = '*Name:* {0} \n *IP Address:* {1} \n *Date:* {2}'.format(inputs["resourceNames"][0], inputs["addresses"][0], now.strftime("%Y-%m-%d %H:%M"))    # Sets the Slack message
    else:
        slackMsg = "No Deployment Payload, but <http://www.kaloferov.com/|Spas Is Awsome>"
        
    #print("[ABX] "+fn+" Slack message: "+slackMsg)  
    actionInputs['slackMsg'] = slackMsg     # Slack message

    body = {    # Set Call body attachments
     "attachments": [
         {
             "fallback": actionInputs['slackAttFallback'],
             "color": actionInputs['slackAttColor'],
             "text" : actionInputs['slackMsg'] ,
             "author_name": actionInputs['slackAttAuthorName'],
             "author_link": actionInputs['slackAttAuthorLink'],
             "author_icon": actionInputs['slackAttAuthorIcon']
         }
     ]
    }
    
    requests.post(actionInputs['slackHook'], data=json.dumps(body), verify=False, headers="")    # Call
    
    # ----- Outputs ----- #
    
    response = {   # Set action outputs
         "slackMsg" : actionInputs['slackMsg']
         }
         
    print("[ABX] "+fn+" Function completed.")   
    print("[ABX] "+fn+" Action completed.")     
    print("[ABX] "+fn+" P.S. Spas Is Awesome !!!")
   
    return response    # Return response 
    # End Function    

