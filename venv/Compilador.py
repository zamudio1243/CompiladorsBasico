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
        self.tipos=[]
        self.valores=[]
        self.numeros=["0","1","2","3","4","5","6","7","8","9","."]
        self.input=[]
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
        self.input.append(cadena)
        if ( cadena in self.logicos or  
        cadena in self.operadores or
         cadena in self.relacionales 
         or cadena in self.reservadas): #Reservados
            self.sintactico.append(cadena)
            return cadena
        else:
            try:
                if isinstance(float(cadena),float):
                    aux = self.sintactico[len(self.sintactico)-3]
                    if(aux == "INT" or aux == "FLOAT" or aux == "STRING"):
                        self.valores.append(cadena)
                    self.sintactico.append("VALOR")
                    return "VALOR"   
            except:
                aux = self.sintactico[len(self.sintactico) - 1]
                aux2 = self.sintactico[len(self.sintactico)-3]
                if (aux2 == "STRING"):
                    self.valores.append(cadena)
                    self.sintactico.append("VALOR")
                    return "VALOR"
                elif (aux == "INT" or aux == "FLOAT" or aux == "STRING"):
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
            if(tok == "DEFINE"):
                self.DEFINE()
                self.CABECERA()
            elif(tok == "VAR"):
                self.VAR()
                self.CABECERA()
            elif (tok == "FUN"):
                self.FUN()
                self.CABECERA()
            else:
                self.errores(" DEFINE o VAR o FUN")
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
                if(tok == ";"):
                    print("",end="")
                else:
                    self.errores(";")
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
            self.tipos.append(tok)
        elif(tok == "FLOAT"):
            self.tipos.append(tok)
        elif(tok == "STRING"):
            self.tipos.append(tok)
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
                else:
                    self.errores("END")
            else:
                self.errores("THEN")

        elif (tok == "WHILE"):
            self.CONDICION()
            self.pointer += 1
            tok = self.lexico(self.pointer)
            if (tok == "DO"):                # No cerramos el while
                self.PROPOSICION()
                self.pointer += 1
                tok = self.lexico(self.pointer)
                if (tok == "END"):
                    print("",end="")
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
            else:
                self.errores(";")
        elif (tok == "OUT"):
            self.NAME()
            self.pointer += 1
            tok = self.lexico(self.pointer)
            if (tok == ";"):
                print("",end="")
            else:
                self.errores(";")
        elif (tok == "CALL"):
            self.NAME()
            self.pointer += 1
            tok = self.lexico(self.pointer)
            if (tok == ";"):
                print("",end="")
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
            elif (tok == "VALOR"):
                print("",end="")
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

    def semantico(self):
        #Verificamos duplicidad en nombres de variables
        error = False
        for i in range(0, len(self.guardados)):
            aux = self.guardados[i]
            for j in range(i+1, len(self.guardados)):
                error = aux == self.guardados[j]
                if(error):
                    print("Repetiste variable")
                    error = False
        #Verificamos coherencia en valor y tipo de dato
        error = False
        for i in range(0, len(self.tipos)):
            if(self.tipos[i] == 'INT'):
                try:
                    result = isinstance(int(self.valores[i]),int)
                except:
                    print(self.guardados[i]+" no es entero")
            elif(self.tipos[i] == 'FLOAT'):
                result = isinstance(float(self.valores[i]), float)
                if not (result):
                    print(self.guardados[i] + " no es float")
            elif(self.tipos[i] == 'STRING'):
                try:
                    result = isinstance(float(self.valores[i]), float)
                    if result:
                        print(self.guardados[i] + " no es string")
                except:
                    print()
        #Verificamos si se usa y no esta declarada
        for i in range(0,len(self.sintactico)):
            if(self.sintactico[i]=="NAME"):
                if not(self.input[i] in self.guardados):
                    print("No se declaro "+self.input[i])
        #Verificamos si coinciden los tipos en operaciones aritmeticas
        error=False
        aux=self.relacionales
        aux.remove("{")
        aux.remove("}")
        aux.remove("(")
        aux.remove(")")
        for i in range(0,len(self.input)):
            if(self.input[i] in aux or self.input[i] in self.operadores
            or self.input[i] in self.logicos):
                if(self.input[i-1] in self.guardados or self.input[i+1] in self.guardados):
                    aux1= self.input[i-1]
                    aux2= self.input[i+1]
                    
                    try:
                            if not(isinstance(aux1, int) and isinstance(aux2, int)):
                                print("No coinciden los tipos de " + aux1 + " y " + aux2)
                    except:
                        try:
                            if not(isinstance(aux1, float) and isinstance(aux2, float)):
                                print("No coinciden los tipos de " + aux1 + " y " + aux2)  
                        except:
                            try:
                                if not(isinstance(aux1, float) and isinstance(aux2, float)):
                                        print("No coinciden los tipos de " + aux1 + " y " + aux2)
                            except:
                                print()


def main():
    file = "./RegistroCaracteres.txt"
    comp = Compilador(file)
    for i in range(0,56):
        print(comp.verificar(comp.generador()) , end=" ")
    comp.BLOQUE()
    #print(comp.input) """
    #print(comp.guardados)
    #print(comp.tipos)
    #print(comp.valores)
    comp.semantico()

main()