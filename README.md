# Packing-list-generator
Create a fully customisable travel packing list based on user input.

## Overview
The user creates a list of questions, e.g. 'How many nights will you be away for?'. They also supply a .csv file with the full list of items they may want under any eventuality, together with the information on when each item is required. The code asks the questions and compiles the list of necessary items.

Questions can be multiple-choice, yes/no or numeric.

It is possible to include AND and OR restrictions on the list of items, for example, only take this item if both Anna and Bob are travelling, or if the trip is in either spring or summer. Full details of how to include these restrictions are given below.

The user has a choice of output format. Your packing list can be written to a .txt file, a .csv file or it can be copied to the clipboard.

## Requirements
The code was written in python 3.10. It will most likely work in other versions, but this has not been tested.\
The code should work on Mac, Windows and Linux, but so far has only been tested on Mac.

Necessary packages:
- csv
- sys

Optional packages:
- pathlib (for writing output to .csv or .txt)
- tkinter (for writing output to .csv or .txt)
- pyperclip (for copying output to clipboard)

## User inputs
Two user inputs are required. These should be included in the section 'Define inputs' of the code.
- The path to the .csv file (as a string)
- The list of questions to ask

The questions are defined as a list of lists. Each question has 3 elements:
- keyword
- question text
- question type

The keyword should exactly match one of the column headers in the .csv file.\
The question type should be one of the following:
- 'number' (used for questions where the answer is a number)
- 'multi' (used for multiple-choice quesions)
- 'yn' (used for yes/no questions)

Example list of questions:
```
QUESTIONS = [
  ['duration', 'How many nights will you be away?', 'number'],
  ['people', 'Who is going?', 'multi'],
  ['abroad', 'Are you travelling abroad? (y/n)', 'yn']
]
```

## Setting up the .csv file
An example csv file is provided.

Column headers should be 'Item' and then one column for each question keyword.\
The code will not run if you have questions without an equivalent column in the csv file. It will run if you have extra columns, but they will not be used.\
The order of the columns (after 'Item') does not matter.

Use the columns to define under what circumstances an item should be taken:
- For numeric ('number') questions: input the minimum number for which the item is necessary. E.g. if the question is 'How many nights will you be away?' and you input 3, that means the item will be added to the list if you are away for at least 3 nights.
- For multiple choice ('multi') questions: input the option for which this item is relevant. E.g. if the question is 'Who is going?' and you input 'Anna', the item will only be added to the list if Anna is going on the trip.
- For yes/no ('yn') questions: input 'y' if you want to take the item when the answer to the question is 'yes', otherwise leave it blank. E.g. if the question is 'Are you travelling abroad?' and you input 'y', then the item is added to the list if you are travelling abroad.

### AND conditions
If you want to take an item only if Anna is travelling and you will be away for at least 3 nights, simply enter both these conditions in that row in the .csv file.

If you want to take an item only if both Anna and Bob are travelling, then under the 'people' column, enter 'Anna AND Bob'.

### OR conditions
If you want to take an item either if Anna is travelling or if you are travelling abroad, then list the item twice in the spreadsheet. On one row put 'Anna' in the people column and in the other put 'y' in the abroad column. Duplicate items are removed as part of generating the packing list, so the item will not be listed twice in the final list.

If you want to take an item if either Anna or Bob are travelling, then under the 'people' column, enter 'Anna, Bob'.

## Running the code
Once the .csv file is ready and the inputs are defined in the script, the code is ready to run. There is no need to edit anything else in the script.
