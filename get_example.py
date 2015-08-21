
# -*- coding: utf-8 -*-

# Python2.X encoding wrapper
import codecs,sys, pycurl2, re
sys.stdout = codecs.getwriter('utf-8')(sys.stdout)

def get_word(file):
	f = codecs.open(file, 'rb', 'utf-8')
	word = []
	for line in f.readlines():
		w = line.strip().split('\t/\t')
		if u'some' in w[1]:
			word.append(w)
	return word

def get_ex_sentence(w):
	count = 1
	f1 = codecs.open('%s.txt' %u'_'.join(w[0].split(' ')), 'wb', 'utf-8')
	f1.close()
	while True:
		c = pycurl2.Curl()
		if count == 1:
			url = 'http://ejje.weblio.jp/sentence/content/%s' %'+'.join(w[0].split(' '))
		else:
			url = 'http://ejje.weblio.jp/sentence/content/%s/%d' %('+'.join(w[0].split(' ')), count)
		print url
		count += 1

		c.setopt(c.URL, str(url))
		f = open('test.txt', 'wb')
		c.setopt(c.WRITEDATA, f)
		c.perform()
		c.reset()
		f.close()

		sentences = read_url(w)
		if sentences == '0' and count == 0:
			print 'Can\'t find any sentence\n'
			return None
			break
		elif sentences == '1':
			print 'Can\'t find enough sentences\n'
			return None
			break
		elif sentences == '0' and count != 0:
			if snt_total(w) > 10:
				return 1
				break
			else:
				print 'Can\'t find enough sentences\n'
				return None
				break
		elif snt_total(w) > 40:
			return 1
			break
		elif count >= 5:
			return 1
			break

def read_url(w):
	l = u''
	flag = 0
	snt = []
	f = codecs.open('test.txt', 'r', 'utf-8')
	for line in f.readlines():
		if u'に一致する英語例文は見つかりませんでした' in line:
			return '0'
		elif u'部分一致の例文検索結果' in line:
			temp = re.split(r'<.*?>', line)
			print '例文:%s件' %temp[5]
			if int(temp[5]) < 15:
				return '1'
			else:
				flag = 1
		if flag == 1:
			l = l + line	
	for i in l.split(u'<div class=qotC>'):
		if i.startswith(u'<p class=qotCE>'):
			eng = re.split(r'<.*?>', i)
			s = u' '.join(eng).split('\n')[0].strip()[:-1].split(u'.')[0]
			if 20 < len(s) < 300 and not re.search(r'\W', u''.join(s.split(u' '))):
				snt.append(u'%s.\n' %re.sub('[ ]{2,}', ' ', s.strip().capitalize()))
	f.close()
	"""
	if len(snt) < 10:
		return '1'
	"""
	f1 = codecs.open('%s.txt' %u'_'.join(w[0].split(' ')), 'a', 'utf-8')
	f1.writelines(list(set(snt)))
	f1.close()

	return 1

def snt_total(w):
	f = codecs.open('%s.txt' %u'_'.join(w[0].split(' ')), 'rb', 'utf-8')
	num = len(f.readlines())
	f.close()
	return num