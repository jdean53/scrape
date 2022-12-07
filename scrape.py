import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import os
import datetime as datetime

'''Doing a Python Module like this allows you to bring it in as a module or run as it's own script from cmd'''

def scrape():
    link = "https://www.ishares.com/us/products/239566/ishares-iboxx-investment-grade-corporate-bond-etf/1467271812596.ajax?fileType=csv&fileName=LQD_holdings&dataType=fund"         # This is the link just with one page, scroll donw and you will see it. 
    path = r"C:\Users\jdean\OneDrive\Documents\scrape\data"                                                     # For some reason have to use a literal and complete path

    # Setting up the options for driver 
    options = webdriver.ChromeOptions()                                                                         # Options class for selenium
    options.headless = True                                 # Just so a Chrome window doesn't pop up
    prefs ={"download.default_directory" : path}            # where we are going to save the downloaded file
    options.add_experimental_option("prefs",prefs)          # Adding the "save to this directory" option to the driver instance

    print(os.getcwd())
    if os.path.exists(r"C:\Users\jdean\chromedriver"): print('exists')
    else: print('the limit does not exist')
    # Go download a chrome driver for selenium aka google "selenium chrome driver and select the correct one for your system"                                          
    # https://chromedriver.chromium.org/downloads
    d = webdriver.Chrome(executable_path=r'C:\Users\jdean\chromedriver', options=options)     # Calling the instance of the driver            
    d.get(link)                             # Go to this link, going to this link will download the file
    time.sleep(1) 
    d.quit()                                # Quite after this is done 

    # Bringing in and manipulating the file
    file_name = os.listdir(path)    # Getting the file name                  

    allocations = pd.read_csv(
        path + '\\' + file_name[0],   # File name is a string so just have to get the element in the string
                                    # There is only one sheet in this file so no need foir declaring the sheet name 
        skiprows=9,                 # No need to get the stuff at the top so skipping those rows
        index_col='Name'            # Just setting the index this is up to you
        )          

    # There is a cell at the end with some legal jargon and a empty row above that so I delete those from the data frame
    allocations = allocations.iloc[:-2]

    # You are going to have to delete the original file we download or next time it won't work 
    # So I am thinking we just save this new file as 'Holdings_as_of_{insert date}.csv' so we have all of them. 
    # Later, since I going to be building a massive thing doing jsut this, I am going to create one with all holdings over time but that's up to you.

    # Saving the new file
    today = datetime.date.today().strftime('%Y_%m_%d')      # Todays date in CSV format friendly way
    new_file_name = 'LQD_Holdings_as_of_' + today + '.csv'  # New file name
    allocations.to_csv(path + '\\' + new_file_name)

    # Deleting the file we brought in
    os.remove(path + '\\' + file_name[0])


if __name__ == "__main__":
    scrape()
