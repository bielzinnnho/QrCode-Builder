from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.uic import loadUi
from PyQt5.QtCore import pyqtSlot
from pyshorteners import Shortener
from notifypy import Notify

def CREATE_SHORT_URL(url):
    link = Shortener()
    return link.tinyurl.short(url)

class QrCodeUI(QMainWindow): 

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        loadUi(("QrCodeBuilder.ui"), self)
        self.show()

        # self.btnGerar.clicked.connect(self.texto)

    def getURL(self):
        return self.url.text()
    
    def setURLShort(self, url):
        return self.urlShort.setText(url)
    
    @pyqtSlot()
    def on_btnGerar_clicked (self):
        if self.url.text().startswith("https://") == False:
            self.urlShort.setText("Insira uma URL válida")
            self.showMessage("Erro", "Insira uma URL válida", "gatinhoPuto.jpg")
            return
        txt = self.getURL()
        url = CREATE_SHORT_URL(txt)
        self.setURLShort(url)
        self.showMessage("Sucesso", "URL encurtada com sucesso!", "gatinhoJoia.jpg")

    def showMessage(self, title, message, icon):
        notification = Notify()
        notification.title = title
        notification.message = message
        notification.icon = icon
        notification.send()
        QMessageBox.information(self, title, message)


if __name__ == "__main__":
    app = QApplication([])
    tela = QrCodeUI()
    app.exec()