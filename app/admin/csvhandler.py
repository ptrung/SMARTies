import csv, io

def csv_file_to_dict(f):
    csv_string = f.read()
    question = []
    answer = []
    dict = {}
    for row in csv.DictReader(csv_string.splitlines(), delimiter=';'):
        question.append(row['question'])
        answer.append(row['answer'])

    dict["question"] = question
    dict["answer"] = answer

    return dict

def questions_to_csv_file(file, questions):


    return dict
