import time
from typing import Callable, Tuple
from selenium import webdriver

options = webdriver.ChromeOptions()
options.add_argument("--headless")


driver = webdriver.Chrome(executable_path="./drivers/chromedriver", chrome_options=options)

driver.get('https://br.investing.com/search/?q=FIIs&tab=articles')


def convergence_condition(
    driver: webdriver.Chrome, 
    last_step: int) -> Tuple[int, bool]:
   current_step = len(driver.find_elements_by_css_selector("a.title"))
   return current_step, last_step == current_step

def complete_loading(
    driver: webdriver.Chrome,
    convergence_condition: Callable,
    last_step: int = 0,
    partial_loading: int = 5) -> webdriver.Chrome:
    
    print(last_step)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(partial_loading)

    current_step, converged = convergence_condition(driver, last_step)

    if not converged:

        driver = complete_loading(
            driver=driver,
            convergence_condition=convergence_condition,
            last_step=current_step,
            partial_loading=partial_loading
        )
    
    return driver


driver = complete_loading(
    driver=driver,
    convergence_condition=convergence_condition,
    partial_loading=5
)

a = driver.find_elements_by_css_selector("div.articleItem")
print(driver.find_elements_by_css_selector("div.articleItem")[0].find_element_by_css_selector("a.title").get_attribute('href').split('/')[3])#, len(list(map(lambda x: x.get_attribute('href'), a))))

driver.quit()