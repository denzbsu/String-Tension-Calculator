# just for studying

import tkinter as tk
from tkinter import ttk, messagebox

from models.string_set import StringSet
from models.observable import Observer


# ----------------------------------------------------------------------
# VIEW: builds the UI, observes the model, and refreshes on changes
# ----------------------------------------------------------------------
class StringSetView(Observer):
    def __init__(self, master: tk.Tk, string_set: StringSet):
        self.master = master
        self.string_set = string_set
        self.string_set.attach(self)          # start observing

        self._build_ui()
        self.refresh()

    # ---------- UI construction ----------
    def _build_ui(self):
        self.master.title("String Set Manager (MVC)")
        self.master.geometry("750x500")

        # Main container
        main = ttk.Frame(self.master, padding="10")
        main.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)

        # ----- Treeview (table) -----
        columns = ("Index", "Scale", "Note", "Gauge", "Tension", "Frequency")
        self.tree = ttk.Treeview(main, columns=columns, show="headings", height=12)
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=90, anchor="center")
        self.tree.grid(row=0, column=0, columnspan=4, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))

        scroll = ttk.Scrollbar(main, orient=tk.VERTICAL, command=self.tree.yview)
        scroll.grid(row=0, column=4, sticky=(tk.N, tk.S))
        self.tree.configure(yscrollcommand=scroll.set)

        # ----- Add String -----
        add_frame = ttk.LabelFrame(main, text="Add String", padding="5")
        add_frame.grid(row=1, column=0, columnspan=5, sticky=(tk.W, tk.E), pady=5)

        ttk.Label(add_frame, text="Scale:").grid(row=0, column=0, padx=5, sticky=tk.W)
        self.scale_entry = ttk.Entry(add_frame, width=10)
        self.scale_entry.grid(row=0, column=1, padx=5)

        ttk.Label(add_frame, text="Note:").grid(row=0, column=2, padx=5, sticky=tk.W)
        self.note_entry = ttk.Entry(add_frame, width=10)
        self.note_entry.grid(row=0, column=3, padx=5)

        ttk.Label(add_frame, text="Gauge:").grid(row=0, column=4, padx=5, sticky=tk.W)
        self.gauge_entry = ttk.Entry(add_frame, width=10)
        self.gauge_entry.grid(row=0, column=5, padx=5)

        self.add_btn = ttk.Button(add_frame, text="Add")
        self.add_btn.grid(row=0, column=6, padx=10)

        # ----- Single-string operations -----
        single_frame = ttk.LabelFrame(main, text="Single String Operations", padding="5")
        single_frame.grid(row=2, column=0, columnspan=5, sticky=(tk.W, tk.E), pady=5)

        ttk.Label(single_frame, text="Index:").grid(row=0, column=0, padx=5, sticky=tk.W)
        self.idx_entry = ttk.Entry(single_frame, width=5)
        self.idx_entry.grid(row=0, column=1, padx=5)

        ttk.Label(single_frame, text="Step:").grid(row=0, column=2, padx=5, sticky=tk.W)
        self.step_entry = ttk.Entry(single_frame, width=5)
        self.step_entry.grid(row=0, column=3, padx=5)

        self.transpose_btn = ttk.Button(single_frame, text="Transpose")
        self.transpose_btn.grid(row=0, column=4, padx=5)

        self.shift_gauge_btn = ttk.Button(single_frame, text="Shift Gauge")
        self.shift_gauge_btn.grid(row=0, column=5, padx=5)

        self.shift_scale_btn = ttk.Button(single_frame, text="Shift Scale")
        self.shift_scale_btn.grid(row=0, column=6, padx=5)

        # ----- All-strings operations -----
        all_frame = ttk.LabelFrame(main, text="All Strings Operations", padding="5")
        all_frame.grid(row=3, column=0, columnspan=5, sticky=(tk.W, tk.E), pady=5)

        ttk.Label(all_frame, text="Step:").grid(row=0, column=0, padx=5, sticky=tk.W)
        self.all_step_entry = ttk.Entry(all_frame, width=5)
        self.all_step_entry.grid(row=0, column=1, padx=5)

        self.transpose_all_btn = ttk.Button(all_frame, text="Transpose All")
        self.transpose_all_btn.grid(row=0, column=2, padx=5)

        self.shift_gauge_all_btn = ttk.Button(all_frame, text="Shift Gauges All")
        self.shift_gauge_all_btn.grid(row=0, column=3, padx=5)

        self.shift_scale_all_btn = ttk.Button(all_frame, text="Shift Scales All")
        self.shift_scale_all_btn.grid(row=0, column=4, padx=5)

        # ----- Remove & Quit -----
        action_frame = ttk.Frame(main)
        action_frame.grid(row=4, column=0, columnspan=5, sticky=(tk.W, tk.E), pady=10)

        self.remove_btn = ttk.Button(action_frame, text="Remove Last")
        self.remove_btn.pack(side=tk.LEFT, padx=5)

        self.quit_btn = ttk.Button(action_frame, text="Quit", command=self.master.quit)
        self.quit_btn.pack(side=tk.RIGHT, padx=5)

        # Make the treeview expandable
        main.columnconfigure(0, weight=1)
        main.rowconfigure(0, weight=1)

    # ---------- Callback binding for the controller ----------
    def bind_add(self, callback):
        self.add_btn.config(command=callback)

    def bind_remove(self, callback):
        self.remove_btn.config(command=callback)

    def bind_transpose(self, callback):
        self.transpose_btn.config(command=callback)

    def bind_shift_gauge(self, callback):
        self.shift_gauge_btn.config(command=callback)

    def bind_shift_scale(self, callback):
        self.shift_scale_btn.config(command=callback)

    def bind_transpose_all(self, callback):
        self.transpose_all_btn.config(command=callback)

    def bind_shift_gauge_all(self, callback):
        self.shift_gauge_all_btn.config(command=callback)

    def bind_shift_scale_all(self, callback):
        self.shift_scale_all_btn.config(command=callback)

    # ---------- Input getters (for controller) ----------
    def get_add_values(self):
        """Return (scale, note, gauge) from entry fields."""
        scale = float(self.scale_entry.get())
        note = self.note_entry.get().strip()
        gauge = self.gauge_entry.get().strip()
        if not note or not gauge:
            raise ValueError("Note and Gauge cannot be empty.")
        return scale, note, gauge

    def get_single_op_values(self):
        """Return (index, step) from entry fields."""
        idx = int(self.idx_entry.get())
        step = int(self.step_entry.get())
        return idx, step

    def get_all_step(self):
        """Return the step for 'all' operations."""
        return int(self.all_step_entry.get())

    # ---------- Display / refresh ----------
    def refresh(self):
        """Clear and repopulate the treeview."""
        for row in self.tree.get_children():
            self.tree.delete(row)

        data = self.string_set.get_all_strings_data()
        for i, d in enumerate(data):
            self.tree.insert(
                "",
                "end",
                values=(i, d["scale"], d["note"], d["gauge"], d["tension"], d["frequency"])
            )

    def update(self, event_type: str, data: dict):
        """Called by the model when something changes."""
        if event_type in ("string_added", "string_removed", "string_changed"):
            self.refresh()

    def show_error(self, message: str):
        """Show an error dialog."""
        messagebox.showerror("Error", message)


