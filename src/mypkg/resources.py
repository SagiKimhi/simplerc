__version__ = '1.0.0'

__all__ = [
    # Use these for managing global resources
    'setrc', 
    'getrc', 
    'delrc',
    'clearrc',

    # Use these if local resource management is needed
    'Resource',
    'ResourceManager',
    'ImmutableResourceError',
]

from threading import RLock
from typing import Any, AnyStr
from dataclasses import dataclass, field

class ImmutableResourceError(RuntimeError):
    pass


@dataclass
class Resource:
    value: Any
    mutable: bool


@dataclass
class ResourceManager:
    _lock: RLock = field(default_factory=RLock, init=False)
    _resources: dict = field(default_factory=dict, init=False)

    def getrc(self, name: AnyStr) -> Any:
        with self._lock:
            return self._resources[name].value

    def setrc(self, name: AnyStr, value: Any, mutable: bool = False) -> None:
        with self._lock:
            rc = self._resources.get(name, None)
            if rc is None:
                self._resources[name] = Resource(value, mutable)
            elif not rc.mutable:
                self._immutable_rc_error()
            else:
                self._resources[name].value = value
                self._resources[name].mutable = mutable

    def delrc(self, name: AnyStr) -> None:
        with self._lock:
            del self._resources[name]

    def clearrc(self):
        with self._lock:
            self._resources.clear()

    @classmethod
    def _immutable_rc_error(cls) -> None:
        raise ImmutableResourceError(
            "Cannot set resource - resource was set as immutable"
        )


_manager = ResourceManager()
getrc = _manager.getrc
setrc = _manager.setrc
delrc = _manager.delrc
clearrc = _manager.clearrc

