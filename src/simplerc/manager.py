from copy import deepcopy
from threading import RLock
from typing import Any, AnyStr, ItemsView, KeysView, ValuesView
from dataclasses import dataclass, field


class _ImmutableResourceError(KeyError):
    pass


@dataclass(
    init=True, repr=True, eq=True, order=True, slots=True, weakref_slot=True
)
class _Resource:
    value: Any
    mutable: bool

    def copy(self) -> "_Resource":
        return self.__class__(self.value, self.mutable)


@dataclass
class _ResourceManager:
    _lock: RLock = field(default_factory=RLock, init=False)
    _resources: dict = field(default_factory=dict, init=False)

    def _asdict(self) -> dict:
        with self._lock:
            return deepcopy(self._resources)

    def _items(self) -> ItemsView:
        with self._lock:
            return self._resources.items()

    def _keys(self) -> KeysView:
        with self._lock:
            return self._resources.keys()

    def _values(self) -> ValuesView:
        return self._resources.values()

    def _len(self) -> int:
        with self._lock:
            return len(self._resources)

    def _get(self, name: AnyStr, default=None) -> _Resource:
        with self._lock:
            rc = self._resources.get(name, default)
            if rc == default:
                return _Resource(value=default, mutable=True)
            else:
                return rc if rc.mutable else rc.copy()

    def _set(self, name: AnyStr, rc: _Resource) -> None:
        with self._lock:
            self._resources[name] = rc

    def _del(self, name: AnyStr) -> None:
        with self._lock:
            del self._resources[name]

    def _getmutable(self, name: AnyStr, default=None) -> _Resource:
        rc = self._get(name, default)
        if not rc.mutable:
            self._immutable_rc_error()
        return rc

    def _getitem(self, key: AnyStr) -> _Resource:
        with self._lock:
            try:
                rc = self._resources[key]
            except KeyError:
                raise
            else:
                return rc if rc.mutable else rc.copy()

    @classmethod
    def _immutable_rc_error(cls) -> None:
        raise _ImmutableResourceError(
            "Cannot complete operation - _Resource was set as immutable"
        )
