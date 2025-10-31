import streamlit as st
import mysql.connector as connector
import pandas as pd
import datetime
import time

con=connector.connect(
    
        host="127.0.0.1",
        port=3306,
        user="root",
        password="Purwanshu@123",
        database="obs",
        connection_timeout=5,
        use_pure=True
)

cur=con.cursor(buffered=True)

def login(emailid,username,password):
    cur.execute(f"select * from customer where email = (select email_id from login where email_id = '{emailid}' and username = '{username}' and password = '{password}');")
    if cur:
        data=cur.fetchone()
        return data
    else:
        return 0

def show_account_info(acc_no):
    cur.execute(f"select * from account_type where account_no = {acc_no}")
    row = cur.fetchone()
    acc_no,deposit_amount,tr_limit,wd_limit,interest_rate=row
    st.write(f"Account Number: {acc_no}")
    st.write(f'Deposit Amount: Rs {deposit_amount}')
    st.write(f"Transaction Limit: Rs {tr_limit}")
    st.write(f"Withdraw Limit: Rs {wd_limit}")
    st.write(f"Interest Rate: {interest_rate}")

def change_withdraw_limit(acc_no):
    new_wd_limit = st.number_input('Enter New Withdraw Limit')
    if new_wd_limit:
        cur.execute(f"update account_type set withdraw_limit = {new_wd_limit} where account_no = {acc_no}")
        con.commit()
        st.success(f"Withdraw limit updated to Rs {new_wd_limit}")

def change_transaction_limit(acc_no):
    new_tr_limit = st.number_input('Enter New Transaction Limit')
    if new_tr_limit:
        cur.execute(f"update account_type set transaction_limit = {new_tr_limit} where account_no = {acc_no}")
        con.commit()
        st.success(f"Withdraw limit updated to Rs {new_tr_limit}")


def showbal(acc_no):
    cur.execute(f"select balance,overdraft from account where acc_no='{acc_no}'")    
    row=cur.fetchone()
    st.write(f"Your balance is Rs {row[0]}")
    st.write(f"Your overdraft is Rs {row[1]}")
    con.commit()
    if row[0]:
        return row[0],"b"
    elif row[1]:
        return row[1],"o"
    else:
        return "none","none"

def show_card_info(acc_no, card):
    if card == "Credit card":
        cur.execute(f"select * from credit_card where account_no = {acc_no}")
        row = cur.fetchone()
        cc_limit,cc_number,cc_cvv,cc_expirydate,acc_no = row
        st.write(f"Card Limit: Rs {cc_limit}")
        st.write(f'Card Number: {cc_number}')
        st.write(f"Card Expiry: {cc_expirydate}")
    elif card == "Debit card":
        cur.execute(f"select * from debit_card where account_no = {acc_no}")
        row = cur.fetchone()
        dc_number,dc_cvv,dc_expirydate,acc_no = row
        st.write(f'Card Number: {dc_number}')
        st.write(f"Card Expiry: {dc_expirydate}")


def change_cc_limit(cc_number,cvv):
    cur.execute(f"select cc_cvv from credit_card where cc_number = {cc_number} and cc_cvv={cvv}")
    row = cur.fetchone()
    if row:
        new_limit = st.number_input("Enter the limit (max Rs 10,00,000)")
        if new_limit and new_limit > 1000000:
            st.error("Please select the limit under Rs 10,00,000")
        elif new_limit:
            cur.execute(f"update credit_card set cc_limit={new_limit} where cc_number = {cc_number}")
            st.success(f"Credit Card limit updated to Rs {new_limit}")
            con.commit()
    else:
        st.error("Wrong card number / cvv")


def display_loan_details(acc_no):
    cur.execute(f"select * from loans where account_no = {acc_no}")
    row = cur.fetchall()
    df = pd.DataFrame(row, columns=['Loan ID', 'Term', 'Rate of Interest', 'Amount', 'Type of Loan', 'Account Number', 'Amount Due'])
    st.table(df)

