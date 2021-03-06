# -*- coding: utf-8 -*-

# Author: Xuzhou Yin 
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
import urllib
from selenium import webdriver
import datetime
import time as systime
from selenium.webdriver.firefox.webdriver import FirefoxProfile
import unicodecsv as csv
import re

base_url = 'http://s.weibo.com/weibo/'
file = "query"
file_index = 6
def scrap():
	global file_index
	with open('query.txt') as f:
		each_query = f.readlines()
	each_query = [x.strip() for x in each_query]
	# print urllib.quote(urllib.quote(each_query[0]))
	for each in each_query:
		query = each
		s = each.split(';')
		keyword = s[0]# urllib.quote(urllib.quote(s[0]))
		date = s[1]
		start = s[2]
		end = s[3]
		page = s[4]
		scrap_each_query(keyword, date, start, end, page, query)
		file_index = file_index + 1

def scrap_each_query(keyword, date, start, end, page, query):
	real_keyword = keyword
	keyword = urllib.quote(urllib.quote(keyword))
	# login_url = 'http://m.weibo.com/'
	# driver = webdriver.Chrome()
	# driver.get(login_url)
	# driver.implicitly_wait(2)
	# string = '登录'
	# driver.find_element_by_link_text ( string.decode('utf-8') ).click()
	# driver.implicitly_wait(2)
	# driver.find_element_by_link_text(string.decode('utf-8') ).click()
	# savedCookies = driver.get_cookies()
	# # login code
	# pickle.dump(driver.get_cookies() , open("chrome.pkl","wb"))
	# driver.close()
	all_content = []
	all_time = []
	userid = []
        profile = FirefoxProfile("/home/gian/.mozilla/firefox/s7kyhk24.default")
	driver = webdriver.Firefox(profile)
	# co = webdriver.ChromeOptions()
	# co.add_argument('user-data-dir=/Users/xuzhouyin/Library/Application Support/Google/Chrome/')
	# driver = webdriver.Chrome(chrome_options = co)
	url = base_url + keyword + "&typeall=1&suball=1&timescope=custom:" + start + ":" + end + "&page=" + "1"
	driver.get(url)
	systime.sleep(5)
	for i in range(int(page)):
		url = base_url + keyword + "&typeall=1&suball=1&timescope=custom:" + start + ":" + end + "&page=" + str(i + 1)
		# url = "http://s.weibo.com/weibo/%25E5%2585%2583%25E6%2597%25A6&typeall=1&suball=1&timescope=custom:2016-12-31:2016-12-31&Refer=g"
		# chrome_options = Options()
		# chrome_options.add_argument("~/Library/Application Support/Google/Chrome/Default");
		# co = webdriver.ChromeOptions()
		# co.add_argument('/Users/xuzhouyin/Library/Application\ Support/Google/Chrome/Default')
		
		# for cookie in pickle.load(open("chrome.pkl", "rb")):
		# 	driver.add_cookie(cookie)
		driver.get(url)
		
		# driver.magage().add_cookie(savedCookies)
		page_source = driver.page_source
		soup = BeautifulSoup(page_source, "html.parser")
		content = soup.findAll("p", { "class" : "comment_txt" })
		time = soup.findAll("a", { "class" : "W_textb" })
                
                try:
                    userid = re.search('nick-name="(.*?)"', str(content[0])).group(1)
                except:
                    userid = 'anon'

		for each in content:
			all_content.append(each.get_text().encode('utf-8'))
		for each in time:
			each = each.get_text()
			each = each.encode('utf-8')
			time = ""
                        print each
			if "月" in each:
				time = str(datetime.datetime.now().year) + "-" + each[0:each.index("月")] + "-" + each[(each.index("月") + 3):each.index("日")]
			else:
				time = each[0:each.index("")]
			all_time.append(time)
	driver.close()
	save_to_csv(file + str(file_index), real_keyword, date, all_content, all_time, query, userid)

def save_to_csv(filename, keyword, date, content, time, query, userid):
	with open('./output/' + filename + '.csv', 'w') as csvfile:
	    spamwriter = csv.writer(csvfile, dialect='excel', encoding='utf-16')
	    spamwriter.writerow(["query", "User ID", "Post Content", "Post ID", "keyword", "event Date", "Post Time"])
	    for i in range(len(content)):
	    	spamwriter.writerow([query, userid, content[i], i + 1, keyword, date, time[i]])

scrap()


#url = base_url + keyword + "&typeall=1&suball=1&timescope=custom:" + start + ":" + end + "&page=" + str(int(page) + 1)
# driver = webdriver.Chrome()
# driver.get("http://s.weibo.com/weibo/%25E5%2585%2583%25E6%2597%25A6&typeall=1&suball=1&timescope=custom:2016-12-31:2016-12-31&Refer=g")
# page_source = driver.page_source
