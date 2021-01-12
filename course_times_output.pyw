import json
import PySimpleGUI as sg

def export_window(file_path):
    """Creates a new window for showing current times for each course"""

    with open("json_data/" + file_path) as json_file:
        current_times = json.load(json_file)

    with open("json_data/daily_times.json") as json_file:
        daily_times = json.load(json_file)

    weekly_times_column = []
    daily_times_column = []
    layout = []

    for course_name in current_times.keys():
        weekly_times_column.append([sg.Text(course_name), sg.Text(str(current_times[course_name]))])

    # First item is the date, so only show the daily times start at item 2
    for course_name in list(daily_times.keys())[1:]:
        daily_times_column.append([sg.Text(daily_times[course_name])])

    layout = [
        [sg.Column(weekly_times_column), sg.Column(daily_times_column)],
        [sg.Button("Close", key="close")]
    ]

    window = sg.Window("Your Times", layout, size=(200, 200), element_justification="c")

    while True:
        event = window.read()[0]
        if event == None or event == "close":
            break

    window.close()

if __name__ == "__main__":
    pass