def repay_loan(acc_no):
    passwd = st.text_input("Enter Password",type='password')
    if passwd:
        cur.execute(f"select * from login where email_id = (select email from customer where account_no = {acc_no}) and password = '{passwd}'")
        row1 = cur.fetchone()
        if row1:
            loan_id = st.number_input("Enter Loan ID")
            if loan_id:
                row2 = cur.execute(f"select * from loans where loan_id = {loan_id}")
                row2 = cur.fetchone()
                if row2:
                    cur.execute(f"select amount_due from loans where loan_id = {loan_id}")
                    amt_due = cur.fetchone()[0]
                    if amt_due>0:
                        avl_bal,status = showbal(acc_no)
                        if status=="b":
                            amt = st.number_input("Enter amount to repay:")
                            if amt and amt > avl_bal:
                                st.error(f"Amount exceeds available balance.")
                            elif amt and amt > amt_due:
                                st.error(f"Amount exceeds your amount due.")
                            elif amt:
                                cur.execute(f"update account set balance = {avl_bal-amt} where acc_no = {acc_no}")
                                cur.execute(f"update loans set amount_due = {amt_due-amt} where loan_id = {loan_id}")
                                con.commit()
                                st.success("Payment Successful")
                                loan_id = st.empty()
                        elif status=="o":
                            st.error(f"You have an overdraft of Rs {avl_bal}.\nDeposit money in your account before repaying loan")
                        else:
                            st.error(f"Your balance is 0.\nDeposit money in your account before repaying loan")
                    else:
                        st.success('You have no amount due')
                else:
                    st.error("Wrong Loan ID")
        else:
            st.error("Wrong Password")

    
def make_payment(sender_name,acc_no,mode):
    to_acc_no = st.number_input("Enter the account number of beneficiary")
    acc_no = int(acc_no)
    if to_acc_no:
        to_acc_no = int(to_acc_no)
        cur.execute(f"select first_name, last_name from customer where account_no = (select acc_no from account where acc_no = {to_acc_no})")
        row = cur.fetchone()
        if row:
            receiver_name = row[0]+' '+row[1]
            st.success(f"Beneficiary Name : {receiver_name}")
            if mode == 'Credit Card':
                cur.execute(f"select cc_limit from credit_card where account_no = {acc_no}")
                cc_limit = cur.fetchone()[0]
                cur.execute(f"select balance, overdraft from account where acc_no = {acc_no}")
                balance, overdraft = cur.fetchone()
                cur.execute(f"select balance, overdraft from account where acc_no = {to_acc_no}")
                ben_bal,ben_od = cur.fetchone()
                amt = st.number_input("Enter amount")
                if amt and amt <= cc_limit:
                    cur.execute(f"update account set overdraft={overdraft + amt} where acc_no = {acc_no}")
                    if amt<=ben_od:
                        cur.execute(f"update account set overdraft = {ben_od - amt} where acc_no = {to_acc_no}")
                    else:
                        new_amt = amt - ben_od
                        cur.execute(f"update account set overdraft = 0, balance = {ben_bal + new_amt} where acc_no = {to_acc_no}")
                    
                    date = datetime.date.today()
                    c_time = time.strftime("%H:%M:%S",time.localtime())
                    
                    con.commit()
                    st.success("Payment Successful")

                    cur.execute(f"select balance, overdraft from account where acc_no = {acc_no}")
                    new_balance, new_overdraft = cur.fetchone()
                    cur.execute(f"select balance, overdraft from account where acc_no = {to_acc_no}")
                    new_ben_bal,new_ben_od = cur.fetchone()

                    cur.execute(f"insert into transaction_history values ('{str(date)}','{str(c_time)}',{amt},'recieved from {acc_no} - {sender_name}',{new_ben_bal},{to_acc_no})")
                    cur.execute(f"insert into transaction_history values ('{str(date)}','{str(c_time)}',{amt},'transferred to {to_acc_no} - {receiver_name}',{new_balance},{acc_no})")
                    con.commit()

                elif amt:
                    st.error(f"Amount exceeds your Credit Card limit.\n Your Credit Card limit is Rs {cc_limit}")

            elif mode == 'Debit Card':
                cur.execute(f"select transaction_limit from account_type where account_no = {acc_no}")
                tr_limit = cur.fetchone()[0]
                cur.execute(f"select balance, overdraft from account where acc_no = {acc_no}")
                balance, overdraft = cur.fetchone()
                cur.execute(f"select balance, overdraft from account where acc_no = {to_acc_no}")
                ben_bal,ben_od = cur.fetchone()
                amt = st.number_input("Enter amount")
                if amt and amt <= tr_limit and amt <= balance:
                    cur.execute(f"update account set balance={balance - amt} where acc_no = {acc_no}")
                    if amt<=ben_od:
                        cur.execute(f"update account set overdraft = {ben_od - amt} where acc_no = {to_acc_no}")
                    else:
                        new_amt = amt - ben_od
                        cur.execute(f"update account set overdraft = 0, balance = {ben_bal + new_amt} where acc_no = {to_acc_no}")
                    
                    date = datetime.date.today()
                    c_time = time.strftime("%H:%M:%S",time.localtime())
                    
                    con.commit()
                    st.success("Payment Successful")

                    cur.execute(f"select balance, overdraft from account where acc_no = {acc_no}")
                    new_balance, new_overdraft = cur.fetchone()
                    cur.execute(f"select balance, overdraft from account where acc_no = {to_acc_no}")
                    new_ben_bal,new_ben_od = cur.fetchone()

                    cur.execute(f"insert into transaction_history values ('{str(date)}','{str(c_time)}',{amt},'recieved from {acc_no} - {sender_name}',{new_ben_bal},{to_acc_no})")
                    cur.execute(f"insert into transaction_history values ('{str(date)}','{str(c_time)}',{amt},'transferred to {to_acc_no} - {receiver_name}',{new_balance},{acc_no})")
                    con.commit()

                elif amt and amt<=tr_limit:
                    st.error(f"Amount exceeds your available balance.\n Your available balance is Rs {balance}")

                elif amt and amt<=balance:
                    st.error(f"Amount exceeds your Transaction limit.\n Your Transaction limit is Rs {tr_limit}")

                elif amt:
                    st.error(f"Amount exceeds your Transaction limit and available balance.\n Your Transaction limit is Rs {tr_limit}.\n Your available balance is Rs {balance}")
                    
        
        else:
            st.error("Invalid Account Number")

