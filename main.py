from antlr4 import *
from TrinoLexer import TrinoLexer
from TrinoParserListener import TrinoParserListener
from TrinoParser import TrinoParser

class TrinoPrintListener(TrinoParserListener):
    def exitPredicated(self, ctx):
        print(ctx.valueExpression().getText())


def main():
    query="select * from a where 8=d and b = 6;"
    
    lexer = TrinoLexer(InputStream(query))
    
    stream = CommonTokenStream(lexer)
    parser = TrinoParser(stream)
    tree = parser.singleStatement()
    printer = TrinoPrintListener()
    walker = ParseTreeWalker()
    walker.walk(printer, tree)

if __name__ == '__main__':
    main()