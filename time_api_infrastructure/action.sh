aws sso login --profile "${2}" && cdk "${1}" --profile "${3}"
