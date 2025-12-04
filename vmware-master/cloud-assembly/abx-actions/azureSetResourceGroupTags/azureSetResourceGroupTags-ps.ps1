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
  #   - Set Azure Resource Group Tags
  #   - Further guidance can be found here: ABX Action to Set a Tag to an Azure Resource Group (http://kaloferov.com/blog/skkb1049)
  # [Inputs]
  #   - azTenantIdIn (String): Azure Tenant ID  
  #   - azClientIdIn (String): Azure Client ID. Set username if using UN/PW auth
  #   - azClientSecretIn (String): Azure Client Secret. Set password if using UN/PW auth 
  #   - resourceGroupNameIn (String): Resource Group Name (e.g. groupa8010d4ff4b9a1be2a9f5cb2b12f1fae)
  #   - resourceGroupTagsIn (String): Resource Group Tags (e.g. key3,value3,key4,value4)
  #   - actionOptionAcceptPayloadInputIn (Boolean): 
  #      - True: Accept deployment payload inputs if present. Fallback is action input. 
  #      - False: Accept only action inputs  
  #   - actionOptionRunOnPropertyIn (Boolean): RunOn Condition acts as a wrapper for the action script. Can be used as an alternative and/or supplement Event Topic Condition filtering
  #      - True: Run action if property value is matched. 
  #      - False: Run action without matching property values.
  #   - runOnPorpertyIn (String): Destination property value for the match when actionOptionRunOnPropertyIn=True (e.g. cas.cloud.zone.type:azure)
  #   - runOnPropertyNameIn (String): Source payload property name , from which to get the value , for the match when actionOptionRunOnPropertyIn=True (e.g. cloudZoneProp)
  #   - runOnPorpertyMatchIn (String): Source payload property value for the match when actionOptionRunOnPropertyIn=True. Used just for testing without payload. (e.g. cas.cloud.zone.type:azure)
  # [Dependency]
  #   - AZ module <= 3.7.0
  #        @{
  #            'Az.Accounts' = '1.7.4'
  #            'Az.Resources' = '1.13.0'
  #            'Az.Storage' = '1.13.0'
  #        }
  # [Subscription]
  #   - Event Topic: compute.provision.post - Trigger on post provisioning
  #   - Condition: event.data.endpointId == "Cloud Assembly Azure Cloud Account ID" - Condition to trigger only for Azure cloud accounts 
  # [Thanks]
  #

Import-Module -Name 'Az.Accounts' -RequiredVersion '1.7.4'
Import-Module -Name 'Az.Resources' -RequiredVersion '1.13.0'
Import-Module -Name 'Az.Storage' -RequiredVersion '1.13.0'

# ----- Global ----- # 
# ----- Functions  ----- #  

function myActionFunction ($context, $payload, $actionInputs) {   # Function that runs the action task code
    $fn = "myActionFunction -"    # Var to hold the funciton name. Used for Write-Host 
    Write-Host "[ABX] $fn Function started."


    # ----- Inputs ----- #
    # Selects source for inputs based on action 
    # option inputs: pyaload or action inputs 
    
    if ($actionOptionAcceptPayloadInput -eq 'True')     # Loop. If Payload exists and Accept Payload input action option is set to True , accept payload inputs . Else except action inputs.
        {
            Write-Host "[ABX] $fn Using PAYLOAD inputs based on AcceptPayloadInput action option"
            $resourceGroupTags = $payload.customProperties.resourceGroupTagsProp    # Get Tags from payload
            $resourceGroupName = $payload.externalIds[0]    # Get externalIds containing the RG name from payload
            $resourceGroupName = $resourceGroupName.Split('/')    # Split externalIDs 
            
            $while_count = 0    # count var used within loop
            while($while_count -ne $resourceGroupName.Count)    # Loop. Get RG name from externalIds
                {
                    if($resourceGroupName[$while_count] -eq "resourcegroups")   # Loop. Find resourcegroups value
                        {
                            $while_count++
                            $resourceGroupName = $resourceGroupName[$while_count]   # Get array element after resourcegroups which is the RG Name
                            break 
                        } else {
                            $while_count++
                        }   # End Loop
                }   # End Loop
                
        } elseif ($actionOptionAcceptPayloadInput -eq 'False') {
            Write-Host "[ABX] $fn Using ACTION inputs based on acceptPayloadInput action option"
            $resourceGroupTags = $payload.resourceGroupTagsIn # Get Tags from action inputs
            $resourceGroupName = $payload.resourceGroupNameIn # Get RG name from action inputs
        } else {
            Write-Host "[ABX] $fn acceptPayloadInput: Invalid action option input"
        }   # End Loop

    $resourceGroupTags = $resourceGroupTags -replace "\\" -replace '[{}]' -replace '[\[\]]' -replace '"key":',''  -replace '"value":','' -replace '"','' -replace ':',','  -replace ';',',' # Strip until comma separated key,value pairs remain. eg. key1,value1,key2,value2 
    $resourceGroupTags = $resourceGroupTags.Split(',') # Split key/value pairs on comma
    Write-Host "[ABX] $fn resourceGroupName: " $resourceGroupName
    Write-Host "[ABX] $fn resourceGroupTags: " $resourceGroupTags


    # ----- Script ----- #
    # Main Action script block to run. 

    # Credential Object
    $secstr = New-Object -TypeName System.Security.SecureString    # Create new secure string object
    $actionInputs["azClientSecret"].ToCharArray() | ForEach-Object {$secstr.AppendChar($_)}   # Convert secret to array
    $cred = new-object -typename System.Management.Automation.PSCredential -argumentlist $actionInputs["azClientId"] , $secstr    # Create new credential object
    
    # Execution
    Write-Host "[ABX] $fn Connecting to Azure..."
    $resp_connectAzAccount = Connect-AzAccount -ServicePrincipal -Credential $cred -Tenant $actionInputs["azTenantId"]     # For username/password auth remove the ServicePrincipal switch
    $tagsHash = (Get-AzResourceGroup -Name $resourceGroupName ).Tags   # Create Tags Hashtable and add any existing tags

    $while_count = 0    # count var used within loop
    while($while_count -lt $resourceGroupTags.Count)    # Loop to add user tags to the Tags Hashtable
        {
            $tagsHash.add($resourceGroupTags[$while_count],$resourceGroupTags[$while_count+1])    # Add user defined tags to the existing tags
            $while_count = $while_count + 2    # Skip 2 values to get to the next key/value pair 
        }   # End Loop
    
    Write-Host "[ABX] $fn Setting Resource Group..."
    $resp_setAzResourceGroup = Set-AzResourceGroup -Name $resourceGroupName -Tag $tagsHash    # Set tags
    
    
    # ----- Outputs ----- #
    
    $response = @{ "resp_setAzResourceGroup" = "$resp_setAzResourceGroup"}   # Set response value
    Write-Host "[ABX] $fn Function return: `n" ($response | ConvertTo-Json)   # Write responce to console
    Write-Host "[ABX] $fn Function completed."  

    return $response    # Return respone
}   # End Function       



