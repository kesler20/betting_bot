import numpy as np
from matplotlib import pyplot as plt
import selenium
from selenium import webdriver as wb
import time
from os import path as ps
x = ps.abspath('msedgedriver.exe')
driver = wb.Edge(x)
import json
import requests

API_KEY = 'f52278ae74d96840245116b31aeef838'
SPORT = 'upcoming' # use the sport_key from the /sports endpoint below, or use 'upcoming' to see the next 8 games across all sports
REGION = 'uk' # uk | us | eu | au
MARKET = 'h2h' # h2h | spreads | totals

def error_handler_decorator(func, *a, **kw):
    def wrapper(*a, **kw):
        try:
            container = func(*a, **kw)
            return container
        except selenium.common.exceptions.ElementNotInteractableException:
            try:
                input_field = driver.find_element_by_id('username')
                input_field.send_keys('uchekesla@gmail.com')
            except Exception:
                try:
                    input_field = driver.find_element_by_id('password')
                    input_field.send_keys('utomiwill@20')
                except Exception:
                    input_field = driver.find_element_by_class_name(a[2]) #send the classname as first input and the keys to the input field as the second  a = [normal_input, attribute, value]
                    input_field.send_keys(a[3])
        except selenium.common.exceptions.InvalidSelectorException: 
            pass
    return wrapper

@error_handler_decorator
def click_button(*a):
    button = driver.find_element_by_xpath(a[0])
    button.click()

@error_handler_decorator
def input_operations(*a):
    input_box = driver.find_element_by_xpath(a[0])
    input_box.send_keys(a[1])

def initialize_betting_bot():
    sports_response = requests.get('https://api.the-odds-api.com/v3/sports', params={
        'api_key': API_KEY
    })

    sports_json = json.loads(sports_response.text)

    if not sports_json['success']:
        print(sports_json['msg'])

    else:
        print('List of in season sports:', sports_json['data'])

    odds_response = requests.get('https://api.the-odds-api.com/v3/odds', params={
        'api_key': API_KEY,
        'sport': 'soccer',
        'region': REGION,
        'mkt': MARKET,
    })

    odds_json = json.loads(odds_response.text)

    if not odds_json['success']:
        print(odds_json['msg'])

    else:
        print('Number of events:', len(odds_json['data']))
        print(odds_json['data'])

        # Check your usage
        print('Remaining requests', odds_response.headers['x-requests-remaining'])
        print('Used requests', odds_response.headers['x-requests-used'])

alpha = 0.99
beta = 1.2
p = lambda x: 1/((1 + alpha*x)**beta)
x0 = np.linspace(0,10)
F = p(x0)
plt.plot(F)
plt.show()

driver.get('https://promotion.williamhill.com/uk/sports/general/ppc/m50/multi?utm_admap=d_ppce_whs&utm_offer=f_m50&utm_source=MICROSOFT&utm_medium=cpc&utm_campaign=Brand+-+WH+-+All+-+All+-+Pure+-+ACQ+-+Desktop+-+Exact+-+%5BWilliam+Hill%5D-UK&utm_term=william+hill&utm_content=81570106612724&utm_targetcountry=uk&utm_profile=j_700000001650943&utm_banner=h_71700000034259901g_58700003941442173i_81570106612724&gclid=18af9957bfe011c8980ef868764de996&gclsrc=3p.ds&msclkid=18af9957bfe011c8980ef868764de996')
click_button('//*[@id="hs_cos_wrapper_button_login"]/a')
time.sleep(3)
click_button('//*[@id="header-root"]/div/div/div/div[1]/div/div/div[2]/div/div[1]/button/span')
time.sleep(3)


input_operations('uchekesla@gmail.com','//*[@id="username"]/div[1]/div[2]','username','uchekesla@gmail.com') 
input_operations('utomiwill@20','//*[@id="password"]/div[1]/div[2]/input',"password",'utomiwill@20') 
click_button('/html/body/div[12]/div/div/div/div/div/div/section/div/div[2]/div[2]/form/div/button')
time.sleep(3)
