import re
from dateparser.search import search_dates
from faker import Faker
import torch
from transformers import PegasusForConditionalGeneration, PegasusTokenizer
from checklist.editor import Editor
import pandas as pd


def dateformat(date):
    dt = search_dates(date)

    def ord(n):
        return str(n) + ("th" if 4 <= n % 100 <= 20 else {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th"))

    converted_text = None
    result = []
    date_format = ['%B %d %Y', '%d %B %Y', '%Y %d %B', '%Y %B %d', '%B %d %y', '%d %B %y', '%y %d %B', '%y %B %d',
                   '%m %d %Y', '%d %m %Y', '%Y %d %m', '%Y %m %d', '%m %d %y', '%d %m %y', '%y %d %m', '%y %m %d',
                   '%w %A of %B %Y', '%Y %w %A of %B', '%d day, %m month of %Y']
    for dt_type in date_format:
        for i in range(len(dt)):
            result.append(re.sub(dt[i][0], str(dt[i][1].date().strftime(dt_type)), date))

    for i in range(len(dt)):
        for j in range(len(result)):
            result.append(re.sub(str(dt[i][1].day), str(ord(dt[i][1].day)), result[j]))
    return result


def dummydata(choice, no):
    fake = Faker('en_US')
    data = []
    if choice == 1:
        len_digits = int(input("Enter the length of digit: "))
        for i in range(int(no)):
            print(fake.random_number(digits=len_digits))
            data.append(fake.random_number(digits=len_digits))
    # elif choice == 2:
    #     format_gen = input("Enter the pattern in comma separated format  (# -numeric, ? - alpha, e.g. ##??:2 - 28Ae,"
    #                        "32DF) : ")
    #     formats = format_gen.split(",")
    #     # print(formats)
    #     for j in formats:
    #         j = j.split(':')
    #         print(j)
    #         for i in range(int(j[1])):
    #             print(fake.bothify(text=j[0]))
    #             data.append(fake.bothify(text=j[0]))
    # elif choice == 3:
    #     for i in range(int(no)):
    #         print(fake.name())
    #         data.append(fake.name())
    elif choice == 2:
        for i in range(int(no)):
            print(fake.phone_number())
            data.append(fake.phone_number())
    # elif choice == 3:
    #     start_date = input("How many years back from this year (e.g. -20y)?")
    #     end_date = input("End year from today(e.g. today/-10y ? :")
    #     for i in range(int(no)):
    #         print(fake.date_between(start_date=start_date, end_date=end_date))
    #         data.append(fake.date_between(start_date=start_date, end_date=end_date))
    elif choice == 3:
        for i in range(int(no)):
            print(fake.ssn())
            data.append(fake.ssn())
    # elif choice == 7:
    #     for i in range(int(no)):
    #         print(fake.email())
    #         data.append(fake.email())
    return data


def paraphrase(text, n):
    tuner = "tuner007/pegasus_paraphrase"
    torch_device = 'cuda' if torch.cuda.is_available() else 'cpu'
    tokenizer = PegasusTokenizer.from_pretrained(tuner)
    model = PegasusForConditionalGeneration.from_pretrained(tuner).to(torch_device)
    batch = tokenizer.prepare_seq2seq_batch([text], truncation=True, padding='longest', max_length=60,
                                            return_tensors='pt').to(torch_device)
    translated = model.generate(**batch, max_length=60, num_beams=30, num_return_sequences=n, temperature=1.5)
    result = tokenizer.batch_decode(translated, skip_special_tokens=True)
    return result


def synonyms(inp_sentence):
    editor = Editor()
    generated_sentence = []
    for i in inp_sentence.split(' '):
        synonym_list = editor.synonyms(inp_sentence, i)
        if len(synonym_list) != 0:
            for val in synonym_list:
                generated_sentence.append(re.sub(i, val, inp_sentence))
    return generated_sentence


# def business(bus, lst):
#     data = {}
#     bus.append(' ')
#     editor = Editor()
#     for j in lst:
#         j = j.replace("adj1", "{adj1}")
#         j = j.replace("adj2", "{adj2}")
#         final_data = []
#         print(bus)
#         for i in range(len(bus)-1):
#             raw_data = editor.template(j, adj=[bus[i], bus[i + 1]], remove_duplicates=True)
#             # print(raw_data.data)
#             final_data.append(raw_data.data[0])
#         j = j.replace('{adj1}', "business synonym")
#         j = j.replace('{adj2}', "business synonym")
#         data[j] = final_data

    return data

