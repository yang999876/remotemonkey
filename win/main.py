import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel
from PyQt5.QtGui import QFontDatabase, QPixmap, QIcon, QFont
from PyQt5.QtCore import Qt, QSize
import paho.mqtt.client as mqtt
import configparser

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.conf = self.loadConf()

        self.initUI()
        self.initMqtt()
        self.state = 0

    def initMqtt(self):
        client_id = "windows"
        broker_address = self.conf['MQTT']['broker']
        port = int(self.conf['MQTT']['port'])

        username = self.conf["Credentials"]["username"]
        password = self.conf["Credentials"]["password"]

        # 创建MQTT客户端实例
        self.client = mqtt.Client(client_id=client_id, callback_api_version=mqtt.CallbackAPIVersion.VERSION1)

        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                print("Connected to MQTT Broker!")
                client.subscribe(self.conf['MQTT']['topic'])
            else:
                print(f"Failed to connect, return code {rc}")

        def on_message(client, userdata, msg):
            print(f"Received message: {msg.payload.decode()} from topic: {msg.topic}")

        self.client.on_connect = on_connect
        self.client.on_message = on_message

        # 建立加密连接
        self.client.username_pw_set(username, password)
        self.client.connect(broker_address, port=port, keepalive=60)

        self.client.loop_start()

    def initUI(self):
        # 设置窗口为无边框
        self.setWindowFlags(Qt.FramelessWindowHint)

        # 设置窗口标题和大小
        self.setFixedSize(1920, 1080)

        # 居中显示窗口
        self.center()

        font_id = QFontDatabase.addApplicationFont('AlibabaPuHuiTi-2-105-Heavy.ttf')
        font_family = QFontDatabase.applicationFontFamilies(font_id)[0]

        # 设置窗口背景图片并缩放到窗口大小
        background = QLabel(self)
        pixmap = QPixmap('bg.png').scaled(self.size(), Qt.KeepAspectRatioByExpanding)
        background.setPixmap(pixmap)
        background.setGeometry(0, 0, 1920, 1080)

        # 创建按钮并设置按钮图片和文本
        self.btn = QPushButton(self)
        self.btn.setGeometry(200, 800, 463, 100)  # 设置按钮的位置和大小
        self.btn.setFont(QFont(font_family, 28))
        self.btn.setText('启动')
        
        # 使按钮布局可见
        self.btn.clicked.connect(self.onButtonClick)

        # 设置按钮的背景图片和文本位置
        self.btn.setStyleSheet("""
            QPushButton {
                background-image: url(btn.png);
                background-position: center;
                background-repeat: no-repeat;
                background-color: transparent;
                border: none;
                text-align: center;
                padding: 20px;
                color: black;
            }
            QPushButton:hover {
                background-image: url(btn_hover.png); /* 悬停时的背景图片 */
            }
        """)

        # 创建标题标签
        title = QLabel('猿神', self)
        title.setFont(QFont(font_family, 86))  # 使用自定义字体
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: white;")  # 设置标题文本颜色
        title.setGeometry(200, 400, 463, 150)

    def center(self):
        # 获取窗口大小并计算居中位置
        qr = self.frameGeometry()
        cp = QApplication.desktop().screenGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def onButtonClick(self):
        if self.state == 0:
            self.btn.setText('关闭')
            self.state = 1
            self.sendMsg()
        elif self.state == 1:
            self.state = 2
            self.sendMsg()
            self.btn.setText('退出')
        elif self.state == 2:
            QApplication.quit()

    def sendMsg(self):
        self.client.publish(topic=self.conf['MQTT']['topic'], payload=self.conf['MQTT']['key'], qos=2)

    def loadConf(self):
        config = configparser.ConfigParser()
        config.read("conf.ini")

        configData = {}
        for section in config.sections():
            configData[section] = {}
            for key in config[section]:
                configData[section][key] = config[section][key]

        return configData

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    ex.show()
    sys.exit(app.exec_())
