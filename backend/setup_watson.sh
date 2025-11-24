#!/bin/bash

# Setup Script for Watson Credentials
# Run this in IBM Cloud Shell (https://cloud.ibm.com/shell)

echo "=================================================="
echo "   Watson Credential Finder"
echo "=================================================="

# 1. Check if logged in (Cloud Shell is usually logged in)
if ! ibmcloud target > /dev/null 2>&1; then
    echo "Not logged in. Please run 'ibmcloud login' first."
    exit 1
fi

echo "🔍 Scanning for Watson services..."

# 2. List all services containing 'watson' or 'orchestrate'
# We use json output for easier parsing if jq is available, but text is safer for basic shell
services=$(ibmcloud resource service-instances --output json | grep -iE "watson|orchestrate" || echo "")

if [ -z "$services" ]; then
    echo "❌ No Watson services found in the current resource group."
    echo "Try switching resource groups with 'ibmcloud target -g <resource_group>'"
    echo "Available resource groups:"
    ibmcloud resource groups
    exit 1
fi

echo "✅ Found potential Watson services."

# 3. Function to get credentials for a service
get_credentials() {
    local service_name="$1"
    local service_id="$2"
    
    echo "--------------------------------------------------"
    echo "Checking service: $service_name"
    
    # List existing keys
    keys=$(ibmcloud resource service-keys --instance-id "$service_id" --output json)
    
    # Check if any key exists
    key_id=$(echo "$keys" | grep -o '"id": "[^"]*"' | head -n 1 | cut -d'"' -f4)
    
    if [ -z "$key_id" ]; then
        echo "   No API keys found. Creating a new key 'auto-generated-key'..."
        # Create a new key
        new_key=$(ibmcloud resource service-key-create "auto-generated-key" Manager --instance-id "$service_id" --output json)
        key_id=$(echo "$new_key" | grep -o '"id": "[^"]*"' | head -n 1 | cut -d'"' -f4)
    else
        echo "   Found existing API key."
    fi
    
    if [ -n "$key_id" ]; then
        # Get key details
        key_details=$(ibmcloud resource service-key "$key_id" --output json)
        
        apikey=$(echo "$key_details" | grep -o '"apikey": "[^"]*"' | cut -d'"' -f4)
        url=$(echo "$key_details" | grep -o '"url": "[^"]*"' | cut -d'"' -f4)
        
        if [ -n "$apikey" ]; then
            echo "   🔑 API KEY: $apikey"
        fi
        if [ -n "$url" ]; then
            echo "   🌐 URL: $url"
        fi
    else
        echo "   ❌ Could not retrieve/create API key."
    fi
}

# 4. Iterate through services (simplified parsing)
# This is a bit hacky without jq, but works for standard output
ibmcloud resource service-instances --output json | grep -E '"name":| "id":' | while read -r line; do
    if [[ $line == *"name"* ]]; then
        current_name=$(echo $line | cut -d'"' -f4)
    elif [[ $line == *"id"* ]]; then
        current_id=$(echo $line | cut -d'"' -f4)
        
        # Check if it matches our filter
        if [[ $current_name == *"watson"* ]] || [[ $current_name == *"orchestrate"* ]]; then
            get_credentials "$current_name" "$current_id"
        fi
    fi
done

echo "=================================================="
echo "Copy the values above to your .env file."
