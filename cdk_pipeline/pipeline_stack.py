from aws_cdk import (
    Stack,
    pipelines as pipelines,
    aws_codepipeline_actions as codepipeline_actions,
    aws_iam as iam, SecretValue
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
                trigger=codepipeline_actions.GitHubTrigger.WEBHOOK,
                authentication=SecretValue.secrets_manager(
                    "cdk_pipeline_github", json_field='github')
            ),
            commands=[
                "npm install -g aws-cdk",
                "curl -sSL https://install.python-poetry.org | python3 -",
                "export PATH=\"/root/.local/bin:$PATH\"",
                "poetry install",
                "cdk synth --no-lookups"
            ],
        )

        pipeline = pipelines.CodePipeline(
            self,
            "Pipeline",
            self_mutation=True,
            pipeline_name=PROJECT_NAME,
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
