import mysql.connector as mc
from PyQt6 import QtWidgets
def view(name_table,tableWidget):
    try:
        mydb = mc.connect(host="localhost", user="root", password="", database="library_system")
        mycursor = mydb.cursor()
        mycursor.execute(f"SELECT * FROM {name_table}")
        data = mycursor.fetchall()
            
        tableWidget.setRowCount(0)
        for row_index,row_data in enumerate(data):
            tableWidget.insertRow(row_index)
            for col_index,col_data in enumerate(row_data):
                 tableWidget.setItem(row_index,col_index,QtWidgets.QTableWidgetItem(str(col_data)))
    except mc.Error as err:
           print(err)    