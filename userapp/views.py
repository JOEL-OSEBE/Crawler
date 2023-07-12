from .serializer import RegisterSerializer, UserSerializer, MyLoginPairSerializer
from .serializer import ChangePasswordSerializer, UserUpdateSerializer
from .serializer import UserDeactivateSerializer, UserActivateSerializer 
from .serializer import RegisterAdminSerializer, RegisterSuperAdminSerializer
from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import viewsets, generics, status
from rest_framework.response import Response
from .jsonrenderers import UserJSONRenderer
from .serializer import CrawlerSerializer
from django.http.request import QueryDict
from rest_framework.views import APIView
from .crawlscript import Crawler
from django.utils import timezone
from .models import User
import jwt




# Health checks


class HealthcheckViewset(viewsets.ViewSet):
    permission_classes = (AllowAny,)

    def checker(self, request):
        if request.method == 'GET':
            return Response({"status": 200})
            

# ===
#Register user

class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class RegisterView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

    def post(self, request, *args,  **kwargs):
        if request.method == "POST":
            errormsg = []

            for i in request.data.keys():
                if request.data.get(i) == '':
                    print(request.data.get(i))
                    msg = f" field {i} is empty"
                    errormsg.append(msg)

            username_unique = User.objects.filter(
                username=request.data.get("username")).values("username")
            username_unique = [
                i for i in username_unique if i['username'] == request.data.get("username")
                ]

            email_unique = User.objects.filter(
                email=request.data.get("email")).values("email")
            email_unique = [i for i in email_unique if i['email']
                            == request.data.get("email")]
            
            if len(username_unique) > 0:
                message_ = "username already exists"
                errormsg.append(message_)
            elif len(email_unique) > 0:
                message_ = "email already exists"
                errormsg.append(message_)

            serializer = self.get_serializer(data=request.data)

            try:
                serializer.is_valid(raise_exception=True)
                user = serializer.save()

                response = {
                    "status": "success",
                    "user": UserSerializer(
                        user,
                        context=self.get_serializer_context()
                    ).data,
                    "message": "user created successfully.",
                }
            except:
                response = {
                    "status": "failed",
                    "reason": errormsg

                }
                pass
            

            return Response(response, status=status.HTTP_200_OK)


class RegisterAdminView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = RegisterAdminSerializer

    def post(self, request, *args,  **kwargs):
        if request.method == "POST":
            errormsg = []

            for i in request.data.keys():
                if request.data.get(i) == '':
                    print(request.data.get(i))
                    msg = f" field {i} is empty"
                    errormsg.append(msg)

            username_unique = User.objects.filter(
                username=request.data.get("username")).values("username")
            username_unique = [
                i for i in username_unique if i['username'] == request.data.get("username")]

            email_unique = User.objects.filter(
                email=request.data.get("email")).values("email")
            email_unique = [i for i in email_unique if i['email']
                            == request.data.get("email")]
            if len(username_unique) > 0:
                message_ = "username already exists"
                errormsg.append(message_)
            elif len(email_unique) > 0:
                message_ = "email already exists"
                errormsg.append(message_)

            serializer = self.get_serializer(data=request.data)

            try:
                serializer.is_valid(raise_exception=True)
                user = serializer.save()

                response = {
                    "status": "success",
                    "user": UserSerializer(
                        user,
                        context=self.get_serializer_context()
                    ).data,
                    "message": "user created successfully.",
                }
            except:
                response = {
                    "status": "failed",
                    "reason": errormsg

                }
                pass

            return Response(response, status=status.HTTP_200_OK)


class RegisterSuperAdminView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = RegisterSuperAdminSerializer

    def post(self, request, *args,  **kwargs):
        if request.method == "POST":
            errormsg = []

            for i in request.data.keys():
                if request.data.get(i) == '':
                    print(request.data.get(i))
                    msg = f" field {i} is empty"
                    errormsg.append(msg)

            username_unique = User.objects.filter(
                username=request.data.get("username")).values("username")
            username_unique = [
                i for i in username_unique if i['username'] == request.data.get("username")]

            email_unique = User.objects.filter(
                email=request.data.get("email")).values("email")
            email_unique = [i for i in email_unique if i['email']
                            == request.data.get("email")]
            if len(username_unique) > 0:
                message_ = "username already exists"
                errormsg.append(message_)
            elif len(email_unique) > 0:
                message_ = "email already exists"
                errormsg.append(message_)

            serializer = self.get_serializer(data=request.data)

            try:
                serializer.is_valid(raise_exception=True)
                user = serializer.save()

                response = {
                    "status": "success",
                    "user": UserSerializer(
                        user,
                        context=self.get_serializer_context()
                    ).data,
                    "message": "user created successfully.",
                }
            except:
                response = {
                    "status": "failed",
                    "reason": errormsg

                }
                pass

            return Response(response, status=status.HTTP_200_OK)

