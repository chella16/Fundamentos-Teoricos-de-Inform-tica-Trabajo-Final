"""
Reconocedor de Gramática - Autómata Finito No Determinista
Reconoce secuencias que siguen los patrones:
- comienza -> leer -> <variable> -> termina
- comienza -> escribir -> <expresion> -> termina
- comienza -> <variable>=<expresion> -> termina
- comienza -> si -> <condicion> -> entonces -> <instrucciones> -> finsi -> termina (condicional simple)
- comienza -> si -> <condicion> -> entonces -> <instrucciones> -> sino -> <instrucciones> -> finsi -> termina (condicional doble)
- comienza -> mientras -> <condicion> -> hacer -> <instrucciones> -> finmientras -> termina (bucle while)
-            print("Formato del archivo .txt:")
            print("  MODO 1 - Líneas individuales:")
            print("    - Una cadena por línea")
            print("    - Cada línea es un pseudocódigo completo")
            print("  MODO 2 - Pseudocódigo multi-línea:")
            print("    - Un pseudocódigo dividido en múltiples líneas")
            print("    - Bloques separados por líneas vacías o comentarios")
            print("    - Detectado automáticamente")
            print("  GENERAL:")
            print("    - Las líneas que comienzan con # son comentarios y se ignoran")
            print("    - Las líneas vacías actúan como separadores en modo multi-línea")ienza -> repetir -> <instrucciones> -> hastaque -> <condicion> -> termina (bucle do-while)
- Combinaciones de leer, escribir, asignaciones, condicionales y bucles dentro del mismo programa

Estados:
- q0: Estado inicial
- q1: Estado después de "comienza" (permite leer, escribir, asignación, si, mientras, repetir o termina)
- q2: Estado final después de "termina"
- q3: Estado después de "leer" (bucle con <variable>)
- q4: Estado después de "escribir" (bucle con <expresion>)
- q5: Estado para asignaciones <variable>=<expresion> (bucle directo a q1)
- q28: Estado después de <variable>=<expresion> (espera punto y coma)
- q29: Estado después de escribir <expresion> (espera punto y coma)
- q6: Estado después de "si" (espera <condicion>)
- q7: Estado después de <condicion> del if (espera "entonces")
- q8: Estado después de "entonces" (bucle con <instrucciones>, puede ir a "sino" o "finsi")
- q9: Estado después de "sino" (bucle con <instrucciones>, termina con "finsi")
- q10: Estado después de "mientras" (espera <condicion>)
- q11: Estado después de <condicion> del while (espera "hacer")
- q12: Estado después de "hacer" (bucle con <instrucciones>, termina con "finmientras")
- q13: Estado después de "repetir" (bucle con <instrucciones>, termina con "hastaque")
- q14: Estado después de "hastaque" (espera <condicion>)
- q15: Estado después de "si" anidado (espera <condicion>)
- q16: Estado después de <condicion> del if anidado (espera "entonces")
- q17: Estado después de "entonces" anidado (bucle con <instrucciones>, puede ir a "sino" o "finsi")
- q18: Estado después de "mientras" anidado (espera <condicion>)
- q19: Estado después de <condicion> del while anidado (espera "hacer")
- q20: Estado después de "hacer" anidado (bucle con <instrucciones>, termina con "finmientras")
- q21: Estado después de "sino" anidado (bucle con <instrucciones>, termina con "finsi")
"""

