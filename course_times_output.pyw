import json
import PySimpleGUI as sg

def export_window(file_path):
    """Creates a new window for showing current times for each course"""

    with open("json_data/" + file_path) as json_file:
        current_times = json.load(json_file)

    layout = []

    for course_name in current_times.keys():
        layout.append([sg.Text(course_name), sg.Text(str(current_times[course_name]))])

    layout.append([sg.Button("Close", key="close")])

    window = sg.Window("Your Times", layout, size=(200, 200), element_justification="c")

    while True:
        event = window.read()[0]
        if event == None or event == "close":
            break

    window.close()

if __name__ == "__main__":
    pass
