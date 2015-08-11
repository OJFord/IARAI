#!/usr/bin/env python3
import	unittest
import	json
from	os			import path
import	sys
sys.path.append('../IARAI')
from	IARAI.iarai	import Interpreter

class InterpreterTestCase(unittest.TestCase):
	def setUp(self):
		fname = 'test_relation.json'
		fpath = path.dirname(path.abspath(__file__)) + '/' + fname
		with open(fpath) as f:
			self.relation = json.loads(f.read())
		self.interpreter = Interpreter(fpath)
		self.interpreter.debugLine('p (' + self.relation['relation'] + ')')	

class Pi(InterpreterTestCase):
	"""Test class for the projection operator"""

	def test_projects_all(self):
		expression = 'p $'
		before, after = self.interpreter.debugLine(expression)
		self.assertEqual(before, after)

	def test_projects_some(self):
		atts = self.relation['attributes']
		rm = atts.pop()

		expression		= 'p_' + ','.join(atts) + ' $'
		before, after	= self.interpreter.debugLine(expression)
		beforeAtts		= before['attributes']
		afterAtts		= after['attributes']

		self.assertNotEqual(beforeAtts,	afterAtts)
		self.assertEqual(	atts,		afterAtts)
		self.assertNotIn(	rm,			afterAtts)

class Sigma(InterpreterTestCase):
	"""Test class for the selection operator"""

	def test_select(self):
		atts	= self.relation['attributes']
		tups	= self.relation['tuples']
		idx		= 0
		k, v	= (atts[idx], tups[-1][idx])

		expression	= 's_' + k + '=' + v + ' $'
		_, after	= self.interpreter.debugLine(expression)

		for tup in after['tuples']:
			self.assertEqual(tup[idx], v)

	def test_select_negate(self):
		atts	= self.relation['attributes']
		tups	= self.relation['tuples']
		idx		= -1
		k, v	= (atts[idx], tups[0][idx])

		expression	= 's_¬' + k + '=' + v + ' $'
		_, after	= self.interpreter.debugLine(expression)

		for tup in after['tuples']:
			self.assertNotEqual(tup[idx], v)

class Rho(InterpreterTestCase):
	"""Test class for the renaming operator"""

	def test_rename_one(self):
		atts	= self.relation['attributes']
		tups	= self.relation['tuples']
		idx		= -1
		old		= atts[idx]
		new		= 'newname' + old # guaranteed different

		expression	= 'r_' + new+ '/' + old + ' $'
		_, after	= self.interpreter.debugLine(expression)

		self.assertEqual(after['attributes'][idx], new)

	def test_rename_multiple(self):
		atts	= self.relation['attributes']
		tups	= self.relation['tuples']
		idx		= [0, 1]
		old		= [ atts[i] for i in idx ]
		new		= [ 'newname' + o for o in old ]  # guaranteed different

		expression	= 'r_' + ','.join([ new[i] + '/' + old[i] for i in idx ]) + ' $'
		_, after	= self.interpreter.debugLine(expression)

		for i in idx:
			self.assertEqual(after['attributes'][i], new[i])

if __name__ == '__main__':
	unittest.main(buffer=True)

