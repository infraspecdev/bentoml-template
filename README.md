# BentoML Template

This repository contains the BentoML template for model API deployments.

## Prerequisites

Before you begin, ensure you have met the following requirements:

1. [install python](https://www.python.org/downloads/)
2. [install pip](https://pip.pypa.io/en/stable/installation/)
3. [install aws](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html) and login to your account.
4. A model stored in a S3 bucket in `.pickle` format.

## Usage

To use this template, clone the repository and customize it according to your model's requirements. Below is a quick start guide:

1. **Clone the repository:**

   ```sh
   git clone https://github.com/infraspecdev/bentoml-template.git
   cd bentoml-template
   ```
2. **Customize the template:**

   - Update `config.ini` to download the correct models from your S3 bucket.
   - Update 'validations.py` to change the input validation for your model.
   - Update `service.py` to use your model.
   - Update `bentofile.yaml` If you have changed the service name in `service.py`.

3. **Run these commands to create a python environment:**
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```
4. **Run these commands to install all the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
5. **Run these commands to start the service:**
    ```bash
    bentoml serve .
    ```
