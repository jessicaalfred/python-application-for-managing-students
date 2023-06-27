from tkinter import *
from tkinter.messagebox import *
from tkinter.scrolledtext import *
import matplotlib.pyplot as plt
import socket
import requests
from sqlite3 import *
import bs4
import lxml
    
# Add button
def f1():
	root.withdraw()
	add_st.deiconify()

# View button
def f2():
	view_stData.delete(1.0, END)
	root.withdraw()
	view_st.deiconify()
	con = None
	try:
		con = connect("stu_test.db")
		cursor = con.cursor()
		sql = "select * from student"
		cursor.execute(sql)
		data = cursor.fetchall()
		info = ""
		for d in data:
			info = info + "rno: " + str(d[0]) + "   name: "+str(d[1]) + "     marks: "+ str(d[2]) +"\n"
		view_stData.insert(INSERT, info)
	except Exception as e:
		print("Issue: ",e)
	finally:
		if con is not None:
			con.close()	

# Back from Add
def f3():
	add_st.withdraw()
	root.deiconify()
	
# Back from view
def f4():
	view_st.withdraw()
	root.deiconify()

# Update button
def f5():
	root.withdraw()
	updt_st.deiconify()

# Back from Update
def f6():
	updt_st.withdraw()
	root.deiconify()

# Delete button
def f7():
	root.withdraw()
	del_st.deiconify()

# Back from Delete
def f8():
	del_st.withdraw()
	root.deiconify()

#Charts for 5* 
def f9():
	con = None
	student, marks = [],[]
	try:
		con = connect("stu_test.db")
		cursor = con.cursor()
		sql = "SELECT * FROM student ORDER BY marks LIMIT 5"
		data = cursor.execute(sql)
		for d in data:
			student.append(d[1])
			marks.append(int(d[2]))
		plt.bar(student, marks)
		plt.ylabel('Marks')
		plt.title("Batch Information")
		plt.grid()
		plt.show()
	except Exception as e:
		showerror("Issue", e)
	finally:
		if con is not None:
			con.close()


# Add-insert
def f10():
	con = None
	try:
		con = connect("stu_test.db")
		cursor = con.cursor()
		if rnoEnter.get() == '':
			raise Exception("No Roll No Entered!")
		if not rnoEnter.get().isdigit():
			rnoEnter.delete(0, END)
			raise Exception("Only Digits accepted")
		rno, name= int(rnoEnter.get()), nameEnter.get()
		if rno < 1:
			rnoEnter.delete(0, END)
			raise Exception("Roll number should be Positive")
		if len(name) < 2:
			nameEnter.delete(0, END)
			raise Exception("Length of name too small")
		if nameEnter.get().isdigit():
			nameEnter.delete(0, END)
			raise Exception("digits not accepted in name")
		if marksEnter.get() == '':
			raise Exception("Please Enter Marks ")
		if not marksEnter.get().isdigit():
			marksEnter.delete(0, END)
			raise Exception("Only digits accepted")
		marks = int(marksEnter.get())
		if marks < 0 or marks > 100:
			marksEnter.delete(0, END)
			raise Exception("Marks out of range")
		args = (rno, name, marks)
		sql = "insert into student values ('%d', '%s', '%d')"
		cursor.execute(sql % args)
		con.commit()
		showinfo("Success",str(rno) + " Record added")
		rnoEnter.delete(0, END)
		marksEnter.delete(0, END)
		nameEnter.delete(0, END)
	except Exception as e:
		con.rollback()
		showerror("Issue: ",e)
	finally:
		if con is not None:
			con.close()

