## HANDS-ON-010: Implementing MLOps Pipeline using GitHub, CodePipeline, CodeBuild, CodeDeploy, Sagemaker Endpoint

This sample shows:
- how to create MLOps Pipeline 
- how to use GitHub Hooks (Getting Source Code from Github to CodePipeline)
- how to create Build CodePipeline (Source, Build), CodeBuild (modelbuild_buildspec.yml), Deploy CodePipeline (Source, Build, DeployStaging, DeployProd), CodeBuild (modeldeploy_buildspec.yml)
- how to save the model and artifacts on S3
- how to create and test models using Notebooks

**Notes:**
- Original Source code was pulled, updated, and adapted:
  - https://github.com/aws-samples/aws-mlops-pipelines-terraform
- "Modelbuild_Pipeline" and "Modeldeploy_Pipeline" are uploaded before. After applying terraform, Webhook in the CodePipeline pulls it from GitHub to inject it into AWS.
- If you run it the first time, please open to request to AWS for the instance: "ml.m5.xlarge" ("ResourceLimitExceeded").
  - https://repost.aws/knowledge-center/sagemaker-resource-limit-exceeded-error  

**Code:** https://github.com/omerbsezer/Fast-AWS/tree/main/hands-out-labs-code/hands-on-010-mlops-sagemaker-github-codepipeline-codebuild-codedeploy


**Architecture:**
- **Model Build Pipeline Source Code, modelbuild_pipeline:**  https://github.com/omerbsezer/modelbuild_pipeline 
- **Model Deploy Pipeline Source Code, modeldeploy_pipeline:** https://github.com/omerbsezer/modeldeploy_pipeline
- AWS Code Pipeline for **Model Build** (CI):
  - AWS Code Pipeline (**modelbuild_ci_pipeline.tf**)
    - Stage: Source (Hook from GitHub: **modelbuild_hooks.tf**)
    - Stage: Build (**modelbuild_codebuild.tf: artifacts, environment, source (modelbuild_buildspec.yml: run build pipeline)**)
  - Sagemaker Data Pipeline (**modelbuild_pipeline project: pipeline.py**):
    - Preprocessing Step (**modelbuild_pipeline project: pipeline.py => preprocess.py**)
    - Model Training Step (**modelbuild_pipeline project: pipeline.py => XGB BuiltIn Container**)
    - Evaluation Step (**modelbuild_pipeline project: pipeline.py => evaluate.py, ConditionStep to evaluate model quality**)
    - Registering Model Step (**modelbuild_pipeline project: pipeline.py => RegisterModel**)
- AWS Code Pipeline for **Model Deploy** (CD):
  - AWS Code Pipeline (**modeldeploy_cd_pipeline.tf**)
    - Stage: Source (Hook from GitHub: **modeldeploy_hooks.tf**)
    - Stage: Build (**modeldeploy_codebuild.tf: artifacts, environment, source (modeldeploy_buildspec.yml: run deploy pipeline => modeldeploy_pipeline project: build.py,  cloud formation to create endpoint)**)  
    - Stage: DeployStaging:
      - Action: Deploy (**Cloudformation, DeployResourcesStaging: modeldeploy_pipeline project => endpoint-config-template.yml**)
      - Action: Build (**Test Staging: modeldeploy_testbuild.tf => modeldeploy_pipeline project: test/test_buildspec.yml**)
      - Action: Approval (**Manual Approval by User**)
    - Stage: DeployProd:
      - Action: Deploy (**Cloudformation, DeployResourcesProd: modeldeploy_pipeline project => endpoint-config-template.yml**)
