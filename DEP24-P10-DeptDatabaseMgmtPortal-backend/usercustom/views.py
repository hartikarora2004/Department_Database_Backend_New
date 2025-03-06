from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from .serializers import UserSerializer,LoginSerializer,OTPSerializer
from .models import CustomUser 
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from rest_framework import status
from otplogin.models import Otpdetails
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.models import Group
from django.http import HttpResponse
import csv
from department.models import Department
from student_details.models import studentDetails
from faculty_details.models import facultyDetails
from staff_details.models import staffDetails
from batch.models import Batch
from django.db import transaction
from .services import create_student,create_faculty,create_staff
from rest_framework.authentication import TokenAuthentication
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from logger_config import logger
from django.core.mail import EmailMessage
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


# # Create a logger
# logger = logging.getLogger(__name__)

# # Set Level of logger
# logger.setLevel(logging.INFO)

# # Create a file handler
# handler = logging.FileHandler('usercustom.log')

# # Set the level of the file handler
# handler.setLevel(logging.INFO)

# # Create a formatter
# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')


# # Add formatter to handler
# handler.setFormatter(formatter)

# # Add handler to logger
# logger.addHandler(handler)


# Class based view to Get User Details using Token Authentication
class UserView(APIView):
  authentication_classes = [JWTAuthentication]
  permission_classes = [IsAuthenticated]
  
  def get(self,request,*args,**kwargs):
    print(request.user)
    user = CustomUser.objects.get(id=request.user.id)
    serializer = UserSerializer(user)
    return Response(serializer.data)
  
  def put(self,request,*args,**kwargs):
    usr = request.user
    print(request.data)
    print(request.FILES)
    print('hello')
    try:
        if request.data['get_email_notification'] != None:
            print(request.data['get_email_notification'])
            usr.get_email_notification = request.data['get_email_notification'] == 'True'
            usr.save()
    except:
        pass
    try:
        if request.data['get_email_broadcast_notification'] != None:
            print(request.data['get_email_broadcast_notification'])
            usr.get_email_broadcast_notification = request.data['get_email_broadcast_notification'] == 'True'
            usr.save()
    except:
        pass
    try:
        if request.data['get_otp_email'] != None:
            print(request.data['get_otp_email'])
            usr.get_otp_email = request.data['get_otp_email'] == 'True'
            usr.save()
    except:
        pass
    
    try:
        if request.data['profile_image'] != None:
            usr.profile_image = request.data['profile_image']
            usr.save()
    except:
        pass
    
    try:
        if request.data['cover_image'] != None:
            usr.cover_image = request.data['cover_image']
            usr.save()
    except:
        pass
    

    # if request.data['password'] != None:
    #     try:
    #         usr.set_password(request.data['password'])
    #         usr.save()
    #         return Response({'data':'Password Changed Successfully'},status = status.HTTP_200_OK)
    #     except:
    #         return Response({'data':'Password Change Failed'},status = status.HTTP_400_BAD_REQUEST)
    return Response({'data':'User Details Updated Successfully'},status = status.HTTP_200_OK)
    

  
