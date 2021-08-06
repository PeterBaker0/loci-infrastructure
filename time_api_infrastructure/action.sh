yes | aws sso login --profile "${2}" && cdk "${1}" --require-approval never --profile "${3}" --output_file "deployment_resources.json"
