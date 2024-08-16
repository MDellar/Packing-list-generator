# Packing-list-generator
Create a fully customisable travel packing list based on user input

## Overview
The user creates a list of questions, e.g. 'How many nights will you be away for?'. They also supply a .csv file with the full list of items they may want under any eventuality, together with the information on when each item is required. The code asks the questions and compiles the list of necessary items.

Questions can be multiple-choice, yes/no or have a number as the answer.

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
- The list of questions to ask (see below)

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

## Running the code
Once the .csv file 
