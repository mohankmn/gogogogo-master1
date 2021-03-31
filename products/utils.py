#here we will store all the functions that e will use in views.py
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
from datetime import datetime, timedelta
import base64
from django.contrib.auth.models import User

def get_salesman_from_id(val):
    print(val)
    user = User.objects.get(id=val)
    return user


def get_image():
    # create a bytes buffer for the image to save
    buffer = BytesIO()
    # create the plot with the use of BytesIO objects as its file
    plt.savefig(buffer, format='png')
    # set the cursor to the beginning of the stream
    buffer.seek(0)
    # retreive the entire content of the 'file'
    image_png = buffer.getvalue()

    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')

    # free the memory of the buffer
    buffer.close()
    return graph

def get_simple_plot(chart_type, *args, **kwargs):
    plt.switch_backend('AGG')
    fig = plt.figure(figsize=(15,4))
    x   = kwargs.get('x')
    y   = kwargs.get('y')
    data = kwargs.get('data')
    if chart_type =='bar':
        title = 'demand per day'
        plt.title(title)
        plt.bar(x, y)
    elif chart_type =='line':
        title = 'demand per day'
        plt.title(title)
        plt.plot(x, y)
    else:
        title = 'Number of times product got sold'
        plt.title(title)
        sns.countplot('name', data=data)

    plt.xticks(rotation=90)
    plt.tight_layout()

    graph = get_image()
    return graph