# Update
def f11():
	con = None
	args = ()
	try:
		con = connect("stu_test.db")
		cursor = con.cursor()
		sql, args  = '', ()
		if urnoEnter.get() == '':
			raise Exception("No Roll No Entered!")
		if not urnoEnter.get().isdigit():
			urnoEnter.delete(0, END)
			raise Exception("Only Digits accepted")
		rno = int(urnoEnter.get())
		if rno < 1:
			urnoEnter.delete(0, END)
			raise Exception("Roll number should be Positive")
		if unameEnter.get() != '' and umarksEnter.get() != '':
			if len(unameEnter.get()) < 2:
				unameEnter.delete(0, END)
				raise Exception("Length of name too small")
			if unameEnter.get().isdigit():
				unameEnter.delete(0, END)
				raise Exception("digits not accepted in name")
			if not umarksEnter.get().isdigit():
				umarksEnter.delete(0, END)
				raise Exception("Only digits accepted")
			marks = int(umarksEnter.get())
			if marks < 0 or marks > 100:
				umarksEnter.delete(0, END)
				raise Exception("Please Enter Valid Marks ")
			name = unameEnter.get()
			args = (name, marks, rno)
			sql = "UPDATE student SET name = '%s', marks = '%d' WHERE rno = '%d'"
		elif unameEnter.get() != '' and umarksEnter.get() == '':
			if len(unameEnter.get()) < 2:
				unameEnter.delete(0, END)
				raise Exception("Length of name should not be less than 2")
			name = unameEnter.get()
			args =  (name, rno)
			sql = "UPDATE student SET name = '%s' WHERE rno = '%d'"
		elif unameEnter.get() == '' and umarksEnter.get() != '':
			if not umarksEnter.get().isdigit():
				umarksEnter.delete(0, END)
				raise Exception("Marks should be digits only")
			marks = int(umarksEnter.get())
			if marks < 0 or marks > 100:
				umarksEnter.delete(0, END)
				raise Exception("Marks out of range")
			args = (marks, rno)
			sql = "UPDATE student SET marks = '%d' WHERE rno = '%d'"
		else:
			raise Exception("Enter the values to be updated")
		cursor.execute(sql % args)
		if cursor.rowcount == 0:
			raise Exception(str(rno) + " not found")
		con.commit()
		showinfo("Success ",str(rno) + " Record updated")
		urnoEnter.delete(0, END)
		umarksEnter.delete(0, END)
		unameEnter.delete(0, END)
	except Exception as e:
		con.rollback()
		showerror("Issue: ",e)
	finally:
		if con is not None:
			con.close()
# Delete
def f12():
	con = None
	try:
		con = connect("stu_test.db")
		cursor = con.cursor()
		if drnoEnter.get() == '':
			raise Exception('Roll number cannot be empty')
		if not drnoEnter.get().isdigit():
			raise Exception("Roll number should be digits only")
		rno = int(drnoEnter.get())
		if rno < 1:
			raise Exception('Roll number cannot be 0 or negative')
		args = (rno)
		sql = "delete from student where rno = '%d'"
		cursor.execute(sql % args)
		if cursor.rowcount == 0:
			raise Exception(str(rno) + " not found")
		con.commit()
		showinfo("Success",str(rno) + " deleted successfully")
	except Exception as e:
		con.rollback()
		showerror("Issue", e)
	finally:
		if con is not None:
			con.close()
		drnoEnter.delete(0, END)

# Message filter
def alter(msg):
	if msg.find(',') != -1 or msg.find(';') != -1:
		motd = msg.replace(',' , '\n')
		motd = msg.replace(';' , '\n')
	else:
		motd, i, j = '', 0, 0
		mesappend = ''
		val = msg.rfind('-')
		partone = msg[0:val]
		parttwo = msg[val:]
		for k in partone:
			if k  == ' ' and j % 6 == 0:
				mesappend = mesappend + k + '\n'
				j += 1
			elif k == ' ':
				mesappend = mesappend + k
				j += 1
			else:
				mesappend = mesappend + k
		motd = mesappend + '\n' + parttwo
	return motd
    
# Location-Temperature-Quote
info, qotd = '',''
try:
	socket.create_connection(("www.google.com", 80))
	res = requests.get("https://ipinfo.io")
	data = res.json()
	city_name = data['city']
	a1 = "http://api.openweathermap.org/data/2.5/weather?units=metric"
	a2 = "&q=" + city_name 
	a3 = "&appid=c6e315d09197cec231495138183954bd"
	res = requests.get(a1 + a2 + a3)
	data = res.json()
	temp = data['main']['temp']
	info = "Location: " + str(city_name) + "\tTemperature: " + str(temp)
	res = requests.get("https://www.brainyquote.com/quote_of_the_day")
	soup = bs4.BeautifulSoup(res.text,'lxml')
	data = soup.find("img", {"class": "p-qotd"})
	msg = data['alt']
	msg = alter(msg)
	qotd = "QOTD: " + str(msg)
except Exception as e:
	showerror("Connection issue",e)
	print(e)


#S.M.S
root = Tk()
root.title("Student Management System")
root.geometry("508x575+400+25")
root.configure(background = "#800080")

btnAdd = Button(root, text="Add", font = ("Arial", 18, "bold"), width = 10,command = f1)
btnView = Button(root, text="View", font = ("Arial", 18, "bold"), width = 10,command = f2)
btnUpdate = Button(root, text="Update", font = ("Arial", 18, "bold"), width = 10, command = f5)
btnDelete = Button(root, text="Delete", font = ("Arial", 18, "bold"), width = 10, command = f7)
btnCharts = Button(root, text="Charts", font = ("Arial", 18, "bold"), width = 10, command = f9)
lblInfo = Label(root, text = info, font = ('Arial', 18, 'bold'), borderwidth = 1, bg = "#800080", relief = "solid")
lblQotd = Label(root, text = qotd, font = ('Arial', 18, 'bold'), borderwidth = 1, bg = "#800080", relief = "solid")

