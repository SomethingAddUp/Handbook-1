from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class OrangeHRM:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 13)
        self.employee_table = (By.CSS_SELECTOR, "div.oxd-table.orangehrm-employee-list")
        self.rows = (By.CSS_SELECTOR, "div.oxd-table-body div.oxd-table-card")
        self.pagination_button = (By.CSS_SELECTOR, "button.oxd-pagination-page-item--page")

    def login(self, username, password):
        self.wait.until(EC.visibility_of_element_located((By.NAME, "username"))).send_keys(username)
        self.driver.find_element(By.NAME, "password").send_keys(password)
        self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))).click()

    def open_pim_page(self):
        self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "ul.oxd-main-menu li")))
        self.driver.find_element(By.XPATH, "//span[normalize-space()='PIM']").click()
        self.wait.until(EC.presence_of_all_elements_located(self.rows))
        return self.driver.find_elements(*self.rows)

    def get_pim_table(self):
        table = self.driver.find_element(*self.employee_table)
        self.wait.until(lambda d: len(table.find_elements(*self.rows)) > 0)
        return table.find_elements(*self.rows)

    def sort_ascending(self):
        self.wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'oxd-table-header-cell')][.//text()[normalize-space()='Id']]//i"))).click()
        self.wait.until(EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='Ascending']"))).click()
        self.wait.until(EC.presence_of_all_elements_located(self.rows))

    def sort_descending(self):
        self.wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'oxd-table-header-cell')][.//text()[normalize-space()='Id']]//i"))).click()
        self.wait.until(EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='Descending']"))).click()
        self.wait.until(EC.presence_of_all_elements_located(self.rows))

    def extract_data_1page(self, column_index):
        download = []
        rows = self.get_pim_table()
        for row in rows:
            cells = row.find_elements(By.CSS_SELECTOR,"div.oxd-table-cell")
            if column_index < len(cells):
                download.append(cells[column_index].text.strip())
            else:
                download.append("")
        return download

    def current_page(self):
        table = self.driver.find_element(*self.employee_table)
        currentpage_button = table.find_elements(By.CSS_SELECTOR, "button.oxd-pagination-page-item--page-selected")
        if len(currentpage_button) == 0:
            return 1
        return int(currentpage_button[0].text.strip())

    def next_page(self):
        table = self.driver.find_element(*self.employee_table)
        before_next = self.current_page()
        WebDriverWait(table, 15).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.oxd-pagination-page-item--next"))).click()
        self.wait.until(lambda d: int(d.find_element(By.CSS_SELECTOR, "button.oxd-pagination-page-item--page-selected").text.strip()) != before_next)

    def flip_to_page(self, page_number):
        table = self.driver.find_element(*self.employee_table)
        self.wait.until(EC.presence_of_element_located(self.pagination_button))
        if self.current_page() == page_number:
            return
        page_button = table.find_elements(*self.pagination_button)
        for button in page_button:
            if int(button.text.strip()) == page_number:
                button.click()
                break
        self.wait.until(lambda d: int(d.find_element(By.CSS_SELECTOR,  "button.oxd-pagination-page-item--page-selected").text.strip()) == page_number)

    def final_page(self):
        table = self.driver.find_element(*self.employee_table)
        page_button = table.find_elements(*self.pagination_button)
        if len(page_button) == 0:
            return 1
        page = [ int(button.text.strip()) for button in page_button ]   # switch a list of button strings to integer
        return max(page)

    def extract_data_allpage(self,column_index):
        Xdownload = []
        lastpage = self.final_page()
        self.flip_to_page(1)
        while True:
            currentpage = self.current_page()
            Xdownload.extend(self.extract_data_1page(column_index))
            if currentpage == lastpage:
                break
            else:
                self.next_page()
        return Xdownload

    def filter(self, filter_object, value, dropdown = False):
        if dropdown:
            self.wait.until(EC.element_to_be_clickable((By.XPATH, f"//label[contains(text(),'{filter_object}')]/following::div[contains(@class, 'oxd-select-text-input')][1]"))).click()
            self.wait.until(EC.element_to_be_clickable((By.XPATH, f"//div[normalize-space() = '{value}']"))).click()
        else:
            label_box = self.wait.until(EC.element_to_be_clickable((By.XPATH, f"//label[contains(text(),'{filter_object}')]/following::input[1]")))
            label_box.clear()
            label_box.send_keys(value)

    def filter_search_click(self):
        self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))).click()
        self.wait.until(EC.presence_of_all_elements_located(self.rows))

    def filter_reset_click(self):
        self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='reset']"))).click()
        self.wait.until(EC.presence_of_all_elements_located(self.rows))