class AutomataReconocedor:
    def __init__(self):
        # Definición de estados
        self.estados = {'q0', 'q1', 'q2', 'q3', 'q4', 'q5', 'q6', 'q7', 'q8', 'q9', 'q10', 'q11', 'q12', 'q13', 'q14', 
                        'q15', 'q16', 'q17', 'q18', 'q19', 'q20', 'q21', 'q28', 'q29', 'q30'}
        self.estado_inicial = 'q0'
        self.estados_finales = {'q2'}
        
        # Palabras válidas del lenguaje (incluye versiones en minúsculas y PascalCase)
        self.palabras_validas = {
            'comienza': 'COMIENZA',
            'leer': 'LEER',
            'escribir': 'ESCRIBIR',
            'si': 'SI',
            'entonces': 'ENTONCES',
            'sino': 'SINO',
            'finsi': 'FINSI',
            'mientras': 'MIENTRAS',
            'hacer': 'HACER',
            'finmientras': 'FINMIENTRAS',
            'repetir': 'REPETIR',
            'hastaque': 'HASTAQUE',
            'termina': 'TERMINA',
            ';': 'PUNTO_COMA',
            # Versiones en PascalCase
            'Comienza': 'COMIENZA',
            'Leer': 'LEER',
            'Escribir': 'ESCRIBIR',
            'Si': 'SI',
            'Entonces': 'ENTONCES',
            'Sino': 'SINO',
            'FinSi': 'FINSI',
            'Mientras': 'MIENTRAS',
            'Hacer': 'HACER',
            'FinMientras': 'FINMIENTRAS',
            'Repetir': 'REPETIR',
            'HastaQue': 'HASTAQUE',
            'Hasta': 'HASTAQUE',  # Versión corta
            'Termina': 'TERMINA'
        }
        
        # Transiciones del autómata
        # Formato: (estado_actual, simbolo) -> conjunto de estados siguientes
        self.transiciones = {
            ('q0', 'COMIENZA'): {'q1'},
            ('q1', 'LEER'): {'q3'},
            ('q1', 'ESCRIBIR'): {'q4'},  # Nueva transición para Escribir
            ('q1', 'ASIGNACION'): {'q28'},  # asignación -> variable=<expresion> -> espera punto y coma
            ('q1', 'SI'): {'q6'},  # Nueva transición para condicional
            ('q1', 'MIENTRAS'): {'q10'},  # Nueva transición para bucle while
            ('q1', 'REPETIR'): {'q13'},  # Nueva transición para bucle do-while
            ('q1', 'TERMINA'): {'q2'},
            ('q3', 'VARIABLE'): {'q30'},  # leer -> variable -> espera punto y coma
            ('q30', 'PUNTO_COMA'): {'q1'},  # leer variable; -> vuelve a q1
            ('q4', 'EXPRESION'): {'q29'},  # escribir -> <expresion> -> espera punto y coma
            ('q6', 'CONDICION'): {'q7'},  # si -> <condicion> -> entonces
            ('q7', 'ENTONCES'): {'q8'},  # entonces -> <instrucciones>
            ('q8', 'INSTRUCCIONES'): {'q8'},  # instrucciones pueden repetirse
            ('q8', 'SINO'): {'q9'},  # sino -> <instrucciones> del else
            ('q8', 'FINSI'): {'q1'},  # finsi -> vuelve a q1 (condicional simple)
            ('q9', 'INSTRUCCIONES'): {'q9'},  # instrucciones del else pueden repetirse
            ('q9', 'FINSI'): {'q1'},  # finsi -> vuelve a q1 (condicional doble)
            ('q10', 'CONDICION'): {'q11'},  # mientras -> <condicion> -> hacer
            ('q11', 'HACER'): {'q12'},  # hacer -> <instrucciones>
            ('q12', 'INSTRUCCIONES'): {'q12'},  # instrucciones pueden repetirse
            ('q12', 'FINMIENTRAS'): {'q1'},  # finmientras -> vuelve a q1
            ('q13', 'INSTRUCCIONES'): {'q13'},  # repetir -> <instrucciones> (pueden repetirse)  
            ('q13', 'HASTAQUE'): {'q14'},  # hastaque -> <condicion>
            ('q14', 'CONDICION'): {'q1'},  # condicion -> vuelve a q1
            
            # TRANSICIONES PARA ESTRUCTURAS ANIDADAS (UN NIVEL ÚNICAMENTE)
            # Desde q8 (después de ENTONCES) se puede ir a while anidado
            ('q8', 'MIENTRAS'): {'q18'},   # while anidado dentro de if
            
            # Desde q9 (después de SINO) se puede ir a while anidado  
            ('q9', 'MIENTRAS'): {'q18'},   # while anidado dentro de else
            
            # Desde q12 (después de HACER en while) se puede ir a if anidado
            ('q12', 'SI'): {'q15'},        # if anidado dentro de while
            
            # Estados para IF anidado dentro de WHILE (q15-q17, q21)
            ('q15', 'CONDICION'): {'q16'}, # si anidado -> <condicion>
            ('q16', 'ENTONCES'): {'q17'},  # entonces anidado -> <instrucciones>
            ('q17', 'INSTRUCCIONES'): {'q17'}, # instrucciones anidadas pueden repetirse
            ('q17', 'SINO'): {'q21'},      # sino anidado -> <instrucciones> del else
            ('q17', 'FINSI'): {'q12'},     # finsi -> vuelve al contexto del while
            
            # Estado para SINO anidado dentro de WHILE
            ('q21', 'INSTRUCCIONES'): {'q21'}, # instrucciones del else anidado pueden repetirse
            ('q21', 'FINSI'): {'q12'},     # finsi -> vuelve al contexto del while
            
            # Estados para WHILE anidado dentro de IF (q18-q20)  
            ('q18', 'CONDICION'): {'q19'}, # mientras anidado -> <condicion>
            ('q19', 'HACER'): {'q20'},     # hacer anidado -> <instrucciones>
            ('q20', 'INSTRUCCIONES'): {'q20'}, # instrucciones anidadas pueden repetirse
            ('q20', 'FINMIENTRAS'): {'q8', 'q9'}, # finmientras -> vuelve al contexto del if (puede ser then o else)
            
            # Estados para punto y coma en escribir y asignación
            ('q28', 'PUNTO_COMA'): {'q1'},  # asignación con punto y coma -> vuelve a q1
            ('q29', 'PUNTO_COMA'): {'q1'},  # escribir con punto y coma -> vuelve a q1
        }
    
    def es_variable(self, palabra):
        """
        Verifica si una palabra es una variable válida
        Solo acepta variables sin < > (para leer y lado izquierdo de asignaciones)
        """
        # Variable sin < > (para leer y asignaciones)
        if palabra.isalnum() and palabra not in self.palabras_validas:
            return True
        return False
    
    def es_expresion(self, palabra):
        """
        Verifica si una palabra es una expresión válida
        Acepta contenido alfanumérico con < > o sin < >
        """
        # Expresión con < >
        if palabra.startswith('<') and palabra.endswith('>'):
            contenido = palabra[1:-1]  # Quita los < >
            return len(contenido) > 0 and contenido.isalnum()
        # Expresión sin < > (para escribir)
        elif palabra.isalnum() and palabra not in self.palabras_validas:
            return True
        return False
    
    def es_asignacion(self, palabra):
        """
        Verifica si una palabra es una asignación válida del formato variable=expresion
        La variable debe ser sin < > y la expresión puede ser con o sin < >
        Nota: El punto y coma ahora es un token separado
        """
        if '=' in palabra:
            partes = palabra.split('=', 1)  # Dividir solo en el primer =
            if len(partes) == 2:
                variable, expresion = partes
                # Variable sin < > (obligatorio)
                if variable.isalnum() and variable not in self.palabras_validas:
                    # Expresión con < >
                    if expresion.startswith('<') and expresion.endswith('>'):
                        exp_contenido = expresion[1:-1]  # quitar < >
                        return len(exp_contenido) > 0 and exp_contenido.isalnum()
                    # Expresión sin < >
                    elif expresion.isalnum() and expresion not in self.palabras_validas:
                        return True
        return False
    
    def es_condicion(self, palabra):
        """
        Verifica si una palabra es una condición válida
        Acepta contenido alfanumérico encerrado entre < >
        """
        if palabra.startswith('<') and palabra.endswith('>'):
            contenido = palabra[1:-1]  # Quita los < >
            return len(contenido) > 0 and contenido.isalnum()
        return False
    
    def es_instrucciones(self, palabra):
        """
        Verifica si una palabra son instrucciones válidas
        Acepta contenido alfanumérico encerrado entre < >
        """
        if palabra.startswith('<') and palabra.endswith('>'):
            contenido = palabra[1:-1]  # Quita los < >
            return len(contenido) > 0 and contenido.isalnum()
        return False
    
    def dividir_pascal_case(self, texto):
        """
        Divide una cadena PascalCase concatenada en palabras individuales
        Ej: 'ComenzaSi' -> ['Comienza', 'Si']
        """
        if not texto:
            return []
            
        # Obtener todas las palabras válidas excluyendo símbolos especiales
        palabras_validas = [p for p in self.palabras_validas.keys() 
                           if p not in [';'] and not p.startswith('<')]
        
        palabras_posibles = []
        
        def buscar_division(texto_restante, palabras_actuales):
            if not texto_restante:
                palabras_posibles.append(palabras_actuales[:])
                return
            
            # Intentar encontrar palabras que empiecen en la posición actual
            for palabra in sorted(palabras_validas, key=len, reverse=True):
                if texto_restante.startswith(palabra):
                    palabras_actuales.append(palabra)
                    buscar_division(texto_restante[len(palabra):], palabras_actuales)
                    palabras_actuales.pop()
        
        buscar_division(texto, [])
        
        # Retornar la división más larga (más palabras encontradas)
        if palabras_posibles:
            return max(palabras_posibles, key=len)
        return []

    def tokenizar_cadena_sin_espacios(self, cadena):
        """
        Tokeniza una cadena que puede estar escrita sin espacios en PascalCase
        Reconoce palabras PascalCase consecutivas como tokens separados
        """
        tokens = []
        i = 0
        
        while i < len(cadena):
            token_encontrado = False
            
            # Buscar asignaciones <var>=<exp> primero (más específico)
            if cadena[i] == '<':
                # Buscar patrón <var>=<exp>
                primer_cierre = cadena.find('>', i)
                if primer_cierre != -1 and primer_cierre + 1 < len(cadena) and cadena[primer_cierre + 1] == '=':
                    segundo_inicio = primer_cierre + 2
                    if segundo_inicio < len(cadena) and cadena[segundo_inicio] == '<':
                        segundo_cierre = cadena.find('>', segundo_inicio)
                        if segundo_cierre != -1:
                            asignacion = cadena[i:segundo_cierre+1]
                            # Verificar si termina con punto y coma
                            if segundo_cierre + 1 < len(cadena) and cadena[segundo_cierre + 1] == ';':
                                tokens.append(asignacion)
                                tokens.append(';')
                                i = segundo_cierre + 2
                            else:
                                tokens.append(asignacion)
                                i = segundo_cierre + 1
                            token_encontrado = True
                
                # Si no es asignación, buscar elementos <...> simples
                if not token_encontrado:
                    fin_elemento = cadena.find('>', i)
                    if fin_elemento != -1:
                        elemento = cadena[i:fin_elemento+1]
                        # Verificar si termina con punto y coma
                        if fin_elemento + 1 < len(cadena) and cadena[fin_elemento + 1] == ';':
                            tokens.append(elemento)
                            tokens.append(';')
                            i = fin_elemento + 2
                        else:
                            tokens.append(elemento)
                            i = fin_elemento + 1
                        token_encontrado = True
            
            # Buscar punto y coma individual
            elif cadena[i] == ';':
                tokens.append(';')
                i += 1
                token_encontrado = True
            
            # Buscar palabras reservadas en PascalCase (incluyendo concatenadas)
            if not token_encontrado:
                # Intentar encontrar el segmento más largo de texto que se puede dividir
                mejor_segmento = ""
                mejor_division = []
                
                # Buscar hacia adelante hasta encontrar un delimitador o final
                j = i
                while j < len(cadena) and cadena[j] not in '<;':
                    j += 1
                
                segmento_texto = cadena[i:j]
                if segmento_texto:
                    # Intentar dividir este segmento
                    division = self.dividir_pascal_case(segmento_texto)
                    if division:
                        # Agregar todas las palabras encontradas
                        for palabra in division:
                            tokens.append(palabra)
                        i = j
                        token_encontrado = True
                    else:
                        # Intentar palabra individual más larga
                        palabras_candidatas = []
                        for palabra in sorted(self.palabras_validas.keys(), key=len, reverse=True):
                            if palabra != ';' and i + len(palabra) <= len(cadena) and cadena[i:i+len(palabra)] == palabra:
                                palabras_candidatas.append(palabra)
                        
                        if palabras_candidatas:
                            palabra_elegida = palabras_candidatas[0]
                            tokens.append(palabra_elegida)
                            i += len(palabra_elegida)
                            token_encontrado = True
            
            if not token_encontrado:
                # Token no reconocido, avanzar un caracter y marcarlo como inválido
                tokens.append(cadena[i])
                i += 1
        
        return tokens

    def analizar_palabras(self, entrada):
        """
        Convierte la entrada en palabras/símbolos válidos
        Maneja tanto entrada con espacios como sin espacios en PascalCase
        """
        # Si la entrada contiene espacios, usar el método tradicional
        if ' ' in entrada:
            palabras = entrada.split()
        else:
            # Si no tiene espacios, tokenizar la cadena
            palabras = self.tokenizar_cadena_sin_espacios(entrada)
        
        palabras_procesadas = []

        for palabra in palabras:
            # Verificar si la palabra termina con punto y coma
            if palabra.endswith(';') and len(palabra) > 1:
                palabra_sin_punto_coma = palabra[:-1]  # Quitar el punto y coma
                
                # Procesar la palabra sin punto y coma
                if palabra_sin_punto_coma in self.palabras_validas:
                    palabras_procesadas.append(self.palabras_validas[palabra_sin_punto_coma])
                elif self.es_asignacion(palabra_sin_punto_coma):
                    palabras_procesadas.append('ASIGNACION')
                elif (self.es_variable(palabra_sin_punto_coma) or self.es_expresion(palabra_sin_punto_coma) or 
                      self.es_condicion(palabra_sin_punto_coma) or self.es_instrucciones(palabra_sin_punto_coma)):
                    palabras_procesadas.append('ELEMENTO')
                else:
                    palabras_procesadas.append('INVALIDO')
                
                # Agregar el punto y coma como token separado
                palabras_procesadas.append('PUNTO_COMA')
                
            elif palabra in self.palabras_validas:
                palabras_procesadas.append(self.palabras_validas[palabra])
            elif palabra == ';':
                palabras_procesadas.append('PUNTO_COMA')
            elif self.es_asignacion(palabra):
                palabras_procesadas.append('ASIGNACION')
            elif (self.es_variable(palabra) or self.es_expresion(palabra) or 
                  self.es_condicion(palabra) or self.es_instrucciones(palabra)):
                # Las clasificamos como elementos genéricos
                # El contexto determinará si es VARIABLE, EXPRESION, CONDICION o INSTRUCCIONES
                palabras_procesadas.append('ELEMENTO')
            else:
                palabras_procesadas.append('INVALIDO')

        return palabras_procesadas
    
    def procesar_cadena(self, cadena):
        """
        Procesa una cadena de entrada y determina si es aceptada por el autómata
        """
        palabras = self.analizar_palabras(cadena)
        print(f"Palabras procesadas: {palabras}")

        # Conjunto de estados actuales (para NFAs)
        estados_actuales = {self.estado_inicial}

        for palabra in palabras:
            if palabra == 'INVALIDO':
                print(f"Palabra inválida encontrada: {palabra}")
                return False

            # Convertir ELEMENTO según el contexto
            if palabra == 'ELEMENTO':
                # Si estamos en q3 (después de LEER), debe ser VARIABLE
                if 'q3' in estados_actuales:
                    palabra = 'VARIABLE'
                # Si estamos en q4 (después de ESCRIBIR), debe ser EXPRESION
                elif 'q4' in estados_actuales:
                    palabra = 'EXPRESION'
                # Si estamos en q6 (después de SI), debe ser CONDICION
                elif 'q6' in estados_actuales:
                    palabra = 'CONDICION'
                # Si estamos en q8 (después de ENTONCES), debe ser INSTRUCCIONES
                elif 'q8' in estados_actuales:
                    palabra = 'INSTRUCCIONES'
                # Si estamos en q9 (después de SINO), debe ser INSTRUCCIONES
                elif 'q9' in estados_actuales:
                    palabra = 'INSTRUCCIONES'
                # Si estamos en q10 (después de MIENTRAS), debe ser CONDICION
                elif 'q10' in estados_actuales:
                    palabra = 'CONDICION'
                # Si estamos en q12 (después de HACER), debe ser INSTRUCCIONES
                elif 'q12' in estados_actuales:
                    palabra = 'INSTRUCCIONES'
                # Si estamos en q13 (después de REPETIR), debe ser INSTRUCCIONES
                elif 'q13' in estados_actuales:
                    palabra = 'INSTRUCCIONES'
                # Si estamos en q14 (después de HASTAQUE), debe ser CONDICION
                elif 'q14' in estados_actuales:
                    palabra = 'CONDICION'
                    
                # Estados anidados - IF anidado
                elif 'q15' in estados_actuales:  # después de SI anidado
                    palabra = 'CONDICION'
                elif 'q17' in estados_actuales:  # después de ENTONCES anidado
                    palabra = 'INSTRUCCIONES'
                elif 'q21' in estados_actuales:  # después de SINO anidado
                    palabra = 'INSTRUCCIONES'
                    
                # Estados anidados - WHILE anidado  
                elif 'q18' in estados_actuales:  # después de MIENTRAS anidado
                    palabra = 'CONDICION'
                elif 'q20' in estados_actuales:  # después de HACER anidado
                    palabra = 'INSTRUCCIONES'

            nuevos_estados = set()

            # Para cada estado actual, buscar transiciones válidas
            for estado in estados_actuales:
                transicion = (estado, palabra)
                if transicion in self.transiciones:
                    nuevos_estados.update(self.transiciones[transicion])

            if not nuevos_estados:
                print(f"No hay transición válida desde {estados_actuales} con palabra '{palabra}'")
                return False

            estados_actuales = nuevos_estados
            print(f"Después de '{palabra}': estados actuales = {estados_actuales}")
        
        # Verificar si algún estado actual es final
        es_aceptada = bool(estados_actuales.intersection(self.estados_finales))
        return es_aceptada
    
    def mostrar_automata(self):
        """
        Muestra la estructura del autómata
        """
        print("=== AUTÓMATA FINITO NO DETERMINISTA ===")
        print(f"Estados: {self.estados}")
        print(f"Estado inicial: {self.estado_inicial}")
        print(f"Estados finales: {self.estados_finales}")
        print("\nTransiciones:")
        for (estado, simbolo), destinos in self.transiciones.items():
            for destino in destinos:
                print(f"  {estado} --({simbolo})--> {destino}")
        print("\nPalabras del lenguaje: comienza/Comienza, leer/Leer, escribir/Escribir, si/Si, entonces/Entonces, sino/Sino, finsi/FinSi, mientras/Mientras, hacer/Hacer, finmientras/FinMientras, repetir/Repetir, hastaque/HastaQue/Hasta, <variable>, <expresion>, <condicion>, <instrucciones>, <var>=<exp>, ;, termina/Termina")
        print("Patrones aceptados:")
        print("  - comienza [leer <variable>]* termina")
        print("  - comienza [escribir <expresion>;]* termina") 
        print("  - comienza [<variable>=<expresion>;]* termina")
        print("  - comienza [si <condicion> entonces <instrucciones>* finsi]* termina")
        print("  - comienza [si <condicion> entonces <instrucciones>* sino <instrucciones>* finsi]* termina")
        print("  - comienza [mientras <condicion> hacer <instrucciones>* finmientras]* termina")
        print("  - comienza [repetir <instrucciones>* hastaque <condicion>]* termina")
        print("  - Combinaciones de leer, escribir, asignaciones, condicionales y bucles")


