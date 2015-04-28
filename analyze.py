import json, sys, collections, Levenshtein

global web,prnt,seo,webC,prntC,seoC,webL,prntL,seoL
web={}
prnt={}
seo={}
counts=[]

def analyze(f,y):
	global web,prnt,seo,counts
	webCY=[]
	prntCY=[]
	seoCY=[]
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
				if len(word)>0:
					if word in web:
						web[word]+=1
					else:
						web[word]=1
			for word in prntH:
				word=word.lower()
				if len(word)>0:
					if word in prnt:
						prnt[word]+=1
					else:
						prnt[word]=1
		if "seo" in article["headline"]:
			seoH=article["headline"]["seo"].split(" ")
			seoCY.append(len(seoH))
			for word in seoH:
				word=word.lower()
				if len(word)>0:
					if word in seo:
						seo[word]+=1
					else:
						seo[word]=1
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

web=collections.Counter(web)
prnt=collections.Counter(prnt)
seo=collections.Counter(seo)
print counts
print "\n"
print web.most_common(30)
print "\n"
print prnt.most_common(30)
print "\n"
print seo.most_common(30)


