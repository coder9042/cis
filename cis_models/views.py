from django.shortcuts import render
from django.http import HttpResponse
from cis_models.models import *
import datetime
import hashlib
from random import randrange


def home(request):
    if('user' in request.session.keys()):
        del request.session['user']
    return render(request,'index.html',{'msg':False})

def resetpass(request):
    if request.method == 'POST':
        if request.POST.get('e_id',''):
            email = request.POST['e_id']
            p = Professor.objects.filter(Email=email)
            s = Students.objects.filter(Email=email)
            if(len(p)==1):
                p = p[0]
                r = resetTable.objects.filter(prof=p)
                r.delete()
                r = resetTable()
                r.prof = p
                rn = randrange(1000,999999)
                r.hex_code = hashlib.sha1(str(rn)).hexdigest()
                #comment the following line
                r.c=str(rn)
                r.save()
                #email to the person
                return render(request, 'reset.html', {'type':2, 'prof':p.Email})
            elif(len(s)==1):
                s = s[0]
                r = resetTable.objects.filter(stud=s)
                r.delete()
                r = resetTable()
                r.stud = s
                rn = randrange(1000,999999)
                r.hex_code = hashlib.sha1(str(rn)).hexdigest()
                r.c=str(rn)
                r.save()
                return render(request, 'reset.html', {'type':2, 'prof':s.Email})
            else:
                return render(request, 'reset.html', {'type':1, 'error':'No such email id exists.'})
        elif request.POST.get('code',''):
            code = hashlib.sha1(request.POST['code']).hexdigest()
            pid = request.POST['code_prof']
            p = Professor.objects.filter(Email=pid)
            s = Students.objects.filter(Email=pid)
            if(len(p)==1):
                r = resetTable.objects.get(prof=p[0])
            else:
                r = resetTable.objects.get(stud=s[0])
            code_actual = r.hex_code
            if code == code_actual:
                return render(request,'reset.html',{'type':3, 'prof':pid})
            else:
                return render(request, 'reset.html', {'type':2, 'prof':pid, 'error':'The two codes do not match.'})
        elif request.POST.get('new_pass',''):
            new_pass = hashlib.sha1(request.POST['new_pass']).hexdigest()
            pid = request.POST['code_prof']
            p = Professor.objects.filter(Email=pid)
            s = Students.objects.filter(Email=pid)
            if(len(p)==1):
                p=p[0]
                p.Password = new_pass
                p.save()
                request.session['user']=p.Username
                p.Last_Login=datetime.datetime.now()
                return render(request,'welcome.html',{'user':p, 'message':'Password successfully changed.'})
            else:
                s=s[0]
                s.Password = new_pass
                s.save()
                request.session['user']=s.Username
                s.Last_Login=datetime.datetime.now()
                isstud = '1'
                return render(request,'welcome.html',{'user':s, 'message':'Password successfully changed.', 'isstud':isstud})
        else:
            pass
    return render(request, 'reset.html',{'type':1})

def login(request,isstud = None):
    if('user' in request.session.keys()):
        username=request.session['user']
        if(isstud == '1'):
            return studlogin(request)
        User=Professor.objects.filter(Username=username)[0]
        return render(request,'welcome.html',{'user':User, 'message':''})
    message='Wrong Username or Password'
    if request.method=='POST':
        name=request.POST['username']
        password=request.POST['pass']
        password=hashlib.sha1(password).hexdigest()
        users=Professor.objects.all()
        for user in users:
            if(user.Username==name and user.Password==password):
                user.Last_Login=datetime.datetime.now()
                user.save()
                """
                #md5(), sha1(), sha224(), sha256(), sha384(), and sha512()
                choice=randrange(7)
                while(choice==0):
                    choice=randrange(7)
                hashed=""
                if(choice==1):
                    hashed=hashlib.md5(name).hexdigest()
                if(choice==2):
                    hashed=hashlib.sha1(name).hexdigest()
                if(choice==3):
                    hashed=hashlib.sha224(name).hexdigest()
                if(choice==4):
                    hashed=hashlib.sha256(name).hexdigest()
                if(choice==5):
                    hashed=hashlib.sha384(name).hexdigest()
                if(choice==6):
                    hashed=hashlib.sha512(name).hexdigest()
                """
                request.session['user']=user.Username
                return render(request, 'welcome.html',{'user':user,'message':''})
    return render(request, 'index.html',{'msg':message.upper()})

