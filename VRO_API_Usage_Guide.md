# VMware Aria Automation Orchestrator - API Usage Guide

## Overview
This guide explains how to call VRO workflows and actions programmatically using the REST API.

## Base URL
```
https://<orchestrator-server>/vco/api
```

## Authentication
Use Basic Authentication or OAuth2 token:
```bash
# Basic Auth
curl -u username:password https://orchestrator-server/vco/api/workflows

# OAuth2 Token
curl -H "Authorization: Bearer <token>" https://orchestrator-server/vco/api/workflows
```

## Common REST API Operations

### 1. List All Workflows
```bash
GET /vco/api/workflows

curl -X GET https://orchestrator-server/vco/api/workflows \
  -u username:password \
  -H "Accept: application/json"
```

### 2. Get Workflow Details
```bash
GET /vco/api/workflows/{workflow-id}

curl -X GET https://orchestrator-server/vco/api/workflows/{workflow-id} \
  -u username:password \
  -H "Accept: application/json"
```

### 3. Execute a Workflow
```bash
POST /vco/api/workflows/{workflow-id}/executions

# Example with parameters
curl -X POST https://orchestrator-server/vco/api/workflows/{workflow-id}/executions \
  -u username:password \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{
    "parameters": [
      {
        "name": "vmName",
        "type": "string",
        "value": {"string": {"value": "test-vm-01"}}
      },
      {
        "name": "cpuCount",
        "type": "number",
        "value": {"number": {"value": 4}}
      }
    ]
  }'
```

### 4. Get Workflow Execution Status
```bash
GET /vco/api/workflows/{workflow-id}/executions/{execution-id}

curl -X GET https://orchestrator-server/vco/api/workflows/{workflow-id}/executions/{execution-id} \
  -u username:password \
  -H "Accept: application/json"
```

### 5. Get Workflow Execution Logs
```bash
GET /vco/api/workflows/{workflow-id}/executions/{execution-id}/logs

curl -X GET https://orchestrator-server/vco/api/workflows/{workflow-id}/executions/{execution-id}/logs \
  -u username:password \
  -H "Accept: application/json"
```

### 6. Cancel Workflow Execution
```bash
DELETE /vco/api/workflows/{workflow-id}/executions/{execution-id}

curl -X DELETE https://orchestrator-server/vco/api/workflows/{workflow-id}/executions/{execution-id} \
  -u username:password
```

### 7. List Actions
```bash
GET /vco/api/actions

curl -X GET https://orchestrator-server/vco/api/actions \
  -u username:password \
  -H "Accept: application/json"
```

### 8. Execute an Action
```bash
POST /vco/api/actions/{action-id}/executions

curl -X POST https://orchestrator-server/vco/api/actions/{action-id}/executions \
  -u username:password \
  -H "Content-Type: application/json" \
  -d '{
    "parameters": [
      {
        "name": "inputParam",
        "type": "string",
        "value": {"string": {"value": "test-value"}}
      }
    ]
  }'
```

### 9. Import Package
```bash
POST /vco/api/packages

curl -X POST https://orchestrator-server/vco/api/packages \
  -u username:password \
  -H "Content-Type: application/zip" \
  --data-binary @package.package
```

### 10. Export Package
```bash
GET /vco/api/packages/{package-id}

curl -X GET https://orchestrator-server/vco/api/packages/{package-id} \
  -u username:password \
  -H "Accept: application/zip" \
  -o exported-package.package
```

## Python Example - Execute Workflow

