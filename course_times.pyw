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
        # Day 0 is Monday
        if subtracted_date.weekday() == 0:
            start_date = subtracted_date
        subtract_days += 1

    # Initialize varaible to hold date object for end date and a counter for
    # the number of days to get to the next Saturday
    end_date = None
    add_days = 0
    # Stop when the end date variable gets filled
    while not end_date:
        added_date = current_date + timedelta(add_days)
        # Day 6 is Sunday
        if added_date.weekday() == 6:
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


def main():
    """Main controlling function"""

    os.chdir("C:\\Users\\Daniel\\Documents\\Programming\\time_management")

    current_day = date.today()

    # Check if the folder for the JSON files exists already, if not then
    # create it
    if "json_data" not in os.listdir():
        os.mkdir("json_data")

        # Make folder to hold preferences
        os.mkdir("json_data/preferences")

        # Make preferences file (it is a JSON file)
        with open("json_data/preferences/preferences.json", "w") as preferences_json_file:
            preferences_json_file.write(json.dumps({"current_semester": "No semster chosen", "current_courses": "No courses"}, indent=4))

    with open("json_data/preferences/preferences.json") as preferences_json_file:
        preferences_data = json.load(preferences_json_file)

        # This is a list of strings that are the names of the current courses
        current_courses = preferences_data["current_courses"]

        # This is a string that is the name of the current semester
        current_semester = preferences_data["current_semester"]
    current_week_filename = current_semester + "/" + create_json_filename(current_day) + ".json"

    # If the current week's JSON file does not yet exist, create it
    if create_json_filename(current_day) + ".json" not in os.listdir("json_data/" + current_semester):
        course_times = {}
        with open("json_data\\" + current_week_filename, "w") as json_file:
            # Initialize the dictionary for the file
            for course in current_courses:
                course_times[course] = 0
            json_file.write(json.dumps(course_times, indent=4))

    # 0 means a start time has not been recorded, so clicking the "Time"
    # button will start timing
    # 1 means a start time has been recorded, so clicking the "Time" button
    # will stop timing
    stopwatch_controller = 0

    layout = [[sg.Text("Current Semester: " + current_semester)],
              [sg.Combo(current_courses, key="course_selected"), sg.Button("Time", key="time"), sg.Button("Entry", key="entry")],
              [sg.Text("Start time: "), sg.Text("00:00", key="start_time")],
              [sg.Text("End time: "), sg.Text("00:00", key="end_time")],
              [sg.Text("Elapsed Minutes: "), sg.Text("000", key="elapsed_time")],
              [sg.Button("Check Times for this Week", key="export")]]

    window = sg.Window("Course Times", layout)

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
            import course_times_output
            course_times_output.export_window(current_week_filename)

    window.close()


if __name__ == "__main__":
    main()