def account_settings(request):
    errors=[]
    if('user' not in request.session.keys()):
        return render(request, 'index.html',{'msg':False})
    else:
        username=request.session['user']
        bl = branches()
        if request.method=='POST':
            name=request.POST['name'].upper()
            designation=request.POST['desig'].upper()
            department=request.POST['deptt'].upper()
            email=request.POST['email']
            phone=request.POST['phone']
            if(len(name)>30):
                errors.append('Maximum allowed length for name is 30 characters.')
            if(len(department)>3):
                errors.append('Only initials of the Department.')
            if not '@' in email:
                errors.append('Invalid Email Id.')
            if len(phone) > 4:
                errors.append('Only 4 Numbers allowed in extension.')
            try:
                p=int(phone)
            except:
                errors.append('Letters not allowed in extension.')
            if len(errors)==0:
                User=Professor.objects.filter(Username=username)
                User=User[0]
                User.Name=name
                User.Designation=designation
                User.Department=department
                User.Email=email
                User.PhoneExtension=phone
                User.save()
                return render(request,'welcome.html',{'user':User,'message':'Settings Updated'})
            else:
                User=Professor.objects.filter(Username=username)[0]
                return render(request,'settings.html',{'user':User,'errors':errors, 'bl':bl})
        else:
            User=Professor.objects.filter(Username=username)[0]
            return render(request, 'settings.html',{'user':User,'errors':errors, 'bl':bl})
        
