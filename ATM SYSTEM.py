import pymysql
import random

con = pymysql.connect(host='localhost', port=3306, database='atm', user='root', password='xxx')

def line():
    print('*****************************************************************')
def space():
    print('*                                                               *')

def main():    
    print()    
    line()
    space()
    print('*\t\t     WELCOME TO ATM SYSTEM\t\t\t*')
    space()
    line()
    print('1. Login')
    print('0. Register')

    n = int(input('\nEnter Option : '))
    PIN = ''
    Username = ''
    Amount = ''
    userACC = ''
    secure = ''

    if n == 0:
        userACC = random.getrandbits(32)
        name = input('Enter Name : ')
        pw = int(input('Enter 6 Digits PIN : '))
        dpst = int(input('Enter starting amount you want to deposite : '))
        print('\033[93m'+'Security Question!'+'\033[0m')
        conf = input('What is the name of your favorite childhood friend? : ')
    
        Username = name
        PIN = pw
        Amount = dpst
        secure = conf    
        val = (userACC,Username,PIN,Amount,secure)
        sql = "INSERT INTO client(userACC, Username, PIN, Amount, secure) VALUES (%s, %s, %s, %s, %s)"
        cur = con.cursor()
        
        cur.execute(sql,val)
        # account information
        print()
        line()
        print('\033[92m'+'\t\tYour account has been created\n'+'\033[0m')
        cur.execute("""SELECT userACC FROM atm.client where PIN='%s' """ % (PIN))
        konfID = cur.fetchone()
        print('Account Number     :',konfID)
        cur.execute("""SELECT Username FROM atm.client where PIN='%s' """ % (PIN))
        konfUname = cur.fetchone()
        print('Username\t   :',konfUname)
        cur.execute("""SELECT PIN FROM atm.client where PIN='%s' """ % (PIN))
        konfPIN = cur.fetchone()
        print('PIN\t\t   :',konfPIN)
        cur.execute("""SELECT Amount FROM atm.client where PIN='%s' """ % (PIN))
        konfAmount = cur.fetchone()
        print('Deposite\t   :',konfAmount)
        cur.execute("""SELECT secure FROM atm.client where PIN='%s' """ % (PIN))
        konfScr = cur.fetchone()
        print('Security Question  :',konfScr)
        print('\033[93m'+"\n\t\tDON'T SHARE THIS INFORMATION !"+'\033[0m')
        line()
        con.commit()
        main()
        
    elif n == 1:
        pwd = int(input('Enter your 6 digits PIN : '))
        cur = con.cursor()
        cur.execute("""SELECT Amount FROM atm.client where PIN='%s' """ % (pwd))
        sum = cur.fetchone()
        def choice():
            print('1. Status\t\t3. Lodgement\t\t5. Change PIN')
            print('2. Withdraw\t\t4. Transfer\t\t6. Quit')
        
        if cur.rowcount == 1:
            print()
            line()
            print('*'+'\033[92m'+'\t\t\tLOGIN SUCCESSFUL\t\t\t'+'\033[0m'+'*')
            line()
            choice()
            act = int(input('\nEnter Option : '))
            if act == 1:
                print()
                line()
                print ('\t\tYou Have',sum,'On Your Account')
                line()
                print()
                con.commit()
                repeat()
            elif act == 2:
                print()
                line()
                print ('\t\tYou Have',sum,'On Your Account')
                line()
                wd = int(input('How much you want to withdraw : '))
                cur.execute("""SELECT Amount FROM atm.client where PIN='%s' """ % (pwd))
                col = cur.fetchone()
                x = list(col)
                for i in x:
                    z = (int(i))
                    c = z - wd
                cur.execute("UPDATE client SET Amount='%s' where PIN='%s' " % (c,pwd))
                cur.execute("""SELECT Amount FROM atm.client where PIN='%s' """ % (pwd))
                update = cur.fetchone()
                print()
                print('\033[92m'+'Your new balance is',update,'\033[0m')
                line()
                con.commit()
                repeat()
            elif act == 3:
                print()
                line()
                print ('\t\tYou Have',sum,'On Your Account')
                line()
                dep = int(input('How much you want to lodge : '))
                cur.execute("""SELECT Amount FROM atm.client where PIN='%s' """ % (pwd))
                col = cur.fetchone()
                x = list(col)
                for i in x:
                    z = (int(i))
                    c = z + dep
                cur.execute("UPDATE client SET Amount='%s' where PIN='%s' " % (c,pwd))
                cur.execute("""SELECT Amount FROM atm.client where PIN='%s' """ % (pwd))
                update = cur.fetchone()
                print()
                print('\033[92m'+'Your new balance is',update,'\033[0m')
                line()
                con.commit()
                repeat()
            elif act == 4:
                print()
                line()
                print ('\t\tYou Have',sum,'On Your Account')
                line()
                to = input('Enter account number to transfer : ')
                tr = int(input('How much you want to transfer : '))
                cur.execute("""SELECT Amount FROM atm.client where PIN='%s' """ % (pwd))
                d = cur.fetchone()
                x = list(d)
                for i in x:
                    z = (int(i))
                    cd = z - tr
                cur.execute("UPDATE client SET Amount='%s' where PIN='%s' " % (cd,pwd))
                cur.execute("""SELECT Amount FROM atm.client where PIN='%s' """ % (pwd))
                update = cur.fetchone()
                print()
                print('\033[92m'+'Your new balance is',update,'\033[0m')
                line()
                cur.execute("""SELECT Amount FROM atm.client where userACC='%s' """ % (to))
                k = cur.fetchone()
                x = list(k)
                for i in x:
                    z = (int(i))
                    ck = z + tr
                cur.execute("UPDATE client SET Amount='%s' where userACC='%s' " % (ck,to))
                con.commit()
                repeat()
            elif act == 5:
                change = int(input('Type New PIN : '))
                cur.execute("UPDATE client SET PIN='%s' where PIN='%s' " % (change,pwd))
                print()
                line()
                print('\033[92m'+'\t\t    Your PIN Has Been Change'+'\033[0m')
                line()
                con.commit()
                repeat()
            elif act == 6:
                end()
            else:
                print('\033[91m' + 'Incorrect Option' + '\033[0m')
                main()
        else:
            print('\033[91m' + "Account doesn't exist" + '\033[0m')
            forgetPin()
        con.commit()
    else:
        print('\033[91m' + 'Incorrect Option' + '\033[0m')
        main()

