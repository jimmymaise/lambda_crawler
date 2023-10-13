# Social Media Data Aggregation

## Overview
The repository is an solution designed to facilitate data crawling from social media platforms like Facebook and Instagram. Built on AWS Lambda and Python, it adopts a git-centric methodology for code review and deployment, replacing the need to rely solely on AWS's web console editor.

## Core Technologies
- **AWS Lambda**: Serverless compute service
- **Python**: Programming language for data crawling and API development
- **Serverless Framework**: Deployment and operational framework
- **Docker**: Containerization platform
- **Node.js**: JavaScript runtime for server-side scripting

## System Requirements
To utilize this framework, ensure that your environment meets the following prerequisites:

### Software
- Node.js
- Docker

### Libraries & Plugins
The following Serverless plugins are required. Install them by executing the commands below:

npm install -g serverless 
sls plugin install -n serverless-python-requirements
sls plugin install -n serverless-step-functions
sls plugin install -n serverless-pseudo-parameters

## User Guide

### Directory Structure
For an understanding of the project's directory layout, please consult the accompanying documentation.

### Code Execution Flow
The main execution script for data crawling from Instagram is located at:
`functions/instagram/post_comment/function_step_scripts/main_step.py`.

### Deployment Configuration
Sample `serverless.yml` files can be found in the `functions/serverless_templates` directory, and for deploying specific functionalities like Instagram comments, refer to:
`functions/instagram/post_comment/deployment/deploy.py`.

### Deployment Procedure
Execute the `deploy.py` script within the `deployment` directory to deploy your code to AWS Lambda.

For additional queries or support, refer to the project documentation or contact the development team.
