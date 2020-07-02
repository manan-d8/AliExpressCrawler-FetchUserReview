"""
created by : Manan Darji 
email : manan8999@gmail.com

This code works fine on date : [02/07/2020]
if not work for you just cheak class names and xpaths are still correct or changed in orignal website
"""
from selenium import webdriver
import pandas as pd
import time

def FetchAndStore():
	try:
		global cmtno

		comments_holder = driver.find_element_by_class_name('feedback-list-wrap')
		print(comments_holder)

		comments = comments_holder.find_elements_by_class_name('feedback-item')

		print(len(comments))
		for i,comment in enumerate(comments):
			try:
				print('='*100)
				# user info  /  name   / country
				userinfo = comment.find_element_by_class_name('fb-user-info')
				user_info_data = userinfo.text.split('\n')
				user_name = user_info_data[0]
				user_country = user_info_data[1]
				feedback_main = comment.find_element_by_class_name('fb-main')
				print("User Name :",user_name , "User Country : ", user_country)
				# comment_data   /    date    
				feedback_content = feedback_main.find_element_by_class_name('buyer-feedback')
				feedback_content_feed_list = feedback_content.find_elements_by_css_selector("*")
				user_feedback_data = feedback_content_feed_list[0].text
				user_feedback_date = feedback_content_feed_list[1].text
				print("Comment :")
				print(user_feedback_data)
				print("Date : ", user_feedback_date)

				feedback_helpful = feedback_main.find_element_by_class_name('j-digg-info-new')
				# helpfull comment   / yes    /no
				feedback_helpful_Yes = feedback_helpful.find_element_by_class_name('thf-digg-useful')
				user_feedback_helpful_yes = int(str(feedback_helpful_Yes.text.split(' ')[1])[1])
				feedback_helpful_No = feedback_helpful.find_element_by_class_name('thf-digg-useless')
				user_feedback_helpful_no = int(str(feedback_helpful_No.text.split(' ')[1])[1])
				print("Comment Helpfull  | Yes : ",user_feedback_helpful_yes ,' | No :', user_feedback_helpful_no)

				#   rate
				feedback_rate = feedback_main.find_element_by_class_name('star-view')
				feedback_rate_span = feedback_rate.find_elements_by_css_selector("*")
				rate = int(feedback_rate_span[0].get_attribute("style").split(':')[1].split('%')[0])//20
				print("Stars : ",rate," *"*rate)

				# product details
				feedback_product_info_div= feedback_main.find_element_by_class_name('user-order-info')
				feedback_product_info = feedback_product_info_div.find_elements_by_css_selector("*")
				product_info = dict()
				tempno = 2
				for info in feedback_product_info:
					if tempno%2==0:
						xdata = info.text.split(':')
						product_info[xdata[0]]= xdata[1]
					tempno+=1
				print("Product Details : ",product_info)
				cmtno+=1
				csv_doc.loc[cmtno] = [ user_feedback_date,user_name,user_country,user_feedback_helpful_yes,user_feedback_helpful_no ,rate,product_info ,user_feedback_data]
			except Exception as e:
				print("Exception : ",e)
	except Exception as e:
		print("*"*50)
		print("Exception : ",e)
		print("please cheak the site if reviews even Exist...!")
		print("*"*50)
		
def LoadPages(Url,x):
	for i in range(x):
		FetchAndStore()
		try:
			if(i!=(x-1)):
				nextbut = driver.find_elements_by_xpath('/html/body/div/div[6]/div/div/a[4]')
				nextbut[0].click()
				time.sleep(1)
		except IndexError as e:
			print("*"*50)
			print("No More reviews Left to Scrappe :)")
			print("Exception : ",e)
			print("*"*50)

			return 0
		except Exception as e:
			print("*"*50)
			print("Exception : ",e)
			print("*"*50)
			return 0

Url = input("Enter URL :")
noOfPage= int(input("No. Of Page :"))

driver = webdriver.Chrome('./chromedriver')

csv_doc = pd.DataFrame(columns = ['date','user_name','user_conutry','helpfull comment','not helpfull comment','stars x/5','product_info','comments']) 
docname=''
cmtno = 0

driver.get(Url)	

time.sleep(3)
try:
	popup_close = driver.find_element_by_class_name("next-dialog-close")
	popup_close.click()
except:
	pass
driver.execute_script("window.scrollTo(0, 500)") 

nametext = driver.find_element_by_class_name('product-title-text')
docname = nametext.text

iframe_comments = driver.find_elements_by_xpath('/html/body/div[5]/div/div[3]/div[2]/div[2]/div[1]/div/div[2]/div[2]/div/iframe')

url_new = iframe_comments[0].get_attribute('src')
driver.get(url_new)
LoadPages(Url , noOfPage)
csv_doc.to_csv('csv/'+docname+'.csv')




