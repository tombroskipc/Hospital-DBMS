import numpy as np
import matplotlib.pyplot as plt


# creating the dataset
def bill_report_graph(untreated_data, start_date=0, end_date=0):
    data = {}
    for each_date in untreated_data:
        data[str(each_date[0])[-4:]] = each_date[1]
    courses = list(data.keys())
    values = list(data.values())
 
    # fig = plt.figure(figsize = (10, 5))

    # creating the bar plot
    plt.bar(courses, values, color ='maroon')
    plt.xlabel("Date")
    plt.ylabel("Total earning each day")
    plt.title(f"Daily report from {start_date} to {end_date}")
    plt.savefig('static/img/between-report.png')
    plt.close()
    return

def bill_report_7_graph(untreated_data):
    data = {}
    for each_date in untreated_data:
        data[str(each_date[0])[-2:]] = each_date[1]
    if len(data) <= 12:
        courses = list(data.keys())
    values = list(data.values())

    # fig = plt.figure(figsize = (10, 5))

    # creating the bar plot
    plt.bar(courses, values, color ='maroon')

    plt.xlabel("Date")
    plt.ylabel("Total earning each day")
    plt.title(f"Daily report last 7 days")
    plt.savefig('static/img/daily-report.png')
    plt.close()
    return