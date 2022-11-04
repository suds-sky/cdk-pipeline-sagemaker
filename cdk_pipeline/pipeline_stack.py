from aws_cdk import (
    Stack,
    pipelines as pipelines,
    aws_iam as iam
)
from constructs import Construct

PROJECT_NAME = "cdk-pipeline-sagemaker"


class PipelineStack(Stack):
    def __init__(self, scope: Construct, id: str):
        super().__init__(scope, id=id)

        synth_step = pipelines.CodeBuildStep(
            id="Synth",
            input=pipelines.CodePipelineSource.git_hub(
                repo_string=f"suds-sky/{PROJECT_NAME}",
                branch="main",
            ),
            commands=[
                "npm install -g aws-cdk",
                "poetry install",
                "cdk synth --no-lookups"
            ]
        )

        pipeline = pipelines.CodePipeline(
            self,
            "Pipeline",
            self_mutation=True,
            pipeline_name=f"{PROJECT_NAME}-poc",
            docker_enabled_for_synth=False,
            docker_enabled_for_self_mutation=False,
            synth=synth_step,
            code_build_defaults=pipelines.CodeBuildOptions(
                role_policy=[
                    iam.PolicyStatement(
                        actions=["sagemaker:ListModelPackages"],
                        resources=["*"],
                    )
                ]
            ),
        )

        pipeline.build_pipeline()
