import csv
import os

def escapar_comillas_simples(cadena):
    return cadena.replace("'", "\\'")

def leer_csv(nombre_archivo, nombre_txt):
    ruta_archivo = os.path.join(os.getcwd(), nombre_archivo)

    with open(ruta_archivo, mode='r', encoding='utf-8-sig') as file, open(nombre_txt, mode='w', encoding='utf-8') as txt_file:
        reader = csv.DictReader(file, delimiter=';')
        
        filas = list(reader)

        txt_file.write('db.NGODs.insertMany([\n')
        
        for i, fila in enumerate(filas):
            if fila['short_name']:
                nombre_completo = f"{fila['name']} ({fila['short_name']})"
            else:
                nombre_completo = fila['name']
            
            fila_texto = '  {\n'
            fila_texto += f"    'name': '{escapar_comillas_simples(nombre_completo)}',\n"
            fila_texto += "    'address': {\n"
            fila_texto += f"      'streetAddress': '{escapar_comillas_simples(fila['streetAddress'])}',\n"
            fila_texto += f"      'department': '{escapar_comillas_simples(fila['department'])}',\n"
            fila_texto += f"      'province': '{escapar_comillas_simples(fila['province'])}',\n"
            fila_texto += f"      'district': '{escapar_comillas_simples(fila['district'])}'\n"
            fila_texto += "    },\n"
            fila_texto += f"    'description': '{escapar_comillas_simples(fila['area'])}',\n"
            fila_texto += "    'status': 'active'\n"
            fila_texto += '  }'
            
            if i < len(filas) - 1:
                fila_texto += ','
                
            txt_file.write(fila_texto + '\n')
        
        txt_file.write(']);\n')

nombre_archivo = "BD-ONGD.csv"
nombre_txt = "insertMQL.txt"

leer_csv(nombre_archivo, nombre_txt)
