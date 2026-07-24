from models.string_set import StringSet
from contorllers.string_set_controller import StringSetController
from views.tk_view import TkView

model = StringSet()

view = TkView()

controller = StringSetController(model, view)

model.add_string(25.5, "B3", "11")
model.add_string(25.75, "F#3", "16p")
model.add_string(26, "D3", "24w")
model.add_string(26.25, "A2", "34")
model.add_string(26.5,  "E2", "46"),
model.add_string(26.75, "A1", "64")
model.add_string(27, "E1", "80")

controller.run()