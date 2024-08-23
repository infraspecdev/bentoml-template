# Test workflow

This GitHub Actions workflow sets up a Continuous Integration (CI) pipeline for the BentoML template. It includes jobs
for running unit tests

## Workflow Overview

1. **Unit Tests**
   This job performs the following steps:

    - **Checkout code:** Checks out the repository code using actions/checkout@v3.
    - **Install Python 3.12.3:** Sets up Python 3.12.3 using actions/setup-python@v5.
    - **Install dependencies:** Installs the required dependencies listed in `requirements.txt`.
    - **Run unit tests:** Executes the unit tests located in the tests/ directory using pytest.

## How to Run

This workflow is triggered automatically on the push event. To view the workflow run:

1. Go to the `Actions` tab in your GitHub repository.
2. Select the `Test` workflow.

The python version is set to 3.8 by default. In case you need to use any other version,
you need to update in the `.github/workflows/main.yaml` file at this step

```bash
- name: Install python
  uses: actions/setup-python@v5
  with:
    python-version: 3.12.3
```