# Login user
class LoginView(APIView):
    model = User
    permission_classes = (AllowAny,)
    # renderer_classes = (UserJSONRenderer,)
    serializer_class = MyLoginPairSerializer

    def post(self, request):
        user = request.data

        try:
            serializer = self.serializer_class(data=user)
            if serializer.is_valid():
                user_model = self.model.objects.get(username=user['username'])
                user_model.last_login = timezone.now()
                user_model.login_status = "logged_in"
                user_model.login_frequency = float(
                    user_model.login_frequency) + 1
                user_model.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
                # print(";;;;;;;",serializer)
            else:

                return Response({
                    "status": "failed",
                    "reason": "Invalid username or password"
                }, status=status.HTTP_200_OK)
        except:
            pass

# Logout user
class LogoutView(APIView):
    model = User
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        user_model = self.model.objects.get(pk=request.user.id)
        user_model.last_logout = timezone.now()
        user_model.login_status = "logged_out"
        user_model.save()

        request.META['HTTP_AUTHORIZATION'] = ""
        return Response({
            "status": "Logout successfull",
            "token": ""
        }, status=status.HTTP_200_OK)

# PROFILES
class ProfileUpdateView(generics.UpdateAPIView):

    """
    Update user profile
    """
    model = User
    permission_classes = (IsAuthenticated,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UserUpdateSerializer

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        errormsg = []

        for i in request.data.keys():
            if request.data.get(i) == '':
                print(request.data.get(i))
                msg = f"field {i} is empty"
                errormsg.append(msg)

        self.object = self.get_object()
        if len(errormsg) == 0:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                serialdata = serializer.data
                self.object.first_name = serializer['first_name'].value
                self.object.last_name = serializer['last_name'].value
                self.object.username = serialdata['username']
                self.object.email = serialdata['email']
                self.object.date_of_birth = serialdata['date_of_birth']
                self.object.updated_at = timezone.now()
                self.object.save()

                response = {
                    'status': 'success',
                    'message': 'Updated successfully',
                }

        else:
            response = {
                "status": "failed",
                "reason": errormsg
            }

        return Response(response, status=status.HTTP_200_OK)

class PasswordResetView(generics.UpdateAPIView):

    """
    Change password
    """
    serializer_class = ChangePasswordSerializer
    model = User

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        errormsg = []

        for i in request.data.keys():
            if request.data.get(i) == '':
                print(request.data.get(i))
                msg = f"field {i} is empty"
                errormsg.append(msg)

        if len(errormsg) == 0:
            self.object = self.get_object()
            serializer = self.get_serializer(data=request.data)

            if serializer.is_valid():
                # Check old password

                if serializer.data.get("confirm_new_password") != serializer.data.get("new_password"):
                    return Response({"status": "-new password- and -confirm new password- do not match"})
                if serializer.data.get("new_password") == serializer.data.get("old_password"):
                    return Response({"status": "-new password- and -old password- should not match"})

                if not self.object.check_password(serializer.data.get("old_password")):
                    return Response({"status": "invalid old password"}, status=status.HTTP_200_OK)

                # set_password also hashes the password that the user will get
                self.object.set_password(
                    serializer.data.get("confirm_new_password"))
                
                self.object.save()
                response = {
                    'status': 'success',
                    'message': 'Password updated successfully',
                }

        else:
            response = {
                'status': 'failed',
                'reason': errormsg,
            }

        return Response(response, status=status.HTTP_200_OK)

class ProfileDeactivateView(generics.UpdateAPIView):

    """
    Deactivate account
    """
    model = User
    permission_classes = (IsAuthenticated,)
    serializer_class = UserDeactivateSerializer

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        tokens_ = jwt.decode(request.META['HTTP_AUTHORIZATION'].replace(
            "Token ", ""), options={"verify_signature": False})

        rdata = {
            "username": tokens_['username'],
            "email": tokens_['personal_email'],
            "is_active": False
        }
        to_querydict = QueryDict('', mutable=True)
        to_querydict.update(rdata)

        errormsg = []

        for i in to_querydict.keys():
            if to_querydict.get(i) == '':
                print(to_querydict.get(i))
                msg = f"field {i} is empty"
                errormsg.append(msg)

        self.object = self.get_object()

        if len(errormsg) == 0:
            serializer = self.get_serializer(data=to_querydict)

            if serializer.is_valid():
                serialdata = serializer.data

                self.object.username = serialdata['username']
                self.object.email = serialdata['email']
                self.object.deactivate_at = timezone.now()
                self.object.is_active = serialdata['is_active']

                self.object.save()

                response = {
                    'status': 'success',
                    'message': 'Deactivated successfully',
                }

        else:
            response = {
                "status": "failed",
                "reason": errormsg
            }

        return Response(response, status=status.HTTP_200_OK)

class ProfileActivateView(generics.UpdateAPIView):

    """
    Reactivate account
    """
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UserActivateSerializer

    def update(self, request):
        data = request.data

        serializer = self.serializer_class(data=data)
        datavalue = {}
        if serializer.is_valid():
            serializer_ = serializer.data
            email = serializer_['email']
            uservalue = User.objects.filter(email=email).values()

            for i in uservalue:

                keys = i.keys()
                for j in keys:
                    datavalue[j] = i[j]

            randompassword = User.objects.make_random_password()
            usermodel = User.objects.get(pk=datavalue['id'])
            usermodel.is_active = True
            usermodel.activate_at = timezone.now()
            usermodel.set_password(randompassword)
            usermodel.save()

            return Response({
                "status": "success",
                'message': 'Activation successfull',
                "password": randompassword
            }, status=status.HTTP_200_OK)


class GetAllUsersView(APIView):
    model = User
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        all_users = self.model.objects.values(
            'username', 'email', 'first_name', 
            'last_name', 'is_admin'
            )
        
        return Response({
            "status": "success",
            "users": all_users
        }, status=status.HTTP_200_OK)


class AssignRightsView(APIView):
    model = User
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        data = request.data

        #if user changing information is superadmin
        access_right = self.model.objects.filter(
            username=request.user).values('is_admin', 'is_superadmin')[0]
        try:
            if access_right['is_admin'] == True and access_right['is_superadmin'] == True:
                try:
                    self.model.objects.filter(username=data.get('username')).update(
                        is_admin=data.get('is_admin').capitalize()
                    )
                except Exception as error:
                    return Response({
                        "status": "failed",
                        "message": "please add is_admin as True or False"
                    }, status=status.HTTP_200_OK)
                updatedright = self.model.objects.filter(username=data.get('username')).values(
                    'username', 'email', 'first_name', 'last_name', 'is_admin')

                return Response({
                    "status": "success",
                    "message": updatedright
                }, status=status.HTTP_200_OK)
            elif access_right['is_admin'] == True and access_right['is_superadmin'] == False:
                try:
                    self.model.objects.filter(username=data.get('username')).update(
                        is_staff=data.get('is_staff').capitalize(),
                        is_admin=False
                    )
                except Exception as error:
                    return Response({
                        "status": "failed",
                        "message": "please add is_staff True or False"
                    }, status=status.HTTP_200_OK)
                updatedright = self.model.objects.filter(username=data.get('username')).values(
                    'username', 'email', 'first_name', 'last_name', 'is_staff')

                return Response({
                    "status": "success",
                    "message": updatedright
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    "status": "failed",
                    "message": "no admin rights"
                }, status=status.HTTP_200_OK)
        except Exception as error:
            return Response({
                            "status": "failed",
                            "message": error
                            }, status=status.HTTP_200_OK)


# Create your crawler views here.
class CrawlViewset(viewsets.ViewSet):
    model = User
    permission_classes = (AllowAny,)

    # crawl by link
    def crawlrequest(self, request):
        if request.method == "POST":

            urls = request.data["url"]
            try:
                crawler = Crawler()
                
                documents = []
                for a_link in urls:
                    
                    all_info = crawler.link_info(a_link)
                    documents.append(all_info)

                respond = {
                            "status":"success",
                            "message":"done crawling",
                            "documents":documents
                            }

            except Exception as error:
                respond = {
                            "status": "failed", 
                            "message": str(error),
                            }
                          
            return Response(respond, status=status.HTTP_200_OK)

    # crawl by keyword
    def searchrequest(self, request):
        if request.method == "POST":
            query = request.data["search"]

            crawler = Crawler()
            google_link = crawler.search(query)

            try:
                documents = []
                for a_link in google_link:

                    all_info = crawler.link_info(a_link)
                    if all_info != None:
                        documents.append(all_info)

                respond = {
                        "status":"success",
                        "message":"done crawling",
                        "documents":documents
                        }

            except Exception as error:

                respond = {
                            "status": "failed", 
                            "message": str(error),
                            }

            return Response(respond, status=status.HTTP_200_OK)
