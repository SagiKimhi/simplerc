__version__ = "0.0.dev1"

__all__ = [
    # Resource Manager, may be used as a dictionary
    # main difference from dict is that it enforces mutability
    # when updating, deleting values
    "manager",

    # dict and dict-views on current resources
    "keys",
    "values",
    "items",
    "rcdict",

    # Common get/set resource methods
    "get",
    "getrc",
    "getmut",
    "set_",
    "setrc",
    "pop",
    "poprc",
    "delrc",
    "delrc_f",

    # Exception raised when trying to modify/delete an immutable resource
    "ImmutableResourceError",

    # Resource object constructed when calling set_ / setrc
    "Resource",

    # You may use additional managers to add lower hierarchy scopes
    "ResourceManager",
]


from weakref import proxy
from typing import Any, AnyStr, Iterator, ItemsView, KeysView, ValuesView

from .manager import _ResourceManager
from .manager import _Resource as Resource
from .manager import _ImmutableResourceError as ImmutableResourceError


class ResourceManager(_ResourceManager):
    def __len__(self) -> int:
        return self._len()

    def __getitem__(self, key) -> Any:
        """ same as get but Raises ImmutableResourceError for missing key """
        return self._getitem(key)

    def __setitem__(self, key, value) -> None:
        self.set_(key, value)

    def __delitem__(self, key) -> None:
        self.delrc(key)

    def __iter__(self) -> Iterator:
        return iter(self._keys())

    def __contains__(self, item) -> bool:
        return item in self._keys()

    def asdict(self) -> dict:
        return self._asdict()

    def items(self) -> ItemsView:
        return self._items()

    def keys(self) -> KeysView:
        return self._keys()

    def values(self) -> ValuesView:
        return self._values()

    def get(self, name: AnyStr, default=None) -> Any:
        return self._get(name, default).value

    def getmut(self, name, default=None) -> Any:
        try:
            rc = self._getmutable(name, default)
        except ImmutableResourceError:
            raise
        else:
            return rc.value

    def getrc(self, name: AnyStr, default=None) -> Resource:
        return self._get(name, default)

    def set_(self, name: AnyStr, value: Any, mutable: bool = False) -> None:
        try:
            rc = self._getmutable(name, None)
        except ImmutableResourceError:
            raise
        else:
            rc.value, rc.mutable = value, mutable
            self._set(name, rc)

    def setrc(self, name: AnyStr, rc: Resource) -> None:
        try:
            _ = self._getmutable(name, None)
        except ImmutableResourceError:
            raise
        else:
            self._set(name, rc)

    def pop(self, name: AnyStr, default=None) -> Any:
        try:
            return self.poprc(name, default).value
        except ImmutableResourceError:
            raise

    def poprc(self, name: AnyStr, default=None) -> Resource:
        """pop a resource, removing it from this manager instance.

        If a resource was set as immutable, ImmutableResourceError is raised.
        """
        try:
            rc = self._getmutable(name, default)
        except ImmutableResourceError:
            raise
        else:
            self.delrc(name)
            return rc

    def delrc(self, name: AnyStr) -> None:
        try:
            self._getmutable(name, None)
        except ImmutableResourceError:
            raise
        else:
            self._del(name)

    def delrc_f(self, name: AnyStr) -> None:
        """the rm -f version of simplerc

        Forces a deletion of a resource that was set as immutable.
        As a general note, I recommend AGAINST using this method,
        unless you are sure it is required, think twice if and why
        you've set the value as immutable in the firstplace.
        """
        self._del(name)


_manager = ResourceManager()
keys = _manager.keys
values = _manager.values
items = _manager.items
rcdict = _manager.asdict
iterate = _manager.__iter__
get = _manager.get
getmut = _manager.getmut
getrc = _manager.getrc
set_ = _manager.set_
setrc = _manager.setrc
pop = _manager.pop
poprc = _manager.poprc
delrc = _manager.delrc
delrc_f = _manager.delrc_f
manager = proxy(_manager)