def procesar_archivo(automata, ruta_archivo):
    """
    Procesa cadenas desde un archivo de texto
    """
    try:
        lineas = ''
        with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
            for line in archivo:  
                lineas +=line.strip()

        lineas =[lineas.replace(" ","")]
        
        print(f"\nPROCESANDO ARCHIVO: {ruta_archivo}")
        print("=" * 50)
        
        for i, linea in enumerate(lineas, 1):
            cadena = linea.strip()
            if not cadena or cadena.startswith('#'):  # Ignorar líneas vacías y comentarios
                continue
                
            print(f"\nLínea {i}: '{cadena}'")
            resultado = automata.procesar_cadena(cadena)
            print(f"Resultado: {'ACEPTADA' if resultado else 'RECHAZADA'}")
            print("-" * 30)
            
    except FileNotFoundError:
        print(f"Error: No se pudo encontrar el archivo '{ruta_archivo}'")
        print("Asegúrate de que el archivo existe y la ruta es correcta.")
    except Exception as e:
        print(f"Error al procesar el archivo: {e}")
def procesar_modo_individual(automata, lineas):
    """
    Procesa el archivo en modo líneas individuales (modo tradicional)
    """
    for i, linea in enumerate(lineas, 1):
        cadena = linea.strip()
        if not cadena or cadena.startswith('#'):  # Ignorar líneas vacías y comentarios
            continue
            
        print(f"\nLínea {i}: '{cadena}'")
        resultado = automata.procesar_cadena(cadena)
        print(f"Resultado: {'ACEPTADA' if resultado else 'RECHAZADA'}")
        print("-" * 30)

