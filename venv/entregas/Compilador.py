import  os
class Compilador:
    def __init__(self, nombreArchvio):
        self.archivo= open(nombreArchvio,"r")
        self.x=self.archivo.read(1)
        self.logicos=['AND','OR']
        self.relacionales=['==','=','<','>','<=','=>','=<','>=','!=','=!']
        self.operadores=['/','*','-','+',';']
        self.reservadas=['DEFINE','INT','FLOAT','STRING','VAR','CALL','IN','OUT','START','END','WHILE','DO','IF','THEN','ELSE','FUN']

    def metodoCar(self):
        return  self.archivo.read(1)
    def generador(self):
        valido = ""
        if not(self.x.isalpha() or self.x.isdecimal()):
            if not(self.x.isspace()): #Es un caracter especial
                valido += self.x
                self.x = self.metodoCar()
                aux = valido + self.x
                if aux in self.relacionales:
                    valido = aux
                    self.x = self.metodoCar()
                elif aux in self.operadores:
                    self.x = self.metodoCar()
                else:
                    if not((valido in self.operadores) or (valido in self.relacionales)):
                        aux = valido
                        valido= valido + " No es un caracter permitido"
            else: #Es un espacio
                while True:
                    self.x = self.metodoCar()
                    if not(self.x.isspace()):
                        valido+=self.generador()
                        break
        elif(self.x.isalpha() or self.x == '_' ):#Es una palabra
            valido+=self.x
            self.x= self.metodoCar()
            if(self.x.isalnum() or self.x == '_'):
                valido+=self.x
                self.x = self.metodoCar()
                while(self.x.isalnum() or self.x == '_' ):
                    if(valido in self.logicos):
                        self.x= self.metodoCar()
                        return valido
                    valido+=self.x
                    self.x = self.metodoCar()
        elif self.x.isdecimal(): #Es un numero
            valido += self.x
            self.x = self.metodoCar();
            while(self.x.isdecimal()):
                valido+=self.x
                self.x = self.metodoCar()
            if(self.x == "." and valido != ""):
                #valido+=x
                self.x = self.metodoCar()
                if(self.x.isdecimal()):
                    valido+="."+self.x
                    self.x= self.metodoCar()
                    while(self.x.isdecimal()):
                        valido+=self.x
                        self.x = self.metodoCar()
        return valido
"""
    def valAlfa(self,x):
        if x is None:
            return False
        else:
            mayusculas = ord(x) > 64 and ord(x) < 91
            minusculas = ord(x) > 96 and ord(x) < 123
            return mayusculas or minusculas

    def valAlfaNum(self,x):
        if x is None:
            return False
        else:
            mayusculas = ord(x) > 64 and ord(x) < 91
            minusculas = ord(x) > 96 and ord(x) < 123
            numeros = ord(x) > 47 and ord(x) < 58
            return  mayusculas or minusculas or numeros

    def valNum(self,x):
        if x is None:
            return False
        else:
            return ord(x) > 47 and ord(x) < 58
"""


def main():
    file = "RegistroCaracteres.txt"
    comp = Compilador(file)
    for i in range(0,5):
        print(comp.generador())

main()
