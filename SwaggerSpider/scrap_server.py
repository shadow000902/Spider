# -*- coding: UTF-8 -*-
import os
import sys
import getopt
import requests
import json
import time

# 1. fetch root_api_doc
# 2. get root api infos and write to json file
# 3. from root api infos get every api_path
# 4. get api_path url info and write to child json file
# 5. format child json file and write to format file


# python test.py  arg1 arg2
# Accept:application/json;charset=utf-8,*/*
# Accept-Encoding:gzip, deflate
# Accept-Language:zh-CN,zh;q=0.8,en;q=0.6
# Connection:keep-alive
# Cookie:sgsa_id=souche.com|1477308440052807; gr_user_id=325c2771-20de-439f-b60d-73948efcb5a4; channel=website; _qddaz=QD.1efojk.umx22h.iunzawha; matchtype=2; locat_cost=0; __utma=121281372.640024446.1498020259.1498020259.1498026097.2; __utmb=121281372.4.7.1498026107584; __utmc=121281372; __utmz=121281372.1498026097.2.2.utmcsr=devsso.sqaproxy.souche.com|utmccn=(referral)|utmcmd=referral|utmcct=/redirect.htm; _security_token=1Lors_lTwr91t2Bi
# DNT:1
# Host:erp-dev2.sqaproxy.souche.com
# Referer:http://erp-dev2.sqaproxy.souche.com/api
# TT:
# User-Agent:Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Mobile Safari/537.36
# X-Requested-With:XMLHttpRequest
# server_url = 'http://erp-dev2.sqaproxy.souche.com/api-docs/souche/app-car-info?_=1498029958834'
server_url = 'http://erp.sqaproxy.souche.com/api-docs'
infoDict = {}


# server_url_info = server_url + '/souche/app-car-info'
# /souche/app-car-action
# + _:1498029958833 unix 时间戳


def make_file_path(request_ulr):
	import urlparse
	urlparse.urlparse(request_ulr)
	open_path = os.path.join(os.path.abspath('.'), 'output' + urlparse.urlparse(request_ulr).path)
	if not os.path.exists(open_path):
		os.makedirs(open_path)
	return open_path + '/res_output.json'


def write_info_to_file(res_text, file_path):
	reload(sys)
	sys.setdefaultencoding('utf-8')
	with open(file_path, 'w') as of:
		# unicode(info).encode('utf-8') 将unicode使用 utf-8编码处理中文字符
		print >> of, res_text.encode('utf-8')


def append_info_to_file(format_file_path, info):
	# print format_file_path
	with open(format_file_path, 'a') as of:
		# print info
		# unicode.encode('utf-8')
		print >> of, info.encode('utf-8')


def wide_chars(s):
	from unicodedata import east_asian_width
	"""return the extra width for wide characters
	ref: http://stackoverflow.com/a/23320535/1276501
	ref: https://blog.tankywoo.com/2017/01/21/python-cli-chinese-align-and-encoding-continue.html"""
	if isinstance(s, str):
		s = s.decode('utf-8')
	return sum(east_asian_width(x) in ('F', 'W') for x in s)


# 读取生成的接口JsonFile 生成对应格式的Info
# 订单中心 001 取消订单 /app/car/appcarsearchaction
def read_and_generate_format_file(file_path):
	format_file_path = os.path.join(os.path.dirname(file_path), infoDict['pathDescription'] + "_" + infoDict['itemDescription'] + '.csv')
	if os.path.exists(file_path):
		with open(file_path) as json_data:
			jsonInfo = json.load(json_data)
			if len(jsonInfo['apis']) > 0:
				for index, jsonItem in enumerate(jsonInfo['apis']):
					# append_info_to_file(
					# 	format_file_path,
					# 	infoDict['rootDescription']
					# 	+ '  '
					# 	+ infoDict['itemDescription']
					# 	+ '  '
					# 	+ '{num:03d}'.format(num=index + 1)
					# 	+ '  '
					# 	+ '{:<25}  {:<50}'.format(jsonItem['operations'][0]['summary'], jsonItem['description'])
					# 	+ jsonItem['path']
					# )
					append_info_to_file(
						format_file_path,
						infoDict['rootDescription']
						+ ', '
						+ infoDict['pathDescription']
						+ '_'
						+ infoDict['itemDescription']
						+ ', '
						+ '{num:03d}'.format(num=index + 1)
						+ '.'
						+ jsonItem['operations'][0]['summary'].encode('utf-8')
						+ '-'
						+ jsonItem['path']
					)


