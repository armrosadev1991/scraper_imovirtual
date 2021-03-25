from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd

DRIVER_PATH = 'C:\\Users\\anton\\PycharmProjects\\cesd\\venv\\chromedriver.exe'
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome(options=chrome_options,executable_path=DRIVER_PATH)
driver.get('https://www.imovirtual.com/')

driver.implicitly_wait(10)
driver.find_element_by_id("onetrust-accept-btn-handler").click();

""" 
change the next two lines if u just want to search for a specific city, in this case Setúbal in the xpath of the var select_option_city
"""
#search_box = driver.find_element_by_id('downshift-0-label').click()
#select_option_city= driver.find_element_by_xpath('/html/body/main/section[1]/div/div/div/div/div/form/div[1]/div[2]/div/div/div/div[2]/ul/li[27]/div/span').click()

driver.implicitly_wait(5)
button_search = driver.find_element_by_xpath("/html/body/main/section[1]/div/div/div/div/div/form/div[1]/div[3]/button")
driver.execute_script("arguments[0].click();", button_search)

num_of_pages=driver.find_element_by_xpath('//*[@id="pagerForm"]/ul/li[5]/a').text

apartments_list = []
for i in range(int(num_of_pages)):
    print(i)
    driver.implicitly_wait(5)
    houses = driver.find_elements_by_tag_name('article')

    for house in houses:
        lis=house.find_elements_by_tag_name('li')
        description = house.find_element_by_tag_name('p').text
        word_to_split = ":"
        if word_to_split in description:
            description = description.split(word_to_split)[1].strip()

        info_array=[]
        for li in lis:
            info_array.append(li.text)

        if len(info_array)>6:
            house_item = {
                'city': description.split(", ")[-1],
                'detailed_location': description,
                'tipology': info_array[1],
                'price': info_array[2],
                'area': info_array[3],
                'area_per_square_meter': info_array[4],
                'bathrooms': info_array[5],
                'apartament_state':info_array[6]
            }

        apartments_list.append(house_item)

    driver.find_element_by_class_name('pager-next').find_element_by_tag_name('a').click()

df=pd.DataFrame(apartments_list)
df.to_csv("houses.csv")