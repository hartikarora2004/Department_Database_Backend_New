from rest_framework.response import Response
from rest_framework import status 
from rest_framework.views import APIView
from .generate_bog_file import generate_file
from .department_info_file import *
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from achievements.models import Achievement
from achievements.serializers import AchievementListSerializer
from events.models import Event
from events.serializers import EventListSerializer
from visits.models import Visit
from visits.serializers import VisitListSerializer
from django.http import HttpResponse
from batch.models import Batch
from publications.models import Publication
from publications.serializers import PublicationListSerializer
from project.models import Project
from project.serializers import ProjectListSerializer
from batch.serializers import BatchSerializer
from department.serializers import DepartmentSerializer
from .models import *
from .serializers import *
from logger_config import logger


class GenerateBog(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, d_code, start_date, end_date):
        try:
            dept = Department.objects.get(id = d_code)
            achievement_records = Achievement.objects.filter(date__range = [start_date, end_date]).filter(department__in = [dept])
            # filter faculty and student achievements
            faculty_achievement_records = achievement_records.filter(participants__groups__name = 'Faculty').distinct()
            student_achievement_records = achievement_records.filter(participants__groups__name = 'Student').distinct()
            student_achievement_records = student_achievement_records.exclude(id__in = faculty_achievement_records)
            # filter events
            events = Event.objects.filter(date__range = [start_date, end_date]).filter(department__in = [dept])
            # get visits
            all_visits = Visit.objects.filter(department__in = [dept])
            # filter visits in date range
            visits_after = all_visits.filter(from_date__gte = end_date)
            visits_before = all_visits.filter(to_date__lte = start_date)
            visits = all_visits.exclude(id__in = visits_after)
            visits = visits.exclude(id__in = visits_before)

            #generate serializers
            department_record = DepartmentSerializer(dept)
            faculty_achievement_records = AchievementListSerializer(faculty_achievement_records, many=True)
            student_achievement_records = AchievementListSerializer(student_achievement_records, many=True)
            events = EventListSerializer(events, many=True)
            visits = VisitListSerializer(visits, many=True)

            response_dict = {}
            response_dict['data'] = {}
            response_dict['headings'] = {}
            response_dict['attributes'] = {}
            response_dict['data']['faculty_achievements'] = faculty_achievement_records.data
            response_dict['headings']['faculty_achievements'] = ['Title', 'Date', 'Participants']
            response_dict['attributes']['faculty_achievements'] = ['title', 'date', 'users']
            response_dict['data']['student_achievements'] = student_achievement_records.data
            response_dict['headings']['student_achievements'] = ['Title', 'Date', 'Participants']
            response_dict['attributes']['student_achievements'] = ['title', 'date', 'users']
            response_dict['data']['events'] = events.data
            response_dict['headings']['events'] = ['Title', 'Date', 'Venue', 'Organizers']
            response_dict['attributes']['events'] = ['title', 'date', 'venue', 'users']
            response_dict['data']['visits'] = visits.data
            response_dict['headings']['visits'] = ['Title', 'Place of Visit', 'Visited by']
            response_dict['attributes']['visits'] = ['title',  'venue', 'users']
            response_dict['data']['department'] = department_record.data

            return Response(response_dict, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'errors':str(e)},status=status.HTTP_400_BAD_REQUEST)


