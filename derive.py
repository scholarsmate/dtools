import sys

import pyparsing as pp

from dtools_lib import transforms
from dtools_lib import delimited_record


# define the grammar
FLD_PFX = '$'
LPAR, RPAR, EQ = map(pp.Suppress, '()=')
identifier = pp.pyparsing_common.identifier
numeric = pp.pyparsing_common.number
constants = pp.Literal('True') | pp.Literal('False') | pp.Literal('None')
quoted_string = pp.quotedString.addParseAction(pp.removeQuotes)
field = pp.Word(FLD_PFX, pp.alphanums + '_').setName('field')
function = pp.Forward()
atom = field | numeric | quoted_string | constants | function
function << identifier + pp.Group(LPAR + pp.Optional(pp.delimitedList(atom)) + RPAR)
assignment = identifier + EQ + pp.Group(function)
grammar = pp.delimitedList(assignment, delim=';')


class ASTNode(object):
    def __init__(self, tokens):
        self.tokens = tokens
        self.assignFields()

    def assignFields(self):
        pass

    def __str__(self):
        return self.__class__.__name__ + ':' + str(self.__dict__)

    __repr__ = __str__


class Assignment(ASTNode):
    def assignFields(self):
        self.lhs, self.rhs = self.tokens
        del self.tokens

    def __call__(self):
        result = self.rhs[0]()
        transforms.RECORD[self.lhs] = result
        return result


class FunctionCall(ASTNode):
    def assignFields(self):
        self.fnName, self.args = self.tokens
        del self.tokens

    def __call__(self):
        args = []
        # Prepare the arguments
        for arg in self.args:
            if isinstance(arg, FunctionCall):
                # depth-first traversal of the AST for functions
                arg = arg()
            if isinstance(arg, basestring):
                # prepare string for evaluation
                arg = '"""{0}"""'.format(arg)
            else:
                # string-ify non sting objects for evaluation
                arg = str(arg)
            args.append(arg)
        # Build and evaluate the function (in the transform package) string, returning the results
        return eval('transforms.{0}({1})'.format(self.fnName, ', '.join(args)))


class FetchField(FunctionCall):
    def __init__(self, f):
        super(FetchField, self).__init__(['Field', f])

    def __call__(self):
        # Remove the field prefix and return the field value
        return transforms.Field(self.args[0][len(FLD_PFX):])


field.setParseAction(lambda t: FetchField(t))
function.setParseAction(FunctionCall)
assignment.setParseAction(Assignment)


def evaluate(expression):
    for exp in expression:
        exp()


sep = '|'
expr = grammar.parseString(sys.argv[1], parseAll=True)
header = sys.stdin.readline().rstrip().split(sep)
for rec in delimited_record.delimited_record_reader(sys.stdin, sep, header):
    transforms.RECORD = rec
    transforms.RECORD_COUNT += 1
    evaluate(expr)
    if transforms.RECORD_COUNT == 1:
        print sep.join(transforms.RECORD.keys())
    print sep.join([str(r) for r in transforms.RECORD.values()])