def display_transaction_history(acc_no):
    cur.execute(f"select date as 'Date',time as 'Time',amount as 'Amount',description as 'Description',available_balance as 'Closing Balance' from transaction_history where account_no = {acc_no}")
    history = cur.fetchall()
    if history:
        columns = [col[0] for col in cur.description]
        data = []
        for row in history:
            converted_row = []
            for value in row:
                if isinstance(value,(str,int,float)):
                    converted_row.append(value)
                else:
                    converted_row.append(str(value))
            data.append(converted_row)
        df = pd.DataFrame(data, columns=columns)
        st.table(df)



def main():
    st.title("Online Banking management system")

    menu = ["Home","Login"]
    choice = st.sidebar.selectbox("Menu",menu)

    if choice == "Home":
        st.subheader("Home")
        st.success("PYTHON and  ADBMS  Mini Project")
        st.write("Purwanshu -25MCD10001")
        st.write("Garv-25MCD10004")
        
    
    elif choice == "Login":
        st.subheader("Login section")

        email_id = st.sidebar.text_input("Email")
        username = st.sidebar.text_input("Username")
        password = st.sidebar.text_input("Password",type = 'password')

        if st.sidebar.checkbox("Login"):
            
            result = login(email_id,username,password)
        
            if result:
                
                cust_id,dob,first_name,last_name,phone_no,email,pan_no,account_no = result
                full_name = first_name+" "+last_name
                
                st.success(f"Logged In as {full_name}")
                
                task = st.selectbox("Action",['Account settings','Check Balance','Cards','Loan','Transfer Funds','Transaction History'])

                if task == 'Account settings':
                    
                    as_task = st.selectbox("Settings",["Show Account Info","Change Withdraw Limit","Change Transaction Limit"])
                    
                    if as_task == "Show Account Info":
                        show_account_info(account_no)
                    
                    elif as_task == "Change Withdraw Limit":
                        change_withdraw_limit(account_no)
                    
                    elif as_task == "Change Transaction Limit":
                        change_transaction_limit(account_no)

                elif task == "Check Balance":
                    
                    st.subheader("Check Balance")
                    
                    if st.button("Check bal"):
                        showbal(account_no)
                
                elif task == "Cards":
                
                    st.subheader("Cards")
                    card=st.selectbox("Type of card",['Credit card','Debit card'])

                    if card == "Credit card":
                       
                        st.subheader("Credit card")
                        card_task = st.selectbox("Settings",["Show Card Info","Change limit"])
                       
                        if card_task == "Show Card Info":
                            show_card_info(account_no,card)
                       
                        elif card_task == "Change limit":
                            cvv = st.text_input("Please enter the CVV:",type='password')
                            cc_number = st.number_input("Please enter the card number:")
                            
                            if cvv and cc_number:
                                change_cc_limit(cc_number,cvv)

                    elif card == "Debit card":
                        
                        st.subheader("Debit card")
                        card_task = st.button("Show Card Info")
                        
                        if card_task:
                            show_card_info(account_no,card)
                
                elif task == "Loan":
                    
                    st.subheader("Loan")
                    display_loan_details(account_no)
                    
                    loan_task = st.selectbox("Action",["Repay Loan"])
                    
                    if loan_task == "Repay Loan":
                        repay_loan(account_no)

                elif task == "Transfer Funds":
                    tf_task = st.selectbox("Choose the Mode of Payment",['Credit Card','Debit Card'])
                    if tf_task:
                        make_payment(full_name,account_no,tf_task)
                    
                elif task == "Transaction History":
                    display_transaction_history(account_no)

            else:
                st.error("Login Failed. Please check with Email, Username and Password")
if __name__ == '__main__':
    main()
