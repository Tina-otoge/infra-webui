import datetime
import typing as t
from dataclasses import dataclass

import boto3

from .config import secrets

creds = {
    "aws_access_key_id": secrets["aws"]["access_key"],
    "aws_secret_access_key": secrets["aws"]["secret_key"],
}


class AWSService:
    SERVICE_NAME = None

    clients = {}
    session = None

    @classmethod
    def get_client(cls, region="us-east-1"):
        if not cls.session:
            cls.session = boto3.Session(**creds)
        if region not in cls.clients:
            client = cls.session.client(cls.SERVICE_NAME, region_name=region)
            cls.clients[region] = client
        return cls.clients[region]


@dataclass
class Instance(AWSService):
    SERVICE_NAME = "ec2"

    image_id: str
    type: t.Literal["t3.small"]
    id: str
    launch_time: datetime.datetime
    state: t.Literal["running", "stopped", "stopping", "pending"]
    region: str

    @classmethod
    def get(cls, id: str, region="us-east-1") -> "Instance":
        client = cls.get_client(region)
        instance = client.describe_instances(InstanceIds=[id])
        instance = instance["Reservations"][0]["Instances"][0]
        return cls(
            image_id=instance["ImageId"],
            type=instance["InstanceType"],
            id=instance["InstanceId"],
            launch_time=instance["LaunchTime"],
            state=instance["State"]["Name"],
            region=region,
        )

    @property
    def client(self):
        return self.get_client(self.region)

    @classmethod
    def describe_instance(cls, id: str, region="us-east-1"):
        client = cls.get_client(region)
        instance = client.describe_instances(InstanceIds=[id])
        instance = instance["Reservations"][0]["Instances"][0]
        return instance

    def get_instance(self):
        return self.describe_instance(self.id, self.region)

    def get_status(self):
        return self.get_instance()["State"]["Name"] == "running"

    def stop(self):
        self.client.stop_instances(InstanceIds=[self.id])

    def start(self):
        self.client.start_instances(InstanceIds=[self.id])
