import json

with open("data/constants.json", encoding="UTF-8") as file_in:
    constants = json.load(file_in)

with open("data/roots.json", encoding="UTF-8") as file_in:
    roots = json.load(file_in)


def check_note_format(note):
    if len(note) < 2:
        return False
    root = note.rstrip('0123456789')
    octave = int(note[len(root):])
    return (root in roots) and (constants["MIN_OCTAVE"] <= octave <= constants["MAX_OCTAVE"])

"""Input format: <note><octave>. Examples: A3, E2, C4"""
def note_to_code(note: str):
    root = note.rstrip('0123456789')
    octave = int(note[len(root):])
    return roots.index(root) + 12 * octave

def code_to_note(code: int):
    index = code % 12
    octave = code // 12
    return roots[index] + str(octave)

def note_to_frequency(note: str):
    freq = 2 ** ((note_to_code(note) - note_to_code("A4")) / 12) * 440
    return round(freq, 1)