# -*- coding: utf-8 -*-

# Python2.X encoding wrapper
import codecs,sys
sys.stdout = codecs.getwriter('utf-8')(sys.stdout)

def main(q):
	f = codecs.open('aozora_%s.text' %q, 'r', 'utf-8')
	l = []
	for line in f.readlines():
		l.append(line.split('冷やす')[0].strip()+'冷やす\n')
	f.close()

	f = codecs.open('aozora_%s.input.text' %q, 'w', 'utf-8')
	f.writelines(l)
	f.close()
if __name__ == '__main__':
	query = 'hiyasu'
	main(query)