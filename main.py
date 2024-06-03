from antlr4 import *
from TrinoLexer import TrinoLexer
from TrinoParserListener import TrinoParserListener
from TrinoParser import TrinoParser


class TrinoWhereListener(TrinoParserListener):
    def __init__(self):
        self.columns = dict()

    def exitPredicated(self, ctx: TrinoParser.PredicatedContext):
        predicate = ctx.predicate_()
        left = ctx.valueExpression().getText()

        if (
            isinstance(predicate, TrinoParser.InListContext)
            or isinstance(predicate, TrinoParser.BetweenContext)
            or isinstance(predicate, TrinoParser.LikeContext)
            or isinstance(predicate, TrinoParser.NullPredicateContext)
            or isinstance(predicate, TrinoParser.InSubqueryContext)
        ):
            self.add_column(left)
        elif predicate != None:
            right = predicate.valueExpression().getText()
            self.add_column(left)
            self.add_column(right)

    def add_column(self, column: str):
        if column in self.columns:
            self.columns[column] += 1
        else:
            self.columns[column] = 1


def get_where_columns(query: str):
    lexer = TrinoLexer(InputStream(query))
    stream = CommonTokenStream(lexer)
    parser = TrinoParser(stream)
    tree = parser.singleStatement()
    listener = TrinoWhereListener()
    walker = ParseTreeWalker()
    walker.walk(listener, tree)

    return listener.columns


def main():
    queries = [
        ("select * from a where d in (4, 5, 6);", {"d": 1}),
        (
            "select * from a where 5 = d and b = 'c';",
            {"d": 1, "b": 1, "'c'": 1, "5": 1},
        ),
        ("select * from a where d between 5 and 7;", {"d": 1}),
        ("select * from a where c like 'a%';", {"c": 1}),
        ("select * from a where b is not null;", {"b": 1}),
    ]

    for query, expected_columns in queries:
        columns = get_where_columns(query)
        if columns != expected_columns:
            print(f"Query: {query} - Failed")
            print(f"Recieved: {columns}, Expected: {expected_columns}")


if __name__ == "__main__":
    main()
