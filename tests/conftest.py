from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pytest
from POM.PSce import OrangeHRM

@pytest.fixture
def driver(request):
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.maximize_window()

    driver.get("https://opensource-demo.orangehrmlive.com/")
    if request.node.get_closest_marker('login'):   # referring to pytest.py
        OrangeHRM(driver).login("Admin", "admin123")    # call out POM feature need to re-declare class. Here, no driver attach to class, so need to re-attach driver as well

    yield driver
    driver.quit()