# ----------------------------------------------------------------------
# CONTROLLER: connects view callbacks to model actions
# ----------------------------------------------------------------------
class StringSetController:
    def __init__(self, master: tk.Tk):
        # 1. Create model
        self.model = StringSet()

        # 2. Create view (it attaches itself to the model)
        self.view = StringSetView(master, self.model)

        # 3. Bind all UI callbacks to controller methods
        self.view.bind_add(self._add_string)
        self.view.bind_remove(self._remove_string)
        self.view.bind_transpose(self._transpose)
        self.view.bind_shift_gauge(self._shift_gauge)
        self.view.bind_shift_scale(self._shift_scale)
        self.view.bind_transpose_all(self._transpose_all)
        self.view.bind_shift_gauge_all(self._shift_gauge_all)
        self.view.bind_shift_scale_all(self._shift_scale_all)

    # ---------- Action methods ----------
    def _add_string(self):
        try:
            scale, note, gauge = self.view.get_add_values()
            self.model.add_string(scale, note, gauge)
        except Exception as e:
            self.view.show_error(str(e))

    def _remove_string(self):
        try:
            self.model.remove_string()
        except Exception as e:
            self.view.show_error(str(e))

    def _transpose(self):
        try:
            idx, step = self.view.get_single_op_values()
            self.model.transpose_string(idx, step)
        except Exception as e:
            self.view.show_error(str(e))

    def _shift_gauge(self):
        try:
            idx, step = self.view.get_single_op_values()
            self.model.shift_gauge(idx, step)
        except Exception as e:
            self.view.show_error(str(e))

    def _shift_scale(self):
        try:
            idx, step = self.view.get_single_op_values()
            self.model.shift_scale(idx, step)
        except Exception as e:
            self.view.show_error(str(e))

    def _transpose_all(self):
        try:
            step = self.view.get_all_step()
            self.model.transpose_all_strings(step)
        except Exception as e:
            self.view.show_error(str(e))

    def _shift_gauge_all(self):
        try:
            step = self.view.get_all_step()
            self.model.shift_all_gauges(step)
        except Exception as e:
            self.view.show_error(str(e))

    def _shift_scale_all(self):
        try:
            step = self.view.get_all_step()
            self.model.shift_all_scales(step)
        except Exception as e:
            self.view.show_error(str(e))


# ----------------------------------------------------------------------
# ENTRY POINT
# ----------------------------------------------------------------------
def main():
    root = tk.Tk()
    app = StringSetController(root)
    root.mainloop()


if __name__ == "__main__":
    main()