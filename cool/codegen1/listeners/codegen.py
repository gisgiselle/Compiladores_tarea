from antlr.coolListener import coolListener
from antlr.coolParser import coolParser
from util.asm import *
from util.structure import allClasses

"""
Los tipos quedarán así:
object 0
IO 1
Int 2
String 3
Boolean 4"""


class Literales(coolListener):
    def __init__(self):
        self.idx = 0
        self.result = ""

    def enterInt(self, ctx:coolParser.IntContext):
        self.result += cTplInt.substitute(idx=self.idx, tag=2, value=ctx.getText())
        self.idx = self.idx + 1

    def enterStr(self, ctx:coolParser.StrContext):
        self.result += cTplInt.substitute(idx=self.idx, tag=2, value=len(ctx.getText()))
        self.idx = self.idx + 1

        self.result += cTplStr.substitute(idx=self.idx, tag=3, size=4+(len(ctx.getText())+1)%4,
                                          sizeIdx=(self.idx-1), value=ctx.getText())
        self.idx = self.idx + 1


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
        literales = Literales()
        self.walker.walk(literales, self.tree)

        self.result = literales.result +\
                      self.tablaNombres() +\
                      self.tablaModelosConstructores() +\
                      self.tablaMetodos() +\
                      self.objetosModelos()

    def tablaNombres(self):
        r = "class_nameTab:\n"
        for k in allClasses().values():
            self.result += cTplInt.substitute(idx=self.idx, tag=2, value=len(k.name))
            self.idx = self.idx + 1

            self.result += cTplStr.substitute(idx=self.idx, tag=3, size=4 + (len(k.name) + 1) % 4,
                                              sizeIdx=(self.idx - 1), value=k.name)
            r += "    .word str_const{}\n".format(self.idx)
            self.idx = self.idx + 1

        return r

    def tablaModelosConstructores(self):
        return ""

    def tablaMetodos(self):
        r = ""
        for k in allClasses().values():
            r += k.name + "_dispTab:\n"
            for k1 in k.methods:
                r += "    .word {}.{}\n".format(k.name, k1)

        return r

    def objetosModelos(self):
        for k in allClasses():
            pass

        return ""

    def segTexto(self):
        pass

"""
    Segmento de Datos:



Algunas etiquetas son fijas y obligatorias, las requiere el runtime

Constantes
    1. Determinar literales string
        1.1 Obtener lista de literales (a cada una asignar un índice) + nombres de las clases
        1.2 Determinar constantes numéricas necesarias
        1.3 Reemplazar en la plantilla:
            - tag
            - tamaño del objeto: [tag, tamaño, ptr al dispTab, ptr al int, (len(contenido)+1)%4] = ?
                (el +1 es por el 0 en que terminan siempre)
            - índice del ptr al int
            - valor (el string)
    2. Determinar literales enteras
        2.1 Literales necesarias en el punto 1
        2.2 + constantes en el código fuente
        2.3 Remplazar en la plantilla:
            - tag
            - tamaño del objeto: [tag, tamaño, ptr al dispTab y contenido] = 4 words
            - valor

Tablas que requiere el runtime
    1. class_nameTab: tabla para los nombres de las clases en string
        1.1 Los objetos ya fueron generados arriba
        1.2 El tag de cada clase indica el desplazamiento desde la etiqueta class_nameTab
    2. class_objTab: prototipos (templates) y constructores para cada objeto
        2.1 Indexada por tag: en 2*tag está el protObj, en 2*tag+1 el init
    3. dispTab para cada clase
        3.1 Listado de los métodos en cada clase considerando herencia

Objetos para copiar cuando se ejecuta new
    El prototipo o plantilla para cada objeto (es decir, de donde new copia al instanciar)
    1. Para cada clase generar un objeto, poner atención a:
        - nombre
        - tag
        - tamaño en words [tag, tamaño, dispTab, atributos ... ] = ?
            Es decir, el tamaño se calcula en base a los atributos + 3, por ejemplo
                Int tiene 1 atributo (el valor) por lo que su tamanio es 3+1
                String tiene 2 atributos (la longitud y el valor (el 0 al final)) por lo que su tamaño es 3+2
        - dispTab
        - atributos
"""


"""
Segmento de Texto:
Código de cada método de acuerdo al dispTab. Debe existir un Main.main
"""