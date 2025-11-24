# IBM watsonx Orchestrate API Setup Guide

This guide helps you find your API endpoint and credentials for IBM watsonx Orchestrate.

## Getting the API Endpoint

The watsonx Orchestrate API endpoint varies depending on the offering that you use. Follow the instructions for your specific offering.

### 1. IBM Cloud Offering

To get the API endpoint for the IBM Cloud offering:

1.  Log in to your [watsonx Orchestrate account](https://cloud.ibm.com/).
2.  Click your **profile icon** > **Settings**.
3.  Select the **API details** tab.
4.  Copy the **Service instance URL**.

**Endpoint Format:**
```
https://<hostname>/instances/<tenant_id>
```

**Where:**
*   `<hostname>` is the watsonx Orchestrate base URL (e.g., `https://api.us-south.watson.orchestrate.cloud.ibm.com/`)
*   `<tenant_id>` is your watsonx Orchestrate tenant ID.

### 2. Amazon Web Services (AWS) Offering

To get the API endpoint for the AWS offering:

1.  Log in to your watsonx Orchestrate account.
2.  Click your **profile icon** > **Settings**.
3.  Select the **API details** tab.
4.  Copy the **Service instance URL**.

**Endpoint Format:**
```
https://api.<region_code>.watson-orchestrate.ibm.com/instances/<tenant_id>
```

**Where:**
*   `<region_code>` is the AWS region where your instance is hosted.
*   `<tenant_id>` is your watsonx Orchestrate tenant ID.

### 3. On-premises Offering

For the on-premises offering, the endpoint depends on the API you want to use.

**watsonx Orchestrate API endpoint:**
```
https://{onprem_host}:{port}/orchestrate/{namespace}/instances/{instanceid}/v1
```

**Parameters:**
*   `{onprem_host}`: Hostname or IP of your IBM Software Hub cluster.
*   `{port}`: Port number if required.
*   `{namespace}`: Namespace where your instance is deployed.
*   `{instanceid}`: Unique identifier of your instance (the number after `orchestrate-` in the instance details URL).

### 4. Using IBM Cloud Shell (Automated)

If you have access to the [IBM Cloud Shell](https://cloud.ibm.com/shell), you can use our helper script to find your credentials automatically.

1.  Open [IBM Cloud Shell](https://cloud.ibm.com/shell).
2.  Copy and paste the following command:

```bash
curl -sL https://raw.githubusercontent.com/Rikinshah787/IBM_WATSON_HAC/main/backend/setup_watson.sh | bash
```
*(Note: If the repo is private or you haven't pushed the script yet, you can copy the content of `backend/setup_watson.sh` and paste it into a file in Cloud Shell)*

**Alternative (Manual Copy-Paste):**
1.  In Cloud Shell, type `nano setup_watson.sh`
2.  Paste the content of `backend/setup_watson.sh`
3.  Press `Ctrl+X`, then `Y`, then `Enter` to save.
4.  Run `bash setup_watson.sh`

---

## Verifying Your Setup

We have provided a debug script to help you verify your configuration.

### Running the Debug Script

1.  Open a terminal in the `backend` directory.
2.  Run the following command:

```bash
python debug_watson_setup.py
```

This script will:
*   Check if your `.env` file exists.
*   Verify your API Key and Project ID are set.
*   Test the connection to IBM watsonx.ai.
*   Test the connection to IBM watsonx Orchestrate.

### Common Issues

*   **Missing Credentials**: Ensure you have copied `.env.example` to `.env` and filled in your values.
*   **Invalid URL**: Make sure your `WATSONX_ORCHESTRATE_URL` includes the `/instances/<tenant_id>` part if required by your specific endpoint version, though typically the base URL is sufficient for the SDK.
*   **Connection Error**: Check your internet connection and ensure you are not behind a corporate firewall blocking the IBM Cloud APIs.