def procesar_modo_multilinea(automata, contenido):
    """
    Procesa el archivo en modo multi-línea donde un pseudocódigo
    puede estar dividido en múltiples líneas
    """
    # Dividir por bloques separados por líneas vacías o comentarios
    bloques = []
    bloque_actual = []
    
    for linea in contenido.split('\n'):
        linea_limpia = linea.strip()
        
        # Si es línea vacía o comentario, finalizar bloque actual
        if not linea_limpia or linea_limpia.startswith('#'):
            if bloque_actual:
                # Unir todas las líneas del bloque en una sola cadena
                pseudocodigo = ' '.join(bloque_actual)
                bloques.append(pseudocodigo)
                bloque_actual = []
        else:
            bloque_actual.append(linea_limpia)
    
    # Procesar último bloque si existe
    if bloque_actual:
        pseudocodigo = ' '.join(bloque_actual)
        bloques.append(pseudocodigo)
    
    # Si solo hay un bloque, procesar todo como una sola cadena
    if len(bloques) == 1:
        print(f"\nPseudocódigo completo: '{bloques[0]}'")
        resultado = automata.procesar_cadena(bloques[0])
        print(f"Resultado: {'ACEPTADA' if resultado else 'RECHAZADA'}")
        print("-" * 30)
    else:
        # Procesar cada bloque por separado
        for i, pseudocodigo in enumerate(bloques, 1):
            print(f"\nPseudocódigo {i}: '{pseudocodigo}'")
            resultado = automata.procesar_cadena(pseudocodigo)
            print(f"Resultado: {'ACEPTADA' if resultado else 'RECHAZADA'}")
            print("-" * 30)

