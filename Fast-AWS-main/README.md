# Fast-AWS
- This repo covers **AWS Hands-on Labs, sample architectures** for different AWS services with **clean demo/printscreens**.

## Why was this repo created?
- It **shows/maps AWS services in short** with reference AWS developer documentation.  
- It shows **AWS Hands-on LABs with clean demos**. It focuses **only AWS services**.
- It contributes to **AWS open source community**.
- Hands-on lab will be **added in time** for different AWS Services and more samples (Bedrock, Sagemaker, ECS, Lambda, Batch, etc.)
  
# Quick Look (How-To): AWS Hands-on Labs
These hands-on labs focus on how to create and use AWS components:
- [HANDS-ON-01: Provisioning EC2s on VPC, Creating Key-Pair, Connecting EC2](https://github.com/omerbsezer/Fast-AWS/blob/main/HANDS-ON-001-EC2-VPC-Connect.md)
- [HANDS-ON-02: Provisioning Lambda, API Gateway and Reaching HTML Page in Python Code From Browser](https://github.com/omerbsezer/Fast-AWS/blob/main/HANDS-ON-002-Lambda-API-Gateway-Python.md)
- [HANDS-ON-03: EBS and EFS Configuration with EC2s](https://github.com/omerbsezer/Fast-AWS/blob/main/HANDS-ON-003-EC2-EBS-EFS.md)
- [HANDS-ON-04: Provisioning ECR, Pushing Image to ECR, Provisioning ECS, VPC, ELB, ECS Tasks, Service on Fargate Cluster](https://github.com/omerbsezer/Fast-AWS/blob/main/HANDS-ON-004-ECR-ECS-ELB-VPC-ECS-Service.md)
- [HANDS-ON-05: Provisioning ECR, Lambda and API Gateway to run Flask App Container on Lambda](https://github.com/omerbsezer/Fast-AWS/blob/main/HANDS-ON-005-Lambda-Container-ApiGateway-FlaskApp.md)
- [HANDS-ON-06: Provisioning EKS with Managed Nodes using Blueprint and Modules](https://github.com/omerbsezer/Fast-AWS/blob/main/HANDS-ON-006-EKS-ManagedNodes-Blueprint.md)
- [HANDS-ON-07: Provisioning CodeCommit, CodePipeline and Triggering CodeBuild and CodeDeploy Container in Lambda](https://github.com/omerbsezer/Fast-AWS/blob/main/HANDS-ON-007-CodeCommit-Pipeline-Build-Deploy-Lambda.md)
- [HANDS-ON-08: Provisioning S3, CloudFront to serve Static Web Site](https://github.com/omerbsezer/Fast-AWS/blob/main/HANDS-ON-008-S3-CloudFront-Static-WebSite.md)
- [HANDS-ON-09: Provisioned Gitlab Runner on EC2, connection to Gitlab Server using Docker on-premise](https://github.com/omerbsezer/Fast-AWS/blob/main/HANDS-ON-009-GitlabServer-on-Premise-GitlabRunner-on-EC2.md)
- [HANDS-ON-10: Implementing MLOps Pipeline using GitHub, CodePipeline, CodeBuild, CodeDeploy, Sagemaker Endpoint](https://github.com/omerbsezer/Fast-AWS/blob/main/HANDS-ON-010-MLOps-SageMaker-GitHub-Codepipeline-CodeBuild-CodeDeploy.md)

# Table of Contents
- [Motivation](#motivation)
- [Common AWS Services In-Short](#servicesshort)
  - [1. Compute Services](#compute)
  - [2. Container Services](#container)
  - [3. Storage Services](#storage)
  - [4. Database Services](#database)
  - [5. Data Analytics Services](#dataanalytics)
  - [6. Integration Services ](#integration)
  - [7. Cloud Financial Management Services](#cloudfinancial)
  - [8. Management & Governance Services](#managementgovernance)
  - [9. Security, Identity, & Compliance Services](#securityidentity)
  - [10. Networking Services](#networking)
  - [11. Migration Services](#migration)
  - [12. Internet of Things Services](#internetofthings)
  - [13. Artificial Intelligence Services](#artificialintelligence)
- [AWS Hands-on Labs](#handsonlabs)
  - [HANDS-ON-01: Provisioning EC2s on VPC, Creating Key-Pair, Connecting EC2](#ec2_vpc_key_pair)
  - [HANDS-ON-02: Provisioning Lambda, API Gateway and Reaching HTML Page in Python Code From Browser](#lambda_apigateway_python)
  - [HANDS-ON-03: EBS and EFS Configuration with EC2s](#ebs_efs_ec2)
  - [HANDS-ON-04: Provisioning ECR, Pushing Image to ECR, Provisioning ECS, VPC, ELB, ECS Tasks, Service on Fargate Cluster](#ecr_ecs_elb_vpc_ecs_service_fargate)
  - [HANDS-ON-05: Provisioning ECR, Lambda and API Gateway to run Flask App Container on Lambda](#ecr_lambda_apigateway_container)
  - [HANDS-ON-06: Provisioning EKS with Managed Nodes using Blueprint and Modules](#eks_managednodes_blueprint)
  - [HANDS-ON-07: Provisioning CodeCommit, CodePipeline and Triggering CodeBuild and CodeDeploy Container in Lambda](#ci_cd)
  - [HANDS-ON-08: Provisioning S3, CloudFront to serve Static Web Site](#s3_cloudfront)
  - [HANDS-ON-09: Provisioned Gitlab Runner on EC2, connection to Gitlab Server using Docker on-premise](#gitlabrunner)
  - [HANDS-ON-10: Implementing MLOps Pipeline using GitHub, CodePipeline, CodeBuild, CodeDeploy, Sagemaker Endpoint](#sagemaker)
- [References](#references)

## Motivation <a name="motivation"></a>
Why should we use / learn cloud?
- **Faster Development:** Rapid provisioning of resources accelerates product development and testing.
- **Access to Advanced Technologies:** Utilize AI, ML, big data analytics, and other tools without building infrastructure from scratch.
- **Flexibility in Work Models:** Enable remote and hybrid work setups with cloud-based tools.
- **High Demand:** Cloud skills are highly sought after in the job market, leading to better career opportunities and higher salaries.
- **Career Paths:** Cloud knowledge is applicable in various roles, including developer, architect, data scientist, and DevOps engineer.
- **Future-Proofing Skills:** Cloud is a foundational technology for emerging trends like AI, IoT, and edge computing.
- **Operational Savings:** Minimized costs for hardware maintenance, upgrades, and energy consumption.
- **Scalability Without Cost Burden:** Scale resources up or down based on needs, avoiding overprovisioning.
- **Global Reach:** Deliver applications and services worldwide with minimal latency using cloud regions and content delivery networks.
- **Disaster Recovery:** Built-in redundancy and backup solutions ensure business continuity during failures.
- **Improved Collaboration:** Cloud platforms facilitate real-time collaboration across teams and geographies.
- **Comprehensive Ecosystem:** Familiarize yourself with cloud providers like AWS, Azure, Google Cloud, and their services.
- **Certifications and Recognition:** Earn globally recognized certifications that validate your skills.
- **Community Support:** Access vast resources, communities, and forums to accelerate your learning.

Why should we use / learn AWS?
- **Industry Leader:** AWS is the largest cloud provider, holding a significant market share, making AWS skills highly valuable.
- **In-Demand Certifications:** AWS certifications are globally recognized and often lead to better job opportunities and higher salaries.
- **Diverse Roles:** AWS knowledge applies to various roles like cloud architect, developer, DevOps engineer, and data scientist.
- **Future-Proof Career:** AWS continues to innovate, ensuring longevity in its relevance and utility.
- **Extensive Services:** Offers 200+ fully featured services, including computing, storage, AI/ML, analytics, IoT, and databases.
- **Custom Solutions:** Provides tools for various industries like healthcare, finance, gaming, and e-commerce.
- **Comprehensive Documentation:** AWS offers detailed tutorials, guides, and examples for users of all levels.
- **Active Community:** Join a global network of AWS professionals, forums, and meetups for support and collaboration.
- **AWS Training:** Gain access to structured training programs and certifications for systematic skill-building.
- **First-Mover Advantage:** AWS has years of experience and maturity, ensuring reliability
- **Continuous Innovation:** AWS consistently introduces new services and updates to meet evolving needs.


## AWS Services In-Short <a name="servicesshort"></a>
There are more than 200 AWS services. Popular services are listed in short.

### 1. Compute Services <a name="compute"></a>
#### Amazon EC2 
- Virtual servers/machines in the cloud
- **Document**: https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/concepts.html

  ![image](https://github.com/user-attachments/assets/cd0f3f0f-b5eb-4ce6-8355-0fab607c1a20)

#### Amazon EC2 Auto Scaling 
- Scale compute capacity to meet demand
- **Document**: https://docs.aws.amazon.com/autoscaling/ec2/userguide/what-is-amazon-ec2-auto-scaling.html

  ![image](https://github.com/user-attachments/assets/16603fd1-fd4c-457b-8f36-e6a8e8ae5ff2)

#### Amazon Lightsail 
- Launch and manage virtual private servers
- **Document**: https://docs.aws.amazon.com/lightsail/latest/userguide/what-is-amazon-lightsail.html

  ![image](https://github.com/user-attachments/assets/60008da9-9416-4627-9aee-9f6736fc7511)

#### AWS App Runner
- Build and run containerized web apps at scale
- **Document**: https://docs.aws.amazon.com/apprunner/latest/dg/what-is-apprunner.html

  ![image](https://github.com/user-attachments/assets/3a22fb4c-0488-4d9d-88ee-b6081cfde4d9)

#### AWS Batch
- Run batch jobs at any scale
- **Document**: https://docs.aws.amazon.com/batch/latest/userguide/what-is-batch.html

  ![image](https://github.com/user-attachments/assets/6f53153d-eb3f-4f9f-99a4-69aea599ed4a)

#### AWS Elastic Beanstalk
- Run and manage web apps
- **Document**: https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/Welcome.html

  ![image](https://github.com/user-attachments/assets/5cdd1b43-af04-4e3d-b2d4-15e92ac55c11)

#### AWS Amplify
- Build, deploy, and host scalable web and mobile apps
- **Document**: https://docs.aws.amazon.com/amplify/latest/userguide/welcome.html

  ![image](https://github.com/user-attachments/assets/0b5d3e6e-2d7c-46a4-9243-9ded17074b8e)

#### AWS Lambda
- Run code without thinking about servers
- **Document**: https://docs.aws.amazon.com/lambda/latest/dg/welcome.html

  ![image](https://github.com/user-attachments/assets/84cd58a9-6a2e-49ff-84e5-b8ca68bab969)
  
#### AWS Outposts
- Run AWS infrastructure on-premises
- **Document**: https://docs.aws.amazon.com/outposts/latest/userguide/what-is-outposts.html 

  ![image](https://github.com/user-attachments/assets/5ca3081a-4fd6-4a3c-8f60-2350a1ae7eff)

#### AWS Parallel Computing Service
- Easily run HPC workloads at virtually any scale
- **Document**: https://docs.aws.amazon.com/pcs/latest/userguide/what-is-service.html

  ![image](https://github.com/user-attachments/assets/4a2146a7-b0a2-4708-9990-d66ea26dafb3)

#### AWS Serverless Application Repository
- Discover, deploy, and publish serverless applications
- **Document**: https://docs.aws.amazon.com/serverlessrepo/latest/devguide/what-is-serverlessrepo.html

  ![image](https://github.com/user-attachments/assets/05ddbc6f-d00a-4426-be4f-824d2fbd2c39)

#### AWS Wavelength
- Deliver ultra-low latency applications for 5G devices
- **Document**: https://docs.aws.amazon.com/wavelength/latest/developerguide/how-wavelengths-work.html

  ![image](https://github.com/user-attachments/assets/dfa8b4b9-4be0-455f-b882-9e90be774d35)
  
### 2. Container Services  <a name="container"></a>
#### Amazon Elastic Container Registry
- Easily store, manage, and deploy container images
- **Document**: https://docs.aws.amazon.com/AmazonECR/latest/userguide/what-is-ecr.html

  ![image](https://github.com/user-attachments/assets/970aab11-7b16-4666-b991-a0245ccc5ff6)

#### Amazon Elastic Container Service (ECS)
- Highly secure, reliable, and scalable way to run containers
- **Document**: https://docs.aws.amazon.com/AmazonECS/latest/developerguide/Welcome.html

  ![image](https://github.com/user-attachments/assets/b84868c1-357e-46e9-90b0-cb69adf5c142)

#### Amazon Elastic Kubernetes Service (EKS)
- The most trusted way to run Kubernetes
- Amazon EKS Anywhere: Kubernetes on your infrastructure
- Amazon EKS Distro: Run consistent Kubernetes clusters
- **Document**: https://docs.aws.amazon.com/eks/latest/userguide/what-is-eks.html

  ![image](https://github.com/user-attachments/assets/269b7c36-cdcb-45e6-b971-44bd3d3a040f)

#### AWS App2Container
- Containerize and migrate existing applications
- **Document**: https://docs.aws.amazon.com/app2container/latest/UserGuide/what-is-a2c.html
  
#### AWS App Runner 
- Build and run containerized web apps at scale
- **Document**: https://docs.aws.amazon.com/apprunner/latest/dg/what-is-apprunner.html

  ![image](https://github.com/user-attachments/assets/bd40d558-4d05-4d1e-a811-f4b252765fca)

#### AWS Fargate
- Serverless compute for containers
- **ECS Fargate Document**: https://docs.aws.amazon.com/AmazonECS/latest/developerguide/AWS_Fargate.html
- **EKS Fargate Document**: https://docs.aws.amazon.com/eks/latest/userguide/fargate-getting-started.html

  ![image](https://github.com/user-attachments/assets/6f2b8ad4-ceaf-4062-9f8c-70dac3f0ef8a)
  
### 3. Storage Services <a name="storage"></a>
#### Amazon Simple Storage Service (S3)
- Scalable storage in the cloud
- **Document**: https://docs.aws.amazon.com/AmazonS3/latest/userguide/Welcome.html

  ![image](https://github.com/user-attachments/assets/7da8eaa2-9ef3-4ad5-abc9-db39b5319471)

#### Amazon S3 Glacier storage classes
- Low-cost archive storage in the cloud
- **Document**: https://docs.aws.amazon.com/amazonglacier/latest/dev/introduction.html

  ![image](https://github.com/user-attachments/assets/bfb0e51b-3865-4d4e-a51e-dd0b436f957d)

#### Amazon Elastic Block Store (EBS)
- EC2 block storage volumes
- **Document**: https://docs.aws.amazon.com/ebs/latest/userguide/what-is-ebs.html

  ![image](https://github.com/user-attachments/assets/72a7f9af-3701-4fef-b34c-4388ff3cffa4)

#### Amazon Elastic File System (EFS)
- Fully managed file system for EC2
- **Document**: https://docs.aws.amazon.com/efs/latest/ug/whatisefs.html

  ![image](https://github.com/user-attachments/assets/d1edfac2-7327-4e69-9506-062bd1fd2781)

#### Amazon FSx for Lustre
- High-performance file system integrated with S3
- **Document**: https://docs.aws.amazon.com/fsx/latest/LustreGuide/what-is.html

  ![image](https://github.com/user-attachments/assets/23f90755-e706-4a18-8fcf-93562a7d6095)

#### Amazon FSx for NetApp ONTAP
- Fully managed storage built on NetApp’s popular ONTAP file system
- **Document**: https://docs.aws.amazon.com/fsx/latest/ONTAPGuide/what-is-fsx-ontap.html

  ![image](https://github.com/user-attachments/assets/0a7cbfb1-5cce-4e9a-8f9e-856423eb871e)

#### Amazon FSx for OpenZFS
- Fully managed storage built on the popular OpenZFS file system
- **Document**: https://docs.aws.amazon.com/fsx/latest/OpenZFSGuide/what-is-fsx.html

  ![image](https://github.com/user-attachments/assets/ad74c091-1847-4430-97db-41e183fda6c3)

#### Amazon FSx for Windows File Server
- Fully managed Windows native file system
- **Document**: https://docs.aws.amazon.com/fsx/latest/WindowsGuide/what-is.html

  ![image](https://github.com/user-attachments/assets/b6f01955-e0e7-46e7-8944-f42b6f7769a6)

#### Amazon File Cache
- High-speed cache for datasets stored anywhere
- **Document**: https://docs.aws.amazon.com/fsx/latest/FileCacheGuide/what-is.html

#### AWS Backup
- Centralized backup across AWS services
- **Document**: https://docs.aws.amazon.com/aws-backup/latest/devguide/whatisbackup.html

#### AWS Elastic Disaster Recovery (DRS)
- Scalable, cost-effective application recovery
- **Document**: https://docs.aws.amazon.com/drs/latest/userguide/what-is-drs.html

#### AWS Snowball
- Accelerate moving offline data or remote storage to the cloud
- **Document**: https://docs.aws.amazon.com/snowball/latest/developer-guide/whatisedge.html

  ![image](https://github.com/user-attachments/assets/b3952505-33d2-4f85-bc45-5be4bf808a0a)

#### AWS Storage Gateway
- Hybrid storage integration
- **S3 File Gateway Document**: https://docs.aws.amazon.com/filegateway/latest/files3/what-is-file-s3.html
- **Volume Gateway Document**: https://docs.aws.amazon.com/storagegateway/latest/vgw/WhatIsStorageGateway.html
- **Tape Gateway Document**: https://docs.aws.amazon.com/storagegateway/latest/tgw/WhatIsStorageGateway.html
- **FSx File Gateway Document**: https://docs.aws.amazon.com/filegateway/latest/filefsxw/what-is-file-fsxw.html

  ![image](https://github.com/user-attachments/assets/a0d4624f-25e4-4ebb-88b7-fa201de2017c)

### 4. Database Services <a name="database"></a>
#### Amazon Aurora
- High performance managed relational database with full MySQL and PostgreSQL compatibility
- **Document**: https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/CHAP_AuroraOverview.html

  ![image](https://github.com/user-attachments/assets/ff0f99bf-72a8-46b7-b1ef-7cc3b16b9e34)

#### Amazon Aurora DSQL
- Fastest serverless distributed SQL database with active-active high availability
- **Document**: https://docs.aws.amazon.com/aurora-dsql/latest/userguide/getting-started.html

#### Amazon Aurora Serverless V2
- Instantly scale to >100,000 transactions per second
- **Document**: https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/aurora-serverless-v2.html

#### Amazon DocumentDB (with MongoDB compatibility)
- Fully managed **Document** database
- **Document**: https://docs.aws.amazon.com/documentdb/latest/developerguide/what-is.html

  ![image](https://github.com/user-attachments/assets/d688eafd-68d3-432a-b53b-6f4b8c62c449)

#### Amazon DynamoDB
- Managed NoSQL database
- **Document**: https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Introduction.html

  ![image](https://github.com/user-attachments/assets/de1a9525-7f85-4534-b837-8f011940b07b)

#### Amazon ElastiCache
- In-memory caching service for Valkey, Memcached, and Redis OSS
- **Document**: https://docs.aws.amazon.com/AmazonElastiCache/latest/dg/WhatIs.html

  ![image](https://github.com/user-attachments/assets/09293da6-3743-4c4e-81d9-f5e1c8e52f54)

#### Amazon Keyspaces (for Apache Cassandra)
- Managed Cassandra-compatible database
- **Document**: https://docs.aws.amazon.com/keyspaces/latest/devguide/what-is-keyspaces.html

  ![image](https://github.com/user-attachments/assets/d269501a-1ecd-4421-937c-8410d6aca37e)

#### Amazon MemoryDB
- Valkey- and Redis OSS-compatible, durable, in-memory database with ultra-fast performance
- **Document**: https://docs.aws.amazon.com/memorydb/latest/devguide/what-is-memorydb.html

  ![image](https://github.com/user-attachments/assets/43a87fad-de4b-47e8-ae66-d1b30d8650fc)

#### Amazon Neptune
- Fully managed graph database service
- **Document**: https://docs.aws.amazon.com/neptune/latest/userguide/intro.html

  ![image](https://github.com/user-attachments/assets/d76168fb-cfd7-4274-bf2d-9c879d90b95b)

#### Amazon RDS
- Managed relational database service for PostgreSQL, MySQL, MariaDB, SQL Server, Oracle, and Db2
- **Document**: https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Welcome.html

  ![image](https://github.com/user-attachments/assets/fdc8224e-991f-4673-bd30-8158158e0c6c)

#### Amazon Timestream
- Fully managed time series database
- **Document**: https://docs.aws.amazon.com/timestream/latest/developerguide/what-is-timestream.html

  ![image](https://github.com/user-attachments/assets/d8ce9ecd-fbf7-4e97-a2e2-8491b5a36703)

#### Amazon Redshift
- Fast, simple, cost-effective data warehousing
- **Document**: https://docs.aws.amazon.com/redshift/latest/gsg/new-user-serverless.html

  ![image](https://github.com/user-attachments/assets/ef4b1c88-42f8-4163-b16a-e65531df1ea6)  

### 5. Data Analytics Services <a name="dataanalytics"></a>
#### Amazon Athena
- Query data in S3 using SQL
- **Document**: https://docs.aws.amazon.com/athena/latest/ug/what-is.html

   ![image](https://github.com/user-attachments/assets/e892742c-8597-4eca-923a-7fc849b8f406)

#### Amazon OpenSearch Service
- Search, visualize, and analyze up to petabytes of text and unstructured data
- **Document**: https://docs.aws.amazon.com/opensearch-service/latest/developerguide/what-is.html

  ![image](https://github.com/user-attachments/assets/9a77bea8-8a26-4915-bf61-cc7047859c38)

#### Amazon EMR
- Easily run big data frameworks
- **Document**: https://docs.aws.amazon.com/emr/latest/ManagementGuide/emr-what-is-emr.html

   ![image](https://github.com/user-attachments/assets/372f2f24-f194-468e-9b1d-7eb1d37cfdd5)

#### Amazon FinSpace
- Analytics for the financial services industry
- **Document**: https://docs.aws.amazon.com/finspace/latest/userguide/finspace-what-is.html

  ![image](https://github.com/user-attachments/assets/34f209fa-7826-4677-9eed-dc62ad4cf8ae)

#### Amazon Kinesis Analytics
- Analyze real-time video and data streams
- **Document**: https://docs.aws.amazon.com/kinesisanalytics/latest/sqlref/analytics-sql-reference-dg.html

   ![image](https://github.com/user-attachments/assets/222d80b3-7f29-457d-84cb-d2c65bc9c056)

#### Amazon Neptune Analytics
- With Neptune Analytics, you can get insights and find trends by processing large amounts of graph data in seconds.
- **Document**: https://docs.aws.amazon.com/neptune-analytics/latest/userguide/what-is-neptune-analytics.html
  
#### Amazon Data Firehose
- Real-time streaming delivery for any data, at any scale, at low-cost
- **Document**: https://docs.aws.amazon.com/firehose/latest/dev/what-is-this-service.html

  ![image](https://github.com/user-attachments/assets/c66f5ad6-08ac-4906-a674-da89b2033d42)

#### Amazon Managed Service for Apache Flink
- Fully managed Apache Flink service
- **Document**: https://docs.aws.amazon.com/managed-flink/latest/java/how-it-works.html

  ![image](https://github.com/user-attachments/assets/273b9754-4bdd-465d-9a94-17754dbd7a24)

#### Amazon Managed Streaming for Apache Kafka
- Fully managed Apache Kafka service
- **Document**: https://docs.aws.amazon.com/msk/latest/developerguide/what-is-msk.html

  ![image](https://github.com/user-attachments/assets/56c5a9e7-bfe2-4c3f-9487-2d04789c72b9)

#### Amazon QuickSight
- Fast business analytics service
- **Document**: https://docs.aws.amazon.com/quicksight/latest/user/welcome.html

  ![image](https://github.com/user-attachments/assets/8cfa4a6a-4c58-4579-8972-6b81c57816d3)

#### AWS Data Exchange
- Find, subscribe to, and use third-party data in the cloud
- **Document**: https://docs.aws.amazon.com/data-exchange/latest/userguide/what-is.html

  ![image](https://github.com/user-attachments/assets/fee58fc6-cad3-4ff0-9178-9374aa06a8d3)

#### AWS Glue
- Simple, scalable, and serverless data integration
- **Document**: https://docs.aws.amazon.com/glue/latest/dg/what-is-glue.html

  ![image](https://github.com/user-attachments/assets/e9ef707e-796a-485f-8450-75782f9a04e5)

#### AWS Lake Formation
- Build, manage, and secure your data lake
- **Document**: https://docs.aws.amazon.com/lake-formation/latest/dg/what-is-lake-formation.html

  ![image](https://github.com/user-attachments/assets/9dffb5c1-30c7-4f14-86a4-8085675814d6)

### 6. Integration Services <a name="integration"></a>
#### AWS Step Functions
- Coordination for distributed applications
- **Document**: https://docs.aws.amazon.com/step-functions/latest/dg/welcome.html

  ![image](https://github.com/user-attachments/assets/f4b3cea3-4675-4aff-af95-93c3b96dc543)

#### Amazon API Gateway
- Build, deploy, and manage APIs
- **Document**: https://docs.aws.amazon.com/apigateway/latest/developerguide/welcome.html

  ![image](https://github.com/user-attachments/assets/3d19e332-6597-4d7f-9c20-ccb883da4d27)

#### Amazon AppFlow
- No-code integration for SaaS apps & AWS services
- **Document**: https://docs.aws.amazon.com/appflow/latest/userguide/what-is-appflow.html

  ![image](https://github.com/user-attachments/assets/75dbff0a-d2d9-44e4-be13-c7de88b37ed0)

#### Amazon EventBridge
- Serverless event bus for SaaS apps & AWS services
- **Document**: https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-what-is.html

  ![image](https://github.com/user-attachments/assets/36966675-9886-4513-9c5e-224a88de42f9)

#### Amazon Managed Workflows for Apache Airflow
- Highly available, secure, and managed workflow orchestration
- **Document**: https://docs.aws.amazon.com/mwaa/latest/userguide/what-is-mwaa.html

  ![image](https://github.com/user-attachments/assets/0a594916-0def-42f9-b3a4-a4ec3f72cfd8)

#### Amazon MQ
- Managed message broker service
- **Document**: https://docs.aws.amazon.com/amazon-mq/latest/developer-guide/welcome.html

  ![image](https://github.com/user-attachments/assets/f8c35e6d-7589-40c2-aae5-1773b5f2c263)

#### Amazon Simple Notification Service (SNS)
- Pub/sub, SMS, email, and mobile push notifications
- **Document**: https://docs.aws.amazon.com/sns/latest/dg/welcome.html

  ![image](https://github.com/user-attachments/assets/0dc84b94-84b4-4aee-bf43-bc0c78bed587)

#### Amazon Simple Queue Service (SQS)
- Managed message queues
- **Document**: https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/welcome.html

  ![image](https://github.com/user-attachments/assets/c8af8b95-433f-4e8d-99d9-8fd1df35ecda)

#### AWS AppSync
- Fully-managed, scalable GraphQL APIs
- **Document**: https://docs.aws.amazon.com/appsync/latest/devguide/what-is-appsync.html

  ![image](https://github.com/user-attachments/assets/dce0a58b-4fcc-463b-8a8a-6f38d20fd853)

### 7. Cloud Financial Management Services <a name="cloudfinancial"></a>
#### AWS Cost Explorer
- Analyze your AWS cost and usage
- **Document**: https://docs.aws.amazon.com/solutions/latest/amazon-marketing-cloud-insights-on-aws/aws-cost-explorer.html

  ![image](https://github.com/user-attachments/assets/3e9960b6-6abd-426c-a552-0272b3695af3)

#### AWS Billing Conductor
- Simplify billing and reporting with customizable pricing and cost visibility
- **Document**: https://docs.aws.amazon.com/billingconductor/latest/userguide/what-is-billingconductor.html

  ![image](https://github.com/user-attachments/assets/e9798c3d-8889-4d1c-9aa4-441407a36090)

#### AWS Billing and Cost Management
- Billing and payments
- Cost analysis
- Cost organization
- Budgeting and planning
- Savings and commitments
- Set custom cost and usage budgets
- **Document**: https://docs.aws.amazon.com/cost-management/latest/userguide/what-is-costmanagement.html

  ![image](https://github.com/user-attachments/assets/410f425d-4702-4125-9d75-4812d3b47d36)

### 8. Management & Governance Services <a name="managementgovernance"></a>
#### Amazon CloudWatch
- Monitor resources and applications
- **Document**: https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/WhatIsCloudWatch.html

  ![image](https://github.com/user-attachments/assets/14fefb53-2af4-4c0e-9fe7-25b1d42c6db2)

#### Amazon Managed Grafana
- Powerful interactive data visualizations
- **Document**: https://docs.aws.amazon.com/grafana/latest/userguide/what-is-Amazon-Managed-Service-Grafana.html

  ![image](https://github.com/user-attachments/assets/af50ac5a-f2f3-45d2-addc-30e14392fff2)

#### Amazon Managed Service for Prometheus
- Highly available, secure monitoring for containers
- **Document**: https://docs.aws.amazon.com/prometheus/latest/userguide/what-is-Amazon-Managed-Service-Prometheus.html

  ![image](https://github.com/user-attachments/assets/302d1b07-0348-484f-bb6e-f59e5900cba6)

#### AWS CloudFormation
- Create and manage resources with templates
- **Document**: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/Welcome.html

  ![image](https://github.com/user-attachments/assets/e0ab7482-19eb-4af9-8033-2735d511c977)

#### AWS CloudTrail
- Track user activity and API usage
- **Document**: https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-user-guide.html

  ![image](https://github.com/user-attachments/assets/23e91461-72e8-4e9c-ba1a-71ad14c3a2af)

#### AWS Command Line Interface
- Unified tool to manage AWS services
- **Document**: https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-welcome.html

  ![image](https://github.com/user-attachments/assets/91bd88c3-da00-40b7-9f89-5ac3fb6e03d7)

#### AWS Compute Optimizer
- Identify optimal AWS Compute resources
- **Document**: https://docs.aws.amazon.com/compute-optimizer/latest/ug/what-is-compute-optimizer.html

  ![image](https://github.com/user-attachments/assets/cf4faa12-9e46-4fde-99f0-bb0b4c313535)

#### AWS Config
- Track resources inventory and changes
- **Document**: https://docs.aws.amazon.com/config/latest/developerguide/WhatIsConfig.html

  ![image](https://github.com/user-attachments/assets/b70d1294-d223-4c6d-87d0-ac7d04f6f278)

#### AWS Control Tower
- Set up and govern a secure, compliant multi-account environment
- **Document**: https://docs.aws.amazon.com/controltower/latest/userguide/what-is-control-tower.html

  ![image](https://github.com/user-attachments/assets/5f5846e4-abd8-45de-802d-412c1b3dc5e8)

#### AWS Health Dashboard
- View important events and changes affecting your AWS environment
- **Document**: https://docs.aws.amazon.com/health/latest/ug/aws-health-dashboard-status.html

#### AWS License Manager
- Track, manage, and control licenses
- **Document**: https://docs.aws.amazon.com/license-manager/latest/userguide/license-manager.html

  ![image](https://github.com/user-attachments/assets/0a274193-519b-4403-abf8-88cb93262edb)

#### AWS Management Console
- Web-based user interface
- **Document**: https://docs.aws.amazon.com/awsconsolehelpdocs/latest/gsg/what-is.html

  ![image](https://github.com/user-attachments/assets/e7a9d3e2-7010-4e0a-8cb0-0131f1a65da7)

#### AWS Managed Services (MS)
- Infrastructure operations management for AWS
- **AMS Document**: https://docs.aws.amazon.com/managedservices/latest/userguide/what-is-ams.html
- **AMS Accelerate Document**: https://docs.aws.amazon.com/managedservices/latest/accelerate-guide/what-is-acc.html
- **AMS Advanced Application Document**: https://docs.aws.amazon.com/managedservices/latest/appguide/intro-aog.html

  ![image](https://github.com/user-attachments/assets/5cd6e21a-67dd-47df-8463-618a275b92a0)

#### AWS Organizations
- Central governance and management across AWS accounts
- **Document**: https://docs.aws.amazon.com/organizations/latest/userguide/orgs_introduction.html

  ![image](https://github.com/user-attachments/assets/64f782f8-3aa0-4b73-a490-6ddd5f986f1b)

#### AWS Proton
- Automated management for container and serverless deployment
- **Document**: https://docs.aws.amazon.com/proton/latest/userguide/Welcome.html
  
  ![image](https://github.com/user-attachments/assets/471f8c8d-089b-4997-81ca-4aafed8c03d7)

#### AWS Service Catalog
- Create and use standardized products
- **Document**: https://docs.aws.amazon.com/servicecatalog/latest/adminguide/introduction.html

  ![image](https://github.com/user-attachments/assets/3a017752-cef4-413f-95a7-62e560f516cb)

#### AWS Systems Manager
- Gain operational insights and take action
- **Document**: https://docs.aws.amazon.com/systems-manager/latest/userguide/what-is-systems-manager.html

  ![image](https://github.com/user-attachments/assets/9f09f421-452e-4ba5-b2d8-bb3d1de2c5fc)

#### AWS Trusted Advisor
- Optimize performance and security
- **Document**: https://docs.aws.amazon.com/awssupport/latest/user/trusted-advisor.html

  ![image](https://github.com/user-attachments/assets/9e0aecef-f058-4b03-abe6-97d96f2bde7d)

#### AWS User Notifications
- Configure and view notifications from AWS services
- **Document**: https://docs.aws.amazon.com/notifications/latest/userguide/what-is-service.html

#### AWS Well-Architected Tool
- Review and improve your workloads
- **Document**: https://docs.aws.amazon.com/wellarchitected/latest/userguide/intro.html

  ![image](https://github.com/user-attachments/assets/6df131da-a943-4e11-8723-dd1fc584ad8a)

### 9. Security, Identity, & Compliance Services <a name="securityidentity"></a>
#### AWS Identity and Access Management (IAM)
- Securely manage access to services and resources
- **Document**: https://docs.aws.amazon.com/IAM/latest/UserGuide/introduction.html

  ![image](https://github.com/user-attachments/assets/efa9d049-501e-43a7-bff4-fc24f2d24db0)

#### Amazon Cognito
- Identity management for your apps. It handles user authentication and authorization for your web and mobile apps.
- With user pools, you can easily and securely add sign-up and sign-in functionality to your apps.
- With identity pools (federated identities), your apps can get temporary credentials that grant users access to specific AWS resources, whether the users are anonymous or are signed in.
- **User Pools Document**: https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pools.html
- **Identity Pools Document**: https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-identity.html
- **Cognito Sync Document**: https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-sync.html

  ![image](https://github.com/user-attachments/assets/f0425ffd-cd4c-430c-bb93-52414971dd9b)

#### Amazon Detective
- Investigate potential security issues
- **Document**: https://docs.aws.amazon.com/detective/latest/userguide/what-is-detective.html

  ![image](https://github.com/user-attachments/assets/ed33e15a-8fcc-40b0-9c1c-634e4a007ba1)

#### Amazon GuardDuty
- Managed threat detection service
- **Document**: https://docs.aws.amazon.com/guardduty/latest/ug/what-is-guardduty.html

  ![image](https://github.com/user-attachments/assets/e16bdb0d-7e48-46ad-ad7e-649d534f41b1)

#### Amazon Inspector
- Automate vulnerability management
- **Document**: https://docs.aws.amazon.com/inspector/latest/user/what-is-inspector.html

  ![image](https://github.com/user-attachments/assets/7055a02a-34bc-4ab3-849b-2b8a451d41fc)

#### Amazon Macie
- Discover and protect your sensitive data at scale
- **Document**: https://docs.aws.amazon.com/macie/latest/user/what-is-macie.html

  ![image](https://github.com/user-attachments/assets/8e500aa9-2ed4-40e7-87a1-646c92d83f20)

#### Amazon Security Lake
- Automatically centralize your security data with a few clicks
- **Document**: https://docs.aws.amazon.com/security-lake/latest/userguide/what-is-security-lake.html

  ![image](https://github.com/user-attachments/assets/bc81e0be-075e-4013-aa7b-6fc9c1ba605d)

#### Amazon Verified Permissions
- Fine-grained permissions and authorization for your applications
- **Document**: https://docs.aws.amazon.com/verifiedpermissions/latest/userguide/what-is-avp.html

  ![image](https://github.com/user-attachments/assets/58fb3f17-ee0b-48a6-a1c8-5c9f9d094ed4)

#### AWS Artifact
- On-demand access to AWS’ compliance reports
- **Document**: https://docs.aws.amazon.com/artifact/latest/ug/what-is-aws-artifact.html

  ![image](https://github.com/user-attachments/assets/462197de-7d4f-4351-9db3-3c8796c2db19)

#### AWS Audit Manager
- Continuously audit your AWS usage
- **Document**: https://docs.aws.amazon.com/audit-manager/latest/userguide/what-is.html

  ![image](https://github.com/user-attachments/assets/0e33f86c-aeaf-491c-98ed-547dbab4405e)

#### AWS Certificate Manager
- Provision, manage, and deploy SSL/TLS certificates
- **Document**: https://docs.aws.amazon.com/acm/latest/userguide/acm-overview.html

  ![image](https://github.com/user-attachments/assets/13497ba5-4044-4244-a2c3-9371cee2fae8)

#### AWS CloudHSM
- Hardware-based key storage for regulatory compliance
- **Document**: https://docs.aws.amazon.com/cloudhsm/latest/userguide/introduction.html

  ![image](https://github.com/user-attachments/assets/ee6b9b67-0555-457b-b88a-df0bc607c2ac)

#### AWS Directory Service
- Host and manage active directory
- **Document**: https://docs.aws.amazon.com/directoryservice/latest/admin-guide/what_is.html

  ![image](https://github.com/user-attachments/assets/0ddf4ff3-2c25-4c36-9580-7d0358d2e7be)

#### AWS Firewall Manager
- Central management of firewall rules
- **Document**: https://docs.aws.amazon.com/waf/latest/developerguide/fms-chapter.html

  ![image](https://github.com/user-attachments/assets/5eb00421-fc9e-4561-b5a2-08438eb49fcd)

#### AWS Key Management Service
- Managed creation and control of encryption keys
- **Document**: https://docs.aws.amazon.com/kms/latest/developerguide/overview.html

  ![image](https://github.com/user-attachments/assets/eb076cc7-efd5-4df9-b0a7-815848b9b19b)

#### AWS Network Firewall
- Network security to protect your VPCs
- **Document**: https://docs.aws.amazon.com/network-firewall/latest/developerguide/what-is-aws-network-firewall.html

  ![image](https://github.com/user-attachments/assets/cdc60d40-7f02-494f-a8db-6addf0bc7e82)

#### AWS Resource Access Manager
- Simple, secure service to share AWS resources
- **Document**: https://docs.aws.amazon.com/resource-explorer/latest/userguide/welcome.html

  ![image](https://github.com/user-attachments/assets/08d9e261-aeb6-414a-9168-08b5071a274c)

#### AWS Secrets Manager
- Rotate, manage, and retrieve secrets
- **Document**: https://docs.aws.amazon.com/secretsmanager/latest/userguide/intro.html

  ![image](https://github.com/user-attachments/assets/02287a44-2061-41dc-a8f5-a1395eaef97a)

#### AWS Security Hub
- Unified security and compliance center
- **Document**: https://docs.aws.amazon.com/securityhub/latest/userguide/what-is-securityhub.html

  ![image](https://github.com/user-attachments/assets/b316495f-753c-4a28-9478-155678c33bfb)

#### AWS Shield
- DDoS protection
- **Document**: https://docs.aws.amazon.com/waf/latest/developerguide/shield-chapter.html

  ![image](https://github.com/user-attachments/assets/c8a242c5-3142-4701-9ee4-143411b25308)

#### AWS IAM Identity Center
- Manage single sign-on access to AWS accounts and apps
- **Document**: https://docs.aws.amazon.com/singlesignon/latest/userguide/what-is.html

  ![image](https://github.com/user-attachments/assets/4cc46a9d-72fc-4885-a4a0-c30fb2db0ecd)

#### AWS WAF
- Filter malicious web traffic
- **Document**: https://docs.aws.amazon.com/waf/latest/developerguide/waf-chapter.html

  ![image](https://github.com/user-attachments/assets/7ad267b9-206e-490f-a5c8-41a59a8f7129)

### 10. Networking Services <a name="networking"></a>
#### Amazon VPC
- Isolated cloud resources
- **Document**: https://docs.aws.amazon.com/vpc/latest/userguide/what-is-amazon-vpc.html

  ![image](https://github.com/user-attachments/assets/72183235-913a-451a-966b-c55fd225149c)

#### Amazon VPC Lattice
- Simplify service-to-service connectivity, security, and monitoring
- **Document**: https://docs.aws.amazon.com/vpc-lattice/latest/ug/what-is-vpc-lattice.html

  ![image](https://github.com/user-attachments/assets/8737afe4-79c6-4e30-be41-4c0ec1d7e50e)

#### Amazon API Gateway
- Build, deploy, and manage APIs
- **Document**: https://docs.aws.amazon.com/apigateway/latest/developerguide/welcome.html

  ![image](https://github.com/user-attachments/assets/bfa8c214-c2db-4917-af1f-b183c9402578)

#### Amazon CloudFront
- Global content delivery network
- **Document**: https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/Introduction.html

  ![image](https://github.com/user-attachments/assets/94d188bd-6c64-43ce-8c27-44f371cf7659)

#### Amazon Route 53
- Scalable domain name system (DNS)
- **Document**: https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/Welcome.html

  ![image](https://github.com/user-attachments/assets/821a916d-0a5e-46f9-bd67-7357d92fff14)

#### AWS App Mesh
- Monitor and control microservices
- **Document**: https://docs.aws.amazon.com/app-mesh/latest/userguide/what-is-app-mesh.html

  ![image](https://github.com/user-attachments/assets/2b16dc07-b981-4fd6-b9ce-5ee1d9fd76ca)

#### AWS Cloud Map
- Service discovery for cloud resources
- **Document**: https://docs.aws.amazon.com/cloud-map/latest/dg/what-is-cloud-map.html

  ![image](https://github.com/user-attachments/assets/220a6eb0-b16b-4ab0-b5cd-e0c4d7b7984a)

#### AWS Cloud WAN
- Easily build, manage, and monitor global wide area networks
- **Document**: https://docs.aws.amazon.com/whitepapers/latest/aws-vpc-connectivity-options/aws-cloud-wan.html

  ![image](https://github.com/user-attachments/assets/46b373c6-20d6-4bb9-85be-ae14e1de72fa)

#### AWS Direct Connect
- Dedicated network connection to AWS
- **Document**: https://docs.aws.amazon.com/directconnect/latest/UserGuide/Welcome.html

  ![image](https://github.com/user-attachments/assets/04c36b7e-4ce3-4c17-9020-d8a321fc9985)

#### AWS Global Accelerator
- Improve application availability and performance
- **Document**: https://docs.aws.amazon.com/global-accelerator/latest/dg/what-is-global-accelerator.html

  ![image](https://github.com/user-attachments/assets/047e1f91-f1ea-40c3-b21c-de984fdb2781)

#### AWS Private 5G
- Easily deploy, manage, and scale a private cellular network
- **Document**: https://docs.aws.amazon.com/private-networks/latest/userguide/what-is-private-5g.html

  ![image](https://github.com/user-attachments/assets/582aa03b-5555-4227-8ad0-fc4b062c9d60)

#### AWS PrivateLink
- Securely access services hosted on AWS
- Connect another VPC and VPC resources with interface endpoint
- **Document**: https://docs.aws.amazon.com/vpc/latest/privatelink/what-is-privatelink.html

  ![image](https://github.com/user-attachments/assets/3cf7d90a-bf62-4d43-9379-f12d2100c847)

#### AWS Transit Gateway
- Easily scale VPC and account connections
- **Document**: https://docs.aws.amazon.com/vpc/latest/tgw/what-is-transit-gateway.html

  ![image](https://github.com/user-attachments/assets/84ca2822-d875-48dc-9df8-44b210ed527a)

#### AWS Verified Access
- Provide secure access to corporate applications without a VPN
- **Document**: https://docs.aws.amazon.com/verified-access/latest/ug/what-is-verified-access.html

  ![image](https://github.com/user-attachments/assets/20cff696-0179-4858-85b2-abed09e64ea9)

#### AWS Client VPN
- Securely access your network resources
- **Document**: https://docs.aws.amazon.com/vpn/latest/clientvpn-user/client-vpn-user-what-is.html

  ![image](https://github.com/user-attachments/assets/d67c3eb6-da70-471b-922b-a5b97f56e3d3)

#### AWS Site-to-Site VPN
-  Enable access to your remote network from your VPC by creating an AWS Site-to-Site VPN connection, and configuring routing to pass traffic through the connection.
- **Document**: https://docs.aws.amazon.com/vpn/latest/s2svpn/VPC_VPN.html

  ![image](https://github.com/user-attachments/assets/cbe8b866-b871-4b9f-b796-7761bfbd550c)

#### Elastic Load Balancing (ELB)
- Distribute incoming traffic across multiple targets
- **Elastic Load Balancing Document**: https://docs.aws.amazon.com/elasticloadbalancing/latest/userguide/what-is-load-balancing.html
- **Application Load Balancer Document**: https://docs.aws.amazon.com/elasticloadbalancing/latest/application/introduction.html
- **Network Load Balancer Document**: https://docs.aws.amazon.com/elasticloadbalancing/latest/network/introduction.html
- **Gateway Load Balancer Document**: https://docs.aws.amazon.com/elasticloadbalancing/latest/gateway/introduction.html
- **Classic Load Balancer Document**: https://docs.aws.amazon.com/elasticloadbalancing/latest/classic/introduction.html

  ![image](https://github.com/user-attachments/assets/25e62a6d-c2f5-45cf-a47d-79ec76bb3e6b)

### 11. Migration Services <a name="migration"></a>
#### AWS Migration Hub
- Track migrations from a single place
- **Document**: https://docs.aws.amazon.com/migrationhub/latest/ug/whatishub.html

  ![image](https://github.com/user-attachments/assets/b5c46b01-0ab9-4703-88cf-038e15807472)

#### AWS Application Discovery Service
- Discover on-premises applications to streamline migration
- **Document**: https://docs.aws.amazon.com/application-discovery/latest/userguide/what-is-appdiscovery.html

  ![image](https://github.com/user-attachments/assets/8d8af72b-aa64-4a41-a49f-c0e6c1c61eae)

#### AWS Application Migration Service (MGN)
- Move and improve your on-premises and cloud-based applications
- **Document**: https://docs.aws.amazon.com/mgn/latest/ug/what-is-application-migration-service.html

  ![image](https://github.com/user-attachments/assets/d54db412-d5a3-4087-9e5d-c9d8ea872ccb)

#### AWS Database Migration Service
- Migrate databases with minimal downtime
- **Document**: https://docs.aws.amazon.com/dms/latest/userguide/Welcome.html

  ![image](https://github.com/user-attachments/assets/8440b854-040c-4c6d-acce-b4c52f5c0c69)

#### AWS DataSync
- Simple, fast, online data transfer
- **Document**: https://docs.aws.amazon.com/datasync/latest/userguide/what-is-datasync.html

  ![image](https://github.com/user-attachments/assets/2c404f24-127e-4b14-847b-95322db11ec1)

#### AWS Migration Acceleration Program
- Comprehensive and proven cloud migration program
- **Document**: https://docs.aws.amazon.com/migrationhub/latest/launchguide/map.html

#### AWS Optimization and Licensing Assessment
- Optimize your license and compute costs before and after migration
- **Document**: https://docs.aws.amazon.com/prescriptive-guidance/latest/optimize-costs-microsoft-workloads/aws-ola.html

#### AWS Transfer Family
- Fully managed SFTP, FTPS, FTP, and AS2 service
- **Document**: https://docs.aws.amazon.com/transfer/latest/userguide/what-is-aws-transfer-family.html

  ![image](https://github.com/user-attachments/assets/6c5f8e91-8f02-46ad-b68e-5067a94a1222)

#### AWS Snowball
- Accelerate moving offline data or remote storage to the cloud
- **Document**: https://docs.aws.amazon.com/snowball/latest/developer-guide/whatisedge.html

  ![image](https://github.com/user-attachments/assets/d5d0bbe3-6dea-4ec2-a8ac-5aeec83d71b8)

### 12. Internet of Things Services <a name="internetofthings"></a>
#### AWS IoT Core
- Connect devices to the cloud
- **Document**: https://docs.aws.amazon.com/iot/latest/developerguide/what-is-aws-iot.html

  ![image](https://github.com/user-attachments/assets/4bdd506f-319d-4faa-ad22-e6cca3c37314)

#### AWS IoT Device Defender
- Security management for IoT devices
- **Document**: https://docs.aws.amazon.com/iot-device-defender/latest/devguide/what-is-device-defender.html

  ![image](https://github.com/user-attachments/assets/08dcd4cf-660b-4d2a-808e-2fff381de3bf)

#### AWS IoT Fleet Hub for AWS IoT Device Management
- Monitor device fleets in near-real time.
- Set alerts to notify your technicians about unusual behavior.
- Running jobs.
- **Document**: https://docs.aws.amazon.com/iot/latest/fleethubuserguide/what-is-aws-iot-monitor.html

  ![image](https://github.com/user-attachments/assets/c4d838a1-0cba-4ab1-b891-b224afcf1657)

#### AWS IoT Events
- IoT event detection and response
- **Document**: https://docs.aws.amazon.com/iotevents/latest/developerguide/what-is-iotevents.html

  ![image](https://github.com/user-attachments/assets/60b1aee1-75f4-4344-837a-b295259b7565)

#### AWS IoT FleetWise
- Easily collect, transform, and transfer vehicle data to the cloud in near-real time
- **Document**: https://docs.aws.amazon.com/iot-fleetwise/latest/developerguide/what-is-iotfleetwise.html

  ![image](https://github.com/user-attachments/assets/4c57a7f8-f8c2-4373-83e1-9137d71e50b4)

#### AWS IoT Greengrass
- Local compute, messaging, and sync for devices
- **Document**: https://docs.aws.amazon.com/greengrass/v2/developerguide/what-is-iot-greengrass.html

  ![image](https://github.com/user-attachments/assets/bcedd14d-fe95-4fab-9d0a-a20f8342d608)

#### Amazon Kinesis Video Streams
- Capture, process, and analyze real-time video streams
- **Document**: https://docs.aws.amazon.com/kinesisvideostreams/latest/dg/what-is-kinesis-video.html

#### FreeRTOS
- Real-time operating system for microcontrollers
- **Document**: https://docs.aws.amazon.com/freertos/latest/userguide/what-is-freertos.html

  ![image](https://github.com/user-attachments/assets/b0f59cb7-cc08-4869-a875-5ca7dd2a39a6)

#### Amazon Location Service
- Securely and easily add location data to applications
- **Document**: https://docs.aws.amazon.com/location/

  ![image](https://github.com/user-attachments/assets/48c430bc-c0df-4fe2-8153-96dd578fc542)

#### AWS Device Farm
- Test Android, iOS, and web apps on real devices in the AWS cloud
- **Document**: https://docs.aws.amazon.com/devicefarm/latest/developerguide/welcome.html
 
  ![image](https://github.com/user-attachments/assets/788ee35d-708b-4306-94ec-9377ce04d66f)

### 13. Artificial Intelligence Services <a name="artificialintelligence"></a>
#### Amazon Q
- Generative AI-powered assistant for work
- **Amazon Q Business Document**: https://docs.aws.amazon.com/amazonq/latest/qbusiness-ug/what-is.html
- **Amazon Q Developer Document**: https://docs.aws.amazon.com/amazonq/latest/qdeveloper-ug/what-is.html

  ![image](https://github.com/user-attachments/assets/425c6210-d353-44c5-8b7d-afc26cdbd9c4)

#### Amazon Bedrock
- Build with foundation models
- **Document**: https://docs.aws.amazon.com/bedrock/latest/userguide/what-is-bedrock.html

  ![image](https://github.com/user-attachments/assets/98329a92-a22f-4e0a-a33d-11e0117a2e43)

#### Amazon SageMaker AI
- Build, train, and deploy machine learning models at scale
- **Document**: https://docs.aws.amazon.com/sagemaker/latest/dg/whatis.html

  ![image](https://github.com/user-attachments/assets/af9fd837-febd-48b9-8f4b-deb2605eddf4)

#### Amazon SageMaker Unified Studio
- It is a unified development experience that brings together AWS data, analytics, artificial intelligence (AI), and machine learning (ML) services.
- It provides a place to build, deploy, execute, and monitor end-to-end workflows from a single interface. 
- **Document**: https://docs.aws.amazon.com/sagemaker-unified-studio/latest/userguide/what-is-sagemaker-unified-studio.html

#### AWS App Studio 
- Fastest and easiest way to build enterprise-grade applications
- **Document**: https://docs.aws.amazon.com/appstudio/latest/userguide/welcome.html

#### Amazon Augmented AI
- Easily implement human review of ML predictions
- **Document**: https://docs.aws.amazon.com/sagemaker/latest/dg/a2i-use-augmented-ai-a2i-human-review-loops.html?icmpid=docs_a2i_lp

  ![image](https://github.com/user-attachments/assets/ef81bb63-95a6-411c-8e96-6c1af9acd9f5)

#### Amazon CodeGuru
- Find your most expensive lines of code
- **CodeGuru Security Document**: https://docs.aws.amazon.com/codeguru/latest/security-ug/what-is-codeguru-security.html
- **CodeGuru Profiler Document**: https://docs.aws.amazon.com/codeguru/latest/profiler-ug/what-is-codeguru-profiler.html
- **CodeGuru Reviewer Document**: https://docs.aws.amazon.com/codeguru/latest/reviewer-ug/welcome.html
- **Bugbust Document**: https://docs.aws.amazon.com/codeguru/latest/bugbust-ug/what-is-aws-bugbust.html

  ![image](https://github.com/user-attachments/assets/3219337d-e112-4e94-b0f7-5bf3989fce40)

#### Amazon Comprehend
- Discover insights and relationships in text
- **Document**: https://docs.aws.amazon.com/comprehend/latest/dg/what-is.html

  ![image](https://github.com/user-attachments/assets/6bf263a6-0949-448a-9257-2a19d6a279b9)

#### Amazon Comprehend Medical
- Extract health data
- **Document**: https://docs.aws.amazon.com/comprehend-medical/latest/dev/comprehendmedical-welcome.html

  ![image](https://github.com/user-attachments/assets/1b4c4876-d34d-4666-b484-f825e448316f)

#### Amazon Fraud Detector
- Detect more online fraud faster
- **Document**: https://docs.aws.amazon.com/frauddetector/latest/ug/what-is-frauddetector.html

  ![image](https://github.com/user-attachments/assets/172bf551-dc87-4033-9e3f-a0186a199d07)

#### Amazon Kendra
- Reinvent enterprise search with ML
- It is a managed information retrieval and intelligent search service that uses natural language processing and advanced deep learning model.
- Unlike traditional keyword-based search, Amazon Kendra uses semantic and contextual similarity—and ranking capabilities—to decide whether a text chunk or document is relevant to a retrieval query.
- **Document**: https://docs.aws.amazon.com/kendra/latest/dg/what-is-kendra.html

  ![image](https://github.com/user-attachments/assets/f00db50a-a5a5-4f8e-86fb-8b3e02ea843f)

#### Amazon Lex
- Build voice and text chatbots
- **Document**: https://docs.aws.amazon.com/lexv2/latest/dg/what-is.html

  ![image](https://github.com/user-attachments/assets/2d96458b-f3c4-4b93-b27a-13428679940f)

#### AWS HealthLake
- Make sense of health data
- **Document**: https://docs.aws.amazon.com/healthlake/latest/devguide/what-is.html

  ![image](https://github.com/user-attachments/assets/75ccc247-6457-4832-8551-59ab89df0e45)

#### Amazon Personalize
- Build real-time recommendations into your applications
- **Document**: https://docs.aws.amazon.com/personalize/latest/dg/what-is-personalize.html

  ![image](https://github.com/user-attachments/assets/80d82681-b6d5-4ea2-a258-60ce9587678b)

#### Amazon Polly
- Turn text into life-like speech
- **Document**: https://docs.aws.amazon.com/polly/latest/dg/what-is.html

  ![image](https://github.com/user-attachments/assets/89097877-52e8-4579-80e8-47a5998e228c)

#### Amazon Rekognition
- Analyze image and video
- **Document**: https://docs.aws.amazon.com/rekognition/latest/dg/what-is.html

  ![image](https://github.com/user-attachments/assets/2d0e9698-adff-4a75-8b1a-f76a8ba6d08c)

#### Amazon Textract
- Extract text and data from **Document**s
- **Document**: https://docs.aws.amazon.com/textract/latest/dg/what-is.html

  ![image](https://github.com/user-attachments/assets/96758965-8986-4276-acd9-71d1447b44bc)

#### Amazon Translate
- Natural and fluent language translation
- **Document**: https://docs.aws.amazon.com/translate/latest/dg/what-is.html

  ![image](https://github.com/user-attachments/assets/e3371ec4-4745-4f06-8620-6369631f8c42)

#### Amazon Transcribe
- Automatic speech recognition
- **Document**: https://docs.aws.amazon.com/transcribe/latest/dg/what-is.html

  ![image](https://github.com/user-attachments/assets/d4c9646d-85fa-4593-90d4-5c932631ae6a)

## AWS Hands-on Labs <a name="handsonlabs"></a>

### HANDS-ON-01: Provisioning EC2s on VPC, Creating Key-Pair, Connecting EC2 <a name="ec2_vpc_key_pair"></a>
- This sample shows:
  - how to create Key-pairs (public and private keys) on AWS,
  - how to create EC2s (Ubuntu 20.04, Windows 2019 Server),
  - how to create Virtual Private Cloud (VPC), VPC Components (Public Subnet, Internet Gateway, Route Table) and link to each others,
  - how to create Security Groups (for SSH and Remote Desktop).

- **Go to the Hands-On:**
  - [HANDS-ON-01: Provisioning EC2s on VPC, Creating Key-Pair, Connecting EC2](https://github.com/omerbsezer/Fast-AWS/blob/main/HANDS-ON-001-EC2-VPC-Connect.md)
 
    ![ec2-vpc](https://github.com/user-attachments/assets/cdec4f1f-09cd-44a9-95db-78748388b057)
  
### HANDS-ON-02: Provisioning Lambda, API Gateway and Reaching HTML Page in Python Code From Browser <a name="lambda_apigateway_python"></a>
- This hands-on shows:
  - how to create Lambda function with Python code,
  - how to create lambda role, policy, policy-role attachment, lambda api gateway permission, zipping code,
  - how to create api-gateway resource and method definition, lambda - api gateway connection, deploying api gateway, api-gateway deployment URL as output
  - details on AWS Lambda, API-Gateway, IAM.

- **Go to the Hands-On:**
  - [HANDS-ON-02: Provisioning Lambda, API Gateway and Reaching HTML Page in Python Code From Browser](https://github.com/omerbsezer/Fast-AWS/blob/main/HANDS-ON-002-Lambda-API-Gateway-Python.md)
 
    ![lambda-cloudwatch-apigw](https://github.com/user-attachments/assets/512124ff-4d0d-4f06-a608-f5276624a164)
  
### HANDS-ON-03: EBS and EFS Configuration with EC2s <a name="ebs_efs_ec2"></a>
- This hands-on shows:
  - how to create EBS, mount on Ubuntu and Windows Instances,
  - how to create EFS, mount on Ubuntu Instance,
  - how to provision VPC, subnet, IGW, route table, security group.

- **Go to the Hands-On:**
  - [HANDS-ON-03: EBS and EFS Configuration with EC2s](https://github.com/omerbsezer/Fast-AWS/blob/main/HANDS-ON-003-EC2-EBS-EFS.md)
 
    ![ebs-efs-ec2](https://github.com/user-attachments/assets/9b2eef86-ca6f-4ba8-b1b5-5766364ebbbd)
  
### HANDS-ON-04: Provisioning ECR, Pushing Image to ECR, Provisioning ECS, VPC, ELB, ECS Tasks, Service on Fargate Cluster <a name="ecr_ecs_elb_vpc_ecs_service_fargate"></a>  
- This hands-on shows:
  - how to create Flask-app Docker image,
  - how to provision ECR and push to image to this ECR,
  - how to provision VPC, Internet Gateway, Route Table, 3 Public Subnets,
  - how to provision ALB (Application Load Balancer), Listener, Target Group,
  - how to provision ECS Fargate Cluster, Task and Service (running container as Service).

- **Go to the Hands-On:**
  - [HANDS-ON-04: Provisioning ECR, Pushing Image to ECR, Provisioning ECS, VPC, ELB, ECS Tasks, Service on Fargate Cluster](https://github.com/omerbsezer/Fast-AWS/blob/main/HANDS-ON-004-ECR-ECS-ELB-VPC-ECS-Service.md)
 
  ![ECR-ECS-ELB-VPC-ECS-Service2](https://github.com/user-attachments/assets/a19b62a9-8218-47f6-81c6-c6672606dadb)

 ### HANDS-ON-05: Provisioning ECR, Lambda and API Gateway to run Flask App Container on Lambda <a name="ecr_lambda_apigateway_container"></a>  
- This hands-on shows:
  - how to create Flask-app-serverless image to run on Lambda,
  - how to create ECR and to push image to ECR,
  - how to create Lambda function, Lambda role, policy, policy-role attachment, Lambda API Gateway permission,
  - how to create API Gateway resource and method definition, Lambda - API Gateway connection, deploying API Gateway.

- **Go to the Hands-On:**
  - [HANDS-ON-05: Provisioning ECR, Lambda and API Gateway to run Flask App Container on Lambda](https://github.com/omerbsezer/Fast-AWS/blob/main/HANDS-ON-005-Lambda-Container-ApiGateway-FlaskApp.md)
 
    ![image](https://user-images.githubusercontent.com/10358317/233119705-ba6544e0-dbfc-49f5-9a65-c20b82f7bae1.png)

### HANDS-ON-06: Provisioning EKS with Managed Nodes using Blueprint and Modules <a name="eks_managednodes_blueprint"></a>  
- This hands-on shows:
  - how to create EKS cluster with managed nodes using BluePrints and Modules.
  - EKS Blueprint is used to provision EKS cluster with managed nodes easily. 
  - EKS Blueprint is used from: 
    - https://github.com/aws-ia/terraform-aws-eks-blueprints

- **Go to the Hands-On:** 
  - [HANDS-ON-06: Provisioning EKS with Managed Nodes using Blueprint and Modules](https://github.com/omerbsezer/Fast-AWS/blob/main/HANDS-ON-006-EKS-ManagedNodes-Blueprint.md)

 ### HANDS-ON-07: Provisioning CodeCommit, CodePipeline and Triggering CodeBuild and CodeDeploy Container in Lambda <a name="ci_cd"></a>  
- This hands-on shows:
  - how to create code repository using CodeCommit,
  - how to create pipeline with CodePipeline, create S3 bucket to store Artifacts for codepipeline stages' connection (source, build, deploy),
  - how to create builder with CodeBuild ('buildspec_build.yaml'), build the source code, create a Docker image,
  - how to create ECR (Elastic Container Repository) and push the build image into the ECR,
  - how to create Lambda Function (by CodeBuild automatically) and run/deploy container on Lambda ('buildspec_deploy.yaml').

- **Go to the Hands-On:**    
  - [HANDS-ON-07: Provisioning CodeCommit, CodePipeline and Triggering CodeBuild and CodeDeploy Container in Lambda](https://github.com/omerbsezer/Fast-AWS/blob/main/HANDS-ON-007-CodeCommit-Pipeline-Build-Deploy-Lambda.md)
 
    ![image](https://user-images.githubusercontent.com/10358317/233652299-66b39788-66ee-4a5e-b8e0-ece418fe98e3.png)

 ### SAMPLE-08: Provisioning S3 and CloudFront to serve Static Web Site <a name="s3_cloudfront"></a>
- This hands-on shows:
  - how to create S3 Bucket, 
  - how to to copy the website to S3 Bucket, 
  - how to configure S3 bucket policy,
  - how to create CloudFront distribution to refer S3 Static Web Site,
  - how to configure CloudFront (default_cache_behavior, ordered_cache_behavior, ttl, price_class, restrictions, viewer_certificate).

- **Go to the Hands-On:**    
  - [HANDS-ON-08: Provisioning S3, CloudFront to serve Static Web Site](https://github.com/omerbsezer/Fast-AWS/blob/main/HANDS-ON-008-S3-CloudFront-Static-WebSite.md)

 ### HANDS-ON-09: Provisioned Gitlab Runner on EC2, connection to Gitlab Server using Docker on-premise <a name="gitlabrunner"></a>
- This hands-on shows:
  - how to run Gitlab Server using Docker on WSL2 on-premise,
  - how to redirect external traffic to docker container port (Gitlab server),
  - how to configure on-premise PC network configuration,
  - how to run EC2 and install docker, gitlab-runner on EC2,
  - how to register Gitlab runner on EC2 to Gitlab Server on-premise (in Home),
  - how to run job on EC2 and returns artifacts to Gitlab Server on-premise (in Home).

- **Go to the Hands-On:**
  - [HANDS-ON-09: Provisioned Gitlab Runner on EC2, connection to Gitlab Server using Docker on-premise](https://github.com/omerbsezer/Fast-AWS/blob/main/HANDS-ON-009-GitlabServer-on-Premise-GitlabRunner-on-EC2.md)

 ### HANDS-ON-10: Implementing MLOps Pipeline using GitHub, CodePipeline, CodeBuild, CodeDeploy, Sagemaker Endpoint <a name="sagemaker"></a>
- This hands-on shows:
  - how to create MLOps Pipeline 
  - how to use GitHub Hooks (Getting Source Code from Github to CodePipeline)
  - how to create Build CodePipeline (Source, Build), CodeBuild (modelbuild_buildspec.yml), Deploy CodePipeline (Source, Build, DeployStaging, DeployProd), CodeBuild (modeldeploy_buildspec.yml)
  - how to save the model and artifacts on S3
  - how to create and test models using Notebooks

- **Go to the Hands-On:**
  - [HANDS-ON-10: Implementing MLOps Pipeline using GitHub, CodePipeline, CodeBuild, CodeDeploy, Sagemaker Endpoint](https://github.com/omerbsezer/Fast-AWS/blob/main/HANDS-ON-010-MLOps-SageMaker-GitHub-Codepipeline-CodeBuild-CodeDeploy.md)
 
    ![image](https://github.com/user-attachments/assets/fa30614b-b4da-4fcc-b901-4b83bbee9440)

## References  <a name="references"></a>
- https://docs.aws.amazon.com
- https://aws.amazon.com/
- https://github.com/aws-samples
- https://github.com/aws-ia/terraform-aws-eks-blueprints
- https://github.com/aws-ia
- https://github.com/orgs/aws-samples/repositories?q=Terraform&type=all&language=&sort=
- https://github.com/aws-samples/aws-generative-ai-terraform-samples
- https://github.com/aws-samples/amazon-eks-machine-learning-with-terraform-and-kubeflow