- Notebooks (for testing) (region: us-east-1)
  - End2end.ipynb
    - https://github.com/omerbsezer/Fast-AWS/tree/main/hands-out-labs-code/hands-on-010-mlops-sagemaker-github-codepipeline-codebuild-codedeploy/Notebooks/SageMaker_Customer_Churn_XGB_end2end.ipynb
  - Pipeline.ipynb (Sagemaker Data Pipeline)
    - https://github.com/omerbsezer/Fast-AWS/tree/main/hands-out-labs-code/hands-on-010-mlops-sagemaker-github-codepipeline-codebuild-codedeploy/Notebooks/SageMaker_Customer_Churn_XGB_Pipeline.ipynb  

   ![image](https://github.com/user-attachments/assets/fa30614b-b4da-4fcc-b901-4b83bbee9440)



## Steps
- Before running Terraform, upload "Modelbuild_Pipeline" and "Modeldeploy_Pipeline" in your GitHub account.
- Run:

```
cd terraform
terraform init
terraform validate
terraform plan
terraform apply
```

- After run:

  ![image](https://github.com/user-attachments/assets/7f03d6ab-f176-4388-96e9-d8e4683cd4f2)

- AWS CodePipeline:

  ![image](https://github.com/user-attachments/assets/5f33dcf1-f947-4be2-a501-826b378f44e9)

- ModelBuild:

  ![image](https://github.com/user-attachments/assets/50fd021e-7ec3-49fd-8937-8f00edb0f848)

- ModelBuild Log:

  ![image](https://github.com/user-attachments/assets/7e75b306-b694-4824-af0e-ecfc91d96d4f)
  
- AWS S3:

  ![image](https://github.com/user-attachments/assets/42293444-0406-4dee-9b91-377043a1c4cc)

- ModelBuild was done successfully:

  ![image](https://github.com/user-attachments/assets/7d40ba8c-9c31-423f-953a-f595513346fc)

- CloudWatch to see the training accuracy:

  ![image](https://github.com/user-attachments/assets/b018d451-3bd8-40cf-b10f-0d774d8a1278)

- CloudWatch, Log Groups, Train Error:

  ![image](https://github.com/user-attachments/assets/58dd3f7e-10e5-4c59-8653-0968c0d6f16f)
    
- ModelDeploy:

  ![image](https://github.com/user-attachments/assets/d183d1c7-c414-43be-b8e7-d47212b05a3a)

  ![image](https://github.com/user-attachments/assets/198605ed-5ef4-4144-b7ef-d77b40af8db2)

- CloudFormation, stack: deploy-staging

  ![image](https://github.com/user-attachments/assets/46fac961-e1ea-4cbf-9c69-c07ab315f0f1)

- SageMaker Dashboard, staging endpoint in service:

  ![image](https://github.com/user-attachments/assets/f29b06f3-a3ac-4bee-94c0-553faf9781de)

- SageMaker, Model:

  ![image](https://github.com/user-attachments/assets/dda681f0-9d11-461e-a2ca-b7208f183b33)

- S3, Model, possible to download:

  ![image](https://github.com/user-attachments/assets/fc7ff989-c062-4628-b22a-42139fa0dd78)

- Try Staging Endpoint with notebook (end2end.ipynb, last cell, enter the endpointname):

```
import pandas as pd
import numpy as np
import sagemaker
import boto3
from sagemaker import get_execution_role

test_data=pd.read_csv('test.csv',header=None)
testdata1=test_data.iloc[0:1,1:]

runtime = boto3.client("sagemaker-runtime")
Endpoint_name='aws-ml-11052023-staging-0306' #<your endpoint name> # update to your own endpoint name

prediction = runtime.invoke_endpoint(
    EndpointName=Endpoint_name,
    Body=testdata1.to_csv(header=False, index=False).encode("utf-8"),
    ContentType="text/csv",
    Accept= "text/csv",
)

print(prediction["Body"].read())
```
- Endpoint returned the result:

  ![image](https://github.com/user-attachments/assets/aeb825c3-c984-4250-ab28-c3a874aaa4b2)

- Approve the Product on the CodePipeline:

  ![image](https://github.com/user-attachments/assets/ae0fafd9-3927-487d-8b75-a3f83f06eb3d)

- SageMaker Dashboard, 2 Endpoints are in-service:

  ![image](https://github.com/user-attachments/assets/08273ef3-87f5-4a5d-9d3f-172688a01494)

- SageMaker, Prod Endpoint:

  ![image](https://github.com/user-attachments/assets/1f2d2d4a-aa8d-40f7-8c1d-fec01fb4f797)

- CloudFormation:

  ![image](https://github.com/user-attachments/assets/359fe99a-ce4b-4da7-b512-11f61c658c58)

- Test Prod Endpoint, returns results:

  ![image](https://github.com/user-attachments/assets/d3206658-30c0-4c67-9e79-4039e08222d7)

- Delete Endpoints manually, if the endpoints are in-service, you have to pay their cost:

  ![image](https://github.com/user-attachments/assets/62ba639f-58e9-41ce-95cd-7de418c7cc39)

- Delete stacks manually in Cloudformation.
- Download artifacts on S3:

```
aws s3 sync s3://artifact-ml-11052023 C:\Users\oesezer\Desktop\aws-artifacts
```

- Downloaded to the local PC:

  ![image](https://github.com/user-attachments/assets/d6e51324-929c-4b84-b403-2ec3b40e12fd)

- Destroy with "terraform destroy":

  ![image](https://github.com/user-attachments/assets/624ee2b6-eb2d-421b-967e-80eb15f82e64)

- Check whether all created artifacts are deleted on CodePipeline, S3, CloudFormation, SageMaker, and CloudWatch (LogGroups) or not. If still some of the artifacts are in the AWS, please delete them all. 

## References
- https://github.com/aws-samples/aws-mlops-pipelines-terraform