def repeat():
    print('Do you want to make another transaction ?')
    answer = input('[ y / n ] : ')
    if answer == 'y':
        main()
    elif answer == 'n':
        end()
    else:
        print('\033[91m' + 'Incorrect Option' + '\033[0m')
        repeat()

def forgetPin():
    fP = input('\nForgot PIN ? [y/n] : ' )
    if fP == 'y':
        name = input('Input your username : ')
        cur = con.cursor()
        cur.execute("""SELECT PIN FROM atm.client where Username='%s' """ % (name))
        if cur.rowcount == 1:
            change = int(input('Type New PIN : '))
            cur.execute("UPDATE client SET PIN='%s' where Username='%s' " % (change,name))
            print()
            line()
            print('\033[92m'+'\t\t    Your PIN Has Been Change'+'\033[0m')
            line()
        else:
            print('\033[91m' + 'Incorrect Username' + '\033[0m')
            forgetUname()
        con.commit()
        main()
    elif fP == 'n':
        main()
    else:
        print('\033[91m' + 'Incorrect Option' + '\033[0m')
        forgetPin()
        
def forgetUname():
    fU = input('\nForgot Username ? [y/n] : ' )
    if fU == 'y':
        scr = input('What is the name of your favorite childhood friend? : ')
        cur = con.cursor()
        cur.execute("""SELECT Username FROM atm.client where secure='%s' """ % (scr))
        if cur.rowcount == 1:
            cur.execute("""SELECT Username FROM atm.client where secure='%s' """ % (scr))
            confirm = cur.fetchone()
            print('\033[92m'+'Your username is',confirm,'\033[0m')
            forgetPin()
        else:
            print()
            line()
            print('\033[91m' + "\t\tYou Can't Access Your Account" + '\033[0m')
            line()
            main()
    elif fU == 'n':
        forgetPin()
    else:
        print('\033[91m' + 'Incorrect Option' + '\033[0m')
        forgetUname()
        
def end():
    print()
    line()
    space()
    print('*\t\t   Thankyou and Have a Nice Day\t\t\t*')
    space()
    line()
    con.commit()        
    exit()

main()
repeat()

# Designed By : Fikrian Nur Abdullah 15220611
#               Juli Martinus Zega   15220614
# Universitas Bina Sarana Informatika Kramat 98 Jakarta
