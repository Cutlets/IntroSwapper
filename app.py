'''
<one line to give the program's name and a brief idea of what it does.>
Copyright (C) 2021 Cutlets(https://github.com/Cutlets)

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
 
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>
'''

import os
import os.path
import sys
import glob
import shutil

from PyQt5.QtWidgets import *
from PyQt5.QtCore import QCoreApplication, Qt
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtGui import QStandardItem
from PyQt5 import uic

form_class = uic.loadUiType("introswapui.ui")[0]

class WindowClass(QDialog, form_class):
    def __init__(self):
        super().__init__(None, Qt.WindowTitleHint)
        self.setupUi(self)
        self.makeInitFolder()
        self.setWindowFlags(
            Qt.WindowCloseButtonHint
        )
        self.fileSwap.clicked.connect(self.swapFile)
        self.fileRestore.clicked.connect(self.restoreFile)
        self.selFolder.clicked.connect(self.folderOpen)
        self.shutDown.clicked.connect(QCoreApplication.instance().quit)

    ##############
    ### UNUSED ###
    def functiontest(self):
        self.progressBar.setValue(0)
        self.progressBar.setRange(0, 19)
        for i in range(20):
            self.progressBar.setValue(i)
    ### UNUSED ###
    ##############

    def makeInitFolder(self):
        os.makedirs("./bvid", exist_ok=True)


    def folderOpen(self):
        folder = QFileDialog.getExistingDirectory(self, "폴더 선택", "C:\Program Files (x86)")
        self.dirInfo.clear()

        if folder == '':
            windows_user_name = os.path.expanduser('~')
            windows_user_name = os.path.join(windows_user_name)
            folder = f"{windows_user_name}"

        folder = os.path.join(folder)

        self.folderDir.setText(folder)
        file_list = os.listdir(folder)

        if len(file_list) == 0:
            file_list.append("파일이 존재하지 않습니다.")

        for f in file_list:
            if os.path.isfile(os.path.join(folder, f)):
                self.dirInfo.addItem(f)

    def swapFile(self):
        self.progressBar.setValue(0)
        
        work_path = self.folderDir.text()

        if work_path == '':
            result = QMessageBox()
            result.setWindowTitle("결과")
            result.setInformativeText("경로가 없습니다.")
            result.setText("교체 실패")
            result.setIcon(QMessageBox.Critical)
            result.setStandardButtons(QMessageBox.Ok)
            result.exec_()
            return

        backup_path = os.path.join(".","bvid")
        swap_path = os.path.join(".","svid")

        if type(self.dirInfo.currentItem()) == type(None):
            result = QMessageBox()
            result.setWindowTitle("결과")
            result.setInformativeText("선택된 파일이 없습니다.")
            result.setText("교체 실패")
            result.setIcon(QMessageBox.Critical)
            result.setStandardButtons(QMessageBox.Ok)
            result.exec_()
            return

        original_f = str(self.dirInfo.currentItem().text())
        original_ext = os.path.splitext(os.path.join(work_path, original_f))[1]

        swap_fWithPath = glob.glob(os.path.join(swap_path, "*"+original_ext))

        if len(swap_fWithPath) > 0:
            self.progressBar.setRange(0, 3)
            o_file = os.path.join(work_path, original_f)
            s_file = swap_fWithPath[0]
            b_file = os.path.join(backup_path, original_f)

            if os.path.isfile(b_file):
                copyReply = QMessageBox.question(self, '파일 중복', '파일이 존재합니다.\n덮어쓰시겠습니까?',
                QMessageBox.Yes, QMessageBox.No)
                if copyReply == QMessageBox.Yes:
                    shutil.copyfile(o_file, b_file)
                    self.progressBar.setValue(1)
                    shutil.copyfile(s_file, o_file)
                    self.progressBar.setValue(2)

                    result = QMessageBox()
                    result.setWindowTitle("결과")
                    result.setInformativeText("교체가 완료되었습니다.")
                    result.setText("교체 성공")
                    result.setIcon(QMessageBox.Information)
                    result.setStandardButtons(QMessageBox.Ok)
                    result.exec_()
                else:
                    self.progressBar.setValue(2)
                    result = QMessageBox()
                    result.setWindowTitle("결과")
                    result.setIcon(QMessageBox.Critical)
                    result.setText("교체 중단")
                    result.setInformativeText("교체가 중단되었습니다.")
                    result.setStandardButtons(QMessageBox.Ok)
                    result.exec_()
                self.progressBar.setValue(3)

            else:
                shutil.copyfile(o_file, b_file)
                self.progressBar.setValue(1)
                shutil.copyfile(s_file, o_file)
                self.progressBar.setValue(2)

                result = QMessageBox()
                result.setWindowTitle("결과")
                result.setText("교체 성공")
                result.setInformativeText("교체가 완료되었습니다.")
                result.setIcon(QMessageBox.Information)
                result.setStandardButtons(QMessageBox.Ok)
                result.exec_()
                self.progressBar.setValue(3)

        else:
            self.progressBar.setRange(0, 1)
            self.progressBar.setValue(1)
            print("No file matched.")

    def restoreFile(self):
        self.progressBar.setValue(0)
        
        work_path = self.folderDir.text()

        if work_path == '':
            result = QMessageBox()
            result.setWindowTitle("결과")
            result.setInformativeText("경로가 없습니다.")
            result.setText("복원 실패")
            result.setIcon(QMessageBox.Critical)
            result.setStandardButtons(QMessageBox.Ok)
            result.exec_()
            return

        backup_path = os.path.join(".","bvid")

        if type(self.dirInfo.currentItem()) == type(None):
            result = QMessageBox()
            result.setWindowTitle("결과")
            result.setInformativeText("선택된 파일이 없습니다.")
            result.setText("복원 실패")
            result.setIcon(QMessageBox.Critical)
            result.setStandardButtons(QMessageBox.Ok)
            result.exec_()
            return

        original_f = str(self.dirInfo.currentItem().text())

        if os.path.isfile(os.path.join(backup_path, original_f)):
            self.progressBar.setRange(0, 3)
            o_file = os.path.join(work_path, original_f)
            b_file = os.path.join(backup_path, original_f)

            shutil.copyfile(b_file, o_file)
            self.progressBar.setValue(1)
            self.progressBar.setValue(2)

            result = QMessageBox()
            result.setWindowTitle("결과")
            result.setText("복원 성공")
            result.setInformativeText("복원이 완료되었습니다.")
            result.setIcon(QMessageBox.Information)
            result.setStandardButtons(QMessageBox.Ok)
            result.exec_()

            self.progressBar.setValue(3)
        else:
            self.progressBar.setRange(0, 1)
            
            result = QMessageBox()
            result.setWindowTitle("결과")
            result.setText("복원 실패")
            result.setInformativeText("복원할 파일이 없습니다..")
            result.setIcon(QMessageBox.Critical)
            result.setStandardButtons(QMessageBox.Ok)
            result.exec_()

            self.progressBar.setValue(1)

if __name__=="__main__":
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    sys.exit(app.exec_())