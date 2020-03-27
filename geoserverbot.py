import sys
import logging
import traceback

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

from bs4 import BeautifulSoup

import json
import time
	


try:
	
	#Log Vars
	log_file = "geoserverbot.log"
	
	logger = logging.getLogger(__name__)
	logger.setLevel(logging.INFO)

	handler = logging.FileHandler(log_file)
	handler.setLevel(logging.INFO)

	formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
	handler.setFormatter(formatter)

	logger.addHandler(handler)
	
	
	
	#General Vars
	debug = True
	error_trace = True
	
	base_url = "http://192.168.10.185:9003/geoserver/web/"

	username = ""
	password = ""
	workspace = ""

	
	
	#Objects
	browser = None
	


	#Fonctions	
	def write_log(l, s):#l => 1: info, 2:warning, 3:error
		global debug
		
		logger.info('%s', str(s))
		
		if debug:
			print("LOG -> level:" + str(l) + " - " + str(s))
			
	def args_control():
		if len(sys.argv) != 4:
			write_log(2, "Args invalid" + str(sys.argv))
			sys.exit(1)
			
		write_log(1, "Args OK")
			
	def fill_vars():
		global browser, username, password, workspace
		username = sys.argv[1]
		password = sys.argv[2]
		workspace = sys.argv[3]
		
		browser = get_browser()
		
		write_log(1, "Vars filled")

	def get_browser():
		#options = webdriver.ChromeOptions()
		#options.add_argument('headless')
		#options.add_experimental_option('excludeSwitches', ['enable-logging'])

		#browser = webdriver.Chrome("chromedriver.exe", options=options)
		temp = webdriver.Chrome("chromedriver.exe") 		
		write_log(1, "Browser created")		
		return temp
	
	def go_to_page(url):
		global browser
		browser.get(url)
		write_log(1, "Go url: " + url)
	
	def open_home_page():
		global base_url
		go_to_page(base_url)
		write_log(1, "Went home page")
		
	def login():
		global browser, username, password
		
		browser.find_element_by_id("username").send_keys(username)
		browser.find_element_by_id("password").send_keys(password)
		
		browser.find_elements_by_css_selector("button[type='submit']")[0].click()
		
	def open_workspaces_page():
		global base_url
		url = base_url + "wicket/bookmarkable/org.geoserver.web.data.workspace.WorkspacePage"
		go_to_page(url)
		
		write_log(1, "Went workspaces page")
		
	def open_workspace_form():
		global browser, workspace
		browser.find_element_by_link_text(workspace).click()
		
	def check_and_save_workspace_form():
		global browser
		
		checks = ["settings:enabled", "services:services:1:enabled", "services:services:2:enabled"]
		
		for check in checks:
			temp = browser.find_elements_by_css_selector("input[name='"+check+"']")[0]
			if(temp.is_selected()):
				continue;
			
			temp.click()	
		
		links = browser.find_elements_by_xpath("//a[@href]")
		for link in links:
			if link.text == "Sakla" or link.text == "Save":
				link.click()
				break;
				
	def update_workspace():
		open_workspaces_page()
		open_workspace_form()
		check_and_save_workspace_form()
		
	def close_browser():
		global browser	
		browser.quit()
		
		write_log(1, "Browser closed")
	
	def main():
		write_log(1, "Started")
		
		args_control()
		fill_vars()
		
		open_home_page()
		login()
		update_wokspace()
						
		close_browser()

	#Main
	if __name__ == "__main__":
		main()


	
except SystemExit as e:
	sys.exit(e)
	
except Exception as e:
	try:
		write_log(3, "Error handled")
	except Exception as ee:
		def write_log(l, s):
			m = "Level: " + str(l) + " - " + str(s)
			print(m)
			with open(log_file, "a") as f:
				f.write(m)
				
		write_log(3, "Error handled")
	
	exc_type, exc_obj, exc_tb = sys.exc_info()	
	write_log(3, "General error! " + str(e) + " (line: " + str(exc_tb.tb_lineno) + ")")
	
	if error_trace:
		print(traceback.print_exc())