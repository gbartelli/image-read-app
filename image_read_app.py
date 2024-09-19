import sys
import os
import time
import requests
from io import BytesIO
from PIL import Image
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QPushButton,
    QVBoxLayout, QHBoxLayout, QFileDialog, QLineEdit, QTextEdit, QMessageBox
)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt

class OCRApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Extrator de Texto de Imagem")

        # Widgets
        self.image_label = QLabel("Nenhuma imagem carregada")
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setFixedSize(400, 300)

        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Insira o URL da imagem aqui")

        self.key_input = QLineEdit()
        self.key_input.setPlaceholderText("Insira sua Subscription Key da Azure")

        self.endpoint_input = QLineEdit()
        self.endpoint_input.setPlaceholderText("Insira seu Endpoint da Azure")

        self.load_button = QPushButton("Carregar imagem local")
        self.load_button.clicked.connect(self.load_image)

        self.extract_button = QPushButton("Retirar texto da imagem")
        self.extract_button.clicked.connect(self.extract_text)

        self.text_output = QTextEdit()
        self.text_output.setReadOnly(True)

        # Layouts
        key_layout = QHBoxLayout()
        key_layout.addWidget(self.key_input)
        key_layout.addWidget(self.endpoint_input)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.load_button)
        button_layout.addWidget(self.extract_button)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.image_label)
        main_layout.addWidget(self.url_input)
        main_layout.addLayout(key_layout)
        main_layout.addLayout(button_layout)
        main_layout.addWidget(self.text_output)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        # Variáveis de estado
        self.image_path = None
        self.image_url = None

    def load_image(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Selecionar Imagem", "", "Imagens (*.png *.jpg *.jpeg *.bmp)")
        if file_name:
            self.image_path = file_name
            self.image_url = None  # Limpa o URL caso exista
            pixmap = QPixmap(self.image_path).scaled(400, 300, Qt.KeepAspectRatio)
            self.image_label.setPixmap(pixmap)
            self.url_input.clear()

    def extract_text(self):
        self.text_output.clear()

        # Obter as chaves de API inseridas pelo usuário
        subscription_key = self.key_input.text()
        endpoint = self.endpoint_input.text()

        if not subscription_key or not endpoint:
            QMessageBox.warning(self, "Chaves de API faltando", "Por favor, insira sua Subscription Key e Endpoint da Azure.")
            return

        # Inicializar o cliente do Azure Computer Vision
        try:
            self.computervision_client = ComputerVisionClient(
                endpoint, CognitiveServicesCredentials(subscription_key)
            )
        except Exception as e:
            QMessageBox.critical(self, "Erro na Autenticação", f"Erro ao conectar ao serviço Azure:\n{e}")
            return

        if self.url_input.text():
            self.image_url = self.url_input.text()
            self.image_path = None  # Limpa o caminho local caso exista
            self.process_image_url()
        elif self.image_path:
            self.process_image_file()
        else:
            self.text_output.setText("Por favor, carregue uma imagem ou insira um URL válido.")

    def process_image_url(self):
        try:
            read_response = self.computervision_client.read(self.image_url, raw=True)

            # Obtém o ID da operação
            operation_location = read_response.headers["Operation-Location"]
            operation_id = operation_location.split("/")[-1]

            # Espera a conclusão da operação
            while True:
                read_result = self.computervision_client.get_read_result(operation_id)
                if read_result.status not in ['notStarted', 'running']:
                    break
                time.sleep(1)

            # Exibe o texto extraído
            if read_result.status == OperationStatusCodes.succeeded:
                extracted_text = ""
                for page in read_result.analyze_result.read_results:
                    for line in page.lines:
                        extracted_text += line.text + "\n"
                self.text_output.setText(extracted_text)
            else:
                self.text_output.setText("Não foi possível extrair o texto da imagem.")

            # Atualiza a visualização da imagem
            response = requests.get(self.image_url)
            img = QPixmap()
            img.loadFromData(response.content)
            pixmap = img.scaled(400, 300, Qt.KeepAspectRatio)
            self.image_label.setPixmap(pixmap)
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Ocorreu um erro ao processar a imagem:\n{e}")

    def process_image_file(self):
        try:
            with open(self.image_path, "rb") as image_file:
                read_response = self.computervision_client.read_in_stream(image_file, raw=True)

            # Obtém o ID da operação
            operation_location = read_response.headers["Operation-Location"]
            operation_id = operation_location.split("/")[-1]

            # Espera a conclusão da operação
            while True:
                read_result = self.computervision_client.get_read_result(operation_id)
                if read_result.status not in ['notStarted', 'running']:
                    break
                time.sleep(1)

            # Exibe o texto extraído
            if read_result.status == OperationStatusCodes.succeeded:
                extracted_text = ""
                for page in read_result.analyze_result.read_results:
                    for line in page.lines:
                        extracted_text += line.text + "\n"
                self.text_output.setText(extracted_text)
            else:
                self.text_output.setText("Não foi possível extrair o texto da imagem.")
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Ocorreu um erro ao processar a imagem:\n{e}")

def main():
    app = QApplication(sys.argv)
    window = OCRApp()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
