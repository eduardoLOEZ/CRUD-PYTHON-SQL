from decouple import config
import os 
import pymysql


#-----------------------SQL QUERYS PARA TABLAS---------------
DROP_TABLE = "DROP TABLE IF EXISTS users"
USERS_TABLE = """CREATE TABLE users(
    id INT UNIQUE AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(50) NOT NULL,
    email VARCHAR(50) NOT NULL,
    edad INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)"""

#-------------------decoradores-----------------
def system_clear(func):
    def wrapper(cursor):

        os.system("cls")

        func(cursor)

        input("")
    wrapper.__doc__ = func.__doc__
    return wrapper




@system_clear
def create_user(cursor):
    """A) crear un usuario"""
    
    username =input("coloca el nombre: ")
    password = input("coloca la contraseña: ")
    email= input("coloca el email: ")
    edad = input("coloca la edad: ")

    query = "INSERT INTO users(username, password, email, edad) VALUES(%s, %s, %s, %s)"
    values = (username, password, email, edad)

    cursor.execute(query, values)
    print("usuario creado exitosamente!")
    

@system_clear
def list_users(cursor):
    """B) listar usuarios"""
    query = "SELECT * FROM users"
    cursor.execute(query)
    result = cursor.fetchall()

    for row in result:
        print(row)


##-----------------------decoradores--------------------------
def user_exists(func):

    def wrapper(cursor):
        id = input("ingresa el id del usuario: ")

        query = "SELECT id FROM users WHERE id= %s"
        cursor.execute(query, (id))

        user=  cursor.fetchone()
        if user:
            func(id, cursor)
        else:
            print("no se encontro el usuario con ese id ")
    wrapper.__doc__ = func.__doc__ #que se muestren las opciones
    return wrapper




@system_clear
@user_exists
def update_user(id,cursor):
    """C) actualizar un usuario"""
    
    new_username= input("ingresa el nuevo nombre: ")
    query = "UPDATE users SET username= %s WHERE id= %s"
    cursor.execute(query,(new_username, id))
    print("usuario actualizado!")


@system_clear
@user_exists
def delete_user(id,cursor):
    """D) eliminar un usuario"""
    query = "DELETE FROM users WHERE id = %s"
    cursor.execute(query, (id,))
    if cursor.rowcount > 0:
        print("Usuario eliminado exitosamente.")
        cursor.execute("ALTER TABLE users AUTO_INCREMENT =1")
    else:
        print("No se encontró ningún usuario con el ID proporcionado.")



    

#----------------------except de las opciones del menu-------------------------
def default():
    print("opcion no valida")

#-----------------------FUNCION PRINCIPAL----------------------
def main():
    options ={
        "a": create_user,
        "b": list_users,
        "c": update_user,
        "d": delete_user
    }

    try:
        connect = pymysql.Connect(host="127.0.0.1",
                              port= 3306,
                              user= config("USER_MYSQL"), 
                              passwd= config("PASSWORD_MYSQL"), 
                              db= config("DB_NAME2"))
        print("conectado a la db")

        with connect.cursor() as cursor:
            #al crear la tabla, comentamos estos dos
            #cursor.execute(DROP_TABLE)
            #cursor.execute(USERS_TABLE)

            while True:
                for function in options.values():
                    print(function.__doc__)#muestre las opciones del menu

                print("quit/q para salir")

                option = input("seleccione una opcion:").lower()

                if option == "quit" or option== "q":
                    break

                function = options.get(option, default)
                function(cursor)
                connect.commit() #persistir los datos de la DB






    except pymysql.Error as err:
        print("error")
        print(err)





if __name__ == "__main__":
    main()

    
