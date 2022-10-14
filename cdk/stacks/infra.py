from pathlib import Path

from aws_cdk import (
    Duration,
    RemovalPolicy,
    Stack,
    aws_certificatemanager,
    aws_ec2,
    aws_ecr_assets,
    aws_ecs,
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
            platform=aws_ecr_assets.Platform.LINUX_AMD64,
        )

        docker_image_asset_nginx = aws_ecr_assets.DockerImageAsset(
            self,
            "DockerImageAsset/Nginx",
            directory=str(PROJECT_DIR),
            file="docker/nginx/Dockerfile",
            network_mode=aws_ecr_assets.NetworkMode.HOST,
            platform=aws_ecr_assets.Platform.LINUX_AMD64,
        )

        vpc = aws_ec2.Vpc.from_lookup(
            self,
            "VPC",
            is_default=True,
        )

        domain = "kaatio.spatineo-devops.com"
        certificate = aws_certificatemanager.Certificate(
            self,
            "Certificate",
            domain_name=domain,
            validation=aws_certificatemanager.CertificateValidation.from_email(),
        )

        cluster = aws_ecs.Cluster(
            self,
            "Cluster",
            vpc=vpc,
        )

        log_group = aws_logs.LogGroup(
            self,
            "LogGroup",
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

        load_balancer = aws_elasticloadbalancingv2.ApplicationLoadBalancer(
            self,
            "ApplicationLoadBalancer",
            internet_facing=True,
            vpc=vpc,
        )

        fargate = aws_ecs.FargateService(
            self,
            "FargateService",
            assign_public_ip=True,
            capacity_provider_strategies=[
                aws_ecs.CapacityProviderStrategy(
                    base=1,
                    capacity_provider="FARGATE_SPOT",
                    weight=1,
                )
            ],
            cluster=cluster,
            desired_count=1,
            security_groups=[
                aws_ec2.SecurityGroup(
                    self,
                    "SecurityGroup/FargateService",
                    vpc=vpc,
                )
            ],
            task_definition=task_definition,
            vpc_subnets=aws_ec2.SubnetSelection(
                subnet_type=aws_ec2.SubnetType.PUBLIC,
            ),
        )

        load_balancer.add_listener(
            "HTTP",
            port=80,
            default_action=aws_elasticloadbalancingv2.ListenerAction.redirect(
                permanent=True,
                port="443",
                protocol="HTTPS",
            ),
        )
        listener = load_balancer.add_listener(
            "HTTPS",
            certificates=[certificate],
            default_action=aws_elasticloadbalancingv2.ListenerAction.fixed_response(404),
            port=443,
            protocol=aws_elasticloadbalancingv2.ApplicationProtocol.HTTPS,
            ssl_policy=aws_elasticloadbalancingv2.SslPolicy.TLS12,
        )
        listener.add_targets(
            "TargetGroup/Application",
            conditions=[
                aws_elasticloadbalancingv2.ListenerCondition.path_patterns(
                    values=["/", "/*"],
                )
            ],
            deregistration_delay=Duration.seconds(30),
            health_check=aws_elasticloadbalancingv2.HealthCheck(
                enabled=True,
                healthy_http_codes="200",
                path="/docs",
                port="80",
                protocol=aws_elasticloadbalancingv2.Protocol.HTTP,
            ),
            load_balancing_algorithm_type=aws_elasticloadbalancingv2.TargetGroupLoadBalancingAlgorithmType.LEAST_OUTSTANDING_REQUESTS,
            port=80,
            priority=1,
            protocol=aws_elasticloadbalancingv2.ApplicationProtocol.HTTP,
            targets=[fargate],
        )

        scalable_target = fargate.auto_scale_task_count(
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
