import asyncio
import time

from PyQt5.QtCore import QMetaObject, Qt, Q_ARG, pyqtSlot
from PyQt5.QtWidgets import QWidget

from app.custom_view.custom_widget import MultiBox
from app.resources.UI_TableInterface import Ui_TableForm


class TableInterface(QWidget, Ui_TableForm):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.cbb = MultiBox(self)
        self.verticalLayout.addWidget(self.cbb)
        self.export_btn.clicked.connect(self.export)
        self.anlaysis_btn.clicked.connect(self.anlaysis)

    def export(self):
        texts = [f"按钮{i}" for i in range(500)]
        st = time.time()
        self.cbb.add_items(texts)
        print(time.time() - st, "创建耗时")

    def anlaysis(self):
        texts = [f"按钮{i}" for i in range(500)]
        loop = asyncio.get_event_loop()
        # 运行异步函数
        start_time = time.time()  # 记录开始时间
        loop.run_until_complete(self.create_components(texts))
        end_time = time.time()  # 记录结束时间
        elapsed_time = end_time - start_time
        print(f"异步任务总耗时: {elapsed_time}秒")
        self.update()

    async def create_components(self,texts):
        batch_size = 2  # 每次添加的项目数量

        for i in range(0, len(texts), batch_size):

            batch_texts = texts[i:i + batch_size]
            print(batch_texts)
            QMetaObject.invokeMethod(self.cbb, "add_button_to_layout", Qt.QueuedConnection,
                                     Q_ARG(list, batch_texts))

    @pyqtSlot(list)
    def add_button_to_layout(self, texts):
        self.cbb.add_items(texts)
