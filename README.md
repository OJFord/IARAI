#IARAI:
####_A Relational Algebra Interpreter_ [![Build Status](https://travis-ci.org/OJFord/IARAI.png)](https://travis-ci.org/OJFord/IARAI)

IARAI is an interpreter for the RA, intended as a learning aid - allowing hopefully straightforward testing of expressions, and continuing an expression with the relation resulting from the previous command.

The full expression used to generate each output is printed, facilitating an interactive arrival at a solution, without need to remember how we got there.

The acronym is both recursive, and palindromic; so you know it must be good.  
(Pronounce 'Yarr-Eye', or think "one Toyota Yaris, multiple Toyota Yari".)

##Installation
```
$ pip install -r requirements.txt
$ chmod a+x IARAI/iarai.py
```

##Usage
```
$ ./IARAI/iarai.py
RA>
```

Feel free to ask for `help` at the prompt, or see below.

##Operators
Currently 'alpha af', the following operators are supported:
 - `p` for ['pi' or 'project'](#projection)
 - `s` for ['sigma' or 'select' (aka 'restrict')](#selection-aka-restriction)
 - `r` for ['rho' or 'rename'](#renaming)

###Projection
`p (relation)` projects all attributes of a given relation.

`p_ATTR1,ATTR2 (relation)` projects only the listed attributes of the given relation.

###Selection (a.k.a Restriction)
`s_ATTR=VAL (relation)` modifies the [working relation](#Working%20Relation) to include only those tuples with the given value for the given attribute.

`s_¬ATTR=VAL (relation)` modifies the working relation to include only those tuples with a value different to the given value for the given attribute. `!` and `~` are also supported negators, in recognition of differing keyboard layouts.

**Note** that although the logical AND is implicitly supported (by chaining: `s_a=1 s_b=2 (relation)`), the logical OR operator is dependent on implementation of the Cartesian product.

###Renaming
`r_new1/old1,new2/old2 (relation)` modifies the attributes in the working relation corresponding to the given old names, to have the new names also given.

##Input
Initial relations are input via a JSON file in the following format:
```lang=JSON
{
	"relation"	: "name",
	"attributes": ["att1", "att2", ..., "attN"],
	"tuples"	: [
		["val1", "val2", ..., "valN"],
		["val1", "val2", ..., "valN"],
		...
		["val1", "val2", ..., "valN"]
	]
}
```

##Output
This file will _not_ be overwritten. At present the only method of storing a result is by redirecting stdout.

The current state of the working relation is - of course - only output on projection.

##Working Relation
This is the relation used internally; modified as a result of all commands. It is always overwritten when a command is entered.

To continue execution on the working relation, use `$` in place of `(relation-name)`. For example, to project the current state of the working relation, enter `p$`.

##Chaining
An alternative to sequential commands utilising the working relation is to chain the operators into a single command, e.g. `p_funds r_funds/money s_name=Bob (accounts)` will project Bob's money from the accounts relation.


##Next Release
Intend to implement the Cartesian/cross product/join in order to complete the algebra. At that point 'anything would be possible'; the derived operators (e.g. division) would be a mere bonus.

Rather than implementing derived operators directly, a future release may allow some form of 'macros', short-handing a chain of commands - as this is possibly more instructive and fitting for the stated aim of aiding learning. Of course, in the mean time, copy-paste works.. (!)

