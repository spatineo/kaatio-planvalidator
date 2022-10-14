import os

import aws_cdk as cdk
from stacks import KaatioPlanValidatorStack

app = cdk.App()

KaatioPlanValidatorStack(
    app,
    "KaatioPlanValidatorStack",
    env=cdk.Environment(
        account=os.environ["CDK_DEFAULT_ACCOUNT"],
        region=os.environ["CDK_DEFAULT_REGION"],
    ),
)

app.synth()
