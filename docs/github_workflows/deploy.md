# GitHub Actions Workflow: Deploy Model API Service

This GitHub Actions workflow automates the deployment of a Model API service to Amazon ECS.
It pulls the build from ECR based on the commit and deploys the service, ensures the deployment
is stable, and manages task definition revisions.

## Workflow Overview

- **Name**: Deploy Model API Service
- **Trigger**: Manually triggered via GitHub Actions UI `(workflow_dispatch)`
- **Environments**: staging, production

## How to Run

1. **Trigger the Workflow:**

    - Go to the GitHub `Actions` tab in your repository.
    - Select `Deploy Model API Service` and click "Run workflow".
    - Choose the deployment environment (staging or production).

## Setup Instructions

### Environment Variables and Secrets

Create new environment `staging`/`production` under `Settings` > `Environments` > `New environment`.
Ensure the following variables and secrets are configured for the deployment environment:

#### Variables

- **AWS_REGION:** The AWS region where your ECS cluster is located.
- **AWS_ROLE_TO_ASSUME:** The IAM role ARN to assume for AWS operations.
- **TASK_DEFINITION_NAME:** The name of the ECS task definition.
- **ECS_CLUSTER_ARN:** The ARN of the ECS cluster.
- **ECS_SERVICE_ARN:** The ARN of the ECS service.
- **ECS_CONTAINER_NAME:** The name of the container in the task definition.
- **ECR_REGISTRY_URI:** The URI of the Amazon ECR registry.
- **ECS_TASK_ARN_PREFIX:** The ARN prefix for the ECS tasks.
- **ENVIRONMENT:** The environment value to tag the ECS task.

The above-mentioned variables are a one-time setup, and their values will be available after the infrastructure setup
for the service is complete.

### Note

When you trigger the deploy workflow, it will retrieve the image from ECR that is tagged and pushed with that commit. If
you have not built the image but attempt to deploy, the deployment will fail because it cannot find the build for
deployment. Ensure that for every deployment of a commit, you have a corresponding build for that commit.

### Rollback Plan

If the model is not behaving properly due to recent changes, you can revert the PR or the changes. Then, run the build
workflow and deploy workflow again. You can also find the last deployed workflow run in the Actions tab. Click "Re-run"
to deploy the changes at that commit ID.
