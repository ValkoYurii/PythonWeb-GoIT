import pickle
import os
import re
import time
from datetime import date, datetime, timedelta
from abc import ABC, abstractmethod

UI = '''
1. Add new contact
2. View contacts
3. Search contact
4. Update contact
5. Delete contact
6. Find contacts with N days to birthday
7. Reset all
8. Clean screen
9. Exit

P.s. Extra function 'Sort files'>>> Don't use it if you not sure!!!
'''

CBUI = '''
"add rec" >>> Add new record
"view rec" >>> View records
"s rec" >>> Search record
"upd" >>> Update record
"del" >>> Delete record
"reset" >>> Reset all
'''

class Str_export(ABC):
    
    @abstractmethod
    def strview(self):
        pass
    

class Clipboard(Str_export):
   
    def __init__(self, rdate=None, record=None, tag=None):
        self.rdate = rdate
        self.record = record
        self.tag = tag

    def strview(self):
        return ("{} {:<30} {}").format(self.rdate, self.record, self.tag)
    
    def __str__(self):
        return Clipboard.strview()
                       
class Person(Str_export):

    def __init__(self, name=None, address=None, phone=None, email=None,  birthday=None):
        self.name = name
        self.address = address
        self.phone = phone
        self.email = email
        self.birthday = birthday
    
    def strview(self):
        return "{:<20} {:<20} {:<15} {:<15} {}".format(self.name, self.address, self.phone, self.email, self.birthday)

    def __str__(self):
        return Person.strview()

class ClipboardAPP(object):
    def __init__(self, database2):
        self.database2 = database2
        self.records = {}
        if not os.path.exists(self.database2):
            file_pointer2 = open(self.database2, 'wb')
            pickle.dump({}, file_pointer2)
            file_pointer2.close()
        else:
            with open(self.database2, 'rb') as record_list:
                self.records = pickle.load(record_list)
    
  
    def getdata(self):
        record = input("Input your note: ")
        tag = input("Input your tag: ")
        rdate = datetime.now().date()
        return rdate, record, tag

   
    def add_cb(self):
        counter = len(self.records)+1
        rdate, record, tag = self.getdata()
        self.records[counter] = Clipboard(rdate, record, tag)
        print('Record stored!')

  
    def view_cb(self):
        if self.records:
            print("{:<5} {:<10} {:<30}".format("№", "date", "record"))
            print('--------------------------------------------------------------------------------------------------------------')
            counter_rec = 1
            for record in self.records.values(): 
                print(counter_rec,'.',record.rdate, '|', record.record, '|', 'TAGS:', record.tag )
                print('--------------------------------------------------------------------------------------------------------------')
                counter_rec+=1
        else:
            print("No records in database.")

       
    def search__cb(self):
        counter = 0
        s_record = input('Input what to find: ')
        for i in self.records.values():
            if s_record in str(i):
                print(i)
                counter+=1
        if counter == 0:
            print("Not found.")
        counter = 0
        
    def update_cb(self):
        ind_to_upd = int(input("Enter # of the record: "))
        if ind_to_upd in self.records:
            print("Found. Enter new details.")
            rdata, record, tag = self.getdata()
            self.records[ind_to_upd].__init__(rdata, record, tag)
            print("Successfully updated.")
        else:
            print("Record not found.")

    def delete_cb(self):
        ind_to_del = int(input("Enter the name to delete: "))
        if ind_to_del in self.records:
            del self.records[ind_to_del]
            print("Record deleted")
        else:
            print("Record not found in the app.")
    def reset_cb(self):
        self.records = {}

    def exit_cb(self):
        return UI

    def enter_cb(self):
        return CBUI
    def __del__(self):
        with open(self.database2, 'wb') as db:
            pickle.dump(self.records, db)
        
    def __str__(self):
        return CBUI