def mostrar_opciones():
    # Preguntar al usuario qué modo quiere usar
    print("\nOPCIONES:")
    print("1. Ejecutar pruebas automáticas")
    print("2. Procesar archivo .txt")
    print("3. Modo interactivo")
    print("4. Limpiar consola")
    print("5. Salir")

def main():
    """
    Función principal del programa
    """
    import sys
    import os
    
    automata = AutomataReconocedor()
    
    print("RECONOCEDOR DE GRAMÁTICA")
    print("=" * 50)
    
    # Verificar argumentos de línea de comandos
    if len(sys.argv) > 1:
        if sys.argv[1] == '--help' or sys.argv[1] == '-h':
            print("Uso del programa:")
            print("  python reconocedor_gramatica.py                    # Modo interactivo")
            print("  python reconocedor_gramatica.py <archivo.txt>      # Procesar archivo")
            print("  python reconocedor_gramatica.py --test             # Ejecutar pruebas automáticas")
            print("  python reconocedor_gramatica.py --help             # Mostrar esta ayuda")
            print("\nFormato del archivo .txt:")
            print("  - Una cadena por línea")
            print("  - Las líneas que comienzan con # son comentarios y se ignoran")
            print("  - Las líneas vacías se ignoran")
            return
        elif sys.argv[1] == '--test':
            # Mostrar información del autómata y ejecutar pruebas
            automata.mostrar_automata()
            print("\n" + "=" * 50)
            ejecutar_pruebas_automaticas(automata)
            return
        else:
            # Procesar archivo
            ruta_archivo = sys.argv[1]
            automata.mostrar_automata()
            print("\n" + "=" * 50)
            procesar_archivo(automata, ruta_archivo)
            return
    
    # Modo por defecto: mostrar información y modo interactivo
    automata.mostrar_automata()
    print("\n" + "=" * 50)
    
    # Preguntar al usuario qué modo quiere usar
    mostrar_opciones()
    
    while True:
        try:
            opcion = input("\nSelecciona una opción (1-5): ").strip()
            if opcion == '1':
                ejecutar_pruebas_automaticas(automata)
            elif opcion == '2':
                ruta_archivo = input("Ingresa la ruta del archivo .txt: ").strip()
                procesar_archivo(automata, ruta_archivo)
            elif opcion == '3':
                modo_interactivo(automata)
            elif opcion == '4':
                # Limpiar pantalla (funciona en Windows y Linux/Mac)
                os.system('cls' if os.name == 'nt' else 'clear')
                print("RECONOCEDOR DE GRAMÁTICA")
                print("=" * 50)
            elif opcion == '5':
                print("¡Hasta luego!")
                break
            else:
                print("Opción inválida. Por favor selecciona 1, 2, 3, 4 ó 5.")
                continue
            mostrar_opciones()
            
        except KeyboardInterrupt:
            print("\n\n¡Hasta luego!")
            break