def course_settings(request, offset):
    if('user' not in request.session.keys()):
        return render(request,'index.html',{'msg':False})
    username=request.session['user']
    User=Professor.objects.filter(Username=username)[0]
    Profs=Professor.objects.all().order_by('Name')
    if(request.method=='POST'):
        errors={}
        if request.POST.get('Save',''):
            c_pid=request.POST['pid']
            c=Courses.objects.filter(course_id=c_pid)[0]
            c.course_id=request.POST['id'].upper()
            c.course_name=request.POST['name'].upper()
            try:
                c.lecture=int(request.POST['L'])
            except:
                c.lecture=""
                errors['L']="L must be integer"
            try:
                c.tutorial=int(request.POST['T'])
            except:
                c.tutorial=""
                errors['T']="T must be integer"    
            try:
                c.practical=int(request.POST['P'])
            except:
                c.practical=""
                errors['P']="P must be integer"
            try:
                c.credit=int(request.POST['C'])
            except:
                c.credit=""
                errors['C']="L must be integer"
            try:
                c.elective_group_number=int(request.POST['egn'])
            except:
                c.elective_group_number=""
                errors['egn']="Elective Group Number must be integer"
            try:
                c.students_strength=int(request.POST['ss'])
            except:
                c.students_strength=""
                errors['ss']="Student Strength must be integer"
            try:
                c.branch_number=int(request.POST['bn'])
            except:
                c.branch_number=""
                errors['bn']="Branch Number must be integer"
            c.semester=request.POST['sem']
            c.time_added=datetime.datetime.now()
            if(len(errors)==0):
                try:
                    temp=Courses.objects.filter(course_id=c_pid)[0]
                    temp.delete()
                    c.save()
                    p_nm=request.POST['prof']
                    p=Professor.objects.filter(Name=p_nm)
                    if(len(p) != 0):
                        p=p[0]
                        c.Teaching.add(p)
                        c.save()
                    courses=Courses.objects.all().order_by("course_id")
                except:
                    errors['dup']="Duplicate Entry"
                    courses=Courses.objects.all().order_by("course_id")
                    return render(request, 'course_setting.html',{'user':User,'page':2,'courses':courses,'profs':Profs,'errors':errors,'data':c})
                return render(request, 'course_setting.html',{'user':User,'page':2,'courses':courses,'profs':Profs})
            else:
                courses=Courses.objects.all().order_by("course_id")
                return render(request, 'course_setting.html',{'user':User,'page':2,'courses':courses,'profs':Profs,'errors':errors,'data':c})
        if request.POST.get('Remove',''):
            c_id=request.POST['id']
            course=Courses.objects.filter(course_id=c_id)[0]
            course.delete()
            courses=Courses.objects.all().order_by("course_id")
            return render(request, 'course_setting.html',{'user':User,'page':2,'courses':courses,'profs':Profs})
        if request.POST.get('Add',''):
            c=Courses()
            c.course_id=request.POST['id'].upper()
            c.course_name=request.POST['name'].upper()
            try:
                c.lecture=int(request.POST['L'])
            except:
                c.lecture=""
                errors['L']="L must be integer"
            try:
                c.tutorial=int(request.POST['T'])
            except:
                c.tutorial=""
                errors['T']="T must be integer"    
            try:
                c.practical=int(request.POST['P'])
            except:
                c.practical=""
                errors['P']="P must be integer"
            try:
                c.credit=int(request.POST['C'])
            except:
                c.credit=""
                errors['C']="L must be integer"
            try:
                c.elective_group_number=int(request.POST['egn'])
            except:
                c.elective_group_number=""
                errors['egn']="Elective Group Number must be integer"
            try:
                c.students_strength=int(request.POST['ss'])
            except:
                c.students_strength=""
                errors['ss']="Student Strength must be integer"
            try:
                c.branch_number=int(request.POST['bn'])
            except:
                c.branch_number=""
                errors['bn']="Branch Number must be integer"
            c.semester=request.POST['sem']
            c.time_added=datetime.datetime.now()
            if(len(errors)==0):
                try:
                    c.save()
                    c_id=c.course_id
                    c=Courses.objects.filter(course_id=c_id)[0]
                    p_nm=request.POST['prof']
                    p=Professor.objects.filter(Name=p_nm)
                    if(len(p) != 0):
                        p=p[0]
                        c.Teaching.add(p)
                        c.save()
                    courses=Courses.objects.all().order_by("course_id")
                except:
                    errors['dup']="Duplicate Entry"
                    courses=Courses.objects.all().order_by("course_id")
                    return render(request, 'course_setting.html',{'user':User,'page':1,'courses':courses,'profs':Profs,'errors':errors,'data':c})
                return render(request, 'course_setting.html',{'user':User,'page':2,'courses':courses,'profs':Profs})
            else:
                courses=Courses.objects.all().order_by("course_id")
                return render(request, 'course_setting.html',{'user':User,'page':1,'courses':courses,'profs':Profs,'errors':errors,'data':c})
    else:
        offset=int(offset)
        courses=Courses.objects.all().order_by("course_id")
        return render(request, 'course_setting.html',{'user':User,'page':offset,'courses':courses,'profs':Profs})

def rooms_settings(request, offset):
    if('user' not in request.session.keys()):
        return render(request,'index.html',{'msg':False})
    else:
        errors={}
        offset=int(offset)
        username=request.session['user']
        User=Professor.objects.filter(Username=username)[0]
        if request.method=='POST':
            if(request.POST.get('Add','')):
                room=Rooms()
                room.room_id=request.POST['id'].upper()
                try:
                    room.room_strength=int(request.POST['strength'])
                except:
                    errors['0']="Room strength must be integer."
                    return render(request, 'rooms_setting.html', {'user':User, 'page':1,'errors':errors})
                if(request.POST['projector'] == 'Yes'):
                    room.projector=1
                else:
                    room.projector=0
                if(request.POST['conference'] == 'Yes'):
                    room.conference=1
                else:
                    room.conference=0
                if(request.POST['lab'] == 'Yes'):
                    room.isLab=True
                else:
                    room.isLab=False
                if room.isLab==True:
                    room.lab_type=request.POST['lab_type'].upper()
                    if room.lab_type == '':
                        errors['1']='Lab department not specified'
                        return render(request, 'rooms_setting.html', {'user':User, 'page':1,'errors':errors})
                    if len(room.lab_type)>2:
                        errors['1']='Department initials cannot be greater than length 2.'
                        return render(request, 'rooms_setting.html', {'user':User, 'page':1,'errors':errors})
                room.time_added=datetime.datetime.now()
                if(len(errors) == 0):
                    room.save()
                rooms=Rooms.objects.all().order_by("room_id")
                return render(request, 'rooms_setting.html', {'user':User, 'page':2, 'rooms':rooms,'errors':errors})
            if request.POST.get('Remove',''):
                r_id=request.POST['id']
                room=Rooms.objects.filter(room_id=r_id)[0]
                room.delete()
                rooms=Rooms.objects.all().order_by("room_id")
                return render(request, 'rooms_setting.html', {'user':User, 'page':2, 'rooms':rooms,'errors':errors})
        else:
            rooms=Rooms.objects.all().order_by("room_id")
            return render(request, 'rooms_setting.html',{'user':User,'page':offset,'rooms':rooms,'errors':errors})

