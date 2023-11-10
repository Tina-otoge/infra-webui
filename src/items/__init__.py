from pathlib import Path

import yaml

INVENTORY_PATH = Path("inventory.yml")


def get_inventory():
    with INVENTORY_PATH.open("r") as f:
        inventory = yaml.safe_load(f)
    for module in Path(__file__).parent.glob("*.py"):
        if module.stem == "__init__":
            continue
        __import__(f"src.items.{module.stem}")
    return {
        k: Item.init(v.get("type"), v.get("params", {})) for k, v in inventory.items()
    }


class Item:
    PARAMS = {}
    ITEMS = {}

    def __init_subclass__(cls):
        cls.ITEMS[cls.__name__.lower()] = cls

    @classmethod
    def init(cls, type, params: dict):
        cls = cls.ITEMS[type]
        for param in cls.PARAMS:
            if param not in params:
                raise ValueError(f"Missing required param {param}")
            if not isinstance(params[param], cls.PARAMS[param]):
                raise ValueError(f"Param {param} must be of type {cls.PARAMS[param]}")
        return cls({param: params[param] for param in cls.PARAMS})

    def get_status(self) -> bool:
        if not hasattr(self, "object"):
            raise NotImplementedError
        return self.object.get_status()

    def start(self):
        if not hasattr(self, "object"):
            raise NotImplementedError
        return self.object.start()

    def stop(self):
        if not hasattr(self, "object"):
            raise NotImplementedError
        return self.object.stop()