def read_root_api_doc_info(root_file_path):
	if os.path.exists(root_file_path):
		with open(root_file_path) as json_data:
			rootJsonInfo = json.load(json_data)
			return rootJsonInfo


def fetch_domain_url(request_ulr):
	cookies = {'_security_token': '1JAOf_1tcdBirk3a',
			   'sgsa_id': 'souche.com|1498324064174',
			   'gr_user_id': '325c2771-20de-439f-b60d-73948efcb5a4',
			   'channel': 'website',
			   '_qddaz': 'QD.1efojk.umx22h.iunzawha',
			   'matchtype': '2',
			   'locat_cost': '0',
			   '__utma': '121281372.640024446.1498020259.1498020259.1498026097.2',
			   '__utmb': '121281372.4.7.1498026107584',
			   '__utmc': '121281372',
			   '__utmz': '121281372.1498026097.2.2.utmcsr=devsso.sqaproxy.souche.com|utmccn=(referral)|utmcmd=referral|utmcct=/redirect.htm'
			   }
	headers = {'Accept': 'application/json;charset=utf-8,*/*',
			   'Accept-Encoding': 'gzip, deflate',
			   'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
			   'Connection': 'keep-alive',
			   'User-Agent': 'Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Mobile Safari/537.36',
			   'X-Requested-With': 'XMLHttpRequest',
			   'Host': 'erp.sqaproxy.souche.com',
			   'Referer': 'http://erp.sqaproxy.souche.com/api'
			   }
	params = {
		'_': time.time() * 1000
	}
	response = requests.get(request_ulr, params=params, headers=headers, cookies=cookies)
	return response


def save_res_info(response):
	# from pprint import pprint
	# pprint(response.headers)
	# pprint(response.encoding)
	# pprint(type(response.text))
	file_path = make_file_path(response.url)
	write_info_to_file(response.text, file_path)
	read_and_generate_format_file(file_path)


def make_root_doc_path():
	root_doc_path = os.path.join(os.path.abspath('.'), 'output/output_global_api.json')
	if not os.path.exists(os.path.dirname(root_doc_path)):
		os.mkdir(os.path.dirname(root_doc_path))
	return root_doc_path


def save_root_api_info(response):
	file_path = make_root_doc_path()
	write_info_to_file(response.text, file_path)


# ERP, app-car-info_车辆信息, 003.车辆详情-/app/car/appCarSearchAction/getCarDetail.json
def read_root_api_info():
	rootApiInfo = read_root_api_doc_info(make_root_doc_path())
	for index, item in enumerate(rootApiInfo['apis']):
		# ERP_API->ERP
		infoDict['rootDescription'] = rootApiInfo['info']['description'][:3]
		infoDict['itemDescription'] = item['description']
		# /souche/* -> *; 即取出/souche/后面的所有字符
		infoDict['pathDescription'] = item['path'][8:]
		print 'Output Info: From=> ', infoDict['rootDescription']
		print 'Output Info: Name=> ', infoDict['itemDescription']
		print 'Output Info: Path=> ', infoDict['pathDescription']
		print 'Output Info: Url=> ', server_url + item['path']
		save_res_info(fetch_domain_url(server_url + item['path']))


def fetch_with_session(request_url):
	pass


def fetch_with_ssl(request__https_url):
	res = requests.get(request__https_url, verify=True)
	pass


if __name__ == '__main__':
	print str(sys.argv)
	rootApiRes = fetch_domain_url(server_url)
	save_root_api_info(rootApiRes)
	read_root_api_info()
