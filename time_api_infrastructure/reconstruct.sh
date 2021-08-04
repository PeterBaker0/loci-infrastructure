aws sso login --profile locipoweruser
cdk destroy --require-approval never --profile lociauto
cdk deploy --require-approval never --profile lociauto
