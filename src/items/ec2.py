from src.aws import Instance

from . import Item


class EC2(Item):
    PARAMS = {
        "id": str,
        "region": str,
    }

    def __init__(self, params):
        self.object = Instance.get(params["id"], params["region"])
