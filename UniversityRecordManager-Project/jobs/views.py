from django.shortcuts import render

from django.http import HttpResponse
from collections import OrderedDict

from fusioncharts import FusionCharts

from .models import Record
# Create your views here.

# Category Dictionary
categ = {
    "u_grad_freshmen": "Freshmen",
    "u_grad_sophomore": "Sophomores",
    "u_grad_junior": "Juniors",
    "u_grad_senior": "Seniors",
    "grad_ms_year_one": "Master's FY",
    "grad_ms_year_two": "Master's SY"
         }


# def index(request):
#     year_data = Record.objects.values_list('record_year', flat=True).order_by('record_year')
#     print(year_data)
#     return render(request, 'jobs/home_coded.html', {
#         'year_arr': year_data,
#     })


# View for Homepage
def homepage(request):
    year_data = Record.objects.values_list('record_year', flat=True).order_by('record_year')
    print(year_data)
    if request.method == "POST" and request.POST.get('data_year') is not '':
        year_to_display = request.POST.get('data_year')
        print(year_to_display)
        # Fetch all records from the Model.
        records = Record.objects
        chart_data = OrderedDict()
        chart_data["caption"] = "Student Count at North Carolina State University for the Year {}".format(
            year_to_display)
        chart_data["subCaption"] = ""
        chart_data["xAxisName"] = "Student Category"
        chart_data["yAxisName"] = "Count"
        chart_data["numberSuffix"] = ""
        chart_data["theme"] = "carbon"

        data_source = OrderedDict()
        data_source["chart"] = chart_data
        data_source["data"] = []

        keys_to_exclude = ["id", "record_year"]

        # Create JSON Data to pass into Fusioncharts.
        for record in records.filter(record_year=year_to_display):
            for field, val in record:
                if field not in keys_to_exclude:
                    data = {}
                    data["label"] = categ[field]
                    data["value"] = val
                    # print(field, val)
                    data_source["data"].append(data)

        # Create an object for the bar chart using the FusionCharts class constructor
        # The chart data is passed to the data_source parameter.
        bar_chart = FusionCharts("column2d", "chart_work", "600", "400", "chart_work-container", "json", data_source)

        # Data filtering for Dropdown

        return render(request, 'jobs/home.html', {
            'output': bar_chart.render(),
            'year_data': year_data,
            'update_flag': True,
        })
    else:
        return render(request, 'jobs/home.html', {
            'year_data': year_data,
            'update_flag': False,
        })
