import mysql.connector as sql
connection = sql.connect(host='localhost', user='root', password='waybig10', database='project')
print(connection)
cursor = connection.cursor()
'''cursor.execute('create table report (Admission_No int PRIMARY KEY AUTO_INCREMENT ,Patient_Name char(50) NOT NULL,'
               'gender ENUM("M","F","O") NOT NULL, Age int NOT NULL, Symptoms char(255),'
                'Date_of_Admission date NOT NULL, Date_of_Discharge date ,'                                
                'Currently ENUM("Deceased", "Healthy", "Under_Medication"), Total_Payment int);')'''


all_fields = ['Admission_No','Patient_name', 'Gender', 'Age', 'Symptoms', 'Date_of_admission', 'Date_of_discharge', 'Currently',
          'Total_payment']
fields = ['Patient_name', 'Gender', 'Age', 'Symptoms', 'Date_of_admission', 'Date_of_discharge', 'Currently',
          'Total_payment']


def add_entry():

    query = 'insert into report(Patient_Name,Gender,Age,Symptoms,Date_of_Admission,Date_of_Discharge, ' \
            'Currently, Total_Payment) values (%s,%s,%s,%s,%s,%s,%s,%s);'

    val =[]

    sp_fields = ['Age','Total_payment']
    for i in fields:
        if i in sp_fields:
            while True:
                try:
                    j = int(input(f'Enter {i} : '))
                    val.append(j)
                    break
                except ValueError:
                    print('try again')
            continue
        sp_fields2 = ['Date_of_admission', 'Date_of_discharge']
        if i in sp_fields2:
            while True:
                try:
                    d = int(input(f'Enter day of {i[8:]} : '))
                    m = int(input(f'Enter the month of {i[8:]} : '))
                    y = int(input(f'Enter the year of {i[8:]}: '))
                    d, m, y = str(d), str(m), str(y)
                    if int(d) // 10 == 0:
                        d = '0' + str(d)
                    if int(m) // 10 == 0:
                        m = '0' + str(m)

                    j = y + '-' + m + '-' + d
                    val.append(j)
                    break
                except ValueError:
                    print('try again')
            continue
        sp_fields3 = ['Gender', 'Currently']
        if i in sp_fields3:
            key = ['M', 'F', 'O', 'Deceased', 'Healthy', 'Under_medication']
            while True:
                try:
                    j = input(f'Enter {i} : ')
                    j = j.capitalize()
                    if j in key:
                        val.append(j)
                        break
                    else:
                        print("Please privide a valid input.Try again")
                        continue
                except ValueError:
                    print('try again')
            continue
        else:
            while True:
                try:
                    j = input(f'Enter {i} : ')
                    val.append(j)
                    break
                except ValueError:
                    print('try again')

    val = tuple(val)
    cursor.execute(query, val)
    val =  list(val)
    val.clear()
    connection.commit()

def display_table():
    query = 'select * from report'
    cursor.execute(query)
    data = cursor.fetchall()
    print('Fields-->', end='\t')
    for k in all_fields:
        print(k,end=' | ')
    print()
    for i, r in zip(data, range(1,len(data)+1)):
        print(r,'Data-->', sep=':\t',end='\t\t')
        for j in i:
            print(j, end='\t|\t')
        print()
    return data
def delete_row():
    
    global index, field_name, record_data
    all_fields = ['Admission_No', 'Patient_name', 'Gender', 'Age', 'Symptoms', 'Date_of_admission', 'Date_of_discharge',
                  'Currently',
                  'Total_payment']
    data = display_table()
    while True:
        try:
            index = int(input("Enter the index of the row you wish to delete :"))
            if index in range(1, len(data)+1):
                index -= 1
                break
            else:
                continue
        except ValueError:
            print('try again')

    field_name = all_fields[0]
    record_data = data[index][0]
    query = f'delete from report where {field_name} like "%{record_data}%"'
    cursor.execute(query)
    connection.commit()

def modify_row():
    global record_ref, field_ref
    while True:
        list = all_fields.copy()
        try:
            l = ''
            n = int(input('Enter number of fields to be modified: '))

            while n != 0:
                for i in range(len(list)):
                    print(i+1,'.)',list[i],sep='')

                index = int(input('Enter field index to modify :')) - 1
                if index in range(len(list)):
                    field_name = list[index]
                    if field_name not in l:
                        if field_name in all_fields:
                            record_data = input(f'Enter the new data: ')
                            l_cap = f',{field_name}="{record_data}"'
                            l += l_cap
                            n-=1
                            list.remove(field_name)
                        else:
                            continue
                else:
                    continue

            for i in range(len(all_fields)):
                print(i + 1, '.)', all_fields[i],sep='')

            index_ref = int(input('Enter the index of the field of reference to modify :')) - 1
            if index_ref in range(len(list)):
                field_ref = all_fields[index_ref]
                if field_ref in fields:
                    record_ref = input(f'Enter the reference data in the field {field_ref} you wish to modify: ')
                    break
                else:
                    continue
            else:
                continue
        except ValueError:
            print('try again')
    cursor.execute(f'update report set {l[1:]} where {field_ref}="{record_ref}" ')
    connection.commit()

