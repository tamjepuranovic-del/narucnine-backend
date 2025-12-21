from .models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import check_password, make_password


class AuthService:

    @staticmethod
    def login(username, password):
        print('Logging in user')
        # proverava username, ako nije u tabeli onda exception
        try:
            user = User.objects.get(username__iexact=username)
            print('Username', user)
        except User.DoesNotExist:
            print('User not found')
            raise Exception('User not found')

            # Handle legacy unhashed passwords
        if not check_password(password, user.password_hash):
                    # If direct comparison works (legacy user)
            if user.password_hash != password:
                raise Exception("Incorrect password")
            else:
                    # Upgrade legacy password to hashed
                user.password_hash = make_password(password)
                user.save()


        #if user.password_hash != password:  # direct comparison
         #   print(f"DB password: '{user.password_hash}'")
          #  print(f"Input password: '{password}'")

           # print('Password mismatch')
            #raise Exception('Incorrect password')

        return user

    @staticmethod
    def get_tokens_for_user(user):
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user_id': user.user_id,
            'username': user.username,
            'role': user.role
        }

    def register(username, password, firs_name, last_name, email):

        #gleda jel username postoji
        if User.objects.filter(username=username).exists():
            raise Exception('User with this username already exists')
        #gleda jel email postoji
        if User.objects.filter(email=email).exists():
            raise Exception('User with this email already exists')

        user = User(username=username, password_hash=make_password(password) ,firs_name=firs_name, last_name=last_name, email=email)
        user.save()
        return user



# update za acc
# update statusa narocnine da li je canceled
# za admina da vidi sve appointmente od svakog usera i lokacije i cancled narocnine, a useri samo mogu svoje
