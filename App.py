from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)

# Mysql Connectin
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'localhost'
app.config['MYSQL_PASSWORD'] = '8fol6mdz'
app.config['MYSQL_DB'] = 'flaskcontacts'
mysql = MySQL(app)

# settings
app.secret_key = 'mysecretkey'

@app.route('/')
def Index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contacs')
    data = cur.fetchall()
    return render_template('index.html', contacts= data)

@app.route('/add_contact', methods=['POST'])
def add_contact():
    if request.method =='POST':
        nombre = request.form['nombre']
        telefono = request.form['telefono']
        email = request.form['email']
        poliza = request.form['poliza']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO contacs(nombre, telefono, email, poliza) VALUES (%s, %s, %s, %s)',
        (nombre, telefono, email, poliza))
        mysql.connection.commit()
        flash("Dato agregado correctamente")

        return redirect(url_for('Index'))
    
@app.route('/edit/<id>')
def get_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contacs WHERE id = %s', (id,)) 
    data = cur.fetchall()
    #flash('Data editado correctamente')
    return render_template('edit-contact.html', contact = data[0])

@app.route('/update/<id>', methods = ['POST'])
def update_contact(id):
    if request.method == 'POST':
        nombre = request.form ['nombre']
        telefono = request.form ['telefono']
        email = request.form ['email']
        cur = mysql.connection.cursor()
        cur.execute(""" 
            UPDATE contacs
            SET nombre = %s,
                telefono = %s,
                email = %s  
            WHERE id = %s     
        """,(nombre, telefono, email, id))
    mysql.connection.commit()
    flash("Contacto editado satisfactoriamente")
   
    return redirect(url_for('Index'))

@app.route('/delete/<string:id>')
def delete_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM contacs WHERE id = %s', (id,))
    mysql.connection.commit()
    flash('Contacto removido satisfactoriamente')
    return redirect(url_for('Index'))


if __name__ == '__main__':
    app.run(port= 3000, debug=True)