class Application(object):

    def __init__(self, database):
        self.database = database
        self.persons = {}
        if not os.path.exists(self.database):
            file_pointer = open(self.database, 'wb')
            pickle.dump({}, file_pointer)
            file_pointer.close()
        else:
            with open(self.database, 'rb') as person_list:
                self.persons = pickle.load(person_list)

    def add(self):
        name, address, phone, email, birthday = self.getdetails()
        if name not in self.persons:
            self.persons[name] = Person(name, address, phone, email, birthday)
        else:
            print("Contact already present.")

    def viewall(self):
        if self.persons:
            print("{:<25} {:<25} {:<20} {:<20} {}".format('Name', 'Address', 'Phone', 'Email', 'Birthday'))
            print('--------------------------------------------------------------------------------------------------------------')
            for person in self.persons.values():
                print("{:<20} {} {:<20} {} {:<20} {} {:<20} {}{}".format(person.name, '|', person.address, '|', person.phone, '|', person.email, '|', person.birthday))
                print('--------------------------------------------------------------------------------------------------------------')
        else:
            print("No contacts in database.")

    def search(self):
        name = input("Enter the name: ")
        name = name.title()
        
        if name in self.persons:
            print('---------------------------------------------------------------------------------------')
            print(self.persons[name])
            print('---------------------------------------------------------------------------------------')
        else:
            print("Contact not found.")

    def getdetails(self):
        #ім'я не може бути пустою стрічкою
        name = ""
        while name == "":
            name = input("Name: ")

        # адреса не проходить валідацію
        address = input("Address: ")

        #перевірка телефону і приведення його до одного типу запису
        phone = None
        while phone == None or "no phone":
            phone = input("Phone or 'no phone':")
            if phone == "no phone": break
            phone = str(phone.strip()
            .removeprefix("+")
            .replace("(", "")
            .replace(")", "")
            .replace("-", "")
            .replace(" ", "")
            )
            print(phone)
            if phone.isdigit() and len(phone)>5 and len(phone)<13:
                break
            else:
                print('Phone number is wrong')
                phone = None
                time.sleep(1)
                os.system('cls')

         #УПРОСТИЛ ПРОВЕРКУ ИМЕЙЛ       
        #перевірка email
        def CorrectEmail(email):
            if email.count('@') > 1 or email.count('@') == 0:
                return (False, 'Неверное количество знаков @')
            [name,domain] = email.split('@')
            if len(domain) < 3:
                return (False, 'Доменное имя короче 3 символов')
            if len(domain) > 256:
                return (False, 'Доменное имя длиннее 256 символов')
            if domain.count('.') == 0:
                return (False, 'Доменное имя не содержит точки')
            includedomain = domain.split('.')
            # список с кодами корректных сиволов a-z - и _
            correctchrlist = list(range(ord('a'),ord('z')+1))
            correctchrlist.extend([ord('-'), ord('_')])
            for k in includedomain:
                # проверяем нет ли пустых подстрок в домене
                if k == '':
                    return (False, 'Доменное имя содержит пустую строку между точками')
                # проверяем нет ли нелегальных символов в подстроках в домене
                for n in k:
                    if ord(n) not in correctchrlist:
                        errormsg = "Недопустимый символ " + n
                        return (False, errormsg)
                if (k[0] == '-') or (k[len(k)-1] == '-'):
                    return (False, 'Доменное имя не может начинаться/заканчиваться знаком "-"')
            if len(name) > 128:
                return (False, 'Имя длиннее 128 символов')
            # Добавляем в список корректных символов . ; " ! : ,
            correctchrlist.extend([ord('.'),ord(';'),ord('"')])
            onlyinquoteschrlist = [ord('!'), ord(','), ord(':')]
            correctchrlist.extend(onlyinquoteschrlist)
            # Проверка на парные кавычки
            if name.count('"')%2 != 0:
                return (False, "Непарные кавычки")
            # Переменные для отслеживания точки и открывающихся кавычек
            doubledot = False
            inquotes = False
            for k in name:
                if (k == '"'):
                    inquotes = not inquotes
                if (ord(k) in onlyinquoteschrlist) and (inquotes == False):
                    return (False, "Недопустимый символ вне кавычек")
                if ord(k) not in correctchrlist:
                    errormsg = "Недопустимый символ " + k
                    return (False, errormsg)
                # проверка на две точки подряд
                if (k == '.'):
                    if doubledot == True:
                        return (False, "Две точки в имени")
                    else:
                        doubledot = True
            return True
    
        email = None
        email_chk = None
        while True:
            email = input("Enter your Email or 'no email': ")
            if email == "no email": break
            email_chk = CorrectEmail(email)
            print(email_chk)
            if email_chk == True:
                break
            time.sleep(2)
            os.system('cls')

        #Перевірка дати народження
        def birthday_validator(birthday):
            bd_num = re.split(r'[\.,\- /:]+', birthday)
            bd_num = ".".join(map(str, bd_num))
            try:
                date_of_birth = datetime.strptime(bd_num, '%d.%m.%Y')
                if date_of_birth.date() >= datetime.today().date():
                    print('Date from future')
                    return None
                birthday = date_of_birth.date()
                return birthday
            except:
                print('Wrong date. Date format \'dd.mm.yyyy\'')
                birthday = None

        birthday_chk = None
        birthday = None
        os.system('cls')
        while birthday_chk == None:
            birthday = input("Enter your birthday or 'no bd': ")
            if birthday == 'no bd':
                break
            elif birthday=='':
                print("You have to enter your birtday or 'no bd': ")
                birthday_chk == '-'
            else:
                birthday_chk=birthday_validator(birthday)
                if birthday_chk != None:
                    birthday=birthday_chk
   
        return name.title(), address, phone, email, birthday

    def update(self):
        name = input("Enter the name: ").title()
        if name in self.persons:
            print("Found. Enter new details.")
            name, address, phone, email, birthday = self.getdetails()
            self.persons[name].__init__(name, address, phone, email, birthday)
            print("Successfully updated.")
        else:
            print("Contact not found.")

    def delete(self):
        name = input("Enter the name to delete: ")
        if name in self.persons:
            del self.persons[name]
            print("Deleted the contact.")
        else:
            print("Contact not found in the app.")

    def reset(self):
        self.persons = {}
    
    def to_birthday(self):
        n_days = 0
        while True:
            try:
                n_days = int(input('Input N days to birthday : '))
                print("{:<25} {:<25} {:<20} {:<20} {}".format('Name', 'Address', 'Phone', 'Email', 'Birthday'))
                print('--------------------------------------------------------------------------------------------------------------')      
            except ValueError:
                os.system('cls')
                print('Input only number of days (digit)!')
            if self.persons:
                iter_dict = {}
      
                # наповнюємо словар значеннями [ім'я: дата] за виключенням "no bd"
                for person in self.persons.values():
                    if person.birthday != "no bd":
                        iter_dict[person.name]=person.birthday
                # знаходимо дату дня народження і звіряємо з датами у базі
                day_now = datetime.now().date()
                to_find_day = day_now + timedelta(days=n_days)
                for i, iter_dict_date in iter_dict.items():
                    if iter_dict_date.day == to_find_day.day and iter_dict_date.month == to_find_day.month:
                        
                        print("{:<20} {} {:<20} {} {:<20} {} {:<20} {}{}".format(self.persons[i].name, '|', self.persons[i].address, '|', self.persons[i].phone, '|', self.persons[i].email, '|', self.persons[i].birthday))
                        
                
                try:
                    find_in_range = int(input('Input range of days: '))
                    for nday in range(find_in_range+1):
                        to_find_day = day_now + timedelta(days=nday)
                        for i, iter_dict_date in iter_dict.items():
                            if iter_dict_date.day == to_find_day.day and iter_dict_date.month == to_find_day.month:
                                get_names = self.persons[i]
                                print('--------------------------------------------------------------------------------------------------------------')   
                                print("{:<20} {} {:<20} {} {:<20} {} {:<20} {} {} {:<3} {}".format(self.persons[i].name, '|', self.persons[i].address, '|', self.persons[i].phone, '|', self.persons[i].email, '|', self.persons[i].birthday, '| Days to bd:', timedelta(days=nday).days))
                except ValueError:
                    print('Input only number of days (digit)!')
                    
                exit_q = input('Exit y/n: ')
                if exit_q == 'y': 
                    os.system('cls')
                    break
                elif exit_q == 'n':
                    pass 
                else: 
                    print('You miss. Go find something')
            else:
                print("No contacts in database.")

    def __del__(self):
        with open(self.database, 'wb') as db:
            pickle.dump(self.persons, db)

    def __str__(self):
        return UI

    # Дивовижна функція, яку краще не запускати
    def sorter():
        file_type_dict = {
            ('jpeg', 'png', 'jpg', 'svg'): [],
            ('avi', 'mp4', 'mov', 'mkv'): [],
            ('doc', 'docx', 'txt', 'pdf', 'xlsx', 'pptx'): [],
            ('mp3', 'ogg', 'wav', 'amr'): [],
            ('zip', 'gz', 'tar'): [],
            ('unknown', ): []
        }

        def sort_file(path, file_type_dict):
            all_file_set = set()
            for element in path.iterdir():
                if element.is_file():
                    all_file_set.add(element.name)
                    for key in file_type_dict:
                        if element.name.rsplit('.', 2)[-1] in set(key):
                            file_type_dict[key].append(element.name)
                        file_type_dict[('unknown', )].extend(
                            all_file_set - set(file_type_dict[key]))
                else:
                    sort_file(element, file_type_dict)
            return file_type_dict


        def output_result_sort(file_type_dict):
            for key, value in file_type_dict.items():
                title_string = str(key).center(78, '-')
                print(title_string)
                for file in value:
                    print(file)
            unknown_type_files = []
            for unknown_file in file_type_dict[('unknown', )]:
                unknown_type_files.append(unknown_file.rsplit('.', 2)[-1])

            print(' unknown type '.center(78, '-'))
            print(set(unknown_type_files))


        if len(sys.argv) <= 1:
            path = Path('')
        else:
            path = Path(sys.argv[1])
        if path.exists():
            if path.is_dir:
                file_type_dict = sort_file(path, file_type_dict)
                output_result_sort(file_type_dict)
            else:
                print(f'{path.absolute} is file')
        else:
            print(f'path {path.absolute()} not exist')