btnAdd.pack(pady = 10)
btnView.pack(pady = 10)
btnUpdate.pack(pady = 10)
btnDelete.pack(pady = 10)
btnCharts.pack(pady = 10)
lblInfo.pack(pady = 10)
lblQotd.pack(pady = 10)

#Add St.
add_st = Toplevel(root)
add_st.title("Add student")
add_st.geometry("500x500+400+100")
add_st.configure(background="#FF00FF")
add_st.withdraw()

lblrno = Label(add_st, text = "enter rno:", font = ('Arial', 18, 'bold'), bg = "#FF00FF")
rnoEnter = Entry(add_st, bd = 5 ,font = ('Arial', 18, 'bold'))
lblname = Label(add_st, text = "enter name:", font = ('Arial', 18, 'bold'), bg = "#FF00FF")
nameEnter = Entry(add_st, bd = 5 ,font = ('Arial', 18, 'bold'))
lblmarks = Label(add_st, text = "enter marks:", font = ('Arial', 18, 'bold'), bg = "#FF00FF")
marksEnter = Entry(add_st, bd = 5 ,font = ('Arial', 18, 'bold'))
add_stSave = Button(add_st, text="Save", font = ("arial", 18, "bold"), command = f10)
add_stBack = Button(add_st, text="Back", font = ("arial", 18, "bold"), command = f3)

lblrno.pack(pady = 10)
rnoEnter.pack(pady = 10)
lblname.pack(pady = 10)
nameEnter.pack(pady = 10)
lblmarks.pack(pady = 10)
marksEnter.pack(pady = 10)
add_stSave.pack(pady = 10)
add_stBack.pack(pady = 10)
rnoEnter.focus()

#View St.
view_st = Toplevel(root)
view_st.title("View student")
view_st.geometry("500x500+400+100")
view_st.withdraw()
view_st.configure(background = "#E6E6FA")
view_stData = ScrolledText(view_st, width = 40, height = 20)
view_stBack = Button(view_st, text = "Back", font= ("arial", 18, "bold"), command = f4)
view_stData.pack(pady = 10)
view_stBack.pack(pady = 10)

#Update St.
updt_st = Toplevel(root)
updt_st.title("Update Student")
updt_st.geometry("500x500+400+100")
updt_st.withdraw()
updt_st.configure(background="#9370DB")
updt_st.withdraw()

ulblrno = Label(updt_st, text = "enter rno:", font = ('Arial', 18, 'bold'), bg = "#9370DB")
urnoEnter = Entry(updt_st, bd = 5 ,font = ('Arial', 18, 'bold'))
ulblname = Label(updt_st, text = "enter name:", font = ('Arial', 18, 'bold'), bg = "#9370DB")
unameEnter = Entry(updt_st, bd = 5 ,font = ('Arial', 18, 'bold'))
ulblmarks = Label(updt_st, text = "enter marks:", font = ('Arial', 18, 'bold'), bg = "#9370DB")
umarksEnter = Entry(updt_st, bd = 5 ,font = ('Arial', 18, 'bold'))
uadd_stSave = Button(updt_st, text="Update", font = ("arial", 18, "bold"), command = f11)
uadd_stBack = Button(updt_st, text="Back", font = ("arial", 18, "bold"), command = f6)

ulblrno.pack(pady = 10)
urnoEnter.pack(pady = 10)
ulblname.pack(pady = 10)
unameEnter.pack(pady = 10)
ulblmarks.pack(pady = 10)
umarksEnter.pack(pady = 10)
uadd_stSave.pack(pady = 10)
uadd_stBack.pack(pady = 10)
urnoEnter.focus()

#Delete St
del_st = Toplevel(root)
del_st.title("Delete Student")
del_st.geometry("500x500+400+100")
del_st.withdraw()
del_st.configure(background = "#FF00FF")

dlblrno = Label(del_st, text="enter rno:", font = ('Arial', 18, 'bold'), bg="#FF00FF")
drnoEnter = Entry(del_st, font = ('Arial', 18, 'bold'), bd = 5)
del_stSave = Button(del_st, text = "Delete" ,font = ('Arial', 18, 'bold'), command = f12)
del_stBack = Button(del_st, text = "Back", font = ('Arial', 18, 'bold'), command = f8)
dlblrno.pack(pady = 10)
drnoEnter.pack(pady = 10)
del_stSave.pack(pady = 10)
del_stBack.pack(pady = 10)
drnoEnter.focus()

root.mainloop()