from PyQt5.QtWidgets import QVBoxLayout, QFormLayout, QLineEdit, QDialog, QPushButton, QTextEdit, QSpinBox, \
    QComboBox, QDateEdit


class AddBookDialog(QDialog):
    def __init__(self, controller):
        super(AddBookDialog, self).__init__()

        self.controller = controller
        self.model = self.controller.model

        self.mainLayout = QVBoxLayout()
        self.formLayout = QFormLayout()

        self.edit_name = QLineEdit()
        self.edit_stock = QSpinBox()
        self.edit_page = QSpinBox()
        self.combo_author = QComboBox()
        self.combo_case = QComboBox()
        self.combo_lang = QComboBox()
        self.combo_genre = QComboBox()
        self.combo_publish_house = QComboBox()
        self.combo_status = QComboBox()
        self.date_publish = QDateEdit()
        self.text_details = QTextEdit()
        self.btn_submit = QPushButton("Ekle")

        self.uis = [self.edit_name, self.edit_stock, self.edit_page]

        self._ui()

    def refactor(self):
        for ui in self.uis:
            ui.setText("")

        # we do not want to include text_details variable, so we make it separated
        self.text_details.setText("")

    def _ui(self):
        self.setWindowTitle(self.model.title)
        self.setWindowIcon(self.model.icon)
        self.setLayout(self.formLayout)

        self.btn_submit.setText("Ekle")
        self.btn_submit.clicked.connect(self.controller.insert_people)

        self.edit_stock.setMinimum(0)
        self.edit_page.setMinimum(1)
        self.text_details.setPlaceholderText("Buraya yazın...")

        self.formLayout.addRow("Ad : ", self.edit_name)
        self.formLayout.addRow("Stok : ", self.edit_stock)
        self.formLayout.addRow("Sayfa Sayısı : ", self.edit_page)
        self.formLayout.addRow("Yazar : ", self.combo_author)
        self.formLayout.addRow("Dolap No : ", self.combo_case)
        self.formLayout.addRow("Dil : ", self.combo_lang)
        self.formLayout.addRow("Tür ", self.combo_genre)
        self.formLayout.addRow("Yayınevi : ", self.combo_publish_house)
        self.formLayout.addRow("Durum : ", self.combo_status)
        self.formLayout.addRow("Yayın Tarihi : ", self.date_publish)
        self.formLayout.addRow("Detaylar : ", self.text_details)
        self.formLayout.addWidget(self.btn_submit)
