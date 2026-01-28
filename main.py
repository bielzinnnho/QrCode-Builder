from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QFileDialog
from PyQt5.QtGui import QPixmap
from PyQt5.uic import loadUi
from PyQt5.QtCore import pyqtSlot
from pyshorteners import Shortener
from notifypy import Notify
from os import path
import qrcode

def CREATE_SHORT_URL(url):
    link = Shortener()
    return link.tinyurl.short(url)

def CREATE_QRCODE(link):
    img = qrcode.make(link)
    img.save("qrcode.png")

def GET_LOCAL_PATH(myPath):
    return

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
        if self.url.text().startswith("https://") == False or self.url.text().startswith("https://tinyurl.com") == True:
            self.urlShort.setText("Insira uma URL válida")
            self.showMessage("Erro", "Insira uma URL válida", "gatinhoPuto.jpg")
            return
        txt = self.getURL()
        url = CREATE_SHORT_URL(txt)
        CREATE_QRCODE(url)
        self.setURLShort(url)
        self.img.setPixmap(QPixmap("qrcode.png"))
        self.btnSalvar.setEnabled(True)
        self.showMessage("Sucesso", "URL encurtada com sucesso!", "gatinhoJoia.jpg")

    @pyqtSlot()
    def on_btnSalvar_clicked(self):
        self.salvar()

    def salvar(self):
        nomeArquivo, _ = QFileDialog.getSaveFileName(self, "Salvar Imagem")
        if nomeArquivo:
            caminho = path.dirname(nomeArquivo)
            nome = nomeArquivo.removeprefix(caminho)
            # Ler a foto do QRCODE
            with open("qrcode.png", "rb") as fotoQrcode:
                dadosQrcode = fotoQrcode.read()
            
            # salvar a foto aonde o user escolheu
            with open(caminho+f"{nome}.png", "wb") as foto:
                foto.write(dadosQrcode)

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