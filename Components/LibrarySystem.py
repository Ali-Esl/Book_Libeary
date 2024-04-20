from PyQt6.QtCore import Qt 
from UI.MainUI import Ui_MainWindow
from UI.ViewAddBook import Ui_ViewAddBook
from UI.ViewAddMember import Ui_ViewAddMember
from PyQt6.QtWidgets import QMainWindow, QWidget,QDialog,QMessageBox,QTableWidgetItem
from mysql import connector as mc

class LibrarySystem(QMainWindow, Ui_MainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)
        self.show()
        self.AddBook_toolButton.clicked.connect(self.view_book)
        self.AddMember_toolButton.clicked.connect(self.view_member)
        
        
        self.Issue_BookID_lineEdit.returnPressed.connect(self.book_id)
        self.Issue_MemberID_lineEdit_2.returnPressed.connect(self.member_id)
        self.IssueBook_toolButton.clicked.connect(self.issue_book)
        
        self.RenewBookID_lineEdit.returnPressed.connect(self.load_issue)
        self.RenewBook_toolButton.clicked.connect(self.renew_book)
        self.SubmitBook_toolButton.clicked.connect(self.delete_issue)
        self.RenewBook_toolButton.clicked.connect(self.load_issue)
        self.SubmitBook_toolButton.clicked.connect(self.load_issue)

    def view_book(self):
        dialog = QDialog()
        dialog_ui = Ui_ViewAddBook()
        dialog_ui.setupUi(dialog)
        dialog.exec()
    
    def view_member(self):
        dialog = QDialog()
        dialog_ui = Ui_ViewAddMember()
        dialog_ui.setupUi(dialog)
        dialog.exec()
    
    def book_id(self):
        id = self.Issue_BookID_lineEdit.text()
        try:
            mydb = mc.connect(host="localhost",user="root",password="",database="library_system")
            mycursor = mydb.cursor()
            query = f"SELECT * FROM addbook WHERE id='{id}'"
            mycursor.execute(query)
            result = mycursor.fetchone()
            if result != None:
                self.Issue_bookName_label.setText("Book Name: " + result[1])        
                self.Issue_BookAuthor_label.setText("Book Author: " + result[2])        
        except mc.Error as err:
            print("An error occurred! "+err)
    
    def member_id(self):
        id = self.Issue_MemberID_lineEdit_2.text()
        try:
            mydb = mc.connect(host="localhost",user="root",password="",database="library_system")
            mycursor = mydb.cursor()
            query = f"SELECT * FROM addmember WHERE id='{id}'"
            mycursor.execute(query)
            result = mycursor.fetchone()
            if result != None:
                self.Issue_MemberName_label_2.setText("Member Name: " + result[1])        
                self.Issue_ContactInfo_label.setText("Member Email: " + result[3])        
        except mc.Error as err:
            print("An error occurred! "+err)
        
    def issue_book(self):
        b_id = self.Issue_BookID_lineEdit.text()
        m_id = self.Issue_MemberID_lineEdit_2.text()
        try:
            if b_id != "":
                if m_id != "":
                    mydb = mc.connect(host="localhost",user="root",password="",database="library_system")
                    mycursor = mydb.cursor()
                    query = "INSERT INTO issue (bookID,memberID) VALUES (%s,%s)"
                    query2 = f"UPDATE addbook SET isAvailable=FALSE WHERE id='{b_id}'"
                    values = (b_id,m_id)
                    mycursor.execute(query,values)
                    mycursor.execute(query2)
                    mydb.commit()
                    QMessageBox.about(self,"Issue Book", "Book Issued Successfully")
                else:
                    self.Issue_MemberID_lineEdit_2.setFocus() 
            else:
                self.Issue_BookID_lineEdit.setFocus() 

        except mc.Error as err:
            print("Error occured! " + err)
            
    def load_issue(self):
        issue_id = self.RenewBookID_lineEdit.text()
        try:
            mydb = mc.connect(host="localhost",user="root",password="",database="library_system")
            mycursor = mydb.cursor()
            if issue_id.rstrip() == "":
                return None
            mycursor.execute(f"SELECT * FROM issue WHERE bookID='{issue_id}'")
            result = mycursor.fetchall()
            self.tableWidget.setRowCount(0)
            for row_number,row_data in enumerate(result):
                self.tableWidget.insertRow(row_number)
                for column_number,data in enumerate(row_data):
                    self.tableWidget.setItem(row_number,column_number,QTableWidgetItem(str(data)))
            
        except mc.Error as err:
            print(f"Error occured! {err}")
    
    def renew_book(self):
        issue_id = self.RenewBookID_lineEdit.text()
        try:
            mydb = mc.connect(host="localhost",user="root",password="",database="library_system")
            mycursor = mydb.cursor()
            if issue_id.rstrip() == "":
                return None
            select1 = mycursor.execute(f"UPDATE issue SET renewCount = renewCount+1 WHERE bookId='{issue_id}'")
            mydb.commit()
        except mc.Error as err:
            print(f"Error occured! {err}")

    def delete_issue(self):
        issue_id = self.RenewBookID_lineEdit.text()
        try:
            mydb = mc.connect(host="localhost",user="root",password="",database="library_system")
            mycursor = mydb.cursor()
            if issue_id.rstrip() == "":
                return None
            mycursor.execute(f"DELETE  FROM issue WHERE bookId='{issue_id}'")
            mycursor.execute(f"UPDATE addbook Set isAvailable=TRUE WHERE id='{issue_id}'")
            mydb.commit()
        except mc.Error as err:
            print(f"Error occured! {err}")