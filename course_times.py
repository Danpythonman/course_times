import shelve
import os
import PySimpleGUI as sg
import time
from datetime import datetime, date


def calculate_elapsed_time(time_1, time_2):
    """Calculates the difference, in minutes, of two times
    Format of times are HH:MM"""

    # Get the hours and minutes from each time
    hours_1 = int(time_1[0:2])
    minutes_1 = int(time_1[3:5])
    hours_2 = int(time_2[0:2])
    minutes_2 = int(time_2[3:5])

    # Calculate the total minutes elapsed
    minutes = (60 - minutes_1) + minutes_2
    hours = hours_2 - hours_1 - 1
    minutes += hours * 60

    return minutes


def export_window():
    """Creates a new window for showing current times for each course"""

    current_courses = ["EECS 1011", "ENG 1101", "MATH 1013", "MATH 1025",
                        "PHYS1800"]

    current_times = []
    with shelve.open("course_times.db") as db:
        print(db["MATH 1025"])
        for course in current_courses:
            current_times.append(db[course])

    layout = []

    i = 0
    for course in current_courses:
        layout.append([sg.Text(course), sg.Text(str(current_times[i]))])
        i += 1

    layout.append([sg.Button("Close", key="close")])

    window = sg.Window("Window 1", layout)

    while True:
        event, values = window.read()
        if event == None or event == "close":
            break

    window.close()

def main():
    """Main controlling function"""

    os.chdir("C:\\Users\\Daniel\\Documents\\Programming\\time_management")

    current_courses = ["EECS 1011", "ENG 1101", "MATH 1013", "MATH 1025",
                        "PHYS1800"]

    current_day = str(date.today())

    with shelve.open("course_times.db") as db:
        # Check if current weekday is Monday
        if datetime.today().weekday() == 0:
            # Check if the data has already been reset today
            if db["last_reset"] != current_day:
                # The data has not been reset yet, so we set all the values of
                # the courses to 0
                for course in current_courses:
                    db[course] = 0

                db["last_reset"] = current_day

    # 0 means a start time has not been recorded, so clicking the "Time"
    # button will start timing
    # 1 means a start time has been recorded, so clicking the "Time" button
    # will stop timing
    stopwatch_controller = 0

    layout = [[sg.Combo(current_courses, key="course_selected"), sg.Button("Time", key="time")],
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
                start_time = time.strftime("%H:%M", t)
                window["start_time"].update(start_time)

                # Timing has started, so update stopwach variable
                stopwatch_controller = 1
            else:
                # Record end time
                t = time.localtime()
                end_time = time.strftime("%H:%M", t)
                window["end_time"].update(end_time)

                elapsed_time = calculate_elapsed_time(start_time, end_time)

                window["elapsed_time"].update(elapsed_time)

                with shelve.open("course_times.db") as db:
                    previous_time = db[values["course_selected"]]
                    new_time = previous_time + elapsed_time
                    db[values["course_selected"]] = new_time

                # Reset stopwatch variable so it is ready to start timing again
                stopwatch_controller = 0

        elif event == "export":
            export_window()

    window.close()


if __name__ == "__main__":
    main()
