from pathlib import Path

from aws_cdk import (
    RemovalPolicy,
    Stack,
    aws_ec2,
    aws_ecr_assets,
    aws_ecs,
    aws_ecs_patterns,
    aws_elasticloadbalancingv2,
    aws_logs,
)
from constructs import Construct

PROJECT_DIR = Path(__file__).parent.parent.parent


class KaatioPlanValidatorStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        docker_image_asset_gunicorn = aws_ecr_assets.DockerImageAsset(
            self,
            "DockerImageAsset/Gunicorn",
            directory=str(PROJECT_DIR),
            file="docker/gunicorn/Dockerfile",
            network_mode=aws_ecr_assets.NetworkMode.HOST,
        )

        docker_image_asset_nginx = aws_ecr_assets.DockerImageAsset(
            self,
            "DockerImageAsset/Nginx",
            directory=str(PROJECT_DIR),
            file="docker/nginx/Dockerfile",
            network_mode=aws_ecr_assets.NetworkMode.HOST,
        )

        vpc = aws_ec2.Vpc.from_lookup(
            self,
            "VPC",
            is_default=True,
        )

        log_group = aws_logs.LogGroup(
            self,
            id="LogGroup",
            log_group_name="/kaatio_plan_validator",
            removal_policy=RemovalPolicy.DESTROY,
            retention=aws_logs.RetentionDays.ONE_MONTH,
        )
        log_group_driver = aws_ecs.AwsLogDriver(
            log_group=log_group,
            stream_prefix="service",
        )
        task_definition = aws_ecs.FargateTaskDefinition(
            self,
            "FargateTaskDefinition",
            cpu=512,
            memory_limit_mib=1024,
        )

        container_gunicorn_port = 8000
        container_gunicorn = task_definition.add_container(
            "FargateTaskDefinition/Container/Gunicorn",
            container_name="gunicorn",
            essential=True,
            image=aws_ecs.EcrImage.from_docker_image_asset(
                asset=docker_image_asset_gunicorn,
            ),
            logging=log_group_driver,
            port_mappings=[
                aws_ecs.PortMapping(
                    container_port=container_gunicorn_port,
                )
            ],
        )
        container_nginx_port = 80
        container_nginx = task_definition.add_container(
            "FargateTaskDefinition/Container/Nginx",
            container_name="nginx",
            environment={
                "GUNICORN_HOST": "localhost",
            },
            essential=True,
            image=aws_ecs.EcrImage.from_docker_image_asset(
                asset=docker_image_asset_nginx,
            ),
            logging=log_group_driver,
            port_mappings=[
                aws_ecs.PortMapping(
                    container_port=container_nginx_port,
                    host_port=container_nginx_port,
                )
            ],
        )

        container_nginx.add_container_dependencies(
            aws_ecs.ContainerDependency(
                condition=aws_ecs.ContainerDependencyCondition.START,
                container=container_gunicorn,
            )
        )

        task_definition.default_container = container_nginx

        fargate = aws_ecs_patterns.ApplicationLoadBalancedFargateService(
            self,
            "ApplicationLoadBalancedFargateService",
            assign_public_ip=True,
            capacity_provider_strategies=[
                aws_ecs.CapacityProviderStrategy(
                    base=1,
                    capacity_provider="FARGATE_SPOT",
                    weight=1,
                )
            ],
            # protocol=aws_elasticloadbalancingv2.ApplicationProtocol.HTTPS,
            public_load_balancer=True,
            # redirect_http=True,
            security_groups=[
                aws_ec2.SecurityGroup(
                    self,
                    "SecurityGroup",
                    vpc=vpc,
                    allow_all_outbound=True,
                )
            ],
            task_definition=task_definition,
            task_subnets=aws_ec2.SubnetSelection(
                subnet_type=aws_ec2.SubnetType.PUBLIC,
            ),
            vpc=vpc,
        )
        scalable_target = fargate.service.auto_scale_task_count(
            max_capacity=2,
            min_capacity=1,
        )
        scalable_target.scale_on_cpu_utilization(
            "CpuScaling",
            target_utilization_percent=50,
        )
        scalable_target.scale_on_memory_utilization(
            "MemoryScaling",
            target_utilization_percent=50,
        )
