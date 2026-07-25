from utilities.observable import Observer, Observable
from models.string_set import StringSet
import tkinter as tk


class TkView(Observer, Observable):
    
    def __init__(self):
        super().__init__()
        self._root = tk.Tk()

        self._startup()

        self._string_set_frame = tk.Frame(self._root)
        self._string_set_frame.grid(row=1, column=0)

        self._rows = {} # id -> labels scale, note, gauge, tension, frequency

    def run(self):
        self._root.mainloop()

    def _startup(self):
        header_frame = tk.Frame(self._root)

        # Labels
        index_label = tk.Label(header_frame, text="ID")
        index_label.grid(row=1, column=0)

        scale_label = tk.Label(header_frame, text="Scale")
        scale_label.grid(row=1, column=1)

        note_label = tk.Label(header_frame, text="Note")
        note_label.grid(row=1, column=2)

        gauge_label = tk.Label(header_frame, text="Gauge")
        gauge_label.grid(row=1, column=3)

        tension_label = tk.Label(header_frame, text="Tension")
        tension_label.grid(row=1, column=4)

        frequency_label = tk.Label(header_frame, text="Frequency")
        frequency_label.grid(row=1, column=5)


        # Buttons
        scale_up = tk.Button(header_frame, text="!", command=lambda: self._action_request("all_scales_up"))
        scale_up.grid(row=0, column=1)

        scale_down = tk.Button(header_frame, text="!", command=lambda: self._action_request("all_scales_down"))
        scale_down.grid(row=2, column=1)

        note_up = tk.Button(header_frame, text="!", command=lambda: self._action_request("all_notes_up"))
        note_up.grid(row=0, column=2)

        note_down = tk.Button(header_frame, text="!", command=lambda: self._action_request("all_notes_down"))
        note_down.grid(row=2, column=2)

        gauge_up = tk.Button(header_frame, text="!", command=lambda: self._action_request("all_gauges_up"))
        gauge_up.grid(row=0, column=3)

        gauge_down = tk.Button(header_frame, text="!", command=lambda: self._action_request("all_gauges_down"))
        gauge_down.grid(row=2, column=3)

        header_frame.grid(row=0, column=0)


        btn_add = tk.Button(self._root, text="Add", command=lambda: self._action_request("add_string"))
        btn_add.grid(row=2, column=0)

        btn_remove = tk.Button(self._root, text="Remove", command=lambda: self._action_request("remove_string"))
        btn_remove.grid(row=3, column=0)

    def update(self, event_type, data):
        if event_type == "string_changed":
            self._rows[data["index"]][data["property"] + "_label"]["text"] = data["value"]
        elif event_type == "string_added":
            string_data = data["string"].get_data()
            
            scale = string_data["scale"]
            note = string_data["note"]
            gauge = string_data["gauge"]
            tension = string_data["tension"]
            frequency = string_data["frequency"]
            
            self._add_row(data["index"], scale, note, gauge, tension, frequency)
        elif event_type == "string_removed":
            self._delete_row(data["index"])

    
    def _add_row(self, index, scale, note, gauge, tension, frequency):
        string_frame = tk.Frame(self._string_set_frame)

        # Labels
        index_label = tk.Label(string_frame, text=f"{index + 1}")
        index_label.grid(row=1, column=0)

        scale_label = tk.Label(string_frame, text=f"{scale}")
        scale_label.grid(row=1, column=1)

        note_label = tk.Label(string_frame, text=f"{note}")
        note_label.grid(row=1, column=2)

        gauge_label = tk.Label(string_frame, text=f"{gauge}")
        gauge_label.grid(row=1, column=3)

        tension_label = tk.Label(string_frame, text=f"{tension}")
        tension_label.grid(row=1, column=4)

        frequency_label = tk.Label(string_frame, text=f"{frequency}")
        frequency_label.grid(row=1, column=5)


        # Buttons
        scale_up = tk.Button(string_frame, text="!", command=lambda: self._action_request("scale_up", {"index": index}))
        scale_up.grid(row=0, column=1)

        scale_down = tk.Button(string_frame, text="!", command=lambda: self._action_request("scale_down", {"index": index}))
        scale_down.grid(row=2, column=1)

        note_up = tk.Button(string_frame, text="!", command=lambda: self._action_request("note_up", {"index": index}))
        note_up.grid(row=0, column=2)

        note_down = tk.Button(string_frame, text="!", command=lambda: self._action_request("note_down", {"index": index}))
        note_down.grid(row=2, column=2)

        gauge_up = tk.Button(string_frame, text="!", command=lambda: self._action_request("gauge_up", {"index": index}))
        gauge_up.grid(row=0, column=3)

        gauge_down = tk.Button(string_frame, text="!", command=lambda: self._action_request("gauge_down", {"index": index}))
        gauge_down.grid(row=2, column=3)

        string_frame.pack()

        self._rows[index] = {
            "frame": string_frame,
            "scale_label": scale_label,
            "note_label": note_label,
            "gauge_label": gauge_label,
            "tension_label": tension_label,
            "frequency_label": frequency_label
        }

    def _delete_row(self, index):
        frame = self._rows[index]["frame"]
        for widget in frame.winfo_children():
            widget.destroy()
        frame.destroy()
        del self._rows[index]
