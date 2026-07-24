from models.observable import Observable, Observer
from models.string import String


class StringSet(Observer, Observable):

    def __init__(self):
        super().__init__()
        self._strings = list()

    def update(self, event_type: str, data: dict):
        """
        Receives events from individual String instances and forwards them.
        """
        if event_type == "property_changed":
            obj = data["object"]
            if obj not in self._strings:
                return
            idx = self._strings.index(obj)
            new_data = {
                "index": idx,
                "object": obj,
                "property": data["property"],
                "value": data["value"]
            }
            self._notify("string_changed", new_data)

    @staticmethod
    def _check_index(func):
        def wrapper(self, index, *args, **kwargs):
            if not (0 <= index < len(self._strings)):
                raise IndexError("Index out of bounds")
            return func(self, index, *args, **kwargs)
        return wrapper

    def add_string(self, scale: float, note: str, gauge: str):
        """
        Adds the string to the end of current string set and notifies the observer.
        """
        new_string = String(scale, note, gauge)
        new_string.attach(self)
        self._strings.append(new_string)
        self._notify("string_added", {
            "index": len(self._strings) - 1,
            "string": new_string
        })
        return new_string

    def remove_string(self):
        """
        Removes the string from the end of current string set and notifies the observer.
        """
        index = len(self._strings) - 1
        self._strings[index].detach(self)
        del self._strings[index]
        self._notify("string_removed", {"index": index})

    @_check_index
    def transpose_string(self, index: int, step: int):
        self._strings[index].transpose(step)

    def transpose_all_strings(self, step: int):
        for string in self._strings:
            string.transpose(step)

    @_check_index
    def shift_gauge(self, index: int, step: int):
        self._strings[index].shift_gauge(step)

    def shift_all_gauges(self, step: int):
        for string in self._strings:
            string.shift_gauge(step)

    @_check_index
    def shift_scale(self, index: int, step: int):
        self._strings[index].shift_scale(step)

    def shift_all_scales(self, step: int):
        for string in self._strings:
            string.shift_scale(step)

    @_check_index
    def get_string_data(self, index: int):
        s = self._strings[index]
        return s.get_data()

    def get_all_strings_data(self):
        return [string.get_data() for string in self._strings]

    @_check_index
    def __getitem__(self, index: int) -> String:
        return self._strings[index]

    def __iter__(self):
        return iter(self._strings)

    def __len__(self):
        return len(self._strings)


if __name__ == "__main__":
    ss = StringSet()

    ss.add_string(25.5, "B3", "11")
    ss.add_string(25.75, "F#3", "16p")
    ss.add_string(26, "D3", "24w")
    ss.add_string(26.25, "A2", "34")
    ss.add_string(26.5,  "E2", "46"),
    ss.add_string(26.75, "A1", "64")
    ss.add_string(27, "E1", "80")

    ss.shift_all_scales(1)

    for d in ss.get_all_strings_data():
        print(d)
