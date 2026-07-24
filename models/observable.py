from abc import ABC, abstractmethod
from weakref import WeakSet
from typing import Any

class Observer(ABC):
    
    @abstractmethod
    def update(self, event_type: str, data: dict):
        pass


class Observable(ABC):

    def __init__(self):
        self._observers: WeakSet[Observer] = WeakSet()

    def attach(self, observer: Observer):
        if observer not in self._observers:
            self._observers.add(observer)

    def detach(self, observer: Observer):
        if observer in self._observers:
            self._observers.discard(observer)
    
    def _notify(self, event_type: str, data: dict):
        for obs in self._observers:
            obs.update(event_type, data)

    def _notify_property_changed(self, property_name: str, value: Any):
        data = {
            "property": property_name,
            "value": value,
            "object": self
        }
        self._notify("property_changed", data)
