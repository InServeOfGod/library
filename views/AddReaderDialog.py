from PyQt5.QtWidgets import QVBoxLayout, QFormLayout, QLineEdit, QDialog, QPushButton, QTextEdit


class AddReaderDialog(QDialog):
    def __init__(self, controller):
        super(AddReaderDialog, self).__init__()

        self.controller = controller
        self.model = self.controller.model

        self.mainLayout = QVBoxLayout()
        self.formLayout = QFormLayout()

        self.edit_name = QLineEdit()
        self.edit_surname = QLineEdit()
        self.edit_email = QLineEdit()
        self.edit_address = QTextEdit()
        self.edit_phone = QLineEdit()
        self.text_details = QTextEdit()
        self.btn_submit = QPushButton("Ekle")

        self.uis = [self.edit_name, self.edit_surname, self.edit_email, self.edit_address, self.edit_phone]

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

        self.edit_phone.setPlaceholderText("+90.(000).000.00.00")
        self.text_details.setPlaceholderText("Buraya yazın...")

        self.formLayout.addRow("İsim : ", self.edit_name)
        self.formLayout.addRow("Soyisim : ", self.edit_surname)
        self.formLayout.addRow("Email : ", self.edit_email)
        self.formLayout.addRow("Adres : ", self.edit_address)
        self.formLayout.addRow("Telefon : ", self.edit_phone)
        self.formLayout.addRow("Detaylar : ", self.text_details)
        self.formLayout.addWidget(self.btn_submit)