def branches():
    courses = Courses.objects.all()
    course_list = []
    for c in courses:
        s1 = c.course_id[0:2]
        s2 = c.course_id[0:3]
        chk = False
        chk2 = False
        for char in s1:
            if char.isdigit():
                chk = True
        for char in s2:
            if char.isdigit():
                chk2 = True
        if chk == False and s1 not in course_list:
            course_list.append(s1)
        if chk2 == False and s2 not in course_list:
            course_list.append(s2)

    return course_list

def prof_settings(request,offset):
    if 'user' not in request.session.keys():
        return render(request,'index.html',{'msg':False})
    offset=int(offset)
    username=request.session['user']
    User=Professor.objects.filter(Username=username)[0]
    #cl = branches()
    if request.method == 'POST':
        errors={}
        if request.POST.get('Add', ''):
            p=Professor()
            data={}
            data['name'] = p.Name=request.POST['name'].upper()
            data['desig'] = p.Designation=request.POST['desig'].upper()
            data['deptt'] = p.Department=request.POST['deptt'].upper()
            data['email'] = p.Email=request.POST['email']
            if len(p.Department) > 3:
                errors['deptt']='Only initials allowed.'
            ph=request.POST['extension']
            try:
                p.PhoneExtension=int(ph)
                if len(ph) > 4:
                    errors['ext']='Only 4 numbers allowed'
                data['ext']=p.PhoneExtension
            except:
                errors['ext']='Only numbers allowed.'
            if(len(errors) == 0):
                try:
                    p.save()
                except:
                    errors['dup']='Duplicate Entry'
                    return render(request, 'professor_setting.html',{'user':User,'page':1,'errors':errors,'data':data})
                profs=Professor.objects.all().order_by('Name')
                return render(request, 'professor_setting.html',{'user':User,'page':2,'profs':profs})
            else:
                return render(request, 'professor_setting.html',{'user':User,'page':1,'errors':errors,'data':data})
        if request.POST.get('Remove', ''):
            nm=request.POST['nm']
            p=Professor.objects.filter(Name=nm)[0]
            p.delete()
            profs=Professor.objects.all().order_by('Name')
            return render(request, 'professor_setting.html',{'user':User,'page':2,'profs':profs})
        if request.POST.get('Save', ''):
            nm=request.POST['p_name']
            p=Professor.objects.filter(Name=nm)[0]
            data={}
            data['name'] = p.Name=request.POST['name'].upper()
            data['desig'] = p.Designation=request.POST['desig'].upper()
            data['deptt'] = p.Department=request.POST['deptt'].upper()
            data['email'] = p.Email=request.POST['email']
            if len(p.Department) > 3:
                errors['deptt']='Only initials allowed.'
            ph=request.POST['ext']
            try:
                p.PhoneExtension=int(ph)
                if len(ph) > 4:
                    errors['ext']='Only 4 numbers allowed'
            except:
                errors['ext']='Only numbers allowed.'
            if(len(errors) == 0):
                try:
                    data['ext']=p.PhoneExtension
                    p.save()
                except:
                    errors['dup']='Duplicate Entry'
                    profs=Professor.objects.all().order_by('Name')
                    return render(request, 'professor_setting.html',{'user':User,'page':2,'profs':profs,'errors':errors,'data':data,'unhide':True,'p_name':nm})
                profs=Professor.objects.all().order_by('Name')
                return render(request, 'professor_setting.html',{'user':User,'page':2,'profs':profs})
            else:
                profs=Professor.objects.all().order_by('Name')
                return render(request, 'professor_setting.html',{'user':User,'page':2,'profs':profs,'errors':errors,'data':data,'unhide':True, 'p_name':nm})
            
    else:
        profs=Professor.objects.all().order_by('Name')
        return render(request, 'professor_setting.html', {'user':User, 'page':offset, 'profs':profs})

