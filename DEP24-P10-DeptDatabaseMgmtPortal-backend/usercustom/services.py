from usercustom.models import CustomUser
from staff_details.models import staffDetails
from faculty_details.models import facultyDetails
from student_details.models import studentDetails
from department.models import Department
from batch.models import Batch
from django.contrib.auth.models import Group


def create_student(row):
    errors = None
    print("hello")
    # check if email is of format 1234abc1234@iitrpr.ac.in

    if row['email'][-13:] != '@iitrpr.ac.in':
        errors = 'Please use IIT Ropar email id.'
        raise Exception(errors)
    row['entry_no'] = row['entry_no'].upper()
    row['username'] = row['entry_no']
    
    batch_string = row['entry_no'][:-4]
    row['year'] = int(row['entry_no'][:-7])

    batch = Batch.objects.filter(name = batch_string)
    if len(batch) == 0:
        errors = 'Batch not found. Please contact admin/staff to create your batch.'
        raise Exception(errors)

    row['batch_id'] = batch[0].id

    try:
        user_new = CustomUser.objects.create_user(
            email = row['email'],
            password='SanW1@2',
        )
    except Exception as e:
        print(e)
        errors = 'email already exists'
        raise Exception(errors)
    user_new.save()
    degree_map = {}
    degree_map['ug'] = 'B.Tech'
    degree_map['pg'] = 'M.Tech'
    degree_map['phd'] = 'Ph.D'
    try:
        user_new.username = row['username']
        user_new.first_name = row['first_name']
        user_new.last_name = row['last_name']
        user_new.department = Department.objects.get(code = row['department_code'])
        user_new.year = row['year']
        user_new.user_type = row['degree']
        user_new.is_activated = True
        user_new.get_email_notification = True
        user_new.get_email_broadcast_notification = True
        user_new.get_otp_email = True
        user_new.groups.add(Group.objects.get(name = 'Student'))
        user_new.save()
        try:
            user_new.doctorate_degree = row['is_doctrate']
        except:
            user_new.doctorate_degree = False
    except Exception as e:
        print(e)
        errors = str(e)
        raise Exception(errors)
    
    print('added all details')

    try:
        print(row['faculty_advisor_email'])
        adv = CustomUser.objects.get(email = row['faculty_advisor_email'])
    except Exception as e:
        print(e)
        raise Exception("faculty advisor email invalid. Please contact admin/staff to add faculty advisor.")
    try:
        st_d = studentDetails.objects.create(
            student = user_new,
            faculty_advisor = adv,
            degree = degree_map[row['degree']],
            batch = Batch.objects.get(id = row['batch_id']),
            entry_no = row['entry_no']
        )
    except Exception as e:
        print(e)
        if 'entry_no' in str(e):
            raise Exception("entry no invalid.")
        raise Exception("batch id invalid.")
    print('saving student details')
    st_d.save()
    return user_new


def create_faculty(row):
    errors = None
    print("hello")
    try:
        user_new = CustomUser.objects.create_user(
            email = row['email'],
            password='SanW1@2',
        )
    except Exception as e:
        print(e)
        errors = 'email already exists'
        raise Exception(errors)
    user_new.save()
    try:
        user_new.username = row['username']
        user_new.first_name = row['first_name']
        user_new.last_name = row['last_name']
        user_new.department = Department.objects.get(code = row['department_code'])
        user_new.year = row['year']
        user_new.user_type = 'fc'
        user_new.is_activated = True
        user_new.get_email_notification = True
        user_new.get_email_broadcast_notification = True
        user_new.get_otp_email = True
        user_new.groups.add(Group.objects.get(name = 'Faculty'))
        user_new.save()
        try:
            print("hello, ",type(row['is_doctrate']))
            user_new.doctorate_degree = row['is_doctrate']
            if row['is_doctrate']:
                try:
                    phd_in = row['phd_instuition']
                except Exception as e:
                    print(e)
                    raise Exception("phd instuition invalid.")
        except:
            user_new.doctorate_degree = True
    except Exception as e:
        print(e)
        errors = str(e)
        raise Exception(errors)
    
    print('added all details')

    try:
        fc_d = facultyDetails.objects.create(
            faculty = user_new,
            designation = row['designation'],
            fac_id = 'NA',
            phd_instuition = phd_in,
            fields_of_interest = row['fields_of_interest'],
        )
    except Exception as e:
        print(e)
        if 'designation' in str(e):
            raise Exception("designation invalid.")
        raise Exception(str(e))
    print('saving student details')
    fc_d.save()
    return user_new


def create_staff(row):
    errors = None
    print("hello")
    try:
        user_new = CustomUser.objects.create_user(
            email = row['email'],
            password='SanW1@2',
        )
    except Exception as e:
        print(e)
        errors = 'email already exists'
        raise Exception(errors)
    user_new.save()
    try:
        user_new.username = row['username']
        user_new.first_name = row['first_name']
        user_new.last_name = row['last_name']
        user_new.department = Department.objects.get(code = row['department_code'])
        user_new.year = row['year']
        user_new.user_type = 'st'
        user_new.is_activated = True
        user_new.get_email_notification = True
        user_new.get_email_broadcast_notification = True
        user_new.get_otp_email = True
        user_new.groups.add(Group.objects.get(name = 'Staff'))
        user_new.save()
        user_new.doctorate_degree = False
    except Exception as e:
        print(e)
        errors = str(e)
        raise Exception(errors)
    print('added all details')
    try:
        sta_d = staffDetails.objects.create(
            staff = user_new,
            type = row['staff_type'],
            sta_id = 'NA'
        )
    except Exception as e:
        print(e)
        if 'type' in str(e):
            raise Exception("staff type invalid.")
        raise Exception(str(e))
    print('saving student details')
    sta_d.save()
    return user_new