def main():
    app = Application('contacts.data')
    cb = ClipboardAPP('records.data')
    choice = ''
    while choice != '9':
        print(app)
        print(cb)
        choice = input('Choose: ')
        if choice == '1':
            app.add()
        elif choice == '2':
            app.viewall()
        elif choice == '3':
            app.search()
        elif choice == '4':
            app.update()
        elif choice == '5':
            app.delete()
        elif choice == '6':
            app.to_birthday()
        elif choice == '7':
            app.reset()
        elif choice == '8':
            os.system('cls')
            cb.enter_cb()
        elif choice == '9':
            print("Exiting.")
        elif choice == 'add rec':
            cb.add_cb()
        elif choice == 'view rec':
            cb.view_cb()
        elif choice == 's rec':
            cb.search__cb()
        elif choice == 'upd':
            cb.update_cb()
        elif choice == 'del':
            cb.delete_cb()
        elif choice == 'reset':
            cb.reset_cb()
        elif choice == 'q':
            os.system('cls')
            cb.exit_cb()
        elif choice=='sort files':
            os.system('cls')
            print('А воно вам дійсно потрібно робити? Обдумайтесь!')
            time.sleep(2)
            os.system('cls')
        else:
            print("Invalid choice.")
        
if __name__ == '__main__':
    main()
