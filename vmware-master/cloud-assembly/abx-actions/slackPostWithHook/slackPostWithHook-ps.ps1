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
  # [Outputs]
  # [Dependency]
  # [Subscription]
  #   - Event Topics:
  #      - compute.provision.post  
  # [Thanks]
  #   - Radostin Georgiev (https://www.linkedin.com/in/radostin-georgiev-1b4a9746) 
  #


# ----- Global ----- # 
# ----- Functions  ----- # 

function handler($context, $payload) {   # Function posts to Slack

    $fn = "handler -"    # Holds the funciton name. 
    Write-Host "[ABX] "+$fn+" Action started."
    Write-Host "[ABX] "+$fn+" Function started."

    # ----- Inputs ----- #
    
    $slackHook = $payload.slackHookIn    # Slack Webhook Url
    $slackContentType = "application/json"
    $slackMethod = "POST"    # Rest method
    $slackHeaders = @{"cookie"="Cookie"}    # Call Header
    $slackAttFallback = $payload.slackAttFallbackIn    # Attachment fallback
    $slackAttColor = $payload.slackAttColorIn    # Attachment color
    $slackAttAuthorName = $payload.slackAttAuthorNameIn    # Attachment author name
    $slackAttAuthorLink = $payload.slackAttAuthorLinkIn    # Attachment author link
    $slackAttAuthorIcon = $payload.slackAttAuthorIconIn    # Attachment author icon

    $actionInputs = @{}
    $actionInputs.Add("slackHook", $slackHook)
    $actionInputs.Add("slackContentType", $slackContentType)
    $actionInputs.Add("slackMethod", $slackMethod)
    $actionInputs.Add("slackHeaders", $slackHeaders)
    $actionInputs.Add("slackAttFallback", $slackAttFallback)
    $actionInputs.Add("slackAttColor", $slackAttColor)
    $actionInputs.Add("slackAttAuthorName", $slackAttAuthorName)
    $actionInputs.Add("slackAttAuthorLink", $slackAttAuthorLink)
    $actionInputs.Add("slackAttAuthorIcon", $slackAttAuthorIcon)

    
    # ----- Script ----- #


    # Enables to test action without payload
    if ( ($payload.resourceNames.Count -gt 0) -or ($payload.addresses.Count -gt 0) ) {
        $slackMsg = "*Name:* " + $payload.resourceNames[0] + "`n *IP Address:* " + $payload.addresses[0]
    } else {
        $slackMsg = "No Deployment Payload, but <http://www.kaloferov.com/|Spas Is Awsome>"
    }

    $actionInputs.Add("slackMsg", $slackMsg)
    Write-Host "[ABX] "+$fn+" Slack message: " + $actionInputs["slackMsg"]
    
    # Body
    $body = ConvertTo-Json @{
        fallback = $actionInputs["slackAttFallback"]
        color = $actionInputs["slackAttColor"]
        text = $actionInputs["slackMsg"]
        author_name = $actionInputs["slackAttAuthorName"]
        author_link = $actionInputs["slackAttAuthorLink"]
        author_icon = $actionInputs["slackAttAuthorIcon"]
    }
    
    
    # Alternatively you can use Invoke-RestMethod and [void]() to suppress output 
    # e.g. $response = Invoke-WebRequest -Uri $url -Headers $headers -Method $method -ContentType $contentType -Body $body
    $slack_resp = Invoke-RestMethod -ContentType $actionInputs["slackContentType"] -Uri $actionInputs["slackHook"] -Headers $actionInputs["slackHeaders"] -Method $actionInputs["slackMethod"] -Body $body -UseBasicParsing    # Call
    
    # ----- Outputs ----- #
    
    $outputs = @{}
    $outputs.Add("slack_resp", $slack_resp)
    
    Write-Host "[ABX] "+$fn+" Message has been sent."
    Write-Host "[ABX] "+$fn+" Function return:" + $outputs
    Write-Host "[ABX] "+$fn+" Function completed."
    Write-Host "[ABX] "+$fn+" Action completed."
    Write-Host "[ABX] "+$fn+" P.S. Spas Is Awesome !!!"
    
    return $outputs    # Return response 
}   # End Function    

