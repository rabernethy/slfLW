import selenium 
from selenium import webdriver
from datetime import date
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains



url='https://nomads.ncep.noaa.gov/cgi-bin/filter_naefsbc_ndgd.pl?dir=%2Fnaefs.{date}%2F00%2Fndgd_gb2'.format(date=date.today().strftime("%Y%m%d"))
print(url)
options = selenium.webdriver.firefox.options.Options()
options.setPreference("browser.download.folderList", 2);
options.setPreference("browser.download.dir", "/Downloads/");
options.setPreference("browser.download.useDownloadDir", true);
options.setPreference("browser.download.viewableInternally.enabledTypes", "");
options.setPreference("browser.helperApps.neverAsk.saveToDisk", "application/octet-stream");
options.add_argument('--headless')


driver = selenium.webdriver.Firefox(options=options)
driver.get(url)
driver.find_element_by_xpath('/html/body/form/p[5]/input[1]').click()
driver.find_element_by_xpath('/html/body/form/p[6]/input[1]').click()

driver.find_element_by_xpath('/html/body/form/p[10]/input[1]').click()

