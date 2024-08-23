# Build and Push to ECR Workflow

This GitHub Actions workflow automates the process of building a Docker image from your BentoML service and pushing it
to Amazon Elastic Container Registry (ECR).

## Workflow Overview

This workflow performs the following steps:

- Checkout the repository code.
- Configure AWS credentials for deployment.
- Login to Amazon ECR.
- Install Python.
- Set a short SHA of the commit in the environment.
- Install required libraries.
- Download models `(optional)`.
- Build the BentoML service.
- Clean package cache.
- Run Docker system prune to free up space.
- Containerize the BentoML service.
- Tag and push the Docker image to Amazon ECR.

## How to Run

This workflow is triggered manually using the `workflow_dispatch` event. To run the workflow:

1. Go to the `Actions` tab in your GitHub repository.
2. Select the `Build and Push to ECR` workflow.
3. Click on the `Run workflow` button

The python version is set to `3.8` by default. In case you need to use any other version,
you need to update in the `.github/workflows/build.yaml` file at this step

```bash
- name: Install python
  uses: actions/setup-python@v5
  with:
    python-version: 3.12.3
```

## Variables and Secrets

### Required Variables

These variables need to be defined in the repository settings under `Settings` > `Secrets and variables` > `actions`:

- **ECR_REGISTRY_URI**: The URI of your ECR repository `(e.g.,XXXXXXXXXXXX.dkr.ecr.ap-south-1.amazonaws.com/iris-classifier-service)`.
The `iris_classifier_service` will needs to be replacedvwith your service name.
