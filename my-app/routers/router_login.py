
from app import app
from flask import render_template, request, flash, redirect, url_for, session

# Importando mi conexión a BD
from conexion.conexionBD import connectionBD

# Para encriptar contraseña generate_password_hash
from werkzeug.security import check_password_hash

# Importando controllers para el modulo de login
from controllers.funciones_login import *
PATH_URL_LOGIN = "public/login"


@app.route('/', methods=['GET'])
def inicio():
    if 'conectado' in session:
        return render_template('public/base_cpanel.html', dataLogin=dataLoginSesion())
    else:
        return render_template(f'{PATH_URL_LOGIN}/base_login.html')


@app.route('/mi-perfil', methods=['GET'])
def perfil():
    if 'conectado' in session:
        return render_template(f'public/perfil/perfil.html', info_perfil_session=info_perfil_session())
    else:
        return redirect(url_for('inicio'))


# Crear cuenta de usuario
@app.route('/register-user', methods=['GET'])
def cpanelRegisterUser():
    if 'conectado' in session:
        return redirect(url_for('inicio'))
    else:
        return render_template(f'{PATH_URL_LOGIN}/auth_register.html')


# Recuperar cuenta de usuario
@app.route('/recovery-password', methods=['GET'])
def cpanelRecoveryPassUser():
    if 'conectado' in session:
        return redirect(url_for('inicio'))
    else:
        return render_template(f'{PATH_URL_LOGIN}/auth_forgot_password.html')


# Crear cuenta de usuario
@app.route('/saved-register', methods=['POST'])
def cpanelResgisterUserBD():
    if request.method == 'POST' and 'name_surname' in request.form and 'pass_user' in request.form:
        name_surname = request.form['name_surname']
        email_user = request.form['email_user']
        pass_user = request.form['pass_user']

        result_data = recibeInsertRegisterUser(
            name_surname, email_user, pass_user)
        if (result_data != 0):
            flash('la cuenta fue creada correctamente.', 'success')
            return redirect(url_for('inicio'))
        else:
            return redirect(url_for('inicio'))
    else:
        flash('el método HTTP es incorrecto', 'error')
        return redirect(url_for('inicio'))


# Actualizar datos de mi perfil
@app.route("/actualizar-datos-perfil", methods=['POST'])
def actualizarPerfil():
    if request.method == 'POST':
        if 'conectado' in session:
            respuesta = procesar_update_perfil(request.form)
            if respuesta == 1:
                flash('Los datos fuerón actualizados correctamente.', 'success')
                return redirect(url_for('inicio'))
            elif respuesta == 0:
                flash(
                    'La contraseña actual esta incorrecta, por favor verifique.', 'error')
                return redirect(url_for('perfil'))
            elif respuesta == 2:
                flash('Ambas claves deben se igual, por favor verifique.', 'error')
                return redirect(url_for('perfil'))
            elif respuesta == 3:
                flash('La Clave actual es obligatoria.', 'error')
                return redirect(url_for('perfil'))
        else:
            flash('primero debes iniciar sesión.', 'error')
            return redirect(url_for('inicio'))
    else:
        flash('primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))

# Validar sesión
@app.route('/login', methods=['GET', 'POST'])
def loginCliente():
    if 'conectado' in session:
        return redirect(url_for('inicio'))
    else:
        if request.method == 'POST' and 'email_user' in request.form and 'pass_user' in request.form:
            email_user = str(request.form['email_user'])
            pass_user = str(request.form['pass_user'])

            # Comprobando si existe una cuenta
            conexion_mysqldb = connectionBD()

            if conexion_mysqldb is None:
                # Manejar el caso de error de conexión
                flash('Error al conectar con la base de datos. Inténtelo de nuevo más tarde.', 'error')
                return render_template(f'{PATH_URL_LOGIN}/base_login.html')

            try:
                cursor = conexion_mysqldb.cursor(dictionary=True)
                cursor.execute("SELECT * FROM users WHERE email_user = %s", [email_user])
                account = cursor.fetchone()

                if account:
                    if check_password_hash(account['pass_user'], pass_user):
                        # Crear datos de sesión, para poder acceder a estos datos en otras rutas
                        session['conectado'] = True
                        session['id'] = account['id']
                        session['name_surname'] = account['name_surname']
                        session['email_user'] = account['email_user']

                        flash('La sesión fue correcta.', 'success')
                        return redirect(url_for('inicio'))
                    else:
                        # La cuenta no existe o el nombre de usuario/contraseña es incorrecto
                        flash('Datos incorrectos, por favor revise.', 'error')
                        return render_template(f'{PATH_URL_LOGIN}/base_login.html')
                else:
                    flash('El usuario no existe, por favor verifique.', 'error')
                    return render_template(f'{PATH_URL_LOGIN}/base_login.html')
            except Exception as e:
                # Capturar cualquier error inesperado al interactuar con la base de datos
                print(f"Error en loginCliente: {e}")
                flash('Se produjo un error al procesar la solicitud. Inténtelo de nuevo.', 'error')
                return render_template(f'{PATH_URL_LOGIN}/base_login.html')
            finally:
                # Asegurarse de cerrar la conexión si fue abierta correctamente
                if conexion_mysqldb.is_connected():
                    conexion_mysqldb.close()
        else:
            flash('Primero debes iniciar sesión.', 'error')
            return render_template(f'{PATH_URL_LOGIN}/base_login.html')



@app.route('/closed-session',  methods=['GET'])
def cerraSesion():
    if request.method == 'GET':
        if 'conectado' in session:
            # Eliminar datos de sesión, esto cerrará la sesión del usuario
            session.pop('conectado', None)
            session.pop('id', None)
            session.pop('name_surname', None)
            session.pop('email', None)
            flash('tu sesión fue cerrada correctamente.', 'success')
            return redirect(url_for('inicio'))
        else:
            flash('recuerde debe iniciar sesión.', 'error')
            return render_template(f'{PATH_URL_LOGIN}/base_login.html')