class UserDetailAPI(APIView):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]

    def get(self, request, id):
        try:
            user = CustomUser.objects.get(id=id)
            serializer = UserSerializer(user)
            return Response({'data':serializer.data, 'errors':None}, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        

class userListAPI(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['groups']

@api_view(['POST'])
def login_page(request):
    serializedData = LoginSerializer(data = request.data)
    if serializedData.is_valid():
        try:
            print(request.data['email'], "We are here")
            current_user = CustomUser.objectsall.get(email = request.data['email'])
            print(current_user)
            Otpdetails.objects.filter(user = current_user).delete()
            otp = Otpdetails.objects.create(user = current_user)
            otp.setup()
            logger.info(f"{request.data['email']} logged in")
            otp.save()
        except CustomUser.DoesNotExist:
            print('no user found')
            return Response({'error':'no user found. Do you want to register.'},status = status.HTTP_401_UNAUTHORIZED)
        return Response(serializedData.data)
    else:
        return Response(serializedData.errors)


@api_view(['POST'])
def otp_verify(request):
    serializedData = OTPSerializer(data = request.data)
    if serializedData.is_valid():
        try:
            current_user = CustomUser.objectsall.get(email = request.data['email'])
            otpObject = Otpdetails.objects.get(user = current_user)
            otp = request.data['otp']
            if otpObject.is_valid_otp(otp):
                otpObject.delete()
                current_user.is_activated = True
                current_user.save()
                token_obj   = RefreshToken.for_user(user = current_user)
                if(request.data['email'] == 'superadmin@iitrpr.ac.in'):
                    print("access token is "+ str(token_obj.access_token))
                return Response({
                    "login": True,
                    'refresh':str(token_obj),
                    'access':str(token_obj.access_token),
                    'user': UserSerializer(current_user).data
                    })
            else:
                return Response({"login":False,"error":"OTP is invalid or expired"},status = status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            print(e)
            return Response({'error':'Invalid request. Use login or register.'},status = status.HTTP_204_NO_CONTENT)
    else:
        return Response(serializedData.errors,status = status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def definations(request):
    grps = Group.objects.all()
    defination = {}
    for grp in grps:
        defination[grp.name] = grp.id
    return Response({'definations':{'groups':defination}},status = status.HTTP_200_OK)


class DeactivateUser(APIView):

    def get (self,request):
        # return Response({'data':'Deactivate User'},status = status.HTTP_200_OK)
        return Response("Deactivate User")
    
    def post(self,request):
        try:
            # user_id = request.POST.get('user_id')
            user_id = request.data['user_id']
            # print("user id is ", user_id)
            user = CustomUser.objects.get(id=user_id)
            user.is_active = False
            user.save()
            return Response({'data':'User Deactivated Successfully'},status = status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response({'data':'User Not Found'},status = status.HTTP_404_NOT_FOUND)

class DeactivateMultipleUser(APIView):
    def post(self, request):
        try:
            user_ids = request.data['user_ids']  # Expect a list of user IDs
            users = CustomUser.objects.filter(id__in=user_ids)
            users.update(is_active=False)
            return Response({'data': 'Users deactivated successfully'}, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response({'error': 'One or more users do not exist'}, status=status.HTTP_400_BAD_REQUEST)

class StudentListUploadView(APIView):
    def get(self, request):
        try:
            filename = 'static/download_files/student.csv'
            with open(filename, 'rb') as fh:
                response = HttpResponse(fh.read(), content_type='text/csv')
                response['Content-Disposition'] = 'inline; filename=student.csv'
                return response
        except Exception as e:
            print(e)
            return Response({'errors':str(e)},status=status.HTTP_400_BAD_REQUEST)
        
    def post(self,request):
        id = 0
        data = {}
        flag = False
        errs = {}
        try:
            with transaction.atomic():
                csv_file = request.FILES['file']
                if not csv_file.name.endswith('.csv'):
                    return Response({'errors':'File is not CSV type'},status=status.HTTP_400_BAD_REQUEST)
                file_data = csv_file.read().decode('utf-8-sig').splitlines()
                reader = csv.DictReader(file_data)
                for row in reader:
                    id+=1
                    try:
                        user_new = create_student(row)
                        data[id] = UserSerializer(user_new).data
                        errs[id] = None
                    except Exception as e:
                        errs[id] = str(e)
                        print('row_number = ',id)
                        print(e)
                        flag = True
                        data[id] = None
                        raise e
                return Response({'data':data,'errors':errs},status=status.HTTP_200_OK)
        except Exception as exc:
            print(exc)
            if flag:
                return Response({'data':data,'errors':errs},status=status.HTTP_400_BAD_REQUEST)
            return Response({'errors':str(exc)},status=status.HTTP_400_BAD_REQUEST)

class FacultyListUploadView(APIView):
    def get(self, request):
        try:
            filename = 'static/download_files/faculty.csv'
            with open(filename, 'rb') as fh:
                response = HttpResponse(fh.read(), content_type='text/csv')
                response['Content-Disposition'] = 'inline; filename=faculty.csv'
                return response
        except Exception as e:
            print(e)
            return Response({'errors':str(e)},status=status.HTTP_400_BAD_REQUEST)
    
    def post(self,request):
        id = 0
        data = {}
        flag = False
        errs = {}
        try:
            with transaction.atomic():
                csv_file = request.FILES['file']
                if not csv_file.name.endswith('.csv'):
                    return Response({'errors':'File is not CSV type'},status=status.HTTP_400_BAD_REQUEST)
                file_data = csv_file.read().decode('utf-8-sig').splitlines()
                reader = csv.DictReader(file_data)
                for row in reader:
                    id+=1
                    try:
                        user_new = create_faculty(row)
                        data[id] = UserSerializer(user_new).data
                        errs[id] = None
                    except Exception as e:
                        errs[id] = str(e)
                        print('row_number = ',id)
                        print(e)
                        flag = True
                        data[id] = None
                        raise e
                return Response({'data':data,'errors':errs},status=status.HTTP_200_OK)
        except Exception as exc:
            print(exc)
            if flag:
                return Response({'data':data,'errors':errs},status=status.HTTP_400_BAD_REQUEST)
            return Response({'errors':str(exc)},status=status.HTTP_400_BAD_REQUEST)
        
class StaffListUploadView(APIView):
    def get(self, request):
        try:
            filename = 'static/download_files/staff.csv'
            with open(filename, 'rb') as fh:
                response = HttpResponse(fh.read(), content_type='text/csv')
                response['Content-Disposition'] = 'inline; filename=staff.csv'
                return response
        except Exception as e:
            print(e)
            return Response({'errors':str(e)},status=status.HTTP_400_BAD_REQUEST)
    
    def post(self,request):
        id = 0
        data = {}
        flag = False
        errs = {}
        try:
            with transaction.atomic():
                csv_file = request.FILES['file']
                if not csv_file.name.endswith('.csv'):
                    return Response({'errors':'File is not CSV type'},status=status.HTTP_400_BAD_REQUEST)
                file_data = csv_file.read().decode('utf-8-sig').splitlines()
                reader = csv.DictReader(file_data)
                for row in reader:
                    id+=1
                    try:
                        user_new = create_staff(row)
                        data[id] = UserSerializer(user_new).data
                        errs[id] = None
                    except Exception as e:
                        errs[id] = str(e)
                        print('row_number = ',id)
                        print(e)
                        flag = True
                        data[id] = None
                        raise e
                return Response({'data':data,'errors':errs},status=status.HTTP_200_OK)
        except Exception as exc:
            print(exc)
            if flag:
                return Response({'data':data,'errors':errs},status=status.HTTP_400_BAD_REQUEST)
            return Response({'errors':str(exc)},status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])       
def student_register(request):
    try:
        with transaction.atomic():
            try:
                new_user = create_student(request.data)
                logger.info(f"{new_user.email} registered as student")

            except Exception as e:
                raise Exception(e)
            ser = UserSerializer(new_user)
            return Response({'data':ser.data,'errors':None}, status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return Response({'data':None, 'errors': str(e)},status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])       
def faculty_register(request):
    try:
        with transaction.atomic():
            new_user = create_faculty(request.data)
            ser = UserSerializer(new_user)
            logger.info(f"{new_user.email} registered as faculty")
            return Response({'data':ser.data,'errors':None}, status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return Response({'data':None, 'errors': str(e)},status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])       
def staff_register(request):
    try:
        with transaction.atomic():
            new_user = create_staff(request.data)
            ser = UserSerializer(new_user)
            logger.info(f"{new_user.email} registered as staff")
            return Response({'data':ser.data,'errors':None}, status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return Response({'data':None, 'errors': str(e)},status=status.HTTP_400_BAD_REQUEST)

class EditProfileView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    parser_classes = [MultiPartParser, FormParser]

    def patch(self, request):
        user = request.user
        data = request.data

        # Update fields if provided in request
        if 'first_name' in data:
            user.first_name = data['first_name']
        if 'last_name' in data:
            user.last_name = data['last_name']
        if 'description' in data:
            user.description = data['description']
        if 'profile_image' in data and data['profile_image'] is not None:
            user.profile_image = data['profile_image']
        
        logger.info(f"{user.email} updated profile")
        # Save the user instance after updating the fields
        user.save(update_fields=['first_name', 'last_name', 'description', 'profile_image'])
        
        # Serialize the user instance to return the updated data
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class SendLogFileView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.method == 'POST':
            email_content = """Hello Admin,

            Attached is the department database log file.

            Best regards,
            Department Data Team
            """
            recipient_email = request.data.get('email')  # Extract recipient email from request data
            if not recipient_email:
                return JsonResponse({'error': 'Recipient email is required'}, status=400)

            email = EmailMessage(
                'Log File',
                email_content,
                'donotreplydepartmentdata@gmail.com',
                [recipient_email],  # Use recipient_email variable
            )
            with open('.dept_db.log', 'rb') as f:
                email.attach('.dept_db.log', f.read(), 'text/plain')

            email.send()
            return JsonResponse({'message': 'Email sent successfully!'}, status=200)
        return JsonResponse({'error': 'Invalid request'}, status=400)