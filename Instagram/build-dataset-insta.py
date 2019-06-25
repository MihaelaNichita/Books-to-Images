# Instagram different approach when checking if keywords match words in the description, 
# because multiple words can be brought together in one hashtag, so i will check for 
# the words in the description to be found in the ‘hashtags’ string (#lovemylife 
# goodvibes => “lovemylife goodvibes”) and add it to the cleared_keywords only if 
# it’s found. Also it needs to be separated.
# Careful for when the hashtags are added in a separated comment
# ! tags can be in the middle of the description - consider them as both part of 
# the description and keywords

# getting the code related to users’ posts in json files by using instagram-scraper.
 # It’s a command-line application written in Python that scrapes and downloads an 
 # instagram user's photos, videos, comments and other media metadata.


import json
import glob

usefuldata = []

def getJsonObjects(filename):
	global objs_dict
	# read file
	with open(filename, 'r',encoding = 'utf-8') as myfile:
	    data=myfile.read()

	# parse file
	objs_dict = json.loads(data)

	usefuldata2 = []
	usefuldata1 = [e['edge_media_to_caption']['edges'] for e in objs_dict['GraphImages']]
	for e in objs_dict['GraphImages']:
		if 'tags' not in e:
			usefuldata2.append([])
			continue
		usefuldata2.append(e['tags'])


	for e in usefuldata1:
		e.append(usefuldata2[usefuldata1.index(e)])

	return usefuldata1




# ['edge_media_to_caption']['edges']



def getJsonObjectsFromAllFiles():
	global usefuldata
	files=glob.glob("users/*.json")

	for filename in files:
		usefuldata += getJsonObjects(filename)

	# for e in usefuldata[100:110]:
	# 	# if dim is 2 then i have tags as well
	# 	print(e)



getJsonObjectsFromAllFiles()