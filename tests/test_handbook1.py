import pytest
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import POM.psce as psce

def AJAX_Wait(driver,filter_object):
    for objects in filter_object:
        WebDriverWait(driver, 13).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "div.oxd-table-card"), objects))

def detect_rows(driver, EmployeeID, LastName, JobTitle):
    rows = driver.find_elements(By.CSS_SELECTOR,"div.oxd-table-body div.oxd-table-card")
    if not rows:
        return False
    for row in rows:
        cells = row.find_elements(By.CSS_SELECTOR,"div.oxd-table-cell")    # already inside the "body" and "card"
        if cells[1].text.strip() == EmployeeID and cells[3].text.strip() == LastName and cells[4].text.strip() == JobTitle:
            return True
    return False

def priority_sort(y):  # standby in case the dynamic table switch to numerical sort
    if y is None:
        return 0, ""
    s = str(y).strip().lower()
    if s == "":
        return 0,""
    if s.isdigit():
        return 1, int(s)

    prefix = ""
    suffix = ""
    for index, char in enumerate(s):
        if not char.isdigit():
            prefix = s[:index]
            suffix = s[index:]
            break
    else:
        prefix = s
    if prefix.isdigit():
        return 1, int(prefix), suffix.lower()

    return 2, s

@pytest.mark.parametrize(("EmployeeID", "LastName", "JobTitle"),[("0034", "Hamilton", "Software Engineer")])
@pytest.mark.login
def test_handbook1(driver, EmployeeID, LastName, JobTitle):
    orangehrm = psce.OrangeHRM(driver)
    rows = orangehrm.open_pim_page()
    assert len(rows) > 0

    orangehrm.filter("Employee Id", EmployeeID, False)
    orangehrm.filter("Job Title", JobTitle, True)
    orangehrm.filter_search_click()
    AJAX_Wait(driver, [EmployeeID, LastName, JobTitle])         # can split into multiple lines without for loop written in def AJAX_Wait
    assert detect_rows(driver, EmployeeID, LastName, JobTitle)

    orangehrm.filter_reset_click()
    orangehrm.sort_ascending()
    XAextract = orangehrm.extract_data_allpage(1)
    normalize1 = [ str(x).strip().lower() for x in XAextract]
    assert normalize1 == sorted(normalize1)

    orangehrm.sort_descending()
    XDextract = orangehrm.extract_data_allpage(1)
    normalize2 = [ str(x).strip().lower() for x in XDextract]
    assert normalize2 == sorted(normalize2, reverse=True)

