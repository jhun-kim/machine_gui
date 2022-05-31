from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QTextEdit ,QListWidget ,QTableView ,QComboBox,QLabel,QLineEdit,QTextBrowser
import sys,pickle

from PyQt5 import uic, QtWidgets ,QtCore, QtGui
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn import metrics
import matplotlib.pyplot as plt
import numpy as np
import data_visualise
import table_display
import pandas as pd
import common



class UI(QMainWindow):
    def __init__(self , df , target, user_actions):
        super(UI, self).__init__()
        uic.loadUi('./ui_files/LinearRegression.ui', self)
        print(self)
        self.user_act = user_actions
        global data 
        data=data_visualise.data_()
        steps = common.common_steps(df , target)

        self.X , self.n_clases, self.target.value , self.df, self.column=  steps.return_data()
        self.df = df
        self.target = target
        print(self.df)
        print(self.target)
        


        self.show()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = UI()
    window.show()

    sys.exit(app.exec_())