def search_by_specific_fields():
    global field , val
    fields = ['Admission_no','Patient_name', 'Gender', 'Age', 'Symptoms', 'Date_of_admission', 'Date_of_discharge', 'Currently',
              'Total_payment']
    sp_fields = ['Admission_no', 'Age', 'Total_payment']
    sp_fields2 = [ 'Date_of_admission', 'Date_of_discharge']
    sp_fields3 = ['Gender', 'Currently']

    while True:
        try:
            list = all_fields.copy()
            l = ''
            dum_f =[]
            n = int(input('Enter number of fields to be searched: '))
            while n != 0:
                for i in range(len(list)):
                    print(i + 1, '.)', list[i], sep='')

                index = int(input("Enter the index for field to be searched: ")) - 1
                if index in range(len(list)):
                    field_name = list[index]
                    if field_name not in l:
                        l = l + f', {field_name}'
                        dum_f.append(field_name)
                        n-=1
                        list.remove(field_name)
                    else:
                        continue
                else:
                    print('index out of range')
                    continue

            for i in range(len(all_fields)):
                print(i + 1, '.)', all_fields[i],sep='')

            index_ref = int(input("Enter the index for field of reference: "))-1
            if index_ref in range(len(list)):
                field = all_fields[index_ref]
                if field in fields:
                    if field in sp_fields:
                        val = int(input(f'Enter the reference value from the field {field}: '))
                    elif field in sp_fields2:
                        val = input(f'Enter the reference value from the field {field}: ')
                    elif field in sp_fields3:
                        val = input(f'Enter the reference value from the field {field} : ')
                        val = val.capitalize()
                        key = ['M', 'F', 'O', 'Deceased', 'Healthy', 'Under_medication']
                        if val not in key:
                            print('try again')
                            continue
                    else:
                        val = input(f'Enter the reference value from the field {field}: ')
                    break
            else:
                print('index out of range')
                continue
        except ValueError:
            print('try again')
    cursor.execute(f"select {l[1:]} from report where {field} like '%{val}%'")
    data = cursor.fetchall()

    for i in data:
        for l in range(len(dum_f)):
            print(dum_f[l], ': ', i[l])
        print()

def search_by():
    global field, val
    fields = ['Admission_no', 'Patient_name', 'Gender', 'Age', 'Symptoms', 'Date_of_admission', 'Date_of_discharge',
              'Currently','Total_payment']
    sp_fields = ['Admission_no', 'Age', 'Total_payment']
    sp_fields2 = ['Date_of_admission', 'Date_of_discharge']
    sp_fields3 = ['Gender', 'Currently']

    while True:
        try:
            print('Sub Menu')
            for i in range(len(all_fields)):
                print(i + 1, '.)', all_fields[i],sep='')

            index = int(input("Enter the index for field to be searched: "))-1
            if index in range(len(fields)):
                field = fields[index]
                if field in fields:
                    if field in sp_fields:
                        val = int(input(f'Enter the value from the field {field} to be searched by: '))
                    elif field in sp_fields2:
                        val = input(f'Enter the value from the field {field} to be searched by: ')
                    elif field in sp_fields3:
                        val = input(f'Enter the value from the field {field} to be searched by: ')
                        key = ['M', 'F', 'O', 'Deceased', 'Healthy', 'Under_medication']
                        val = val.capitalize()
                        if val not in key:
                            print('try again')
                            continue
                    else:
                        val = input(f'Enter the value from the field {field} to be searched by: ')
                    break
            else:
                print('index out of range')
                continue
        except ValueError:
            print('try again')

    cursor.execute(f"select * from report where {field} like '%{val}%'")
    data = cursor.fetchall()
    for i in data:
        for l in range(len(fields)):
            print(fields[l], ': ', i[l])
        print()

print('COVID REPORT')
ch=0
while ch != 7:

    print('1.Add: helps you to add a single row into the table', '2.Delete: helps you to delete a row in a table',
          '3.Modify: helps you to modify a certain number of fields in a specific row',
          '4.Display Table: displays the entire table','5.Search by: displays all the contents in the row you are searching for',
          '6.Search By Specific Fields: displays specific fields that you specify you want to search from a row ',
          '7.Exit', sep='\n')
    ch = int(input("Enter your choice: "))
    if ch == 1:
        add_entry()
    elif ch==2:
        delete_row()
    elif ch==3:
        modify_row()
    elif ch==4:
        display_table()
    elif ch==5:
        search_by()
    elif ch==6:
        search_by_specific_fields()
    elif ch==7:
        print('its sad to see you leave. we hope to see you again later.')
        break
    else:
        continue