def manage_appoint(request, typ, pk):
    if 'user' not in request.session.keys():
        return render(request,'index.html',{'msg':False})
    typ = int(typ)
    pk = int(pk)
    a=appointment.objects.get(pk=pk)
    if typ == 1:
        a.confirmed = 1
        a.save()
    elif typ == 2:
        a.delete()
    return prof_req(request)

def prof_req(request):
    if 'user' not in request.session.keys():
        return render(request,'index.html',{'msg':False})
    username=request.session['user']
    User=Professor.objects.filter(Username=username)[0]
    r=Request.objects.filter(user=User)
    a=appointment.objects.filter(professor=User)
    if User.Username == 'admin':
        r=Request.objects.all()
    return render(request, 'myrequests.html',{'user':User, 'req':r, 'app':a})

def manage_req(request, typ, pk):
    if 'user' not in request.session.keys() or request.session['user'] != 'admin':
        return render(request,'index.html',{'msg':False})
    typ = int(typ)
    pk = int(pk)
    r=Request.objects.get(pk=pk)
    if request.session['user'] != 'admin':
        a=appointment.objects.get(pk=pk)
    if typ == 1:
        if r.t1 != None:
            r.t1.approved = True
            r.t1.save()
        if r.t2 != None:
            r.t2.approved = True
            r.t2.save()
        if r.t3 != None:
            r.t3.approved = True
            r.t3.save()
        if r.t4 != None:
            r.t4.approved = True
            r.t4.save()
        if request.session['user'] != 'admin':
            a.confirmed = True
            a.save()
        r.save()
    if typ == 2:
        if r.t1 != None:
            r.t1.delete()
        if r.t2 != None:
            r.t2.delete()
        if r.t3 != None:
            r.t3.delete()
        if r.t4 != None:
            r.t4.delete()
        r.delete()
        if request.session['user'] != 'admin':
            a.delete()
    return prof_req(request)

#def docs_view(request):
#    return render(request, "_build/html/index.html")


#students
def studhome(request):
    if('user' in request.session.keys()):
        del request.session['user']
    return render(request,'students.html',{'msg':False})

def studlogin(request):
    if('user' in request.session.keys()):
        username=request.session['user']
        User=Students.objects.filter(Username=username)[0]
        isstud = '1'
        batch = '0'
        return render(request,'welcome.html',{'user':User, 'message':'', 'batch':batch, 'isstud':isstud})
    message='Wrong Username or Password'
    if request.method=='POST':
        name=request.POST['username']
        password=request.POST['pass']
        isstud = '1'
        batch = '0'
        password=hashlib.sha1(password).hexdigest()
        users=Students.objects.all()
        for user in users:
            if(user.Username==name and user.Password==password):
                user.Last_Login=datetime.datetime.now()
                user.save()
                request.session['user']=user.Username
                return render(request, 'welcome.html',{'user':user,'message':'', 'batch':batch, 'isstud':isstud})
    return render(request, 'students.html',{'msg':message.upper()})

def Appointments(request,offset):
    if ('user' not in request.session.keys()):
        return render(request,'students.html')
    isstud='1'
    batch = '0'
    offset=int(offset)
    username=request.session['user']
    Profs=Professor.objects.all()
    Days=range(1,32)
    date_now=datetime.datetime.now()
    Months=[]
    Months.append(date_now.month)
    Months.append(date_now.month+1)
    Hours=range(0,24)
    Minutes=range(0,60,5)
    chkmonth_1=[1,3,5,7,8,10,12]
    chkmonth_2=[4,6,9,11]
    if request.method == 'POST':
        errors={}
        if request.POST.get('Make',''):
            p=Professor()
            data={}
            data['name'] = p.Name=request.POST['prof'].upper()
            data['deptt'] = p.Department=request.POST['deptt'].upper()
            data['month'] = month=int(request.POST['month'].upper())
            data['day'] = day=int(request.POST['day'].upper())
            data['hour'] = hour=int(request.POST['hour'].upper())
            data['minute'] = minute=int(request.POST['minute'].upper())
            if len(p.Department) > 3:
                errors['deptt'] = 'only initials are allowed'
            users=Professor.objects.filter(Department = p.Department, Name = p.Name)
