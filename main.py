# from moviepy.editor import VideoFileClip
# from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QPushButton, QLabel
# import os
# # 核心代码
# # # video_path = '1.mp4'  # 替换为您的视频文件路径
# # # audio = VideoFileClip(video_path).audio
# # # audio.write_audiofile('output_audio.wav')

from moviepy.editor import VideoFileClip, AudioFileClip
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QPushButton, QLabel
from PyQt5.QtCore import QThread, pyqtSignal
import os

class ConvertThread(QThread):
    update_progress_signal = pyqtSignal(str)

    def __init__(self, video_path):
        super().__init__()
        self.video_path = video_path

    def run(self):
        video_clip = VideoFileClip(self.video_path)
        audio_clip = video_clip.audio
        output_audio_path = os.path.splitext(self.video_path)[0] + "_audio.wav"
        audio_clip.write_audiofile(output_audio_path, verbose=False)
        self.update_progress_signal.emit("音频文件已保存")

class 视频转音频转换器(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.video_path = None
        self.conversion_thread = None

    def initUI(self):
        self.setWindowTitle("视频转音频转换器")
        self.setGeometry(100, 100, 400, 200)

        self.label = QLabel("选择一个视频文件:")
        self.label.move(20, 20)

        self.btn_browse = QPushButton("浏览", self)
        self.btn_browse.move(20, 50)
        self.btn_browse.clicked.connect(self.browse_video)

        self.btn_convert = QPushButton("转换", self)
        self.btn_convert.move(20, 100)
        self.btn_convert.clicked.connect(self.convert_video)

        self.progress_label = QLabel("", self)
        self.progress_label.move(20, 150)

    def browse_video(self):
        options = QFileDialog.Options()
        video_file, _ = QFileDialog.getOpenFileName(self, "打开视频文件", "", "视频文件 (*.mp4 *.avi *.mkv *.mov);;所有文件 (*)", options=options)
        self.video_path = video_file
        if self.video_path:
            self.progress_label.setText("视频文件已上传")

    def convert_video(self):
        if self.video_path:
            self.progress_label.setText("转换中...")
            self.btn_convert.setEnabled(False)
            self.conversion_thread = ConvertThread(self.video_path)
            self.conversion_thread.update_progress_signal.connect(self.update_progress)
            self.conversion_thread.start()

    def update_progress(self, message):
        self.progress_label.setText(message)
        self.btn_convert.setEnabled(True)

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    window = 视频转音频转换器()
    window.show()
    sys.exit(app.exec_())

