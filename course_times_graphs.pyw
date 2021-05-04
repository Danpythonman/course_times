import os
import json
import PySimpleGUI as sg
import matplotlib.pyplot as plt
import numpy as np

def value(val):
    return np.round(val/100 * total, 0)

def graphWindow(semester):
    """Displays the graphs of the course times"""

    os.chdir("C:\\Users\\Daniel\\Documents\\Programming\\time_management\\json_data\\" + semester)

    with open(os.listdir()[0]) as json_file:
        course_list = json.load(json_file).keys()

    layout = [
        [sg.Text("Total Time Spent By Course"), sg.Button("Pie Chart", key="total_time")],
        [sg.Text("Time Spent by Week"), sg.Button("Line Chart", key="weekly_time")]
    ]

    window = sg.Window("View Data", layout)

    # --- Main event loop ---
    while True:
        event, values = window.read()

        if event == None or event == "Exit":
            break

        elif event == "total_time":
            total_time = 0

            total_course_times = dict.fromkeys(course_list, 0)

            for data_file in os.listdir():
                with open(data_file) as json_file:
                    json_data = json.load(json_file)
                    for course in course_list:
                        current_course_time = json_data[course]
                        total_course_times[course] += current_course_time
                        total_time += current_course_time

            pie_chart = np.array(list(total_course_times.values()))
            plt.pie(pie_chart, labels=course_list, autopct=lambda p:"{:.0f}".format(p*total_time/100/60))
            plt.show()

        elif event == "weekly_time":
            week_dates = []
            week_values = []
            counter = 1

            for data_file in os.listdir():
                week_dates.append("Week " + str(counter))
                total_time = 0
                with open(data_file) as json_file:
                    json_data = json.load(json_file)
                    for course_time in list(json_data.values()):
                        total_time += course_time / 60
                week_values.append(total_time)
                counter += 1

            plt.plot(week_dates, week_values)
            plt.show()

graphWindow("Winter 2021")