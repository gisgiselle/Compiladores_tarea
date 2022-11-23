from antlr.coolListener import coolListener
from antlr.coolParser import coolParser
from util.asm import *
from util.dummyasm import *
from util.structure import allClasses

class TextSegment(coolListener):
    def __init__(self):
        self.result = ""

    def enterKlass(self, ctx:coolParser.KlassContext):
        self.currentKlass = ctx.TYPE(0).getText()

    def enterMethod(self, ctx:coolParser.MethodContext):
        self.result += dummyMethodOpen.substitute(Klass=self.currentKlass, method=ctx.ID().getText())

    def exitMethod(self, ctx:coolParser.MethodContext):
        self.result += ctx.expr().code + dummyMethodClose

    def exitStr(self, ctx:coolParser.StrContext):
        # Del segmento de datos se requiere que los [indices est[en generados
        ctx.code = litTpl.substitute(literal="str_const{}".format(10),
                                     value=ctx.getText())

    def exitPri(self, ctx:coolParser.PriContext):
        ctx.code = ctx.primary().code

    def exitCall(self, ctx:coolParser.CallContext):
        #usar callParametersTpl, callStr1, callTpl_instance
        r = ""
        for p in ctx.params:
            r += callParametersTpl.substitute(exp=p.code) # <- push
        r += callStr1a # cargo el self en $a0

        #IO.out_string está en la posición 4, es decir, offset 12
        r += callTpl_instance.substitute(off=12, method=ctx.getText())

        ctx.code = r

class CodeGen():
    def __init__(self, walker, tree):
        self.result = ""
        self.tree = tree
        self.walker = walker
        self.idx = 0

    def generar(self):
        self.segDatos()
        self.segTexto()

    def segDatos(self):
        self.result += dummyasm

    def segTexto(self):
        textSegment = TextSegment()
        self.walker.walk(textSegment, self.tree)

        self.result += textSegment.result


"""
Segmento de Texto:
Código de cada método de acuerdo al dispTab. Debe existir un Main.main
"""