from antlr.coolParser import coolParser
from antlr.coolListener import coolListener
from util.exceptions import BadClassName, InvalidInheritance
from util.structure import setBaseKlasses, Klass, lookupClass, Method

class HierarchyNamesListener(coolListener):
    def __init__(self):

        #Crear estructura inicial de clases
        setBaseKlasses()

    def enterKlass(self, ctx: coolParser.KlassContext):
        #test_redefinedclass
        try:
            if lookupClass(ctx.TYPE(0).getText()) is None:
                raise Exception
        except KeyError:
            #Bien aquí
            pass
        self.klass = Klass(ctx.TYPE(0).getText())

class HierarchyListener(coolListener):
    def __init__(self):

        #Crear estructura inicial de clases
        setBaseKlasses()

    def enterKlass(self, ctx: coolParser.KlassContext):


        #test_inheritsbool, test_inheritsselftype, test_inheritsstring
        if not ctx.TYPE(1) is None and ctx.TYPE(1).getText() in ['Int', 'String', 'Bool', 'SELF_TYPE']:
            raise InvalidInheritance()

        # Crear esta clase, para este subárbol la voy a guardar en self.klass
        if ctx.TYPE(1) is None:
            self.klass = Klass(ctx.TYPE(0).getText())
        else:
            #test_missingclass
            self.klass = Klass(ctx.TYPE(0).getText(), ctx.TYPE(1).getText())

    def enterMethod(self, ctx:coolParser.MethodContext):
        #params contiene un arreglo de formal, que tiene ID y el TYPE, lo convierto a Klass para usarlo más adelante
        params = []
        for p in ctx.params:
            if p.TYPE().getText() == 'SELF_TYPE':
                raise BadClassName()
            params.append ( (p.ID().getText(), lookupClass(p.TYPE().getText())) )

        # test_overridingmethod4, test_signaturechange

        #Crear un método en la clase actual
        self.klass.addMethod(ctx.ID().getText(), Method(ctx.TYPE(), params))


    def enterAttribute(self, ctx:coolParser.AttributeContext):
        #test_attroverride

        #Declaro un atributo, pero el tipo lo guardo como Klass, no como string
        self.klass.addAttribute(ctx.ID().getText(), lookupClass(ctx.TYPE().getText()))

