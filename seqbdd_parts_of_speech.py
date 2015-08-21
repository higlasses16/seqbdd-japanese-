
# -*- coding: utf-8 -*-

# Python2.X encoding wrapper
import codecs,sys, MeCab, time, nltk, copy, subprocess
sys.stdout = codecs.getwriter('utf-8')(sys.stdout)
from node_arrange_ver_testset import *
# from node_arrange import *
# from get_example import *
global cache, mode
cache = {}
mode = 'b'
SAVE_PATH = "/Users/piranon/Documents/lab_report/Data/seqbdd(japanese)/"

def getnode(data, left, right, f0, f1):
	if right.data == '0':
		return left
	elif cache.has_key("<%s,%s,%s>" % (data, f0, f1)):
		# print "cache exist\n"
		return cache["<%s,%s,%s>" % (data, f0, f1)]
	
	new_node = Node('%s(%s)' %(data[0], data[1]))
	new_node.left = left
	new_node.right = right
	cache["<%s,%s,%s>" %(data, f0, f1)] = new_node

	return new_node


def seqbdd(f):
	
	# f0_word = u''
	# f1_word = u''
	
	f.sort()
	# print 'f = %s' %f
	f0 = []
	f1 = []
	if f == [[]]:	
		return Node('1')
	if f == []:		
		return Node('0')
	if f[0] == []:
		del f[0]
	x = f[0][0]

	for i in range(len(f)):
		if f[i][0] == x:
			f1.append(f[i][1:])
		else:
			f0.append(f[i][:])

	# for w in f0:
	# 	f0_word += '%s, ' %w
	# for w in f1:
	# 	f1_word += '%s, ' %w

	# print 'Getnode(%s, f0[%s], f1[%s])' %(x, f0_word, f1_word)

	r  = getnode(x, seqbdd(f0), seqbdd(f1), f0, f1)

	# global num
	# num += 1
	# r.test_print()
	# r.print_tree(num)
	return r

def nltk_tagger(file):
	f = codecs.open(file, 'r', 'utf-8')
	word_tagged = []
	for line in f.readlines():
		line = nltk.word_tokenize(line)
		word_tagged.append(nltk.pos_tag(line))
	f.close()
	return word_tagged

def mecab_tagger(file):
	tagger = MeCab.Tagger('-Ochasen')
	f = codecs.open(file)
	tagged = []
	for line in f.readlines():
		# enc = line.encode('utf-8')
		node = tagger.parseToNode(line)
		line_tagged = []
		while node:
			if node.feature.split(",")[1] == "格助詞":
				line_tagged.append((u"%s" %node.surface, "%s" %(node.feature.split(",")[7] + node.feature.split(",")[1])))
			elif node.feature.split(",")[1] != "*":
				if node.feature.split(",")[0] in node.feature.split(",")[1]:
					line_tagged.append((u"%s" %node.surface, "%s" %node.feature.split(",")[1]))
				else:
					line_tagged.append((u"%s" %node.surface, "%s%s" %(node.feature.split(",")[1], node.feature.split(",")[0]))) 
			else:
				line_tagged.append((u"%s" %node.surface, "%s" %node.feature.split(",")[0]))
			node = node.next
		tagged.append(line_tagged[1:-1])
	return tagged


def remove_word(sentences):
	for words in sentences:
		for w in words:
			del w[0]
	return sentences

def set_list(nest):
	temp = []
	for words in nest:
		if words not in temp:
			temp.append(words)
	return temp



def numbering(sentences, mode):
	for words in sentences:
		for i in range(len(words)):
			words[i] = list(words[i])
			if words[i][1] == ':':
				words[i][1] = 'ETC'
			if mode == 'a':
				words[i].append(u'%s' %i)
			else:
				words[i].append(u'%s' %(len(words) - i - 1))
	return sentences
def reset():
	global cache
	cache = {}
	if mode == 'a':
		after_tree = None
	else:
		before_tree = None