```python
import requests
import json
import time

class VROClient:
    def __init__(self, server, username, password):
        self.server = server
        self.auth = (username, password)
        self.base_url = f"https://{server}/vco/api"
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
    
    def get_workflows(self):
        """List all workflows"""
        response = requests.get(
            f"{self.base_url}/workflows",
            auth=self.auth,
            headers=self.headers,
            verify=False  # Use verify=True with proper SSL cert
        )
        return response.json()
    
    def get_workflow_by_name(self, workflow_name):
        """Find workflow by name"""
        workflows = self.get_workflows()
        for workflow in workflows.get('link', []):
            if workflow_name in workflow.get('attributes', [{}])[0].get('value', ''):
                return workflow['href'].split('/')[-1]
        return None
    
    def execute_workflow(self, workflow_id, parameters=None):
        """Execute a workflow with parameters"""
        payload = {"parameters": parameters or []}
        
        response = requests.post(
            f"{self.base_url}/workflows/{workflow_id}/executions",
            auth=self.auth,
            headers=self.headers,
            data=json.dumps(payload),
            verify=False
        )
        return response.json()
    
    def get_execution_status(self, workflow_id, execution_id):
        """Get workflow execution status"""
        response = requests.get(
            f"{self.base_url}/workflows/{workflow_id}/executions/{execution_id}",
            auth=self.auth,
            headers=self.headers,
            verify=False
        )
        return response.json()
    
    def wait_for_completion(self, workflow_id, execution_id, timeout=300):
        """Wait for workflow execution to complete"""
        start_time = time.time()
        while time.time() - start_time < timeout:
            status = self.get_execution_status(workflow_id, execution_id)
            state = status.get('state')
            
            if state in ['completed', 'failed', 'canceled']:
                return status
            
            time.sleep(5)
        
        raise TimeoutError(f"Workflow execution timed out after {timeout} seconds")

# Usage Example
if __name__ == "__main__":
    # Initialize client
    vro = VROClient(
        server="orchestrator.example.com",
        username="admin",
        password="password"
    )
    
    # Find workflow
    workflow_id = vro.get_workflow_by_name("Create Virtual Machine")
    
    # Define parameters
    parameters = [
        {
            "name": "vmName",
            "type": "string",
            "value": {"string": {"value": "test-vm-01"}}
        },
        {
            "name": "cpuCount",
            "type": "number",
            "value": {"number": {"value": 4}}
        },
        {
            "name": "memoryMB",
            "type": "number",
            "value": {"number": {"value": 8192}}
        }
    ]
    
    # Execute workflow
    execution = vro.execute_workflow(workflow_id, parameters)
    execution_id = execution['id']
    
    print(f"Workflow execution started: {execution_id}")
    
    # Wait for completion
    result = vro.wait_for_completion(workflow_id, execution_id)
    
    print(f"Workflow completed with state: {result['state']}")
```

## PowerShell Example - Execute Workflow

```powershell
# VRO REST API Client in PowerShell

$vroServer = "orchestrator.example.com"
$username = "admin"
$password = "password"

# Create credential
$securePassword = ConvertTo-SecureString $password -AsPlainText -Force
$credential = New-Object System.Management.Automation.PSCredential($username, $securePassword)

# Base URL
$baseUrl = "https://$vroServer/vco/api"

# Ignore SSL certificate (for testing only)
add-type @"
    using System.Net;
    using System.Security.Cryptography.X509Certificates;
    public class TrustAllCertsPolicy : ICertificatePolicy {
        public bool CheckValidationResult(
            ServicePoint srvPoint, X509Certificate certificate,
            WebRequest request, int certificateProblem) {
            return true;
        }
    }
"@
[System.Net.ServicePointManager]::CertificatePolicy = New-Object TrustAllCertsPolicy

# Get all workflows
function Get-VROWorkflows {
    $uri = "$baseUrl/workflows"
    $response = Invoke-RestMethod -Uri $uri -Method Get -Credential $credential -ContentType "application/json"
    return $response
}

# Execute workflow
function Start-VROWorkflow {
    param(
        [string]$WorkflowId,
        [array]$Parameters
    )
    
    $uri = "$baseUrl/workflows/$WorkflowId/executions"
    
    $body = @{
        parameters = $Parameters
    } | ConvertTo-Json -Depth 10
    
    $response = Invoke-RestMethod -Uri $uri -Method Post -Credential $credential `
        -ContentType "application/json" -Body $body
    
    return $response
}

