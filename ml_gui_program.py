from PyQt5.QtWidgets import *
import sys,pickle
from PyQt5 import uic, QtWidgets ,QtCore, QtGui
from data_visualise import data_
from table_display import DataFrameModel
from add_steps import add_steps
# from linear_rg import print_success
import linear_rg

class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()
        uic.loadUi('mainwindow.ui', self)
        print(self)
        global data, steps
        data = data_()
        steps = add_steps()

        self.Browse = self.findChild(QPushButton , "Browse")
        self.columns = self.findChild(QListWidget , "column_list")
        self.table = self.findChild(QTableView , "tableView")
        self.data_shape = self.findChild(QLabel , "shape")
        self.label_2 = self.findChild(QLabel , "label_2")
        self.submit_btn = self.findChild(QPushButton , "Submit")
        self.target_col = self.findChild(QLabel , "target_col")
        self.cat_column = self.findChild(QComboBox , "cat_column")
        self.convert_btn = self.findChild(QPushButton , "convert_btn")
        self.dropcolumn = self.findChild(QComboBox , "dropcolumn")
        self.drop_btn = self.findChild(QPushButton , "drop")
        self.empty_column = self.findChild(QComboBox , "empty_column")
        self.fillmean = self.findChild(QPushButton , "fillmean")
        self.fillna = self.findChild(QPushButton , "fillna")
        self.scale_btn = self.findChild(QPushButton , "scale_btn")

        self.scatter_x = self.findChild(QComboBox , "scatter_x")
        self.scatter_y = self.findChild(QComboBox , "scatter_y")
        self.scatter_c = self.findChild(QComboBox , "scatter_c")
        self.scatter_marker = self.findChild(QComboBox , "scatter_mark")
        self.scatterplot_btn = self.findChild(QPushButton , "scatterplot")
    
        self.plot_x = self.findChild(QComboBox, "plot_x")
        self.plot_y = self.findChild(QComboBox, "plot_y")
        self.plot_btn = self.findChild(QPushButton, "plot")
        self.colour_2 = self.findChild(QComboBox, "plot_c")
        self.marker_2 = self.findChild(QComboBox, "plot_mark")

        self.train_btn = self.findChild(QPushButton , "train")

        self.Browse.clicked.connect(self.getCSV)
        self.columns.clicked.connect(self.target)
        self.submit_btn.clicked.connect(self.set_target)
        self.convert_btn.clicked.connect(self.con_cat)
        self.drop_btn.clicked.connect(self.dropc)
        self.fillmean.clicked.connect(self.fillme)
        self.fillna.clicked.connect(self.fill_na)
        self.scale_btn.clicked.connect(self.scale_value)

        self.scatterplot_btn.clicked.connect(self.scatter_plot)
        self.plot_btn.clicked.connect(self.line_plot)

        self.train_btn.clicked.connect(self.train_func)
    
    def train_func(self):
        myDict={"Linear Regression" :linear_rg, }

        if self.target_value !="":
            self.win=myDict[self.model_select.currentText()].UI(self.df , self.target_value, steps)

    def line_plot(self) :
        x=self.plot_x.currentText()
        y=self.plot_y.currentText()

        c=self.colour_2.currentText()
        marker= self.marker_2.currentText()
        data.scatter_plot(df=self.df,x=x,y=y,c=c,marker=marker )

    def scatter_plot(self):
        x=self.scatter_x.currentText()
        y=self.scatter_y.currentText()
        c=self.scatter_c.currentText()
        marker= self.scatter_marker.currentText()
        data.scatter_plot(df=self.df,x=x,y=y,c=c,marker=marker )

    def scale_value(self):
        if self.scaler.currentText() == 'StandardScale':
            self.df, func_name =  data.StandardScale(self.df, self.target_value)
        elif self.scaler.currentText() == 'MinMaxScal':
            self.df, func_name =  data.MinMaxScale(self.df, self.target_value)
        else:
            self.df, func_name =  data.PowerScale(self.df, self.target_value)

        steps.add_text(self.scaler.currentText()+" applied to data")
        steps.add_pipeline(self.scaler.currentText(),func_name)
        self.filldetails()

    def fillme(self):
        selected = self.df[self.empty_column.currentText()]
        type = self.df[self.empty_column.currentText()].dtype
        if type !='object':
            self.df[self.empty_column.currentText()] = data.fillmean(self.df, self.empty_column.currentText())
            self.filldetails()
            # print("not object")
        else:
            print("datatype is object ")
    

    def fill_na(self):
        self.df[self.empty_column.currentText()] = data.fillna(self.df, self.empty_column.currentText())
        self.filldetails()
        print("유후~~!")

    def filldetails(self ,flag = 1):
        if flag ==0:
            self.df = data.read_file(str(self.filePath))
        
        self.columns.clear()
        self.column_list = data.get_column_list(self.df)
        print(self.column_list)

        for i , j in enumerate(self.column_list):
            # print (i,j)
            stri = f'{j} ------ {str(self.df[j].dtype)}'
            # print(stri)
            self.columns.insertItem(i, stri)

        x , y  = data.get_shape(self.df)
        self.data_shape.setText(f'({x} ,{y})')
        self.fill_combo_box()
    
    def fill_combo_box(self):

        self.cat_column.clear()
        self.cat_column.addItems(self.column_list)
        self.dropcolumn.clear()
        self.dropcolumn.addItems(self.column_list)
        self.empty_column.clear()
        self.empty_column.addItems(self.column_list)

        self.scatter_x.clear()
        self.scatter_x.addItems(self.column_list)
        self.scatter_y.clear()
        self.scatter_y.addItems(self.column_list)
    
        self.plot_x.clear()
        self.plot_x.addItems(self.column_list)
        self.plot_y.clear()
        self.plot_y.addItems(self.column_list)

        x = DataFrameModel(self.df)
        self.table.setModel(x)
        



    def  getCSV(self):
        self.filePath , _ = QtWidgets.QFileDialog.getOpenFileName(self , "Open file", "" , "csv(*.csv)")
        self.columns.clear()
        # print(self.filePath)
        if self.filePath !="":
            self.filldetails(0)

    def target(self):
        self.item = self.columns.currentItem()

    def set_target(self):
        self.target_value = str(self.item.text()).split()[0]
        # print(self.target_value)
        steps.add_code(f"target=data[{self.target_value}]")
        self.target_col.setText(self.target_value)

        
    def con_cat(self):
        
        selected = self.cat_column.currentText()
        # print(selected)
        self.df[selected] , func_name = data.convert_category(self.df,selected)
        steps.add_text("Column "+ selected + " converted using LabelEncoder")
        steps.add_pipeline("LabelEncoder",func_name)
        self.filldetails()

    def dropc(self):
        selected = self.dropcolumn.currentText()
        self.df = data.drop_columns(self.df , selected)
        steps.add_code("data=data.drop('"+self.dropcolumn.currentText()+"',axis=1)")
        steps.add_text("Column "+ self.dropcolumn.currentText()+ " dropped")
        self.filldetails()
        

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = UI()
    window.show()

    app.exec_()