function handler ($context, $payload) {    # Main Function. Evaluates if action script should run based on RunOn Conditions
    $fn = "handler -"    # Var to hold the funciton name. Used for Write-Host 
    Write-Host "[ABX] $fn Action started."
    Write-Host "[ABX] $fn Function started."
    Write-Host "[ABX] $fn Running on:" $PSVersionTable.PSVersion
    
    
    # ----- Action Options  ----- #  
    
    $actionOptionAcceptPayloadInput = $payload.actionOptionAcceptPayloadInputIn    # If set to False inputs from deployment payload will be ignored in favor of action inputs. 
    $actionOptionRunOnProperty = $payload.actionOptionRunOnPropertyIn    # Run only if given constraint , passed via custom peorprty , matches azure endpoint. 
    $runOnPorperty = $payload.runOnPorpertyIn   # Property to match against when deciding weather to run the action or not. Alternative to Event Topic Condition filterring
    $runOnPropertyName = $payload.runOnPropertyNameIn   # <<< TODO: CHANGE for actionOptionRunOnPropertyIn=True >>> Source payload property name to match agains
    $runOnPorpertyMatch = ""    # Destination property value to match agians 


    # ----- Inputs  ----- #  
    
    $azTenantId = $payload.azTenantIdIn    # Tenant ID / Directory ID
    $azClientId = $payload.azClientIdIn    # App ID / Client ID. Set username if using UN/PW auth
    $azClientSecret = $payload.azClientSecretIn    # Value / Client Secret. Set password if using UN/PW auth 

    $actionInputs = @{      # Build actionInputs Object
        "azTenantId" = "$azTenantId";
        "azClientId" = "$azClientId" ;
        "azClientSecret" = "$azClientSecret";
    }


    # ----- RunOn Evals  ----- # 
    # Evaluates if action script should run based on RunOn
    # Conditions. 
    
    if (($actionOptionAcceptPayloadInput -eq 'True') -AND ($actionOptionRunOnProperty -eq "True"))    # Loop. Get property to match against. 
        {   
            $runOnPorpertyMatch = $payload.customProperties.$runOnPropertyName 
        } else {
            $runOnPorpertyMatch = $payload.runOnPorpertyMatchIn
        }   # End Loop
        
    Write-Host "[ABX] $fn runOnPropertyName: " $runOnPropertyName
    Write-Host "[ABX] $fn runOnPorperty: " $runOnPorperty
    Write-Host "[ABX] $fn runOnPorpertyMatch: " $runOnPorpertyMatch
    
    if ((($actionOptionRunOnProperty -eq "True") -AND ($runOnPorperty -eq $runOnPorpertyMatch)) -OR (($actionOptionRunOnProperty -eq "False")))   # Loop. Run only if property is matched. Alternative to Event Topic Condition filterring
        {
            $runOnProperty_eval = "RUN"
            Write-Host "[ABX] $fn runOnProperty_eval: " $runOnProperty_eval
            Write-Host "[ABX] $fn runOnProperty matched or RunOnProperty action option disabled."
            Write-Host "[ABX] $fn Running myActionFunction..."          
            $resp_myActionFunction = myActionFunction -context $context -payload $payload -actionInputs $actionInputs    # Run Function
        } else {
            $runOnProperty_eval = "DO_NOT_RUN"
            Write-Host "[ABX] $fn runOnProperty_eval: " $runOnProperty_eval
            Write-Host "[ABX] $fn Skipping action based on RunOnProperty action option."   
            $resp_myActionFunction = ""
        }   # End Loop
    
    
    # ----- Outputs  ----- # 

    $resp_handler = @{ "runOnProperty_eval" = "$runOnProperty_eval"}    # Set function response 
    $outputs = ($resp_handler + $resp_myActionFunction)   # Set action outputs 
    Write-Host "[ABX] $fn Function return: `n" ($resp_handler | ConvertTo-Json)    # Write function responce to console  
    Write-Host "[ABX] $fn Function completed."     
    Write-Host "[ABX] $fn Action return: `n" ($outputs | ConvertTo-Json)    # Write action outputs to console     
    Write-Host "[ABX] $fn Action completed."     
    Write-Host "[ABX] $fn P.S. Spas Is Awesome !!!"
    
    return $outputs    # Return outputs 
}   # End Function    




