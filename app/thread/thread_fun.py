from PyQt5.QtCore import pyqtSignal, QThread

from app.dash_app.plot_resample import SimpleChartApp


class DashThread(QThread):
    signal = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super().__init__()
        self.queue = kwargs.get('queue')
        self.chart_app: SimpleChartApp = kwargs.get('chart_app')
        self.host = kwargs.get('host')
        self.port = kwargs.get('port')

    def run(self):
        self.chart_app.run(self.host, self.port)

    def stop(self):
        self.chart_app.stop_event.set()
