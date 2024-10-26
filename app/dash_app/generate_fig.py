import math
import random

import numpy as np
import plotly.graph_objs as go
from plotly.subplots import make_subplots


class CustomPlot:
    config = {
        "scrollZoom": True,
        "editable": True,
        "staticPlot": False,
        "displayModeBar": True,
        "displaylogo": False,
        "modeBarButtonsToRemove": [
            "sendDataToCloud",
            "editInChartStudio",
            "lasso2d",
            "drawrect",
            "select2d",
        ],
        "toImageButtonOptions": {
            "format": "png",
            "filename": "custom_image",
            "scale": 1,
        },
        "showLink": False,
        "showTips": True,
        "locale": "zh",
        "doubleClick": "reset+autosize",
        "doubleClickDelay": 300,
        "sendData": False,
        "watermark": True,
        "modeBarButtonsToAdd": ["toggleHover","hoverCompareCartesian", "toggleSpikelines", "tableRotation"],
        "autosizable": True,
    }
    @classmethod
    def generate_random_data(cls,num_points=10000, noise_level=5):
        x_values = list(range(num_points))
        y_values = [math.sin(2 * math.pi * x / 100) * 50 + 50 + random.uniform(-noise_level, noise_level) for x in
                    x_values]

        return {'x': x_values, 'y': y_values}

    @classmethod
    def generate_figure(cls):
        fig=go.Figure()
        return fig
