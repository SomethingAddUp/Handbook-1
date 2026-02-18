from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class OrangeHRM:     # Professional 1: try to name class start with capital letter
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 13)

    def login(self, username, password):
        self.wait.until(EC.visibility_of_element_located((By.NAME, "username"))).send_keys(username)
        self.driver.find_element(By.NAME, "password").send_keys(password)
        self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))).click()

    def PIM_page(self):
        self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "ul.oxd-main-menu li")))
        self.driver.find_element(By.XPATH, "//span[normalize-space()='PIM']").click()
        self.wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.oxd-table-body div.oxd-table-card")))
        return self.driver.find_elements(By.CSS_SELECTOR,"div.oxd-table-body div.oxd-table-card")

    def PIM_table(self):
        table = self.driver.find_element(By.CSS_SELECTOR, "div.oxd-table.orangehrm-employee-list")
       # WebDriverWait(table, 15).until(lambda d: len(d.find_elements(By.CSS_SELECTOR, "div.oxd-table-body div.oxd-table-card")) > 0)
        self.wait.until(lambda d: len(table.find_elements(By.CSS_SELECTOR, "div.oxd-table-body div.oxd-table-card")) > 0)
        return table.find_elements(By.CSS_SELECTOR,"div.oxd-table-body div.oxd-table-card")

    def sort_Ascending(self):
        self.wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'oxd-table-header-cell')][.//text()[normalize-space()='Id']]//i"))).click()
        self.wait.until(EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='Ascending']"))).click()
    ##    self.wait.until(lambda d: d.find_element(By.CSS_SELECTOR,"div.oxd-table-body div.oxd-table-card").text != before_sort)
        self.wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,"div.oxd-table-body div.oxd-table-card")))      # not just DOM but really at least 1 row exists

    def sort_Descending(self):
        self.wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'oxd-table-header-cell')][.//text()[normalize-space()='Id']]//i"))).click()
        self.wait.until(EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='Descending']"))).click()
        self.wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,"div.oxd-table-body div.oxd-table-card")))

    def extractdata_1_page(self, column_index):
        download = []
        rows = self.PIM_table()
        for row in rows:
            cells = row.find_elements(By.CSS_SELECTOR,"div.oxd-table-cell")
            if column_index < len(cells):
                download.append(cells[column_index].text.strip())
            else:
                download.append("")
        return download

    def current_page(self):
        table = self.driver.find_element(By.CSS_SELECTOR, "div.oxd-table.orangehrm-employee-list")
        currentpage_button = table.find_elements(By.CSS_SELECTOR, "button.oxd-pagination-page-item--page-selected")  # return a list of button, but there is only 1 selected button page
        if len(currentpage_button) == 0:
            return 1
        return int(currentpage_button[0].text.strip())   # happen index 0 is page number for orangehrm

    def next_page(self):
        # Optional to add if current page is total page, then return
        table = self.driver.find_element(By.CSS_SELECTOR, "div.oxd-table.orangehrm-employee-list")
        before_next = self.current_page()
        WebDriverWait(table, 15).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.oxd-pagination-page-item--next"))).click()
        self.wait.until(lambda d: int(d.find_element(By.CSS_SELECTOR, "button.oxd-pagination-page-item--page-selected").text.strip()) != before_next)

    def flipto_page(self, page_number):
        table = self.driver.find_element(By.CSS_SELECTOR, "div.oxd-table.orangehrm-employee-list")
        self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "button.oxd-pagination-page-item--page")))
        if self.current_page() == page_number:
            return
        page_button = table.find_elements(By.CSS_SELECTOR, "button.oxd-pagination-page-item--page")
        for button in page_button:
            if int(button.text.strip()) == page_number:
                button.click()
                break
        self.wait.until(lambda d: int(d.find_element(By.CSS_SELECTOR,  "button.oxd-pagination-page-item--page-selected").text.strip()) == page_number)

    def finalpage(self):
        table = self.driver.find_element(By.CSS_SELECTOR, "div.oxd-table.orangehrm-employee-list")
        page_button = table.find_elements(By.CSS_SELECTOR, "button.oxd-pagination-page-item--page")   # return a list of button. With index [0] will only give you first page button of the list
        if len(page_button) == 0:   # or "if not page_button"
            return 1
        page = [ int(button.text.strip()) for button in page_button ]   # swap a list of buttons naming to integers as you cannot use max() on non-integers -- string (lexicographic sort) or mix numerical
    #    page = [ int(button.text.strip()) for button in page_button if button.text.strip().isdigit()]   # optional defensive solution
        return max(page)

    def extractdata_all_page(self,column_index):
        Xdownload = []
        lastpage = self.finalpage()
        self.flipto_page(1)
        while True:
            currentpage = self.current_page()
            Xdownload.extend(self.extractdata_1_page(column_index))
            if currentpage == lastpage:
                break
            else:
                self.next_page()
        return Xdownload
