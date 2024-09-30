#!/opt/anaconda3/bin/python3
# -*- coding: utf-8 -*-
"""
Automatically generate a packing list based on user input
"""

import csv
import sys

##############################################################################
#
# Define inputs
#
##############################################################################

# Set path to items csv file
itemsPath='PATH/TO/FILE/packing_items.csv'

# Set path to questions csv file
questionsPath='PATH/TO/FILE/packing_questions.csv'

##############################################################################
#
# Run
#
##############################################################################

#Read items csv file
with open(itemsPath, 'r', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    data = list(reader)

#Read questions csv file
QUESTIONS = []
with open(questionsPath, 'r', newline='') as f:
    reader = csv.reader(f)
    for row in reader:
        QUESTIONS.append(row)

# Check all keywords in questions csv appear in items csv column names
missingColumns = [item for item in [x[0] for x in QUESTIONS[1:]] if item not in list(data[0].keys())[1:]]
if len(missingColumns)>0:
    print(f'Keyword(s): [{", ".join(missingColumns)}] are not in the column names in the items csv file')
    sys.exit("Exiting")

# Check for csv column names without keywords
missingKeywords = [item for item in list(data[0].keys())[1:] if item not in [x[0] for x in QUESTIONS]]
if len(missingKeywords)>0:
    print('There are column names in the items csv file which are not included in the keywords in the questions csv file.')
    print(f'The missing keyword(s) are: {", ".join(missingKeywords)}')
    while True:
        answer = input('\nDo you want to continue? (y/n)')
        if answer =='y': 
            break
        elif answer == 'n':
            sys.exit("Exiting")
        else:
            print("\nPlease enter y or n")
            continue

#Read possible options for multiple-choice questions from items csv file
for q in QUESTIONS:
    if q[2] == 'multi':
        #Read unique values
        unique_values = set()
        for row in data:
            value = row[q[0]]
            unique_values.add(value)
        #Remove blank
        unique_values = [item for item in unique_values if item != '']
        #Remove ANDs
        if any(' AND ' in item for item in unique_values):
            for i in unique_values:
                if ' AND ' in i:
                    newValues = i.split(' AND ')
                    newValues = [item.strip() for item in newValues]
                    for item in newValues:
                        if item not in unique_values:
                            unique_values.append(item)
            unique_values = [item for item in unique_values if ' AND ' not in item]
        #Remove ORs
        if any(',' in item for item in unique_values):
            for i in unique_values:
                if ',' in i:
                    newValues = i.split(',')
                    newValues = [item.strip() for item in newValues]
                    for item in newValues:
                        if item not in unique_values:
                            unique_values.append(item)
            unique_values = [item for item in unique_values if ',' not in item]
        unique_values = sorted(unique_values)
        q.append(unique_values)
    else:
        q.append('NA')

#Add question on output format
QUESTIONS.append(["output","How would you like your packing list formatted?", 'multi',['.txt','.csv','copy to clipboard']])

#Ask questions
answers=[]
for keyword, question, Qtype, options in QUESTIONS:
    if Qtype == 'number':
        while True:
            try:
                answer = int(input(f"\n{question} "))
            except ValueError:
                print("\nPlease enter a number")
                continue
            if answer == '':
                print("\nPlease enter a number")
                continue
            else:
                answers.append(answer)
                break
    if Qtype == 'yn':
        while True:
            answer = input(f"\n{question} ")
            if (answer =='y' or answer =='n'): 
                answers.append(answer)
                break
            if answer == '':
                print("\nPlease enter y or n")
                continue
            else:
                print("\nPlease enter y or n")
                continue
    if Qtype == 'multi':
        while True:
            print(f"\n{question}")
            print("Enter one or more numbers, separated by commas")
            sorted_options = sorted(options)
            for label, option in enumerate(sorted_options):
                print(f"  {label}) {option}")
            answer_label = input().strip()
            if not answer_label:  # Check if the input is empty
                print("\nPlease enter one or more numbers, separated by commas")
                continue
            try:
                answer_label = answer_label.replace(",", " ").split()
                answer_label = [int(i) for i in answer_label]
            except ValueError:
                print("\nPlease enter one or more numbers, separated by commas")
                continue
            if any((i>len(options)-1) or (i<0) for i in answer_label):
                print("\nPlease enter valid numbers")
                continue
            else:
                answer = list(set([sorted_options[i] for i in answer_label]))
                answers.append(answer)
                break

# Set up condition checks

# Create dictionaries for question types and answer indices
q_types = {item[0]: item[2] for item in QUESTIONS}
ans_indices = {item[0]: index for index, item in enumerate(QUESTIONS[1:]) if item[0]!='output'}

# Create a class to check whether conditions for including an item are met
class ItemClass:
    def __init__(self, header, *args):
        self.item = args[0]
        # Map column names to values
        data = dict(zip(header, args))
        # Dynamically create attributes based on the header and data
        for key in q_types.keys():
            setattr(self, key, data.get(key, None))
    
    def conditionCheck(self,att):
        if q_types[att]=='number':
            if float(getattr(self,att))<=answers[ans_indices[att]]:
                return(True)
            else:
                return(False)
        if q_types[att]=='yn':
            if getattr(self,att) == answers[ans_indices[att]]:
                return(True)
            else:
                return(False)
        if q_types[att]=='multi':
            # Items with 'AND'
            if 'AND' in getattr(self,att):
                toInclude = [i for i in QUESTIONS[1:][ans_indices[att]][3] if i in getattr(self,att)]
                if all(i in answers[ans_indices[att]] for i in toInclude):
                    return(True)
                else:
                    return(False)
            # Items with multiple possibilities in csv ('OR')
            elif ',' in getattr(self,att):
                toInclude = [i for i in QUESTIONS[1:][ans_indices[att]][3] if i in getattr(self,att)]
                if any(i in answers[ans_indices[att]] for i in toInclude):
                    return(True)
                else:
                    return(False)
            # All other items (e.g. only one element, no AND or OR)
            else:
                if getattr(self,att) in answers[ans_indices[att]]:
                    return(True)
                else:
                    return(False)                

# Read items csv file using itemClass
my_list = []
with open(itemsPath, 'r') as f:
    reader = csv.reader(f)
    header = next(reader)  # Read the header row
    for row in reader:
        my_list.append(ItemClass(header, *row))

# Make packing list
toTake = []
for x in my_list:
    conditions = []
    for c in list(ans_indices.keys()):
        if not getattr(x, c) == '':
            conditions.append(0)
            if x.conditionCheck(c):
                conditions[-1] = 1
    if all(i == 1 for i in conditions):
        toTake.append(x.item)

# Remove duplicates
toTake = list(set(toTake))

# Write output
if any(item in answers[-1] for item in ['.csv','.txt']):
    from pathlib import Path
    import tkinter as tk
    from tkinter import filedialog 
    if '.csv' in answers[-1]:
        root = tk.Tk()
        root.withdraw()
        save_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            title="Save as"
        )
        root.update()
        root.destroy()
        if save_path:
            save_path = Path(save_path)
            with save_path.open('w', newline='') as file:
                writer = csv.writer(file)
                for item in toTake:
                    writer.writerow([item])
            print(f"\nYour packing list was saved to: {save_path}")
        else:
            print("\nSave cancelled")
    if '.txt' in answers[-1]:
        root = tk.Tk()
        root.withdraw()
        save_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            title="Save as"
        )
        root.update()
        root.destroy()
        if save_path:
            save_path = Path(save_path)
            with save_path.open('w') as file:
                for item in toTake:
                    file.write(f"{item}\n")
            print(f"\nYour packing list was saved to: {save_path}")
        else:
            print("\nSave cancelled")

if 'copy to clipboard' in answers[-1]:
    import pyperclip
    separator = '\n'
    toTakeStr = separator.join(toTake)
    pyperclip.copy(toTakeStr)
    print('\nYour packing list has been copied to the clipboard')





