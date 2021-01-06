import os
import time
from datetime import datetime, date, timedelta
import json
import PySimpleGUI as sg


def create_json_filename(current_date):
    """
    Creates the name for the current week's JSON file.
    The name will be start date to end date in this format:
    YYYY-MM-DD--YYYY-MM-DD
    """

    # -- IMPORTANT --
    # In the datetime module, Monday is 0, Tuseday is 1, ..., Sunday is 6

    # Initialize varaible to hold date object for start date and a counter for
    # the number of days to get to the last Sunday
    start_date = None
    subtract_days = 0
    # Stop when the start date variable gets filled
    while not start_date:
        subtracted_date = current_date - timedelta(subtract_days)
        # Day 6 is Sunday
        if subtracted_date.weekday() == 6:
            start_date = subtracted_date
        subtract_days += 1

    # Initialize varaible to hold date object for end date and a counter for
    # the number of days to get to the next Saturday
    end_date = None
    add_days = 0
    # Stop when the end date variable gets filled
    while not end_date:
        added_date = current_date + timedelta(add_days)
        # Day 5 is Saturday
        if added_date.weekday() == 5:
            end_date = added_date
        add_days += 1

    # Return the file name without the ".json"
    return start_date.strftime("%y-%m-%d") + "--" + end_date.strftime("%y-%m-%d")


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

    current_day = date.today()

    current_week_filename = create_json_filename(current_day) + ".json"

    # Check if the folder for the JSON files exists already, if not then
    # create it
    if "json_data" in os.listdir():
        # Check if the folder for the JSON files is empty and if it is, add the
        # first JSON file
        if os.listdir("json_data") == []:
            with open("json_data\\" + current_week_filename, "w") as json_file:
                pass
    else:
        os.mkdir("json_data")

    # If the current week's JSON file does not yet exist, create it
    if current_week_filename not in os.listdir("json_data"):
        with open("json_data\\" + current_week_filename, "w") as json_file:
            pass

    # 0 means a start time has not been recorded, so clicking the "Time"
    # button will start timing
    # 1 means a start time has been recorded, so clicking the "Time" button
    # will stop timing
    stopwatch_controller = 0

    layout = [[sg.Combo(["PHYS 1800"], key="course_selected", default_value="PHYS 1800"), sg.Button("Time", key="time"), sg.Button("Entry", key="entry")],
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

                with open("json_data\\" + current_week_filename) as json_file:
                    course_times = json.load(json_file)

                course_times[values["course_selected"]] += elapsed_time

                with open("json_data\\" + current_week_filename, "w") as json_file:
                    json_file.write(json.dumps(course_times, indent=4))

                # Reset stopwatch variable so it is ready to start timing again
                stopwatch_controller = 0

        elif event == "entry":
            entered_time = int(sg.popup_get_text("Enter the time you want to add or subtract"))

            with open("json_data\\" + current_week_filename) as json_file:
                course_times = json.load(json_file)

            course_times[values["course_selected"]] += entered_time

            with open("json_data\\" + current_week_filename, "w") as json_file:
                json_file.write(json.dumps(course_times, indent=4))

        elif event == "export":
            export_window()

    window.close()


if __name__ == "__main__":
    main()