def mkdot(file):
	f = codecs.open(file, 'r', 'utf-8')
	l = []
	for line in f.readlines():
		l.append(line.replace(u"label=", u"label=\"").replace(u"];", u"\"];"))

	f.close()
	f = codecs.open(file, 'w', 'utf-8')
	f.writelines(l)
	f.close()

def output_jpeg(query):
	subprocess.call(['dot','-Tjpg','dot/%s.dot' %query,'-o','img/%s.jpg' %query])
	subprocess.call(['open','img/%s.jpg' %query])


def main(w):
	"""
	ctr_dic = load_contractions()
	# print ctr_dic
	split_text('sample_afraid.txt', u'afraid')
	sys.exit()
	"""
	"""
	words = get_word('answer_word_1.txt')
	for w in words:
	"""
	# w = unicode(raw_input("query >> "), 'utf-8')

	#sample_words = get_ex_sentence(w)
	sample_words = 1

	if sample_words:
		s = time.clock()
		# query = u'%s' %w[0].split(' ')[0]
		query = 'aozowa_hiyasu'
		# word_with_tag = nltk_tagger('%s.txt' %u'_'.join(w[0].split(' ')))

		# word_eng = nltk_tagger('test.txt')
		# print type(word_eng[0][0][0]), type(word_eng[0][0][1])
		word_jp = mecab_tagger('input_text/aozora_hiyasu.input.text')
		# print type(word_jp[0][0][0]), type(word_jp[0][0][1])


		"""
		before_query = []
		after_query = []
		for i in range(len(word_with_tag)):
			for j in range(len(word_with_tag[i])):
				if word_with_tag[i][j][0] == query:
					after_query.append(word_with_tag[i][j:])
					before_query.append(word_with_tag[i][:j])
		"""
		cache = {}
		if mode == 'a':
			# after_numed = numbering(word_eng, 'a')
			after_numed = numbering(word_jp, 'a')
			# after_numed = numbering(word_with_tag, 'a')

			rank_a = copy.deepcopy(after_numed)
			after = set_list(remove_word(after_numed))
			after_tree = seqbdd(after)
		else:
			before_numed = numbering(word_jp, 'b')
			rank_b = copy.deepcopy(before_numed)
			before = set_list(remove_word(before_numed))
			before_tree = seqbdd(before)
		e = time.clock()
		print "\nseqbdd make:%.3f [sec]" %(e - s)
		

		s = time.clock()
		if mode == 'a':
			graph =	after_tree.make_graph(query)
			graph =	after_tree.print_tree(graph)
			# after_tree.test_output('%s_test.jpeg' %query)
			for sentence in rank_a:
				graph = after_tree.rank(sentence, graph)
			graph_com = after_tree.remove_rank1(graph, query)
			graph_com = after_tree.node_compress(graph_com)

			####出力####
			after_tree.dot_output('dot/%s.dot' %query, graph_com)
			mkdot('dot/%s.dot' %query)
			after_tree.output('img/%s_test.jpeg' %query, graph)
			output_jpeg(query)
			after_tree.reset_graph()

		else:
			graph = before_tree.make_graph(query)
			graph = before_tree.print_tree(graph)
			for sentence in rank_b:
				graph = before_tree.rank(sentence, graph)
			graph_com = before_tree.remove_rank1(graph, query)
			graph_com = before_tree.node_compress(graph_com)

			# pattern = [query]
			# before_tree.get_patterns(graph_com, query, pattern, [], 0)


			###出力###	
			# before_tree.output()

			before_tree.dot_output('dot/%s.dot' %query, graph_com)
			mkdot('dot/%s.dot' %query)
			# before_tree.output('%s_before.jpeg' %query)
			output_jpeg(query)
			before_tree.reset_graph()

		e = time.clock()
		print "output seqbdd image:%.3f [sec]" % (e - s)
		reset()

if __name__ == '__main__':
	w = 'test'
	main(w)
