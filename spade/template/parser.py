import logging
import ply.yacc as yacc
from spade.template.lexer import create_lexer, tokens, get_location
from spade.template.ast import StructDecl, FieldDecl, ArrayDecl, Ast

# Disabling unused-argument because it's triggering for lexer methods that
# require a parameter be present, even if it isn't used.
# Also disabling the no-self-use check because it triggers for some reason
# on yacc methods.  Unsure as to why this is, but I think it's due to yacc
# being weird and it doesn't appear to affect anything relating to the
# execution of this program.
# pylint: disable=invalid-name,no-self-use

logging.basicConfig(
    level = logging.DEBUG,
    filename = "log.txt",
    filemode = "w",
    format = "%(filename)10s:%(lineno)4d:%(message)s")

class TemplateParserException(Exception): pass

class TemplateParser(object):
    """Parses template files."""

    def __init__(self):
        # yacc requires these be listed here in order for it to work
        self.tokens = tokens

        # Create yacc with logging enabled
        log = logging.getLogger()
        self.parser = yacc.yacc(
            module=self,
            start='ast',
            write_tables=False,
            debug=True,
            debuglog=log)

    def p_ast(self, p):
        """ ast : declaration_list """
        p[0] = Ast(p[1])

    def p_declaration_list(self, p):
        """ declaration_list : declaration
                             | declaration_list declaration
        """
        p[0] = []
        if len(p) == 2:        # First option (declaration)
            p[0].append(p[1])  # Add the new declaration to the list
        else:                  # Second option (declaration_list struct_field)
            p[0] += p[1]       # Add the declaration to the overall list
            p[0].append(p[2])  # Add the new declaration to the list

    def p_declaration(self, p):
        """ declaration : struct """
        p[0] = p[1]

    def p_struct(self, p):
        """ struct : STRUCT NAME LBRACE struct_field_list RBRACE SEMICOLON
        """
        p[0] = StructDecl(p[2], p[4])

    def p_struct_field_list(self, p):
        """ struct_field_list : struct_field
                              | struct_field_list struct_field
        """
        p[0] = []
        if len(p) == 2:        # First option (struct_field)
            p[0].append(p[1])  # Add the new struct field to the list
        else:                  # Second option (struct_field_list struct_field)
            p[0] += p[1]       # Add the struct list to the overall list
            p[0].append(p[2])  # Add the new struct field to the list

    def p_struct_field_1(self, p):
        """ struct_field : NAME NAME SEMICOLON """
        #""" struct_field : TYPE NAME SEMICOLON """
        p[0] = FieldDecl(p[1], p[2])

    def p_struct_field_2(self, p):
        """ struct_field : NAME NAME LBRACKET NUMBER RBRACKET SEMICOLON """
        #""" struct_field : TYPE NAME LBRACKET NUMBER RBRACKET SEMICOLON """
        p[0] = ArrayDecl(FieldDecl(p[1], p[2]), p[4])

    #def p_struct_field_3(self, p):
    #    """ struct_field : NAME NAME LBRACKET NAME RBRACKET SEMICOLON """
    #    #""" struct_field : TYPE NAME LBRACKET NAME RBRACKET SEMICOLON """
    #    p[0] = ArrayDecl(FieldDecl(p[1], p[2]), p[4])

    def p_error(self, p):
        if p:
            line, col = get_location(p)
            print(("Parsing error at line:{}, col:{} - Unexpected token "
                    "\"{}\"").format(line, col, p.type))
        else:
            print("Syntax error at EOF")

    @classmethod
    def parse_string(cls, text):
        return cls().parser.parse(text, lexer=create_lexer())

    @classmethod
    def parse_file(cls, filename):
        with open(filename, "r") as f:
            return cls.parse_string(f.read())

        return None