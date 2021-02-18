 

## Project Title

Lambda Collection Functions

## Introduction

We implement this feature to take the advantages of AWS Lambda but still have a standard git-based approach where code can be reviewed prior to being deployed to production instead using the AWS web console editor. On the other hand, with this framework, we can easily deploy a Lambda ETL.

## Prerequisites

Install Nodejs

Install Docker

Install serverless & plugins:
npm install -g serverless 
sls plugin install -n serverless-python-requirements
sls plugin install -n serverless-step-functions
sls plugin install -n serverless-pseudo-parameters



## How to use
Check this docs to know about the folder structure
https://docs.google.com/spreadsheets/d/16-D7BmGKEq5GNWTmgrDvtrdmgRasiaqri1780XMIVSo/edit#gid=600373381

Check file functions/instagram/post_comment/function_step_scripts/main_step.py to know how it run.

Check functions/serverless_templates and functions/instagram/post_comment/deployment/deploy.py to how it make serverless.yml

Run the deploy.py file in deployment folder for deploying it to AWS.



