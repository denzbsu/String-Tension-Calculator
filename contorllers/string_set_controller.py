from models.string_set import StringSet
from views.tk_view import TkView
from utilities.observable import Observer
from utilities.notes import transpose
from utilities.gauges import get_gauge_shift

class StringSetController(Observer):

    def __init__(self, model: StringSet, view: TkView):
        self._model = model
        self._view = view

        self._model.attach(view)
        self._view.attach(self)

    def update(self, event_type: str, data: dict):
        if event_type == "action_requested":
            action = data.get("action")
            index = data.get("index")

            if action == "remove_string":
                if len(self._model) > 1:
                    self._model.remove_string()
            elif action == "add_string":
                prev_string = self._model[len(self._model) - 1]
                self._model.add_string(prev_string.scale, transpose(prev_string.note, -5), get_gauge_shift(prev_string.gauge, 5))
            elif action == "all_notes_up":
                self._model.transpose_all_strings(1)
            elif action == "all_notes_down":
                self._model.transpose_all_strings(-1)
            elif action == "all_gauges_up":
                self._model.shift_all_gauges(1)
            elif action == "all_gauges_down":
                self._model.shift_all_gauges(-1)
            elif action == "all_scales_up":
                self._model.shift_all_scales(0.1)
            elif action == "all_scales_down":
                self._model.shift_all_scales(-0.1)
            elif action == "note_up":
                self._model.transpose_string(index, 1)
            elif action == "note_down":
                self._model.transpose_string(index, -1)
            elif action == "gauge_up":
                self._model.shift_gauge(index, 1)
            elif action == "gauge_down":
                self._model.shift_gauge(index, -1)
            elif action == "scale_up":
                self._model.shift_scale(index, 0.1)
            elif action == "scale_down":
                self._model.shift_scale(index, -0.1)
            
    def run(self):
        self._view.run()