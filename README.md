# Portfolio #1: Python Selenium in OrangeHRM Demo

## Description
This project allows me to acquire first-hand experience by identifying proper locator syntax, 
navigation flow, python logic, re-usable helpers and parametrize markers.

## Tech Stack
- Python 3.14, Selenium WebDriver, Conftest + Pytest
- ChromeDriver, WebDriver Manager

## Webpage
- OrangeHRM Demo : https://opensource-demo.orangehrmlive.com/

## Features
1. Login and PIM page verifications. Extract employee list table.
2. Filter a specific employee from employee form.
3. Clear filter. Test both ascending and descending sorts after numerical / text normalization.

## Challenges
- Handle dynamic UI change by pinpointing the employee list table container before pagination aim.
- Determine table sort order in numerical or lexicographic mode.

## Setup & Run
1. Clone the repository to your local machine
   - git clone https://github.com/SomethingAddUp/Handbook-1.git
   - cd Handbook-1
2. Install dependencies required for the tests
   - pip install -r requirements.txt
3. Run automated tests
   - pytest
