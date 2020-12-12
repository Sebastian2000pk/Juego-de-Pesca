from tkinter import * 
import os

def Acceso_aceptado():
	#Aqui va la pantalla del juego de pygame
    pantalla.destroy()
    

def contrasenya_no_reconocida():
	global pantalla4
	pantalla4 = Toplevel(pantalla)
	pantalla4.title('Error')
	pantalla4.geometry('300x250')

	global emergente
	emergente = PhotoImage(file = "images/quien.png")
	mi_frame = Frame(pantalla4)
	mi_frame.pack()
	Label(mi_frame, image = emergente).pack()	

	Label(pantalla4, text = '¿Y tu constraseña?\n—> Error en la constraseña <—').pack()
	Button(pantalla4, text = 'OK', command = pantalla4.destroy).pack()

def usuario_no_existente():
	global pantalla5
	pantalla5 = Toplevel(pantalla)
	pantalla5.title('Error')
	pantalla5.geometry('300x250')

	global emergente
	emergente = PhotoImage(file = "images/eresnuevo.png")
	mi_frame = Frame(pantalla5)
	mi_frame.pack()
	Label(mi_frame, image = emergente).pack()	

	Label(pantalla5, text = '¿Eres nuevo?\n—> Usuario no encontrado <—').pack()
	Button(pantalla5, text = 'OK', command = pantalla5.destroy).pack()

def usuario_existente():
	global pantalla6
	pantalla6 = Toplevel(pantalla)
	pantalla6.title('Error')
	pantalla6.geometry('300x250')

	global emergente
	emergente = PhotoImage(file = "images/yoteconozco.png")
	mi_frame = Frame(pantalla6)
	mi_frame.pack()
	Label(mi_frame, image = emergente).pack()	

	Label(pantalla6, text = 'Yo te conozco\n—> Este usuario ya existe <—').pack()
	Button(pantalla6, text = 'OK', command = pantalla6.destroy).pack()	

def registrar_usuario():
	nombre_usuario_info = nombre_usuario.get()
	contrasenya_info = contrasenya.get()

	file = open("respaldo.txt", 'a')
	if nombre_usuario_info not in usuarios.keys() and contrasenya_info != ' ' and nombre_usuario_info != ' nombre_usuario_info' :
		usuarios[nombre_usuario_info] = contrasenya_info
		file.write(nombre_usuario_info+':'+contrasenya_info+':'+'0')
		file.write('\n')
		file.close()
		Label(pantalla1, text = 'Bienvenido a la familia\n—> Registrado exitosamente <—', fg = 'green', font = ('calibri', 11)).pack()
	else:
		usuario_existente()

	nombre_usuario_llave.delete(0, END)
	contrasenya_llave.delete(0, END)

def registro():
	global pantalla1

	pantalla1 = Toplevel(pantalla)
	pantalla1.title('Registro')
	pantalla1.geometry('300x250')

	global nombre_usuario
	global contrasenya
	global nombre_usuario_llave
	global contrasenya_llave

	nombre_usuario = StringVar()
	contrasenya = StringVar()

	Label(pantalla1, text = 'Por favor ingresa los datos').pack()
	Label(pantalla1, text = '').pack()
	Label(pantalla1, text = 'Nombre de usuario * ').pack()

	nombre_usuario_llave = Entry(pantalla1, textvariable = nombre_usuario)
	nombre_usuario_llave.pack()
	Label(pantalla1, text = 'Contraseña * ').pack()
	contrasenya_llave = Entry(pantalla1, textvariable = contrasenya)
	contrasenya_llave.pack()
	Label(pantalla1, text = '').pack()
	Button(pantalla1, text = 'Registrarse', width = 10, height =1, command = registrar_usuario).pack()

def verificar_ingreso():
	global nombre_usuario1
	nombre_usuario1 = nombre_usuario_llave.get()
	contrasenya1 = contrasenya_llave.get()
	nombre_usuario_entrada1.delete(0, END)
	contrasenya_entrada1.delete(0, END)

	actualizar()
	
	if nombre_usuario1 in usuarios:
		file1 = open("respaldo.txt", 'r')
		#print(contrasenya1)
		#print(usuarios[nombre_usuario1])
		if contrasenya1 == usuarios[nombre_usuario1]:
			Acceso_aceptado()
		else:
			contrasenya_no_reconocida()
	else:
		usuario_no_existente()

#In case of some errors you can try this: login_verify v.2

#def login_verify():
#    username1 = username_verify.get()
#    password1 = password_verify.get()
#
#    username_entry1.delete(0, END)
#    password_entry1.delete(0, END)
#
#    list_of_files = os.listdir() 
#    if username1 in list_of_files:
#        file1 = open(username1, "r")
#        verify = file1.read().splitlines() 
#        verify1 = verify[1] #NEW
#        if password1 == verify1: #NEW
#            login_sucess()
#        else:
#            password_not_recognised()
#    else:
#        user_not_found()

#------------------------------------------------------------------

def Ingreso():

	global pantalla2
	pantalla2 = Toplevel(pantalla)
	pantalla2.title('Ingreso')
	pantalla2.geometry('300x250')
	Label(pantalla2, text = 'Por favor ingresa los datos para ingresar').pack()
	Label(pantalla2, text = '').pack()
	
	global nombre_usuario_llave
	global contrasenya_llave 

	nombre_usuario_llave = StringVar()
	contrasenya_llave = StringVar()

	global nombre_usuario_entrada1
	global contrasenya_entrada1 

	Label(pantalla2, text = 'Nombre de usuario * ').pack()
	nombre_usuario_entrada1 = Entry(pantalla2, textvariable = nombre_usuario_llave)
	nombre_usuario_entrada1.pack()
	Label(pantalla2, text = '').pack()
	Label(pantalla2, text = 'Contraseña * ').pack()
	contrasenya_entrada1 = Entry(pantalla2, textvariable = contrasenya_llave, show = '*')
	contrasenya_entrada1.pack()
	Label(pantalla2, text = '').pack()
	Button(pantalla2, text = 'Ingresar', width = 10, height = 1, command = verificar_ingreso).pack()

def actualizar():

	global lineas_separadas

	file = open("respaldo.txt", 'r')
	lineas_separadas = file.readlines()
	file.close()
	#print(lineas_separadas)

	for linea in lineas_separadas:
		linea = linea.replace('\n', '')
		linea = linea.split(':')			
		usuarios[linea[0]] = linea[1]
		#print(linea)

def pantalla_principal():
	global pantalla
	global usuarios

	usuarios = {}
	actualizar()
	pantalla = Tk()
	pantalla.geometry('700x480')
	pantalla.title('Club de pesca')
	Label(text = 'Club de pesca', bg = 'grey', width = '300', height = '2', font = ('Calibri', 13)). pack()
	Label(text = '').pack()
	icono = PhotoImage(file = "images/iconologin.png")
	Label(image = icono).pack()
	Button(text = 'Ingresar', height = '2', width = '30', command = Ingreso).pack()
	Button(text = 'Registrarse', height = '2', width = '30', command = registro).pack()

	pantalla.mainloop()

	return nombre_usuario1