# Get execution status
function Get-VROExecutionStatus {
    param(
        [string]$WorkflowId,
        [string]$ExecutionId
    )
    
    $uri = "$baseUrl/workflows/$WorkflowId/executions/$ExecutionId"
    $response = Invoke-RestMethod -Uri $uri -Method Get -Credential $credential
    return $response
}

# Example usage
$workflows = Get-VROWorkflows
$workflowId = "your-workflow-id"

$parameters = @(
    @{
        name = "vmName"
        type = "string"
        value = @{
            string = @{
                value = "test-vm-01"
            }
        }
    },
    @{
        name = "cpuCount"
        type = "number"
        value = @{
            number = @{
                value = 4
            }
        }
    }
)

$execution = Start-VROWorkflow -WorkflowId $workflowId -Parameters $parameters
Write-Host "Execution started: $($execution.id)"

# Wait for completion
do {
    Start-Sleep -Seconds 5
    $status = Get-VROExecutionStatus -WorkflowId $workflowId -ExecutionId $execution.id
    Write-Host "Current state: $($status.state)"
} while ($status.state -notin @('completed', 'failed', 'canceled'))

Write-Host "Workflow finished with state: $($status.state)"
```

## Common Parameter Types

### String
```json
{
  "name": "paramName",
  "type": "string",
  "value": {"string": {"value": "myString"}}
}
```

### Number
```json
{
  "name": "paramName",
  "type": "number",
  "value": {"number": {"value": 100}}
}
```

### Boolean
```json
{
  "name": "paramName",
  "type": "boolean",
  "value": {"boolean": {"value": true}}
}
```

### Array
```json
{
  "name": "paramName",
  "type": "Array/string",
  "value": {
    "array": {
      "elements": [
        {"string": {"value": "item1"}},
        {"string": {"value": "item2"}}
      ]
    }
  }
}
```

### VC:VirtualMachine (vCenter object)
```json
{
  "name": "vm",
  "type": "VC:VirtualMachine",
  "value": {
    "sdk-object": {
      "type": "VC:VirtualMachine",
      "id": "vm-123"
    }
  }
}
```

## Error Handling

Always check for errors in responses:

```python
def execute_workflow_safe(self, workflow_id, parameters):
    try:
        response = requests.post(
            f"{self.base_url}/workflows/{workflow_id}/executions",
            auth=self.auth,
            headers=self.headers,
            data=json.dumps({"parameters": parameters}),
            verify=False
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e}")
        print(f"Response: {e.response.text}")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None
```

## Best Practices

1. **Use SSL Certificates**: Always verify SSL in production (set `verify=True`)
2. **Authentication**: Use OAuth2 tokens instead of basic auth for production
3. **Error Handling**: Always implement proper error handling
4. **Timeouts**: Set appropriate timeouts for long-running workflows
5. **Logging**: Log all API calls for debugging and audit purposes
6. **Rate Limiting**: Respect API rate limits
7. **Async Execution**: For long workflows, use async patterns to avoid blocking

## Useful API Endpoints Reference

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/workflows` | GET | List all workflows |
| `/workflows/{id}` | GET | Get workflow details |
| `/workflows/{id}/executions` | POST | Execute workflow |
| `/workflows/{id}/executions/{exec-id}` | GET | Get execution status |
| `/workflows/{id}/executions/{exec-id}/logs` | GET | Get execution logs |
| `/workflows/{id}/executions/{exec-id}` | DELETE | Cancel execution |
| `/actions` | GET | List all actions |
| `/actions/{id}/executions` | POST | Execute action |
| `/packages` | GET | List packages |
| `/packages` | POST | Import package |
| `/packages/{id}` | GET | Export package |

## Documentation Links

- Official REST API Guide: https://techdocs.broadcom.com/vmware-cis/aria/aria-automation/
- API Explorer: Available in Orchestrator Client under API Explorer menu
