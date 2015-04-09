import urllib2,json,sys
from datetime import date, timedelta
from itertools import cycle

def defineDate(d):
	d=d.split("T")[0].split("-")
	y=int(d[0])
	m=int(d[1])
	d=int(d[2])
	return date(y,m,d)

global doc,i
output=sys.argv[1]
try:
	f = file(sys.argv[2], 'r')
	f = f.read()
	doc=json.loads(f)
	now=defineDate(doc[len(doc)-1]["pub_date"])-timedelta(days=1)
	doc=[]
except:
	doc=[]
	now=date.today()
apis=[
	"fbf0a8d4d2ee7a1da3cc16ae1fc34241:3:64789311",
	"4cb36df77426d67fb3f61601644e49ca:17:64789311"
	]
url="http://api.nytimes.com/svc/search/v2/articlesearch.json?sort=newest&fl=headline%2Cpub_date&api-key=<sample-key>&page=<page>&fq=source:(%22The%20New%20York%20Times%22),document_type:(%22article%22)&begin_date=<_b_>&end_date=<_e_>"
out = file(output, 'w')
i = cycle(range(2))
end=date(2011,12,31)
currentLen=len(doc)

def stringify(d):
	return str(d.year)+('%02d' % d.month)+('%02d' % d.day)

def query(e,b,offset):
	global doc,i
	current=url.replace("<sample-key>",apis[i.next()]).replace("<_b_>",b).replace("<_e_>",e).replace("<page>",str(offset))
	request = urllib2.Request(current)
	response = urllib2.urlopen(request)
	data=response.read()
	data=json.loads(data)
	doc=doc+data["response"]["docs"]
	offset=offset+1
	hits=int(data["response"]["meta"]["hits"])
	currentLen=len(doc)
	return (currentLen,offset,hits)

while end<now:
	e=stringify(now)
	b=stringify(now-timedelta(days=1))
	offset=0
	hits=100000000
	lenB=len(doc)
	while hits>(offset*10):
		(currentLen,offset,hits)=query(e,b,offset)
	now=now-timedelta(days=2)
	print "Got "+str(len(doc)-lenB)+" documents for "+b+" to "+e+". "+str(len(doc))+" docs in total."
	out.seek(0,0)
	out.write(json.dumps(doc))


out.close()