class GenerateReport(APIView):
    authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]

    def get(self,request):
        try:
            dept = request.user.department
            ser = BogMeetingFileSerializer(BogMeetingFile.objects.filter(department = dept), many=True)
            print("BOG Report Generated by " + request.user.email)
            logger.info("BOG Report Generated by " + request.user.email)
            return Response({'data':ser.data, 'errors':None},status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({'data':None, 'errors':str(e)},status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        try:
            filename = "static/BoG.docx"
            print(request.data)
            dept = Department.objects.get(id = request.data['department'])
            achievement_records = Achievement.objects.filter(id__in = request.data['faculty_achievements'])
            student_achievement_records = Achievement.objects.filter(id__in = request.data['student_achievements'])
            events = Event.objects.filter(id__in = request.data['events'])
            visits = Visit.objects.filter(id__in = request.data['visits'])
            temp = request.data
            name = f"BOG_Report_{dept.code}_{temp['year']}"
            start_date = temp['startDate']
            end_date = temp['endDate']
            if 'filename' in request.data:
                name = request.data['filename']
            temp['name'] = name
            file_obj = BogMeetingFileSerializer(data = temp)
            if file_obj.is_valid():
                file_obj.save()
            else:
                print(file_obj.errors)
            generate_file(filename,start_date, end_date, achievement_records = achievement_records, student_achievement_records = student_achievement_records, event_records = events, visit_records = visits)
            with open(filename, 'rb') as fh:
                response = HttpResponse(fh.read(), content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
                response['Content-Disposition'] = 'inline; filename=' + name + '.docx'
                return response
        except Exception as e:
            print(e)
            return Response({'errors':str(e)},status=status.HTTP_400_BAD_REQUEST)
                
class GenerateDinfo(APIView):
    authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]


    def get(self, request,d_code,start_date,end_date):
        # print(start_date, end_date, d_code)
        try:
            dept = Department.objects.get(id = d_code)
            batches = Batch.objects.filter(department = dept)
            # get achievements
            achievement_records = Achievement.objects.filter(date__range = [start_date, end_date]).filter(department__in = [dept])
            # filter faculty and student achievements
            faculty_achievement_records = achievement_records.filter(participants__groups__name = 'Faculty').distinct()
            student_achievement_records = achievement_records.filter(participants__groups__name = 'Student').distinct()
            student_achievement_records = student_achievement_records.exclude(id__in = faculty_achievement_records)
            # get events
            events = Event.objects.filter(date__range = [start_date, end_date]).filter(department__in = [dept])
            # get visits
            all_visits = Visit.objects.filter(department__in = [dept])
            # filter visits in date range
            visits_after = all_visits.filter(from_date__gte = end_date)
            visits_before = all_visits.filter(to_date__lte = start_date)
            visits = all_visits.exclude(id__in = visits_after)
            visits = visits.exclude(id__in = visits_before)
            visits = visits.distinct()
            # filter faculty and student visits
            fac_visit = visits.filter(user__groups__name = 'Faculty').distinct()
            st_visit = visits.exclude(id__in = fac_visit)
            # get publications
            all_publications = Publication.objects.filter(department__in = [dept])
            # filter publications published and accepted in date range.
            publications_published = all_publications.filter(published_date__range = [start_date, end_date])
            publications_accepted = all_publications.filter(accepted_date__range = [start_date, end_date])
            publications = publications_published | publications_accepted
            publications = publications.distinct()
            # get projects
            all_projects = Project.objects.filter(department__in = [dept])
            # filter projects started and completed in date range.
            projects_before = all_projects.filter(end_date__lte = start_date)
            projects_after = all_projects.filter(start_date__gte = end_date)
            projects = all_projects.exclude(id__in = projects_before)
            projects = projects.exclude(id__in = projects_after)
            projects = projects.distinct()

            # Genenrating serializers
            fac_achievement_serializer = AchievementListSerializer(faculty_achievement_records, many = True)
            st_achievement_serializer = AchievementListSerializer(student_achievement_records, many = True)
            event_serializer = EventListSerializer(events, many = True)
            fac_visit_serializer = VisitListSerializer(fac_visit, many = True)
            st_visit_serializer = VisitListSerializer(st_visit, many = True)
            publication_serializer = PublicationListSerializer(publications, many = True)
            project_serializer = ProjectListSerializer(projects, many = True)
            batch_serializer = BatchSerializer(batches, many = True)

            response_data = {}
            response_data['data'] = {}
            response_data['headings'] = {}
            response_data['attributes'] = {}
            response_data['errors'] = None
            response_data['data']['faculty_achievements'] = fac_achievement_serializer.data
            response_data['data']['student_achievements'] = st_achievement_serializer.data
            response_data['data']['events'] = event_serializer.data
            response_data['data']['faculty_visits'] = fac_visit_serializer.data
            response_data['data']['student_visits'] = st_visit_serializer.data
            response_data['data']['publications'] = publication_serializer.data
            response_data['data']['projects'] = project_serializer.data
            response_data['data']['batches'] = batch_serializer.data
            response_data['headings']['faculty_achievements'] = ['Title', 'Date', 'Participants']
            response_data['attributes']['faculty_achievements'] = ['title', 'date', 'users']
            response_data['headings']['student_achievements'] = ['Title', 'Date', 'Participants']
            response_data['attributes']['student_achievements'] = ['title', 'date', 'users']
            response_data['headings']['events'] = ['Title', 'Date', 'Venue', 'Organizers']
            response_data['attributes']['events'] = ['title', 'date', 'venue','users']
            response_data['headings']['faculty_visits'] = ['Title', 'Place of Visit', 'Visited by']
            response_data['attributes']['faculty_visits'] = ['title',  'venue', 'users']
            response_data['headings']['student_visits'] = ['Title', 'Place of Visit', 'Visited by']
            response_data['attributes']['student_visits'] = ['title',  'venue', 'users']
            response_data['headings']['publications'] = ['Title', 'Authors', 'Published Date', 'Accepted Date']
            response_data['attributes']['publications'] = ['title', 'authors', 'published_date', 'accepted_date']
            response_data['headings']['projects'] = ['Title', 'Start Date', 'End Date', 'Project Members', 'Investors']
            response_data['attributes']['projects'] = ['title', 'start_date', 'end_date', 'users', 'investors']
            response_data['headings']['batches'] = ['Id', 'Batch Name', 'Year']
            response_data['attributes']['batches'] = ['id', 'name', 'year']
            return Response(response_data, status = status.HTTP_200_OK)
        except Exception as e:
            return Response({'errors':str(e)},status=status.HTTP_400_BAD_REQUEST)
        


class GenerateDinfo_file(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self,request):
        try:
            dept = request.user.department
            ser = DinfoMeetingFileSerializer(DinfoMeetingFile.objects.filter(department = dept), many =True )
            return Response({'data':ser.data, 'errors':None},status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({'data':None, 'errors':str(e)},status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        try:
            filename = "static/Dinfo.docx"
            batches = Batch.objects.filter(id__in = request.data['batches'])
            dep = Department.objects.get(id = request.data['department'])
            achievement_records = Achievement.objects.filter(id__in = request.data['faculty_achievements'])
            student_achievement_records = Achievement.objects.filter(id__in = request.data['student_achievements'])
            events = Event.objects.filter(id__in = request.data['events'])
            visits = Visit.objects.filter(id__in = request.data['faculty_visits'])
            st_visit = Visit.objects.filter(id__in = request.data['student_visits'])
            publications = Publication.objects.filter(id__in = request.data['publications'])
            project_records = Project.objects.filter(id__in = request.data['projects'])
            year = request.data['year']
            temp = request.data
            name = f"dinfo_{dep.code}_{year}"
            if 'filename' in request.data:
                name = request.data['filename']
            temp['name'] = name
            dinfo_obj = DinfoMeetingFileSerializer(data = request.data)
            final_start_date = request.data['startDate']
            final_end_date = request.data['endDate']
            print("validating")
            if dinfo_obj.is_valid():
                print("validated")
                dinfo_obj.save()
            else:
                print(dinfo_obj.errors)
            generate_file_now(filename, batches, dep, start_date=final_end_date, end_date=final_start_date,
                              publications_records = publications, year = year, 
                              project_records = project_records, achievement_records = achievement_records, 
                              student_achievement_records = student_achievement_records, 
                              event_records = events, visit_records = visits, st_visit_records = st_visit)
            with open(filename, 'rb') as fh:
                response = HttpResponse(fh.read(), content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
                response['Content-Disposition'] = 'inline; filename=' + name + '.docx'
                return response
        except Exception as e:
            print(e)
            return Response({'errors':str(e)},status=status.HTTP_400_BAD_REQUEST)


class GetDinfo(APIView):
    authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]

    def get(self,request,id):
        try:
            obj = DinfoMeetingFile.objects.get(id = id)
            filename = "dinfo_prev.docx"
            print("check here")
            print(request.data)
            generate_file_now(f"static/{obj.name}.docx", 
                              obj.batches.all(), 
                              obj.department,
                              start_date="", end_date="",
                              publications_records = obj.publications.all(), 
                              year = obj.year, 
                              project_records = obj.projects.all(), 
                              achievement_records = obj.faculty_achievements.all(), 
                              student_achievement_records = obj.student_achievements.all(), 
                              event_records = obj.events.all(), 
                              visit_records = obj.faculty_visits.all(), 
                              st_visit_records = obj.student_visits.all()
                              )
            with open(f"static/{obj.name}.docx", 'rb') as fh:
                response = HttpResponse(fh.read(), content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
                response['Content-Disposition'] = 'inline; filename=' + f"{obj.name}.docx"
                return response
        except Exception as e:
            print(e)
            return Response({'errors':str(e)},status=status.HTTP_400_BAD_REQUEST)
            
class GetBog(APIView):
    authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]

    def get(self,request,id):
        try:
            obj = BogMeetingFile.objects.get(id = id)
            filename = "bog_prev.docx"
            generate_file(f"static/{obj.name}.docx", 
                          start_date="2020", end_date="2021",
                          achievement_records = obj.faculty_achievements.all(), 
                          student_achievement_records = obj.student_achievements.all(), 
                          event_records = obj.events.all(), 
                          visit_records = obj.visits.all()
                          )
            with open(f"static/{obj.name}.docx", 'rb') as fh:
                response = HttpResponse(fh.read(), content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
                response['Content-Disposition'] = 'inline; filename=' + f"{obj.name}.docx"
                return response
        except Exception as e:
            print(e)
            return Response({'errors':str(e)},status=status.HTTP_400_BAD_REQUEST)