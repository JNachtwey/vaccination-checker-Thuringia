import time
from selenium import webdriver
from selenium.common.exceptions import NoAlertPresentException, UnexpectedAlertPresentException
from selenium.webdriver.support.ui import Select
import ctypes




# 1.Step: Define here your locations (Impfzentren) which needs to checked
targetLocations = {"Leinefelde", "Mühlhausen", "Nordhausen"}

alerttext = """Leider gibt es für die gewählte Indikation zurzeit keine Impfstellen mit buchbaren Terminen."""

def Mbox(title, text, style):
    return ctypes.windll.user32.MessageBoxW(0, text, title, style)


def check_vaccine(driver):
    # webpage
    text: str = None

    try:
        driver.get("https://www.impfen-thueringen.de/terminvergabe/index.php")

# 2.Step: First Indication
        # Click on Indikation Beruf
        driver.find_element_by_xpath('//*[@id="select2-select-indi-container"]').click()

        # Find options to select
        indication = Select(driver.find_element_by_name("ID_LIB_Indikation"))
        time.sleep(2)

# 3.Step: Sub Indication
        # Select Indication
        indication.select_by_visible_text("Berufliche Indikation | Nachweis erforderlich!")
        time.sleep(2)

        # Select Sub Indication
        subindication = Select(driver.find_element_by_name("ID_LIB_Indikation_Sub"))
        subindication.select_by_visible_text(
        "Personal mit hohem Expositionsrisiko in medizinischen Einrichtungen/ Pflegeeinrichtungen mit Patientenkontakt")

        # Catch locations
        location_list: Select = Select(driver.find_element_by_name("ID_LIB_Ort"))

        # Catch Alert
        alertFired: bool = True
        unexpectedalert: bool = True

        driver.switch_to.alert
        text = driver.switch_to.alert.text
        driver.switch_to.alert.accept()
    except NoAlertPresentException:
        alertFired = False
        pass
    except UnexpectedAlertPresentException:
        alertFired = True
        unexpectedalert = True
        print()
        pass

    if alertFired is True and unexpectedalert is False and alerttext in text:
        print("No vaccination available")
        print(text)
        return False
    elif alertFired is True and unexpectedalert is True:
        print("No vaccination available")
        return False
    elif location_list is not None:

        for location in location_list.options:
            if location.text is not None:
                if check_location(location.text) is True:
                    Mbox('Stoff steht bereit', location.text, 1)
                    return True


def check_location(checkingLocation: str):
    for targetLocation in targetLocations:
        print("checking " + targetLocation + " in " + checkingLocation  )
        if targetLocation in checkingLocation:
            print(checkingLocation)
            return True

def main():
    driver = webdriver
    options = webdriver.ChromeOptions()
    options.add_argument("no-sandbox")
    options.add_argument("--disable-setuid-sandbox")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--enable-automation=false")
    options.add_argument("--headless")

    result = False
    while result is not True:
        driver = webdriver.Chrome(executable_path="/Users/Jo/AppData/Local/Programs/Python/Python38/chromedriver.exe",  options=options)
        driver.implicitly_wait(300)

        result = check_vaccine(driver)
        time.sleep(300)  # wait 5 minutes before next crawl
        driver.close()
        driver.quit()

if __name__ == "__main__":
    main()
