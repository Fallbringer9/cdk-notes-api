from aws_cdk import (
    Stack,
    RemovalPolicy,
    Duration,
    aws_dynamodb as ddb,
    aws_apigateway as apigw,
    aws_lambda as _lambda,
    aws_logs as logs,
)
from constructs import Construct


class CdkNotesApiStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # DynamoDB — table simple (Free Tier friendly)
        self.table = ddb.Table(
            self, "NotesTable",
            table_name="notes-table",
            partition_key=ddb.Attribute(name="note_id", type=ddb.AttributeType.STRING),
            billing_mode=ddb.BillingMode.PAY_PER_REQUEST,
            removal_policy=RemovalPolicy.RETAIN,
            encryption=ddb.TableEncryption.DEFAULT,
        )

        # API Gateway — squelette
        self.api = apigw.RestApi(
            self, "NotesApi",
            rest_api_name="notes-api",
            deploy_options=apigw.StageOptions(
                stage_name="prod",
                logging_level=apigw.MethodLoggingLevel.INFO,
                data_trace_enabled=False,
                metrics_enabled=True,
            ),
            cloud_watch_role=True,
        )

        # Arbo: /notes et /notes/{id}
        notes = self.api.root.add_resource("notes")
        note_id = notes.add_resource("{id}")

        # Lambda: CreateNote (POST /notes)
        create_note_fn = _lambda.Function(
            self, "CreateNoteFn",
            function_name="notes-create",
            description="Create a note item in DynamoDB (PutItem)",
            runtime=_lambda.Runtime.PYTHON_3_11,
            handler="handler.handler",
            code=_lambda.Code.from_asset("src/create_note"),
            timeout=Duration.seconds(5),
            memory_size=128,
            environment={
                "NOTES_TABLE": self.table.table_name,
            },
            log_retention=logs.RetentionDays.ONE_WEEK,
        )

        # IAM minimal: écriture sur la table
        self.table.grant_write_data(create_note_fn)

        # Route: POST /notes -> CreateNoteFn
        notes.add_method("POST", apigw.LambdaIntegration(create_note_fn))

        # Lambda: GetNote (GET /notes/{id})
        get_note_fn = _lambda.Function(
            self, "GetNoteFn",
            function_name="notes-get",
            description="Get a note item from DynamoDB (GetItem)",
            runtime=_lambda.Runtime.PYTHON_3_11,
            handler="handler.handler",
            code=_lambda.Code.from_asset("src/get_note"),
            timeout=Duration.seconds(5),
            memory_size=128,
            environment={"NOTES_TABLE": self.table.table_name},
            log_retention=logs.RetentionDays.ONE_WEEK,
        )

        # IAM minimal: lecture sur la table
        self.table.grant_read_data(get_note_fn)

        # Route: GET /notes/{id} -> GetNoteFn
        note_id.add_method("GET", apigw.LambdaIntegration(get_note_fn))

        delete_note_fn = _lambda.Function(
            self, "DeleteNoteFn",
            function_name="notes-delete",
            runtime=_lambda.Runtime.PYTHON_3_11,
            handler="handler.handler",
            code=_lambda.Code.from_asset("src/delete_note"),
            timeout=Duration.seconds(5),
            memory_size=128,
            environment={"NOTES_TABLE": self.table.table_name},
            log_retention=logs.RetentionDays.ONE_WEEK,
        )

        self.table.grant_read_data(delete_note_fn)
        self.table.grant_write_data(delete_note_fn)
        note_id.add_method("DELETE", apigw.LambdaIntegration(delete_note_fn))
