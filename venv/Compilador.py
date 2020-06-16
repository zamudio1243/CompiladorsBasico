import  os
class Compilador:
    def __init__(self, nombreArchvio):
        self.archivo= open(nombreArchvio,"r")
        self.x=self.archivo.read(1)
        self.logicos=['AND','OR']
        self.relacionales=['==','=','<','>','<=','=>','=<','>=','!=','=!','{','}','(',')']
        self.operadores=['/','*','-','+',';']
        self.reservadas=['DEFINE','INT','FLOAT','STRING','VAR','CALL','IN','OUT','START','END','WHILE','DO','IF','THEN','ELSE','FUN']
        self.guardados=[]
        self.numeros=["0","1","2","3","4","5","6","7","8","9","."]
        self.sintactico=[]
        self.pointer=0

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
            self.x = self.metodoCar()
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

    def verificar (self, cadena):
        #print("",end="")('Llego: '+cadena)
        if ( cadena in self.logicos or  
        cadena in self.operadores or
         cadena in self.relacionales 
         or cadena in self.reservadas): #Reservados
            self.sintactico.append(cadena)
            return cadena
        else:
            try:
                if isinstance(float(cadena),float):
                    self.sintactico.append("VALOR")
                    return "VALOR"   
            except:
                self.guardados.append(cadena)
                self.sintactico.append("NAME")
                return "NAME"

    def lexico(self,i):
        return self.sintactico[i]

    def BLOQUE(self):
        tok= self.lexico(self.pointer)
        if(tok== "START"):
            self.CABECERA()
            self.PROPOSICION()
            self.pointer+=1
            tok = self.lexico(self.pointer)
            if(tok== "END"):
                print()
                print("Se compilo con exito")
            else:
                self.errores("END")
        else:
            self.errores("START")
    def CABECERA(self):
        self.pointer += 1
        tok = self.lexico(self.pointer)
        if(tok !="IF" and tok != "WHILE" and tok!= "CALL"
        and tok != "OUT" and tok !="NAME" and tok!= "IN"):
            self.pointer -= 1
            self.DEFINE()
            self.VAR()
            #self.NAME()
            self.FUN()
        else:
            self.pointer -= 1

    def DEFINE(self):
        self.pointer += 1
        tok = self.lexico(self.pointer)
        if (tok != "VAR" and tok != "FUN" and tok != "NAME"):
            if(tok =="DEFINE"):
                self.TIPO()
                self.NAME()
                self.pointer += 1
                tok = self.lexico(self.pointer)
                if (tok == "="):
                    self.VALOR()
                    self.pointer += 1
                    tok = self.lexico(self.pointer)
                    if(tok == ";"):
                        print("",end="")
                        #todo bien, todo correcto?
                    else:
                        self.errores(";")
                else:
                    self.errores("=")
            else:
                self.errores("DEFINE")
        else:
            self.pointer -= 1

    def VAR(self):
        self.pointer += 1
        tok = self.lexico(self.pointer)
        if (tok != "FUN" and tok != "NAME"):
            if(tok == "VAR"):
                self.TIPO()
                self.NAME()
                self.pointer += 1
                tok = self.lexico(self.pointer)
                if(tok == ";"):
                    print("",end="")
                    #todo bien, todo correcto
                else:
                    self.errores(";")
            else:
                self.errores("VAR")
        else:
            self.pointer -= 1


    def NAME(self):
        self.pointer += 1
        tok = self.lexico(self.pointer)
        if (tok != "{" and tok != "=" and tok != "FUN"):
            if(tok == "NAME"):
                self.pointer += 1
                tok = self.lexico(self.pointer)
                if (tok == "="):
                    self.pointer += 1
                    tok = self.lexico(self.pointer)
                    if(tok == "VALOR"):
                        print("",end="")
                        # todo bien, todo correcto
                        """
                        self.pointer += 1
                        tok = self.lexico(self.pointer)
                        if(tok == ";"):
                            print("",end="")
                            # todo bien, todo correcto
                        else:
                            self.errores(";")
                        """
                    else:
                        self.errores("VALOR")
                else:
                    self.errores("VALOR")
            else:
                self.errores("NAME")

        else:
            self.pointer -= 1

    def FUN(self):
        self.pointer += 1
        tok = self.lexico(self.pointer)
        if (tok != "IF" and tok != "WHILE" and tok != "CALL"
        and tok != "OUT" and tok != "NAME" and tok != "IN"):
            if(tok == "FUN"):
                self.pointer += 1
                tok = self.lexico(self.pointer)
                if(tok == "NAME"):
                    self.pointer += 1
                    tok = self.lexico(self.pointer)
                    if(tok == "{"):
                        self.BLOQUE()
                        self.pointer += 1
                        tok = self.lexico(self.pointer)
                        if(tok == "}"):
                            print("",end="")
                            #Todo bien,todo correcto?
                        else:
                            self.errores("}")
                    else:
                        self.errores("{")
                else:
                    self.errores("NAME")
            else:
                self.errores("FUN")
        else:
            self.pointer -= 1

    def TIPO(self):
        self.pointer += 1
        tok = self.lexico(self.pointer)
        if(tok == "INT"):
            print("",end="")
            # Todo bien,todo correcto?
        elif(tok == "FLOAT"):
            print("",end="")
            # Todo bien,todo correcto?
        elif(tok == "STRING"):
            print("",end="")
            # Todo bien,todo correcto?
        else:
            self.errores("INT o FLOAT o STRING")

    def PROPOSICION(self):
        self.pointer += 1
        tok = self.lexico(self.pointer)
        if (tok == "IF"):
            self.CONDICION()
            self.pointer += 1
            tok = self.lexico(self.pointer)
            if(tok == "THEN"):
                self.PROPOSICION()
                self.AUX1()
                self.pointer += 1
                tok = self.lexico(self.pointer)
                if(tok == "END"):
                    self.pointer -= 1
                    print("",end="")
                    # Todo bien,todo correcto?
                else:
                    self.errores("END")
            else:
                self.errores("THEN")

        elif (tok == "WHILE"):
            self.CONDICION()
            self.pointer += 1
            tok = self.lexico(self.pointer)
            if (tok == "DO"):                ############# No cerramos el while
                self.PROPOSICION()
                self.pointer += 1
                tok = self.lexico(self.pointer)
                if (tok == "END"):
                    print("",end="")
                    # Todo bien,todo correcto?
                else:
                    self.errores("END")
            else:
                self.errores("DO")

        elif (tok == "IN"):
            self.NAME()
            self.pointer += 1
            tok = self.lexico(self.pointer)
            if(tok == ";"):
                print("",end="")
                # Todo bien,todo correcto?
            else:
                self.errores(";")
        elif (tok == "OUT"):
            self.NAME()
            self.pointer += 1
            tok = self.lexico(self.pointer)
            if (tok == ";"):
                print("",end="")
                # Todo bien,todo correcto?
            else:
                self.errores(";")
        elif (tok == "CALL"):
            self.NAME()
            self.pointer += 1
            tok = self.lexico(self.pointer)
            if (tok == ";"):
                print("",end="")
                # Todo bien,todo correcto?
            else:
                self.errores(";")
        elif (tok == "NAME"):
            self.pointer += 1
            tok = self.lexico(self.pointer)
            if(tok == "="):
                self.AUX2()
                self.AUX3()
                self.pointer += 1
                tok = self.lexico(self.pointer)
                if (tok == ";"):
                    print("",end="")
                    # Todo bien,todo correcto?
                else:
                    self.errores(";")
            else:
                self.errores("=")
        else:
            self.errores("IF O WHILE O IN O OUT O CALL O NAME")

    def AUX1(self):
        self.pointer += 1
        tok = self.lexico(self.pointer)
        if(tok != "END"):
            if(tok == "ELSE"):
                self.PROPOSICION()

            else:
                self.errores("END")
        else:
            self.pointer-=1

    def AUX2(self):
        self.pointer += 1
        tok = self.lexico(self.pointer)
        if(tok != "+" and tok != "-" and tok != "*" and tok != "/"
        and tok != ";"):
            if (tok == "NAME"):
                print("",end="")
                # Todo bien,todo correcto?
            elif (tok == "VALOR"):
                print("",end="")
                # Todo bien,todo correcto?
            else:
                self.errores("NAME o VALOR")
        else:
            self.pointer -= 1

    def AUX3(self):
        self.pointer += 1
        tok = self.lexico(self.pointer)
        if(tok != ";"):
            if (tok == "+"):
                self.AUX2()
                self.AUX3()
            elif (tok == "-"):
                self.AUX2()
                self.AUX3()
            elif (tok == "*"):
                self.AUX2()
                self.AUX3()
            elif (tok == "/"):
                self.AUX2()
                self.AUX3()
            else:
                self.errores("NAME o VALOR")
        else:
            self.pointer -= 1

    def CONDICION(self):
        self.pointer += 1
        tok = self.lexico(self.pointer)
        if(tok == "("):
            self.AUX4()
            self.pointer += 1
            tok = self.lexico(self.pointer)
            if (tok == ")"):
                print("",end="")
                # Todo bien,todo correcto?
            else:
                self.errores(")")
        else:
            self.errores(")")

    def AUX4(self):
        self.pointer += 1
        tok = self.lexico(self.pointer)
        if(tok == "NAME"):
            self.AUX5()
        elif(tok == "VALOR"):
            self.AUX5()
        else:
            self.errores("NAME o VALOR")
    def AUX5(self):
        self.pointer += 1
        tok = self.lexico(self.pointer)
        if(tok== "=="):
            self.AUX6()
        elif(tok == "=<"):
            self.AUX6()
        elif (tok == "<="):
            self.AUX6()
        elif (tok == ">="):
            self.AUX6()
        elif (tok == "=>"):
            self.AUX6()
        elif (tok == "!="):
            self.AUX6()
        elif (tok == "=!"):
            self.AUX6()
        else:
            self.errores("comparador(==,<=,!= etc)")

    def AUX6(self):
        self.pointer += 1
        tok = self.lexico(self.pointer)
        if (tok == "NAME"):
            self.AUX7()
        elif (tok == "VALOR"):
            self.AUX7()
        else:
            self.errores("NAME o VALOR")

    def AUX7(self):
        self.pointer += 1
        tok = self.lexico(self.pointer)
        if(tok != ")"):
            if (tok == "AND"):
                self.AUX4()
            elif (tok == "OR"):
                self.AUX4()
            else:
                self.errores("AND u OR")
        else:
            self.pointer -= 1



    def errores(self,aux):
        print("Se esperaba "+aux)

def main():
    file = "./RegistroCaracteres.txt"
    comp = Compilador(file)
    for i in range(0,32):
        print(comp.verificar(comp.generador()) , end=" ")
    comp.BLOQUE()

main()
