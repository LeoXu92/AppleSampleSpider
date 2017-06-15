#coding: utf-8

import requests
import json
import sys
import datetime
import os
from contextlib import closing

def all_sample_code():
	'''
	library.json来源于https://developer.apple.com/library/content/navigation/library.json
	"columns": { "name"       :  0,
             "id"         :  1,
             "type"       :  2,
             "date"       :  3, 
             "updateSize" :  4,
             "topic"      :  5,
             "framework"  :  6,
             "release"    :  7,
             "subtopic"   :  8,
             "url"        :  9,
             "sortOrder"  : 10,
             "displayDate": 11,
             "platform"   : 12,
           },
    但是columns中platform后面多了一个逗号，不符合json，需要删掉。
	'''
	f = open('library.json', 'r+')
	return json.loads(f.read(), strict=False)


def get_download_url(item):
	name = item[9].split('/')[2]
	book_url = 'https://developer.apple.com/library/content/samplecode/%s/book.json' % name
	r = requests.get(url=book_url)
	print book_url
	download_url = 'https://developer.apple.com/library/content/samplecode/%s/%s' % (name ,r.json()['sampleCode'])
	return download_url.encode("utf-8")

def download_file(url, path):
	if not os.path.exists(path):
		os.makedirs(path)
	start = datetime.datetime.now().replace(microsecond=0)
	filename = url.split('/')[-1]
	filepath = os.path.join(path,filename)
	with closing(requests.get(url, stream=True)) as response:
		chunk_size = 1024 # 单次请求最大值
		content_size = int(response.headers['content-length'])
 		with open(filepath, "wb") as file:
 			for data in response.iter_content(chunk_size=chunk_size):
 				file.write(data)
	end = datetime.datetime.now().replace(microsecond=0)
	print '%s下载完成，用时：%s' % (filename, end-start)

if __name__ == '__main__':
	codes = all_sample_code()
	for x in codes['documents']:
		if x[2] == 5:
			download_url = get_download_url(x)
			print 'download url:', download_url
			download_file(download_url, 'files')