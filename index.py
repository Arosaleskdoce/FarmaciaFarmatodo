from tkinter import ttk
from tkinter import *

import sqlite3

class Product:
    
    db_name = 'database.db'

    def __init__(self, window):
        self.wind = window
        self.wind.title('FARMATODO')

        # Creacion del contenedor Frame
        frame = LabelFrame(self.wind, text = 'SISTEMA DE ACTUALIZACION DE STOCK')
        frame.grid(row = 0, column = 0, columnspan= 3 , pady = 20)

        # New product Input
        Label(frame, text = 'Agregar nuevo producto: ').grid(row = 1, column = 0)
        self.aggproducto = Entry(frame)
        self.aggproducto.focus()
        self.aggproducto.grid(row = 1, column = 1)

        # Precio Input
        Label(frame, text = 'Precio: ').grid(row = 2, column = 0)
        self.precio = Entry(frame)
        self.precio.grid(row = 2, column = 1)

        # Boton para guardar e añadir a la bd
        ttk.Button(frame, text = 'GUARDAR', command=self.add_product).grid(row = 3, columnspan = 2, sticky = W + E)
        
        #Mensaje pos accion
        self.mensaje = Label(text='', fg = 'red')
        self.mensaje.grid(row=3, column = 0, columnspan = 2, sticky = W + E)

        # Tabla en la vista para dividir producto de precios
        self.tree = ttk.Treeview(height= 10, columns = 2)
        self.tree.grid(row = 4, column = 0, columnspan = 2)
        self.tree.heading('#0' , text = 'PRODUCTO', anchor=CENTER)
        self.tree.heading('#1' , text = 'PRECIO', anchor=CENTER)

        #Botones parte inferior de la tabla
        ttk.Button(text = 'BORRAR', command = self.delete_product).grid(row = 5, column = 0, sticky= W + E)
        ttk.Button(text = 'EDITAR', command= self.edit_product).grid(row = 5, column = 1, sticky= W + E)

        self.get_products()

    def run_query(self, query, parameters = ()):
      with sqlite3.connect(self.db_name) as conn:
          cursor = conn.cursor()
          result = cursor.execute(query, parameters)
          conn.commit()
          return result

    def get_products(self):
        #Limpiar datos
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)
        #query datos
        query = 'SELECT *FROM product ORDER BY name DESC'
        db_rows = self.run_query(query)
        for row in db_rows:
            self.tree.insert('', 0, text = row[1], values= row[2])

        #Condicion para validar campos input
    def validation(self):
        return len(self.aggproducto.get()) != 0 and len(self.precio.get()) !=0

    def add_product(self):
        if self.validation():
            query = 'INSERT INTO product Values(NULL, ?, ?)'
            parameters = (self.aggproducto.get(), self.precio.get())
            self.run_query(query, parameters)
            self.mensaje['text'] = 'El producto {} fue agregado al stock satisfactoriamente'.format(self.aggproducto.get())
            self.aggproducto.delete(0, END)
            self.precio.delete(0, END)
        else:
            self.mensaje['text'] = 'PRODUCTO Y PRECIO, OBLIGATORIOS PARA REGISTRAR STOCK'
        self.get_products()

    def delete_product(self):
        self.mensaje['text'] = ''
        try:
            self.tree.item(self.tree.selection())['text'][0]
        except IndexError as e:
            self.mensaje['text'] = '¡CAMPEON! RECUERDA SELECCIONAR PARA BORRAR REGISTROS'
            return
        self.mensaje['text'] = ''
        aggproducto = self.tree.item(self.tree.selection())['text']
        query = 'DELETE FROM product WHERE name = ?'
        self.run_query(query, (aggproducto, ))
        self.mensaje['text'] = 'Registro de producto {} borrado'.format(aggproducto)
        self.get_products()

        #Condicion para editar 
    def edit_product(self):
        self.mensaje['text'] = ''
        try:
            self.tree.item(self.tree.selection())['text'][0]
        except IndexError as e:
            self.mensaje['text'] = '¡CAMPEON! RECUERDA SELECCIONAR PARA BORRAR REGISTROS'
            return
        aggproducto = self.tree.item(self.tree.selection())['text']
        antiguo_precio = self.tree.item(self.tree.selection())['values'][0]
        self.edit_wind = Toplevel()
        self.edit_wind.title = 'Edicion Producto'

        #antiguo producto
        Label(self.edit_wind, text = 'Producto anterior').grid(row = 0, column = 1)
        Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value = aggproducto), state = 'readonly').grid(row = 0, column = 2)    

        #nuevo producto
        Label(self.edit_wind, text = 'Nuevo Producto').grid(row = 1, column = 1)
        nuevo_aggproducto = Entry(self.edit_wind) 
        nuevo_aggproducto.grid(row = 1, column = 2) 
    

        #antiguo precio
        Label(self.edit_wind, text = 'Precio Anterior').grid(row = 2, column = 1)
        Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value = antiguo_precio), state = 'readonly').grid(row = 2, column = 2)    

        #nuevo precio
        Label(self.edit_wind, text = 'Nuevo Precio').grid(row = 3, column = 1)
        nuevo_precio = Entry(self.edit_wind) 
        nuevo_precio.grid(row = 3, column = 2) 

        #Boton para guardar lo actualizado

        Button(self.edit_wind, text = 'ACTUALIZAR', command = lambda: self.edit_records(nuevo_aggproducto.get(), aggproducto, nuevo_precio.get(), antiguo_precio)).grid(row = 4, column=2, sticky= W)
       
        #Condicion para actualizar con su consulta y query
    def edit_records(self, nuevo_aggproducto, aggproducto, nuevo_precio, antiguo_precio):
        query = 'UPDATE product Set name = ?, price = ? WHERE name = ? AND price = ?'
        parameters = (nuevo_aggproducto , nuevo_precio, aggproducto, antiguo_precio)
        self.run_query(query, parameters)
        self.edit_wind.destroy()
        self.mensaje['text'] = 'REGISTRO {} ACTUALIZADO EXITOSAMENTE'.format(aggproducto)
        self.get_products()


if __name__ == '__main__':
    window = Tk()
    application = Product(window)
    window.mainloop()
