import warnings
import Funtion
import pandas as pd
from datetime import datetime
date = datetime.now()
date = date.strftime("%d_%m_%Y_%H_%M")
warnings.filterwarnings('ignore')
i = True
result1=[]
writer = pd.ExcelWriter('./Utterance generated/data_'+date+'.xlsx', engine='openpyxl')
while i:
    print(
        "1.Different date format generation\n"
        "2.Dummy data generation\n"
        "3.Paraphrase generation\n"
        "4.Language synonyms generation\n")
    option = int(input("Choose an option : "))

    if option == 1:
        print("-------------------Date Format-----------------")
        name = 'Date format'
        date = input("Enter the date in format(15th August 1999) : ")
        result = Funtion.dateformat(date)
        data = {name: result}

    elif option == 2:
        print("-------------------Dummy Data-----------------")
        result1=[]
        name = "Dummy data"
        print("1.Numeric data 2.Phone number,3.SSN")
        # dum = {1: 'name', 2: 'phone_number', 3: 'ssn', 4: 'free_email', 5: 'address', 6: 'credit_card_number'}
        n = int(input("Enter your choice : "))
        num = int(input("Number of data you want to generate : "))
        result = Funtion.dummydata(n, num)
        data = {name: result}

    elif option == 3:
        print("-------------------Paraphrase generation-----------------")
        name = 'Paraphrase'
        text = input("Enter the example text: ")
        n = int(input("Enter the number of output data required: "))
        result = Funtion.paraphrase(text, n)
        data = {name: result}

    elif option == 4:
        print("-------------------Language synonyms generation-----------------")
        name = 'Language Synonyms'
        inp_sentence = input("Enter the sentence: ")
        result = Funtion.synonyms(inp_sentence)
        data = {name: result}

    elif option == 5:
        print("-------------------Business synonyms generation-----------------")
        name = 'Business synonyms'
        var = input("Do you want to load business synonyms through excel sheet?[Y/N]")
        if var.lower() == 'y':
            var1 = input("Enter the excel sheet name without extension: ")
            sheet = input("Enter the sheet name : ")
            dc = pd.read_excel('./Utterance generated/'+var1+'.xlsx', engine='openpyxl', sheet_name=sheet)
            bus = list(dc['Utterance'])
        else:
            bus = [sen for sen in input("Enter the business synonyms in comma separated format : ").split(",")]
        txt = "Enter the sentence or sentence with comma separated format (e.g.,'i need details on adj1 or i need " \
              "adj1 or adj2, do i have coverage for adj1'): "
        lst = [sen for sen in input(txt).split(",")]
        result = Funtion.business(bus, lst)
        data = result

    print(result)
    df = pd.DataFrame(data)

    # print(df)
    df.to_excel(writer, sheet_name=name, engine='openpyxl', index=False)

    re_run = input("Do you want run again.?[Y/N]")
    if re_run.lower() == 'n':
        i = False
        writer.save()
