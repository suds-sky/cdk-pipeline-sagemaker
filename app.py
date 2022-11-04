#!/usr/bin/env python3

import aws_cdk as cdk

from cdk_pipeline.pipeline_stack import PipelineStack

app = cdk.App()
PipelineStack(app, "ml-pipeline")

app.synth()
