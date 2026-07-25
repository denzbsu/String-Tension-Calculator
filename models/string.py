import json
from utilities.observable import Observable
from utilities.notes import transpose, note_to_frequency, check_note_format
from utilities.gauges import gauge_to_unit_weight, check_gauge, get_gauge_shift

with open("data/constants.json", encoding="UTF-8") as file_in:
    constants = json.load(file_in)


class String(Observable):

    def __init__(self, scale: float, note: str, gauge: str):
        super().__init__()
        self._set_scale(scale)
        self._set_note(note)
        self._set_gauge(gauge)


    # ------ Raw setters ------ 
    def _set_scale(self, value: float) -> None:
        if (value > constants["MAX_SCALE"]):
            value = constants["MAX_SCALE"]
        elif (value < constants["MIN_SCALE"]):
            value = constants["MIN_SCALE"]
        else:
            self._scale = value

    # Fix needed: if note is out of bounds, it should be set with boundary value
    def _set_note(self, value: str) -> None:
        if not check_note_format(value):
            raise ValueError("Invalid note format")
        self._note = value

    def _set_gauge(self, value: str) -> None:
        if not check_gauge(value):
            raise ValueError("Missing gauge")
        self._gauge = value


    # ------ Notificators for dependent properties ------ 
    def _update_tension(self) -> None:
        self._notify_property_changed("tension", self.tension)

    def _update_frequency(self) -> None:
        self._notify_property_changed("frequency", self.frequency)


    # ------ Methods for special changing of properties ------ 
    def transpose(self, step: int) -> bool:
        new_note = transpose(self.note, step)
        self.note = new_note

    def shift_gauge(self, step: int) -> None:
        new_gauge = get_gauge_shift(self.gauge, step)
        self.gauge = new_gauge

    def shift_scale(self, step: float) -> bool:
        new_scale = self.scale + step
        self.scale = round(new_scale, 3)

    def get_data(self):
        return {
            "scale": self.scale,
            "note": self.note,
            "gauge": self.gauge,
            "tension": self.tension,
            "frequency": self.frequency
        }


    # ------ Properties -------
    @property
    def scale(self) -> float:
        return self._scale

    @scale.setter
    def scale(self, value: float) -> None:
        if value == self._scale:
            return
        self._set_scale(value)
        self._notify_property_changed("scale", value)
        self._update_tension()

    @property
    def gauge(self) -> str:
        return self._gauge
    
    @gauge.setter
    def gauge(self, value: str) -> None:
        if value == self._gauge:
            return
        self._set_gauge(value)
        self._notify_property_changed("gauge", value)
        self._update_tension()

    @property
    def note(self) -> str:
        return self._note

    @note.setter
    def note(self, value: str) -> None:
        if value == self._note:
            return
        self._set_note(value)
        self._notify_property_changed("note", value)
        self._update_frequency() # Update frequency firstly, tension - secondly!
        self._update_tension()

    @property
    def frequency(self) -> float:
        return note_to_frequency(self.note)

    @property
    def tension(self) -> float:
        unit_weight = gauge_to_unit_weight(self.gauge)
        tension = (2 * self.scale * self.frequency) ** 2 * unit_weight / constants["GRAVITATIONAL"]
        return round(tension, 2)