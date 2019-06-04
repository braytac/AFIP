#!/usr/bin/env python
# coding: utf-8

# In[71]:


from pathlib import Path
import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
 
    return None 


def create_table(conn, sql):
    """
    Crear tabla
    """
    cur = conn.cursor()
    cur.execute('DROP TABLE facturas')
    conn.commit()
    cur.execute(sql)
    conn.commit()
    cur.close()


def create_tables(conn,database):
 
    tabla_facturas = """ CREATE TABLE IF NOT EXISTS facturas (
                                        id integer PRIMARY KEY,
                                        destinatario text NOT NULL,
                                        cuit text NOT NULL,
                                        concepto text NOT NULL,
                                        monto real,
                                        desde text,
                                        hasta text
                                    ); """
 
    # create a database connection
    conn = create_connection(database)
    if conn is not None:
        # create projects table
        print("Creando tabla Facturas")
        create_table(conn, tabla_facturas)
        # create tasks table
    else:
        print("Error! cannot create the database connection.")

def eliminar_registro(conn,id):
    cur = conn.cursor()
    cur.execute("DELETE FROM facturas WHERE id=?",id)
    conn.commit()
    #cur.execute("update sqlite_sequence set seq=0 where name='facturas'")
    #cur = conn.cursor()
    #cur.execute("VACUUM")
    cur.close()
        
def limpiar_db(conn):
    cur = conn.cursor()
    cur.execute("DELETE FROM facturas")
    conn.commit()
    #cur.execute("update sqlite_sequence set seq=0 where name='facturas'")
    #cur = conn.cursor()
    #cur.execute("VACUUM")
    cur.close()

def insertar_factura(conn, datos):
    """
    Guardar nueva factura
    :param conn:
    :param datos:
    :return: facturas id
    """

    sql = ''' INSERT INTO facturas (cuit,destinatario,monto,concepto,desde,hasta)
              VALUES (?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, datos)
    conn.commit()
    cur.close()    
    return cur.lastrowid

def select_factura(conn):
    #sql = """ SELECT * FROM facturas WHERE strftime( '%m', desde )='10' """
    sql = """ SELECT nro_comprobante,destinatario,monto,desde,hasta FROM facturas ORDER BY id ASC """
    cur = conn.cursor()
    cur.execute(sql)
    r = cur.fetchall()
    cur.close()    
    return r

def guardar_factura(conn, factura_campos):
    # guardar nueva factura
    factura_id = insertar_factura(conn, factura_campos) 
    return factura_id
        

database = Path('FacturasAFIP.db')

# Si lo estoy ejecutando como programa principal
# y no es un módulo de otro programa
#if __name__ == '__main__':
#    guardar_factura()


#create_tables(conn,database)
#limpiar_db(conn)
#eliminar_registro(conn,'1')

def mostrar_facturas(conn):
    facturas = select_factura(conn)
    for factura in facturas:
        if len(factura[1]) < 25:
            tab = "\t\t\t";
        else:
            tab = ""
        print(str(factura[0])+"\t"+
              str(factura[1])+tab+"\t"+
              str(factura[2])+"\t"+
              str(factura[3])+"\t"+
              str(factura[4]))
        
#        nro_comprobante,destinatario,monto,desde,hasta
#conn = create_connection(database)
"""
factura_campos = ('30677980032',
                  'FUNDACION DE LA FACULTAD DE INGENIERIA',
                  '5000',
                  'Mantenimiento DB y carga de personal en lectores biométricos',
                  '2019-03-01',
                  '2019-03-01')
guardar_factura(conn,factura_campos)
"""
#mostrar_facturas(conn)
#conn.close()
