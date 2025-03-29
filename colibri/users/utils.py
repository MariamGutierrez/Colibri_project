from django.contrib.auth import get_user_model

User = get_user_model() 

class UserDAO: 
    """ Data Access Object para la gestión de usuarios """

    @staticmethod 
    def get_user_by_id(user_id):
        """ Obtiene un usuario por su ID """
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None

    @staticmethod
    def get_user_by_username(username):
        """ Obtiene un usuario por su nombre de usuario """
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            return None

    @staticmethod
    def create_user(username, email, password):
        """ Crea un nuevo usuario """
        user = User.objects.create_user(username=username, email=email, password=password)
        return user

    @staticmethod
    def delete_user(user_id):
        """ Elimina un usuario por su ID """
        user = UserDAO.get_user_by_id(user_id)
        if user:
            user.delete()
            return True
        return False
