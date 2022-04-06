
from flask import Flask
from flask import render_template,request,redirect,url_for,flash
from flaskext.mysql import MySQL
from datetime import datetime
import os 
from flask import send_from_directory


app=Flask(__name__)
app.secret_key="Montesino"
mysql=MySQL()

#configuracion para la conexion
app.config['MYSQL_DATABASE_HOST']='localhost'
app.config['MYSQL_DATABASE_USER']='root'
app.config['MYSQL_DATABASE_PASSWORD']=''
app.config['MYSQL_DATABASE_DB']='sistema'
mysql.init_app(app)

CARPETA = os.path.join('uploads')
app.config['CARPETA'] = CARPETA

@app.route('/uploads/<nombreFoto>')
def uploads(nombreFoto):
    return send_from_directory(app.config['CARPETA'],nombreFoto)

@app.route('/')
def index():


    sql="SELECT * FROM `empleados`;"# (`id`, `nombre`, `apellido`, `correo`, `celular`, `foto`) VALUES (NULL, 'Adriana', 'Hernandez', 'adrianaHernandez@gmail.com', '923638794', 'fotoAmorcito.jpg');"
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql)

    empleados =cursor.fetchall()
    print(empleados)

    conn.commit()
    return render_template('empleados/index.html',empleados=empleados)


@app.route('/destroy/<int:id>')
def destroy(id):
    conn=mysql.connect()
    cursor=conn.cursor()

    cursor.execute("SELECT  foto FROM empleados WHERE id =%s",id)
    fila = cursor.fetchall()
        
    os.remove(os.path.join(app.config['CARPETA'],fila[0][0]))
       

    cursor.execute("DELETE FROM empleados WHERE id=%s",id)
    conn.commit()
    return redirect('/')#una vez ejecutes la instruccion de  borrar 'regresa a la url de donde vivo'


@app.route('/edit/<int:id>')
def edit(id):
    conn=mysql.connect()
    cursor=conn.cursor()

    cursor.execute("SELECT * FROM empleados WHERE id =%s",(id))
    empleados =cursor.fetchall()
    conn.commit()
    return render_template('empleados/edit.html',empleados=empleados)

@app.route('/update', methods=['POST'])
def update():

    _nombre=request.form['txtNombre']
    _apellido=request.form['txtApellido']
    _correo=request.form['txtCorreo']
    _celular=request.form['txtCelular']
    _foto=request.files['txtFoto']
    id=request.form['txtId']

   
    

    sql="UPDATE  empleados  SET  nombre=%s, apellido=%s, correo= %s, celular=%s WHERE id =%s; " 
    datos=(_nombre,_apellido,_correo,_celular,id)

    conn=mysql.connect()
    cursor=conn.cursor()

    now = datetime.now()
    tiempo = now.strftime("%Y%H%M%S")


    if _foto.filename !='':
        nuevoNombreFoto = tiempo + _foto.filename
        _foto.save("uploads/"+ nuevoNombreFoto)

        cursor.execute("SELECT  foto FROM empleados WHERE id =%s",id)
        fila = cursor.fetchall()
        
        os.remove(os.path.join(app.config['CARPETA'],fila[0][0]))
        cursor.execute("UPDATE empleados SET foto =%s WHERE id=%s",(nuevoNombreFoto,id))
        conn.commit()     
    

    cursor.execute(sql,datos)#ejecucion del comando sql y para el values tenemos %s que es lo que recibira de la viable datos(orden especifico)
   
    conn.commit()

    return redirect('/')#edita y se va al index


@app.route('/create')
def create():
    return render_template('empleados/create.html') 


@app.route('/store', methods=['POST'])
def storage():

    _nombre=request.form['txtNombre']
    _apellido=request.form['txtApellido']
    _correo=request.form['txtCorreo']
    _celular=request.form['txtCelular']
    _foto=request.files['txtFoto']#como se recibira una foto el .files nos ayuda para la carga de archivos

    if _nombre =='' or _apellido == '' or _correo=='' or _celular == '' or _foto.filename=='':
        flash('Recuerda llenar Todos los Datos De los Campos ')
        return redirect(url_for('create'))

    now = datetime.now()
    tiempo = now.strftime("%Y%H%M%S")

    if _foto.filename !='':
        nuevoNombreFoto = tiempo + _foto.filename
        _foto.save("uploads/"+nuevoNombreFoto)

    sql="INSERT INTO `empleados` (`id`, `nombre`, `apellido`, `correo`, `celular`, `foto`) VALUES (NULL, %s, %s, %s, %s, %s);"
    datos=(_nombre,_apellido,_correo,_celular,nuevoNombreFoto)

    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql,datos)#ejecucion del comando sql y para el values tenemos %s que es lo que recibira de la viable datos(orden especifico)
    conn.commit()
    return redirect('/')



if __name__=='__main__':
    app.run(debug=True)