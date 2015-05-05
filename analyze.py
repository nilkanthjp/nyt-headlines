import json, sys, collections, Levenshtein
from stop_words import get_stop_words

global web,prnt,seo,webC,prntC,seoC,webL,prntL,seoL,stop_words
web={}
prnt={}
seo={}
counts=[]
stop_words = get_stop_words('english')

def analyze(f,y):
	global web,prnt,seo,counts
	webCY=[]
	prntCY=[]
	seoCY=[]
	web[y]={}
	prnt[y]={}
	seo[y]={}
	for article in f:
		if "print_headline" in article["headline"] and "main" in article["headline"]:
			webH=article["headline"]["main"]
			prntH=article["headline"]["print_headline"]
			ratio=Levenshtein.ratio(webH.lower(),prntH.lower())
			webH=webH.split(" ")
			prntH=prntH.split(" ")
			webCY.append(len(webH))
			prntCY.append(len(prntH))
			for word in webH:
				word=word.lower()
				if word not in  stop_words:
					if len(word)>0:
						if word in web[y]:
							web[y][word]+=1
						else:
							web[y][word]=1
			for word in prntH:
				word=word.lower()
				if word not in  stop_words:
					if len(word)>0:
						if word in prnt[y]:
							prnt[y][word]+=1
						else:
							prnt[y][word]=1
		if "seo" in article["headline"]:
			seoH=article["headline"]["seo"].split(" ")
			seoCY.append(len(seoH))
			for word in seoH:
				word=word.lower()
				if word not in  stop_words:
					if len(word)>0:
						if word in seo[y]:
							seo[y][word]+=1
						else:
							seo[y][word]=1
	counts.append({
		"year":str(y),
		"print":float(sum(prntCY))/float(len(prntCY)),
		"web":float(sum(webCY))/float(len(webCY)),
		"seo":float(sum(seoCY))/float(len(seoCY))
	})

for y in range(2006,2016):
	f = "nyt"+str(y)+".json"
	f = open(f,'r')
	f = json.loads(f.read())
	analyze(f,y)
	web[y]=collections.Counter(web[y])
	prnt[y]=collections.Counter(prnt[y])
	seo[y]=collections.Counter(seo[y])

print counts

for y in range(2006,2016):
	print "\n"+str(y)
	print web[y].most_common(20)
	print prnt[y].most_common(20)
	print seo[y].most_common(20)


