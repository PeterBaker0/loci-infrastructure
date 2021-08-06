aws sso login --profile locipoweruser
yes | cdk destroy --require-approval never --profile lociauto
yes | cdk deploy --require-approval never --profile lociauto
