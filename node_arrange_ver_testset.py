
# -*- coding: utf-8 -*-

# Python2.X encoding wrapper
import codecs,sys, os
sys.stdout = codecs.getwriter('utf-8')(sys.stdout)
import pydot
global i, parent, flag_0, patterns
i = 0
flag_0 = 0
patterns = []
from collections import Counter
from operator import itemgetter

class Node:
	"""
	木のクラス：左右の子と自分自身のデータを持つ
	"""
	def __init__(self, data):
		"""
		木構造
		"""
		self.data = data
		self.left = None
		self.right = None

	def insert(self, data):
		"""
		ノードの挿入メソッド
		"""
		if data < self.data:
			if self.left is None:
				self.left = Node(data)
			else:
				self.left.insert(data)
		elif data > self.data:
			if self.right is None:
				self.right = Node(data)
			else:
				self.right.insert(data)
	def make_graph(self, name):
		graph = pydot.Dot('%s' %name, graph_type='digraph')#, suppress_disconnected = True)
		return graph

	def search_parent_0(self, node):
		"""
		input: seqbdd, node(instance)
		output: node's parent
		"""

		if self.right == node:
			global parent            	#global変数 parentに見つけたparentを保存
			parent = self

		if self.left == node:	#0−枝のため再び探索
			if self == root: 	#親が根の場合
				global flag_0
				flag_0 = 1
				global parent
				parent = self
			else:				#通常操作
				global parent		
				parent = self
				root.search_parent_0(parent)

		else:
			if self.left:
				self.left.search_parent_0(node)
			if self.right:
				self.right.search_parent_0(node)

	def print_tree(self, graph):
	 	"""
	 	input: seqbdd
	 	do:	add edge and node to graph instance
	 	"""
	 	if i == 0:
	 		global root
	 		root = self
	 		global i
	 		i = 1

	 	if self.left:
	 		if  not self.left.data == '0':
	 			if self.left.data == '1':
		 			graph.add_node(pydot.Node('%s' %self, label = '%s' %self.data))
	 				edge = pydot.Edge('%s' %self, self.left.data, label = '0')
	 			elif self == root:
		 			graph.add_node(pydot.Node('%s' %self, label = '%s' %self.data))
		 			graph.add_node(pydot.Node('%s' %self.left, label = '%s' %self.left.data))
		 			edge = pydot.Edge('%s' %self, '%s' %self.left, label = '0')
	 			else:
	 				root.search_parent_0(self)		#0-枝ではなくなるまで親をたどる
		 			graph.add_node(pydot.Node('%s' %parent, label = '%s' %parent.data))
		 			graph.add_node(pydot.Node('%s' %self.left, label = '%s' %self.left.data))
		 			if flag_0 == 1:
		 				edge = pydot.Edge('%s' %parent, '%s' %self.left, label = '0')
		 				global flag_0
		 				flag_0 = 0
		 			else:
		 				edge = pydot.Edge('%s' %parent, '%s' %self.left, color = 'red', label = '0')
	 			graph.add_edge(edge)
	 			self.left.print_tree(graph)

	 	if self.right:
	 		if self.right.data == '1':
	 			node = pydot.Node('%s' %self, label = '%s' %self.data)
	 			edge = pydot.Edge('%s' %self, self.right.data, color = 'red', label = '0')
	 			if not node in graph.get_node_list():
			 		graph.add_node(node)
			 	if not graph.get_edge('%s' %self, self.right.data):
					graph.add_edge(edge)
	 		else:
	 			node = pydot.Node('%s' %self, label = '%s' %self.data)
	 			node_child = pydot.Node('%s' %self.right, label = '%s' %self.right.data)
		 		edge = pydot.Edge('%s' %self, '%s' %self.right, color = 'red', label = '0')
	 			if not node in graph.get_node_list():
		 			graph.add_node(node)
		 		if not node_child in graph.get_node_list():
		 			graph.add_node(node_child)
		 		if not graph.get_edge('%s' %self, '%s' %self.right):
			 		graph.add_edge(edge)
	 		self.right.print_tree(graph)
	 	return graph


	def rank(self, sentence, graph):
		# print self.data, sentence
		try:
			if self.data == '%s(%s)' %(sentence[0][1], sentence[0][2]):
				if not self.right.data == '1':
					node = graph.get_node('%s' %self)
					if not isinstance(node, list):
						node.set_label('%s' %node.get_label() + r"\n" + '%s' %sentence[0][0])
					else:
						for i in node:
							if i.get_label()[:len(self.data)] == '%s' %self.data:
								i.set_label('%s' %i.get_label() + r"\n" + '%s' %sentence[0][0])
					edge = graph.get_edge('%s' %self, '%s' %self.right)
					edge.set_label(str(int(edge.get_label()) + 1))
					self.right.rank(sentence[1:], graph)
				else:
					node = graph.get_node('%s' %self)
					if not isinstance(node, list):
						node.set_label('%s' %node.get_label() + r"\n" + '%s' %sentence[0][0])
					else:
						for i in node:
							if i.get_label()[:len(self.data)] == '%s' %self.data:
								i.set_label('%s' %i.get_label() + r"\n" + '%s' %sentence[0][0])
					
					edge = graph.get_edge('%s' %self, self.right.data)
					edge.set_label(str(int(edge.get_label()) + 1))
			elif self == root:
				edge = graph.get_edge('%s' %self, '%s' %self.left)
				edge.set_label(str(int(edge.get_label()) + 1))
				self.left.rank(sentence, graph)
			elif self.left.data == '%s(%s)' %(sentence[0][1], sentence[0][2]):
				root.search_parent_0(self)
				edge = graph.get_edge('%s' %parent, '%s' %self.left)
				# print edge
				edge.set_label(str(int(edge.get_label()) + 1))
				if flag_0 == 1:
					edge = graph.get_edge('%s' %parent, '%s' %parent.left)
					edge.set_label(str(int(edge.get_label()) - 1))
					global flag_0
					flag_0 = 0
				else:
					edge = graph.get_edge('%s' %parent, '%s' %parent.right)
					edge.set_label(str(int(edge.get_label()) - 1))
				self.left.rank(sentence, graph)
			else:
				self.left.rank(sentence, graph)
			return graph
		except IndexError:
			pass
	def remove_rank1(self, graph, name):
		graph_com = pydot.Dot('%s_com' %name, graph_type = 'digraph', suppress_disconnected = True)

		for edge in graph.get_edge_list():
			if not edge.get_label() == '1':
				graph_com.add_edge(edge)
				sources = graph.get_node(edge.get_source())
				destinations = graph.get_node(edge.get_destination())
				if not isinstance(sources, list):
					sources = []
					sources.append(graph.get_node(edge.get_source()))
				if not isinstance(destinations, list):
					destinations = []
					destinations.append(graph.get_node(edge.get_destination()))
				for n in sources:
					# if not n.get_name() in [n.get_name() for n in graph_com.get_nodes()]:
					graph_com.add_node(n)
				for n in destinations:
					# if not n.get_name() in [n.get_name() for n in graph_com.get_nodes()]:
					graph_com.add_node(n)
		return graph_com

		# self.remove_subgraph()		#
				# for n in graph.get_node(edge.get_destination()):
					# n.set_style('invis')
			# for n in graph.get_node(edge.get_source()):
				# if n.get_style() == None:
					# break
				# else:
					# edge.set_style('invis')
	"""
	ひとまず、下の方の余計なサブグラフのカットは保留で・・・
	"""

	def remove_subgraph(self, graph_com):
		for edge in graph_com.get_edges():
			for n in graph_com.get_node(edge.get_destination()):
				print n.get_label()

		sub_nodes = [graph_com.get_node(edge.get_destination()).get_name() for edge in graph_com.get_edges()]
		for node in graph_com.get_node_list():
			print node.get_name() in sub_nodes or not node.get_name() == graph_com.get_node(root).get_name()
			if not node.get_name() in sub_nodes or not node.get_name() == graph_com.get_node(root).get_name():
				print node, sub_nodes
				print node in graph_com.get_node(edge.get_destination())
		return graph_com

				# if not node in [graph_com.get_node(edge.get_destination()) for edge in graph_com.get_edge_list()]:
					# node.set_style('invis')
					# print node.get_label()
					# self.remove_subgraph_2(node)

	def remove_subgraph_2(self, node):
		# sub_parent = graph_com.get_node(node)
		node.set_style('invis')
		print 'test'
		for sub_e in graph_com.get_edge_list():
			if node == graph_com.get_node(sub_e.get_source()):
				print graph_com.get_node(sub_e.get_source())
				sub_e.set_style('invis')
				if not graph_com.get_node(sub_e.get_destination()).get_label() == '1':
					print graph_com.get_node(sub_e.get_destination())
					self.remove_subgraph_2(graph_com.get_node(sub_e.get_destination()))

	def node_compress(self, graph_com):
		cnt = Counter()
		for n in graph_com.get_nodes():
			cnt.clear()
			tag = n.get_label().split(r"\n")[0]
			cnt = Counter(n.get_label().split(r'\n'))
			# print n.get_label().split(r'\n')[0], '\n'
			if float(cnt.most_common(1)[0][1])/sum(cnt.values()) >= 0.6:
				n.set_label(u"%s" %tag + r'\n' + "%s" %cnt.most_common(1)[0][0])
				n.set_shape('doublecircle')
				n.set_fontcolor('red')
			else:
				pass
		return graph_com
				# n.set_label('\n'.join(['%s:%d' %(w, n) for w, n in cnt.most_common()]))


	def pattern_extract(self, graph_com, query):
		pattern = [query]
		red_edge = []
		for edge in graph_com.get_edges():
			for node in graph_com.get_node(edge.get_source()):
				if node.get_label() == query:
					if edge.get_color() == 'red':
						red_edge.append(edge)
		for i in range(len(red_edge)):
			red_edge[i] = (red_edge[i], int(red_edge[i].get_label()))
		red_edge.sort(key=itemgetter(1), reverse = True)

		if red_edge == [] or graph_com.get_node(red_edge[0][0].get_destination()) == []:
			return pattern

		destination_node = graph_com.get_node(red_edge[0][0].get_destination())[0]
		if destination_node.get_label() == '.':
			return pattern
		elif destination_node.get_fontcolor() == 'red':
			pattern.append(destination_node.get_label())
			return self.pattern_extract_sub(graph_com, destination_node.get_label(), pattern, [])
		else:
			pattern.append(['*', destination_node.get_label().split(r'\n')[0][:-3]])
			return self.pattern_extract_sub(graph_com, destination_node.get_label(), pattern, [])
					
	def pattern_extract_sub(self, graph_com, query, pattern, something):
		red_edge = []
		for edge in graph_com.get_edges():
			for node in graph_com.get_node(edge.get_source()):
				if node.get_label() == query:
					if edge.get_color() == 'red':
						red_edge.append(edge)
		for i in range(len(red_edge)):
			red_edge[i] = (red_edge[i], int(red_edge[i].get_label()))
		red_edge.sort(key=itemgetter(1), reverse = True)

		# print red_edge
		if red_edge == [] or graph_com.get_node(red_edge[0][0].get_destination()) == []:
			return pattern
		elif isinstance(graph_com.get_node(red_edge[0][0].get_destination()), list):
			destination_node = graph_com.get_node(red_edge[0][0].get_destination())[0]
		else:
			destination_node = graph_com.get_node(red_edge[0][0].get_destination())

		if destination_node.get_label() == '.':
			return pattern
		elif destination_node.get_fontcolor() == 'red':
			if not something == []:
				for l in something:
					pattern.append(l)
			pattern.append(destination_node.get_label())
			self.pattern_extract_sub(graph_com, destination_node.get_label(), pattern, [])
			return pattern
		else:
			something.append(['*', destination_node.get_label().split(r'\n')[0][:-3]])
			self.pattern_extract_sub(graph_com, destination_node.get_label(), pattern, something)
			return pattern

	def get_patterns(self, graph_com, query, pattern, something, flag):
		red_edge = []
		edges = []
		# print query
		# print 'edges:%d' %len(graph_com.get_edges())
		for edge in graph_com.get_edges():
			for node in graph_com.get_node(edge.get_source()):
				if node.get_label() == query:
					if edge.get_color() == 'red' and not edge.get_label() == '1':
						red_edge.append(edge)
		red_edge = list(set(red_edge))

		for i in range(len(red_edge)):
			red_edge[i] = (red_edge[i], int(red_edge[i].get_label()))
		red_edge.sort(key=itemgetter(1), reverse = True)

		# print 'red_edges:%d' %len(red_edge)
		if red_edge == [] or graph_com.get_node(red_edge[0][0].get_destination()) == []:
			if flag == 0:
				pattern.append(something[0])
			if not pattern in patterns:
				global patterns
				patterns.append(pattern)
			# print patterns, '\n'
			return None

		for edge in red_edge:
			node = graph_com.get_node(edge[0].get_destination())
			if isinstance(node, list):
				node = node[0]
			temp_p = pattern[:]
			p = self.which_br(graph_com, node)
			if p == None:
				continue
			elif p[1] == 1 and flag == 1:
				temp_p.append(p[0])
				if not temp_p in patterns:
					self.get_patterns(graph_com, node.get_label(), temp_p, something, 1)
			elif p[1] == 1 and flag == 0:
				if not something == []:
					temp_p.extend(something)
				temp_p.append(p[0])
				if not temp_p in patterns:
					self.get_patterns(graph_com, node.get_label(), temp_p, [], 1)
			elif p[1] == 0:
				something.append(p[0])
				if not temp_p in patterns:
					self.get_patterns(graph_com, node.get_label(), temp_p, something, 0)
			something = []
		print 'roop end'


	def which_br(self, graph_com, node):
		if node.get_label() == '.':
			return None
		elif node.get_fontcolor() == 'red':
			return (node.get_label(), 1)
		else:
			return ('*/%s' %node.get_label().split(r'\n')[0][:-3], 0)



	def output(self, name, graph_com):

		text = 'pattern : %s\n\n' %patterns
		f = codecs.open('get-patterns_2.txt', 'a', 'utf-8')
		f.write(text)
		f.close()

		try:
			os.makedirs('Result2/%s' %name.split(u'/')[-2])
		except OSError:
			pass
	 	graph_com.write_jpeg(name)

	def dot_output(self, name, graph_com):
		graph_com.write_raw(name)
		print "write file <%s>" %name

	def test_print(self):
		if self.left:
			self.left.test_print()
		print self.data, self
		if self.right:
			self.right.test_print()
			
	def reset_graph(self):
		global i, patterns
		i = 0
		patterns = []