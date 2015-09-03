#!/usr/bin/env python3
from	sys			import argv, exit
from	cmd			import Cmd
from	copy		import deepcopy
from	tabulate	import tabulate

import	json
import	shlex

__author__	= 'OJFord'
__version__	= '0.1'

class Interpreter(Cmd):
	"""IARAI: A Relational Algebra Interpreter."""

	def __init__(self, relfile):
		super().__init__()
		self.prompt	= 'RA> '
		self.intro	= '^D to exit. help[ cmd] for more info. Tab completion.'
		self.doc_header	= 'Relation may be given as `(jsonfile.relation)`.'
		self.doc_header += 'Alternatively, `$` refers to working relation.'

		with open(relfile) as f:
			self.file	= json.loads(f.read())
		self.fname		= self.file['relation']
		self.working	= None
		self.chain		= ''	# working command chain

	def write(self):
		print( self.chain + ' (' + self.working['relation'] + ')' )
		print( tabulate(self.working['tuples'], headers=self.working['attributes']) )
		print()

	def debugLine(self, line):
		before	= deepcopy(self.working)
		self.postcmd( self.onecmd( self.precmd(line) ), line)
		after	= self.working
		return before, after

	@staticmethod
	def chainable(cmd, args):
		return cmd + ('_' + args[1:] if args[1:] else '') + ' '

	def cmdloop(self):
		try:
			return super().cmdloop()
		except KeyboardInterrupt:
			# cancel command without crashing out of interpreter
			self.intro = None
			return self.cmdloop()

	def precmd(self, line):
		if not line or line == 'EOF' or line.find('help') == 0:
			return line

		argsend = line.find('(')
		if argsend == -1:
			argsend = line.find('$')

		rel	= line[argsend:]
		cmd	= line[0]
		args= shlex.split( line[1:argsend] )

		if len(args) >= 2 or len(args) >= 1 and args[0][0] not in ['_','(','$']:
			if args[0][0] == '_':
				rrecurse= ' '.join(args[1:])
				largs	= args[0]
			else:
				rrecurse= ' '.join(args)
				largs	= ''

			# execute end of line
			self.postcmd( self.onecmd( self.precmd(rrecurse+rel) ), rrecurse+rel )
			# 'restart' to finish up left of line
			return self.precmd(cmd + largs + ' $')

		elif rel == '$':
			if not self.working:
				print('Error: no current working relation, use file first.')
				raise KeyboardInterrupt # hacky af
			else:
				# continue with working relation
				pass

		elif rel == '(' + self.fname + ')':
			self.chain = ''
			self.working = deepcopy(self.file)

		else:
			print('Error: last argument must be a valid relation.')
			raise KeyboardInterrupt # hacky af

		if args:	# single string args, just remove leading '_'
			args = ' ' + args[0][1:]
		else:
			args = ''

		self.chain = self.chainable(cmd, args) + self.chain
		return cmd+args

	def default(self, line):
		# undo add command to chain.. unfortunately precmd() executes even on invalid
		cmd, args	= line[0], shlex.split(line[1:])
		self.chain	= self.chain[ len( self.chainable(cmd, args) ):]
		super().default(line)
	
	def emptyline(self):
		# overrides super's repeat last line, which would make little sense
		pass

	def do_EOF(self, line):
		"""Exits."""
		return True

	def do_p(self, args):
		""" 'p' for pi - project.
		Projects the given attributes of a relation, or all if none specified.
		usage: p [ATTR,...] (REL)
		"""

		if args:
			allAtts = self.working['attributes']
			# put in same order
			prjAtts = [ att for att in allAtts if att in args.split(',') ]
			prjAtts+= [ att for att in args.split(',') if att not in prjAtts ]
			# project
			for i,tup in enumerate(self.working['tuples']):
				self.working['tuples'][i] = [ o for j,o in enumerate(tup) if allAtts[j] in prjAtts ]
				self.working['tuples'][i]+= [ None for o in prjAtts if o not in allAtts ]
			self.working['attributes'] = prjAtts

		self.write()

	def do_s(self, args):
		""" 's' for sigma - select.
		Selects from a relation that which satisfies the given proposition.
		usage: s [PROP] (REL)
		"""

		if '/\\' in args or '\\/' in args:
			raise Exception('Error: not implemented, use e.g. `s_prop2 s_prop1 $` to AND for now')

		if args:
			if args[0] in ['¬', '~', '!']:
				neg	= True
				args= args[1:]
			else:
				neg	= False
			(att, val) = tuple(args.split('='))
		else:
			att = val = None

		if att:
			tups = self.working['tuples']
			atts = self.working['attributes']
			if neg:
				self.working['tuples'] = [ t for t in tups if t[ atts.index(att) ] != val ]
			else:
				self.working['tuples'] = [ t for t in tups if t[ atts.index(att) ] == val ]

	def do_r(self, args):
		""" 'r' for rho - rename.
		Renames a given attribute of a relation.
		usage: r NEW_NAME/OLD_NAME (REL)
		"""

		pairs	= [ tuple(p.split('/')) for p in args.split(',') ]
		atts	= self.working['attributes']
		for (new, old) in pairs:
			if old in atts:
				self.working['attributes'][ atts.index(old) ] = new

if __name__ == '__main__':
	if len(argv) != 2:
		print('Error: Single argument - JSON relation file - required.')
		print('usage: python iarai.py relation.json')
		exit(1)
	else:
		Interpreter(argv[1]).cmdloop()

