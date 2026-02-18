import pytest
import POM.PSce as PSce

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

@pytest.mark.login
def test_handbook1(driver):
    orangehrm = PSce.OrangeHRM(driver)
    table = orangehrm.PIM_page()
    assert len(table) > 0

    orangehrm.sort_Ascending()
    XAextract = orangehrm.extractdata_all_page(1)
    normalize1 = [ str(x).strip().lower() for x in XAextract]
    assert normalize1 == sorted(normalize1)

    orangehrm.sort_Descending()
    XDextract = orangehrm.extractdata_all_page(1)
    normalize2 = [ str(x).strip().lower() for x in XDextract]
    assert normalize2 == sorted(normalize2, reverse=True)

