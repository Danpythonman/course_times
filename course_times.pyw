import os
import time
import PySimpleGUI as sg
from datetime import datetime, date


def calculate_elapsed_time(time_1, time_2):
    """Calculates the difference, in minutes, of two times
    Format of times are HH:MM,DD"""

    # Get the day of each time
    day_1 = int(time_1[6:])
    day_2 = int(time_2[6:])

    # Get the hours and minutes from each time
    hours_1 = int(time_1[0:2])
    minutes_1 = int(time_1[3:5])
    hours_2 = int(time_2[0:2])
    minutes_2 = int(time_2[3:5])

    # Calculate the total minutes elapsed
    if day_1 == day_2:
        minutes = (60 - minutes_1) + minutes_2
        hours = hours_2 - hours_1 - 1
        minutes += hours * 60
    else:
        minutes = 60 - minutes_1
        hours = 24 - hours_1 - 1
        minutes += minutes_2
        hours += hours_2
        minutes += hours * 60

    return minutes


def export_window():
    """Creates a new window for showing current times for each course"""

    current_courses = ["EECS 1011", "ENG 1101", "MATH 1013", "MATH 1025",
                        "PHYS1800"]

    current_times = []

    layout = []

    i = 0
    for course in current_courses:
        layout.append([sg.Text(course), sg.Text(str(current_times[i]))])
        i += 1

    layout.append([sg.Button("Close", key="close")])

    window = sg.Window("Window 1", layout, size=(200, 200), element_justification="c")

    while True:
        event, values = window.read()
        if event == None or event == "close":
            break

    window.close()


def main():
    """Main controlling function"""

    os.chdir("C:\\Users\\Daniel\\Documents\\Programming\\time_management")

    # Check if the folder for the JSON files exists already, if not then
    # create it
    if "json_data" in os.listdir():
        # Check if the folder for the JSON files is empty and if it is, add the
        # first JSON file
        if os.listdir("json_data") == []:
            pass
    else:
        os.mkdir("json_data")

    current_day = str(date.today())

    # ----- Reset data for the week

    # 0 means a start time has not been recorded, so clicking the "Time"
    # button will start timing
    # 1 means a start time has been recorded, so clicking the "Time" button
    # will stop timing
    stopwatch_controller = 0

    layout = [[sg.Combo(current_courses, key="course_selected"), sg.Button("Time", key="time"), sg.Button("Entry", key="entry")],
              [sg.Text("Start time: "), sg.Text("00:00", key="start_time")],
              [sg.Text("End time: "), sg.Text("00:00", key="end_time")],
              [sg.Text("Elapsed Minutes: "), sg.Text("000", key="elapsed_time")],
              [sg.Button("Check Times for this Week", key="export")]]

    window = sg.Window("Window 1", layout)

    # --- Main event loop ---
    while True:
        event, values = window.read()

        if event == None or event == "Exit":
            break

        elif event == "time":
            if stopwatch_controller == 0:
                # Record start time
                t = time.localtime()
                start_time = time.strftime("%H:%M,%d", t)
                window["start_time"].update(start_time[0:5])

                # Set end time to 00:00 so user knows that timing has started
                window["end_time"].update("00:00")

                # Timing has started, so update stopwach variable
                stopwatch_controller = 1
            else:
                # Record end time
                t = time.localtime()
                end_time = time.strftime("%H:%M,%d", t)
                window["end_time"].update(end_time[0:5])

                elapsed_time = calculate_elapsed_time(start_time, end_time)

                window["elapsed_time"].update(elapsed_time)

                # ----- Add times to database

                # Reset stopwatch variable so it is ready to start timing again
                stopwatch_controller = 0

        elif event == "entry":
            entered_time = sg.popup_get_text("Enter the time you want to add or subtract")

            # ----- Add this time to the database
            previous_time = values["course_selected"]
            new_time = previous_time + int(entered_time)

        elif event == "export":
            export_window()

    window.close()


if __name__ == "__main__":
    main()