def ejecutar_pruebas_automaticas(automata):
    """
    Ejecuta las pruebas automáticas predefinidas
    """
    # Ejemplos de prueba
    ejemplos = [
        "comienza termina",
        "comienza leer <x> termina",
        "comienza leer <variable1> leer <y> termina",
        "comienza leer <a> leer <b> leer <c> termina",
        "comienza escribir <mensaje>; termina",  # Nuevo: usando escribir con punto y coma
        "comienza escribir <resultado>; termina",  # Nuevo: escribir expresión con punto y coma
        "comienza leer <x> escribir <x>; termina",  # Nuevo: combinando leer y escribir
        "comienza escribir <saludo>; leer <nombre> escribir <despedida>; termina",  # Nuevo: múltiples operaciones
        "comienza <x>=<5>; termina",  # Nuevo: asignación simple con punto y coma
        "comienza <resultado>=<suma>; termina",  # Nuevo: asignación con nombres largos
        "comienza leer <a> <b>=<a>; termina",  # Nuevo: combinando leer y asignación
        "comienza <x>=<10>; escribir <x>; termina",  # Nuevo: asignación y escritura
        "comienza <a>=<1>; <b>=<2>; <c>=<suma>; termina",  # Nuevo: múltiples asignaciones
        "comienza si <condicion1> entonces <accion1> finsi termina",  # Nuevo: condicional simple
        "comienza si <x> entonces <y>=<10> finsi termina",  # Nuevo: condicional con asignación
        "comienza si <edad> entonces escribir <mensaje> finsi termina",  # Nuevo: condicional con escritura
        "comienza si <test> entonces <inst1> <inst2> finsi termina",  # Nuevo: múltiples instrucciones
        "comienza leer <x> si <x> entonces escribir <x> finsi termina",  # Nuevo: combinando todo
        "comienza si <condicion> entonces <accion1> sino <accion2> finsi termina",  # Nuevo: condicional doble
        "comienza si <x> entonces <inst1> sino <inst2> finsi termina",  # Nuevo: if-else simple
        "comienza si <edad> entonces <msg1> <msg2> sino <msg3> finsi termina",  # Nuevo: múltiples instrucciones en ambas ramas
        "comienza leer <x> si <x> entonces <y> sino <z> finsi termina",  # Nuevo: combinando leer con if-else
        "comienza mientras <condicion1> hacer <accion1> finmientras termina",  # Nuevo: bucle while simple
        "comienza mientras <x> hacer <inst1> <inst2> finmientras termina",  # Nuevo: múltiples instrucciones en while
        "comienza leer <x> mientras <x> hacer <y>=<10> finmientras termina",  # Nuevo: combinando leer con while
        "comienza mientras <contador> hacer <incremento> finmientras escribir <resultado> termina",  # Nuevo: while con escritura
        "comienza repetir <accion1> hastaque <condicion1> termina",  # Nuevo: do-while simple
        "comienza repetir <inst1> <inst2> hastaque <test> termina",  # Nuevo: múltiples instrucciones en do-while
        "comienza leer <x> repetir <proceso> hastaque <fin> termina",  # Nuevo: combinando leer con do-while
        "comienza repetir <calculo> hastaque <limite> escribir <resultado> termina",  # Nuevo: do-while con escritura
        "comienza si <condicion> entonces mientras <cond2> hacer <inst> finmientras finsi termina",  # Nuevo: while dentro de if
        "comienza mientras <condicion> hacer si <cond2> entonces <inst> finsi finmientras termina",  # Nuevo: if dentro de while
        "comienza mientras <condicion> hacer si <cond2> entonces <inst1> sino <inst2> finsi finmientras termina",  # Nuevo: if-else dentro de while
        # Ejemplos con PascalCase sin espacios
        "ComenzaLeer<x>Termina",  # Nuevo: PascalCase sin espacios
        "ComenzaEscribir<mensaje>;Termina",  # Nuevo: PascalCase escribir con punto y coma
        "Comienza<x>=<5>;Termina",  # Nuevo: PascalCase asignación con punto y coma
        "ComenzaSi<condicion>Entonces<accion>FinSiTermina",  # Nuevo: PascalCase condicional
        "ComenzaMientras<contador>Hacer<incremento>FinMientrasTermina",  # Nuevo: PascalCase while
        "ComenzaRepetir<calculo>Hasta<limite>Termina",  # Nuevo: PascalCase do-while
        "leer <x> termina",  # Inválido: no comienza con "comienza"
        "comienza leer termina",  # Inválido: falta variable después de leer
        "comienza escribir termina",  # Inválido: falta expresión después de escribir
        "comienza escribir <mensaje> termina",  # Inválido: falta punto y coma después de expresión
        "comienza <x>=<5> termina",  # Inválido: falta punto y coma después de asignación
        "comienza <x>= termina",  # Inválido: asignación incompleta
        "comienza =<5> termina",  # Inválido: falta variable en asignación
        "comienza si <cond> entonces finsi termina",  # Inválido: falta instrucción
        "comienza si entonces <inst> finsi termina",  # Inválido: falta condición
        "comienza si <cond> <inst> finsi termina",  # Inválido: falta 'entonces'
        "comienza si <cond> entonces <inst> termina",  # Inválido: falta 'finsi'
        "comienza si <cond> entonces <inst1> sino termina",  # Inválido: falta instrucción después de sino
        "comienza si <cond> entonces sino <inst> finsi termina",  # Inválido: falta instrucción antes de sino
        "comienza si <cond> sino <inst> finsi termina",  # Inválido: falta 'entonces'
        "comienza mientras <cond> <inst> finmientras termina",  # Inválido: falta 'hacer'
        "comienza mientras hacer <inst> finmientras termina",  # Inválido: falta condición
        "comienza mientras <cond> hacer finmientras termina",  # Inválido: falta instrucción
        "comienza mientras <cond> hacer <inst> termina",  # Inválido: falta 'finmientras'
        "comienza repetir hastaque <cond> termina",  # Inválido: falta instrucción
        "comienza repetir <inst> <cond> termina",  # Inválido: falta 'hastaque'
        "comienza repetir <inst> hastaque termina",  # Inválido: falta condición
        "comienza leer <x>",  # Inválido: no termina con "termina" 
        "comienza termina leer <x>",  # Inválido: orden incorrecto
    ]
    
    print("\nPRUEBAS AUTOMÁTICAS:")
    print("-" * 30)
    for i, ejemplo in enumerate(ejemplos, 1):
        print(f"\nPrueba {i}: '{ejemplo}'")
        resultado = automata.procesar_cadena(ejemplo)
        print(f"Resultado: {'ACEPTADA' if resultado else 'RECHAZADA'}")
        print("-" * 30)

def modo_interactivo(automata):
    """
    Modo interactivo para ingresar cadenas por consola
    """
    print("\nMODO INTERACTIVO:")
    print("Ingresa cadenas para verificar (escribe 'salir' para terminar)")
    
    while True:
        try:
            entrada = input("\nIngresa una cadena: ").strip()
            
            if entrada.lower() == 'salir':
                print("¡Hasta luego!")
                break
            
            if not entrada:
                print("Por favor ingresa una cadena válida.")
                continue
            
            resultado = automata.procesar_cadena(entrada)
            print(f"\nResultado: {'ACEPTADA' if resultado else 'RECHAZADA'}")
            
        except KeyboardInterrupt:
            print("\n\n¡Hasta luego!")
            break
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()