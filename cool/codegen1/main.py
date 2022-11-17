from antlr4 import *
from antlr.coolLexer import coolLexer
from antlr.coolParser import coolParser
from os import getcwd

#from listeners.semantic import SemanticListener
from listeners.codegen import CodeGen
from listeners.hierarchy import HierarchyListener

PATH=getcwd()


def save(result, file):
    # Completar esta función que recibe el string con el código ensamblador y lo tiene que salvar en
    # la carpeta actual con el mismo nombre de archivo, pero la extensión .s, por ejemplo:
    # '../resources/semantic/input/anattributenamedself.cool' => anattributenamedself.s
    pass


def compile(file):
    parser = coolParser(CommonTokenStream(coolLexer(FileStream(file))))
    tree = parser.program()

    walker = ParseTreeWalker()

    #Temporalmente omitimos el análisis semántico
    walker.walk(HierarchyListener(), tree)

    c = CodeGen(walker, tree)
    c.generar()
    #save(c.getText(), file)
    print(c.result)

def dummy():
    raise SystemExit(1)


if __name__ == '__main__':
    compile('../resources/codegen/input/fibo.cool')
