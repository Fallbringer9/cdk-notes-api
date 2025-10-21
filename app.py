import aws_cdk as cdk
from cdk_notes_api.cdk_notes_api_stack import CdkNotesApiStack

app = cdk.App()

env_eu = cdk.Environment(
    account="309232818774",     # <-- ton Account ID
    region="eu-west-3",         # Paris
)

CdkNotesApiStack(app, "CdkNotesApiStack", env=env_eu)

app.synth()