##            if len(users)==0:
##                errors['name'] = 'Professor does not belong to IITP'
            date_given=datetime.datetime.now()
            try:
                date_given=datetime.datetime(date_given.year,month,day,hour,minute)
                if date_given.month == date_now.month:
                    if date_given.day < date_now.day:
                        errors['date']='Date does not exist'
                    elif date_given.day == date_now.day:
                        if date_given.hour < date_now.hour:
                            errors['date']='time has passed out'
                        elif date_given.hour == date_now.hour:
                            errors['date']='Appointments must be set atleast before 1 hour'
                        elif date_given.hour > date_now.hour:
                            if date_now.minute - date_given.minute < 60:
                                errors['date']='Appointments must be set atleast before 1 hour'
            except:
                errors['date']='Please check date and time'
            if not errors:
                if users:
                    user=users[0]
                subject='Requested Appointment'
               # message='This is to inform that ' + username + 'want to meet you between ' + hour + 'hours ' +minute+'minutes.Please take into consideration.Thanks CIS' 
##                send_mail(
##                        subject,
##                        message,
##                        user.Email,
##                        ['admin@iitp.ac.in']
##                    )
                appProf=appointment()
                appProf.student = Students.objects.filter(Username=username)[0]
                appProf.professor = Professor.objects.filter(Name=p.Name, Department=p.Department)[0]
                appProf.Hour=hour
                appProf.Day=day
                appProf.Month=month
                appProf.Minute=minute
                appProf.confirmed = 0
                appProf.save()
                stud = Students.objects.filter(Username=username)[0]
                studApp=stud.appointment_set.all()
                return render(request, 'Appointments.html',{'user':username,'page':2,'appointments':studApp, 'batch':batch, 'isstud':isstud})
            else:
                return render(request, 'Appointments.html',{'user':username,'page':1,'errors':errors,'data':data,'profs':Profs,'months':Months,'days':Days,'hours':Hours,'minutes':Minutes, 'batch':batch, 'isstud':isstud})
        #stud = Students.objects.filter(Username=username)[0]
        #studApp=stud.appointment_set.all()
        #if studApp == null:
        #    return render(request, 'Appointments.html',{'user':username,'page':offset,'appointments':studApp,'profs':Profs})    
    else:
        stud = Students.objects.filter(Username=username)[0]
        studApp=stud.appointment_set.all()
        for app in studApp:
            if app.Month < date_now.month:
                app.delete()
            elif app.Month == date_now.month:
                if app.Day < date_now.day:
                    app.delete()
        stud = Students.objects.filter(Username=username)[0]
        studApp=stud.appointment_set.all()
        return render(request, 'Appointments.html', {'user':username, 'page':offset, 'appointments':studApp, 'profs':Profs,'months':Months,'days':Days,'hours':Hours,'minutes':Minutes, 'batch':batch, 'isstud':isstud})

def changePassword(request):
    if ('user' not in request.session.keys()):
        return render(request,'students.html')
    user=request.session['user']
    isstud='1'
    batch = '0'
    User = Students.objects.filter(Username=user)[0]
    isstud = '1'
    if request.method == 'POST' :
        errors={}
        currPassword = request.POST['currpass']
        currPassword = hashlib.sha1(currPassword).hexdigest()
        new1=request.POST['newpass1']
        new2=request.POST['newpass2']
        if (User.Password != currPassword):
            errors['currpass']='Wrong Password'
        if(new1!=new2):
            errors['newpass']='Password did not match'
        if len(errors)==0:
            newpass=request.POST['newpass1']
            newpass=hashlib.sha1(newpass).hexdigest()
            User.Password=newpass
            User.save()
            return render(request, 'welcome.html', {'user':User, 'errors':errors, 'batch':batch, 'isstud':isstud})
        return render(request, 'options.html', {'user':User, 'errors':errors, 'batch':batch, 'isstud':isstud})
    else:
        return render(request, 'options.html', {'user':User, 'batch':batch, 'isstud':isstud})
