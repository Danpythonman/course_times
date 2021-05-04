import os
import json
import PySimpleGUI as sg


def main():
    """Main controlling function"""

    os.chdir("C:\\Users\\Daniel\\Documents\\Programming\\time_management")

    # Check if the folder for the JSON files exists already, if not then
    # create it
    if "json_data" not in os.listdir():
        os.mkdir("json_data")

        # Make folder to hold preferences
        os.mkdir("json_data/preferences")

        # Make preferences file (it is a JSON file)
        with open("json_data/preferences/preferences.json", "w") as preferences_json_file:
            preferences_json_file.write(json.dumps({"current_semester": "No semster chosen", "current_courses": None}, indent=4))

        semesters = os.listdir("json_data")
        semesters.remove("preferences")

    else:
        semesters = os.listdir("json_data")
        semesters.remove("preferences")

    layout = [
        [sg.Text("Choose Semester:"), sg.Combo(semesters, key="semester_selected"), sg.Button("Choose", key="choose_semester")],
        [sg.Text("Add New Semester:"), sg.Input(key="new_semester_name"), sg.Button("Add", key="add_semester")],
        [sg.Text("Add"), sg.Input(key="number_of_courses", size=(2,1)), sg.Text("new courses"), sg.Button("Go", key="add_courses")],
        [sg.Text("View Data of Selected Semester"), sg.Button("View", key="data")]
    ]

    window = sg.Window("Choose Semester", layout)

    # --- Main event loop ---
    while True:
        event, values = window.read()

        if event == None or event == "Exit":
            break

        elif event == "choose_semester":
            if values["semester_selected"] != "":
                with open("json_data/preferences/preferences.json") as preferences_json_file:
                    course_times_settings = json.load(preferences_json_file)

                course_times_settings["current_semester"] = values["semester_selected"]

                with open("json_data/preferences/preferences.json", "w") as preferences_json_file:
                    preferences_json_file.write(json.dumps(course_times_settings))
            else:
                sg.popup("Choose a semester or add a new one")

        elif event == "add_semester":
            if values["new_semester_name"] != "":
                os.mkdir("json_data/" + values["new_semester_name"])

                with open("json_data/preferences/preferences.json") as preferences_json_file:
                    course_times_settings = json.load(preferences_json_file)

                course_times_settings["current_semester"] = values["new_semester_name"]

                with open("json_data/preferences/preferences.json", "w") as preferences_json_file:
                    preferences_json_file.write(json.dumps(course_times_settings))
            else:
                sg.popup("Choose a name for the new semester")

        elif event == "add_courses":
            if values["number_of_courses"] != "":
                course_names = []
                for course_number in range(int(values["number_of_courses"])):
                    course_names.append(sg.popup_get_text(str(course_number + 1) + ". Enter course name"))

                with open("json_data/preferences/preferences.json") as preferences_json_file:
                    course_times_settings = json.load(preferences_json_file)

                course_times_settings["current_courses"] = course_names

                with open("json_data/preferences/preferences.json", "w") as preferences_json_file:
                    preferences_json_file.write(json.dumps(course_times_settings, indent=4))
            else:
                sg.popup("Enter a number")

        elif event == "data":
            from course_times_graphs import graphWindow
            graphWindow(values["semester_selected"])


if __name__ == "__main__":
    main()
