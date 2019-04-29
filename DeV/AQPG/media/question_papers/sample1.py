from tkinter import *
import sqlite3
root=Tk()
root.geometry('450x450')
root.title("database using sqlite and Tkinter")
root.configure(background="powder blue")

textin = StringVar()
textinn = StringVar()

menu = Menu(root)
root.config(menu=menu)
def helpp():
     help(sqlite3)

subm = Menu(menu)
menu.add_cascade(label="help",menu=subm)
subm.add_command(label="sqlite3 docs",command=helpp)



db  = sqlite3.connect('sql.db')
cursor = db.cursor()
#cursor.execute("create table  peopl(name text, phone text)")
db.commit()

lab = Label(root,text='name:',font=('none 13 bold'))
lab.place(x=0,y=0)


entname=Entry(root,width=20,font=('none 13 bold'),textvar=textin)
entname.place(x=80,y=0)

entphone=Entry(root,width=20,font=('none 13 bold'),textvar=textinn)
entphone.place(x=80,y=40)

lab1 = Label(root,text='phone:',font=('none 13 bold'))
lab1.place(x=0,y=40)



def insert():
    
    name1 = textin.get()
    phone1 = textinn.get()
    conn = sqlite3.connect('sql.db')
    with conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO peopl(name,phone)VALUES (?,?)')
        db.close()
     #print "hlooo"
def show():

    connt = sqlite3.connect('sql.db')
    cursor = connt.cursor()
    cursor.excute('select * from peopl')
    for row in cursor.fetchall():
        print(row)


name=StringVar()
phone=StringVar()
def updatecontact():
    nam=name.get()
    ph=phone.get()

    connnt=sqlite3.connect('sql.db')
    cursor = connnt.cursor()
    cursor.execute("update peopl set name=? where phone=?",(nam,ph))
    connnt.commit()




dell = StringVar()
def det():
    dee = dell.get()
    connnt = sqlite3.connect('sql.db')
    cursor = connnt.cursor()
    cursor.execute('delete from peopl where name=?',(nam,ph))

def drop():
    connnt=sqlite3.connect('sql.db')
    cursor = connnt.cursor()
    cursor.execute("drop table people")
    connnt.commit()



buttdrop=Button(root,padx=2,pady=2,text='drop table',command=drop,font=('none 13 bold'))
buttdrop.place(x=180,y=380)

buttupdate=Button(root,padx=2,pady=2,text='update',command=updatecontact,font=('none 13 bold'))
buttupdate.place(x=80,y=280)

labuname=Label(root,text='Update Name',font=('none 13 bold'))
labuname.place(x=0,y=200)

enttupadtename=Entry(root,width=20,font=('none 13 bold'),textvar = name)
enttupadtename.place(x=160,y=200)


labuphone=Label(root,text='Provide Phone no.',font=('none 13 bold'))
labuphone.place(x=0,y=240)


enttupadtename=Entry(root,width=20,font=('none 13 bold'),textvar = phone)
enttupadtename.place(x=210,y=240)

labdelet=Label(root,text='delet',font=('none 13 bold'))
labdelet.place(x=0,y=340)

endelet=Entry(root,width=20,font=('none 13 bold'),textvar = dell)
endelet.place(x=90,y=340)


butdel=Button(root,padx=2,pady=2,text='delet',command=det,font=('none 13 bold'))
butdel.place(x=90,y=380)
    

but=Button(root,padx=2,pady=2,text='submit',command=insert,font=('none 13 bold'))
but.place(x=60,y=100)

res=Button(root,padx=2,pady=2,text='show',command=show,font=('none 13 bold'))
res.place(x=160,y=100)

        
root.mainloop()



