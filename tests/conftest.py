from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import pytest
from POM.psce import OrangeHRM

@pytest.fixture
def driver(request):
    service = Service(ChromeDriverManager().install())

    chrome_options = Options()
    chrome_options.add_argument("--lang=en-US")

    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.maximize_window()

    driver.get("https://opensource-demo.orangehrmlive.com/")
    if request.node.get_closest_marker('login'):
        OrangeHRM(driver).login("Admin", "admin123")

    yield driver
    driver.quit()
