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
  #   - Connects to Microsoft Azure using PowerShell 
  # [Inputs]
  #   - azTenantIdIn (String): Azure Tenant ID  
  #   - azClientIdIn (String): Azure Client ID. Set username if using UN/PW auth
  #   - azClientSecretIn (String): Azure Client Secret. Set password if using UN/PW auth 
  # [Outputs]
  # [Subscription]
  # [Dependency]
  #   - AZ module <= 3.7.0
  #        @{
  #            'Az.Accounts' = '1.7.4'
  #        }
  # [Thanks]
  #    - Radostin Georgiev (https://www.linkedin.com/in/radostin-georgiev-1b4a9746) 
  #    - Angel Ivanov (https://www.linkedin.com/in/iwanow955/)
  #

Import-Module -Name 'Az.Accounts' -RequiredVersion '1.7.4'

# ----- Global ----- # 
# ----- Functions  ----- #  

function handler ($context, $payload) {    # Main Function. 
    $fn = "handler -"    # Var to hold the funciton name. Used for Write-Host 
    Write-Host "[ABX] $fn Action started."
    Write-Host "[ABX] $fn Function started."
    Write-Host "[ABX] $fn Running on:" $PSVersionTable.PSVersion
    
    
    # ----- Inputs  ----- #  
    
    $azTenantId = $payload.azTenantIdIn    # Tenant ID / Directory ID
    $azClientId = $payload.azClientIdIn    # App ID / Client ID. Set username if using UN/PW auth
    $azClientSecret = $payload.azClientSecretIn    # Value / Client Secret. Set password if using UN/PW auth 

    $actionInputs = @{      # Build actionInputs Object
        "azTenantId" = "$azTenantId";
        "azClientId" = "$azClientId" ;
        "azClientSecret" = "$azClientSecret";
    }
    
    # ----- Script ----- #
    # Main Action script block to run. 

    # Credential Object
    $secstr = New-Object -TypeName System.Security.SecureString    # Create new secure string object
    $actionInputs["azClientSecret"].ToCharArray() | ForEach-Object {$secstr.AppendChar($_)}   # Convert secret to array
    $cred = new-object -typename System.Management.Automation.PSCredential -argumentlist $actionInputs["azClientId"] , $secstr    # Create new credential object
    
    # Connect to Azure
    Write-Host "[ABX] $fn Connecting to Azure..."
    $resp_connectAzAccount = Connect-AzAccount -ServicePrincipal -Credential $cred -Tenant $actionInputs["azTenantId"]     # For username/password auth remove the ServicePrincipal switch
    Write-Host $resp_connectAzAccount
    
    
    # ----- Outputs ----- #
    
    $response = Get-AzSubscription  # Get Azure Subscription

    Write-Host $response    # Write action outputs to console   
    return $outputs    # Return outputs 
}   # End Function  