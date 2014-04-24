from django.shortcuts import render
from django.http import HttpResponse
from cis_models.models import *
from django.db.models import Q
import random, datetime
from filter import *

table={}
tt_name=''
yr=1
def timetable(request,tt,batch=None,isstud=None):
    #print "Top"
    #print tt
    if 'user' not in request.session.keys():
        return render(request, 'index.html',{'msg':False})
    usernm=request.session['user']
    if(isstud != '1'):
        user=Professor.objects.get(Username=usernm)
        isstud = '0'
    else:
        isstud='1'
        user=Students.objects.get(Username=usernm)
    if(batch is None):
        isflip='0'
    else:
        isflip=batch
    error=''
    T=''
    if request.method == 'POST':
        if not request.POST.get('select'):
            T=tt()
            heading=request.POST['heading']
            div=heading.index(':')
            #print heading
            d=heading[0:div]
            s=heading[(div+1):]
            #return HttpResponse(str(d)+":"+str(s))
            Cell_obj=Cell.objects.filter(slot=s, day=d.lower())[0]
            if request.POST.get('Clear',''):
                temp=tt.objects.filter(Cell=Cell_obj)
                ex = request.POST['extra'];
                print ex
                print temp
                if ex == 'None':
                    cid=request.POST['courseid']
                    c=Courses.objects.get(course_id=cid)
                    print "course"
                    print c
                    temp=temp.filter(Course=c)
                else:
                    temp=temp.filter(Extra=ex)
                print temp
                temp.delete()
            if request.POST.get('Manual',''):
                T.Cell=Cell_obj
                c_id=request.POST['courses']
                if c_id == 'other':
                    T.Extra=request.POST['other']
                else:
                    try:
                        Course_obj=Courses.objects.filter(course_id=c_id)[0]
                    except:
                        request.method=''
                        return timetable(request,tt)
                    T.Course=Course_obj
                link=request.POST['link']
                if link != '':
                    T.Link=link
                if request.POST.get('tut',''):
                    if request.POST['tut']=='yes':
                        T.isTutorial=1
                else:   
                    T.isTutorial=0;
                r_id=request.POST['rooms']
                Room_obj=Rooms.objects.filter(room_id=r_id)[0]
                T.Room=Room_obj
                if(c_id!='other'and T.Room.room_strength >= T.Course.students_strength) or c_id=='other':
                    chk=False
                    if c_id == 'other':
                        dt=int(request.POST['day'])
                        mn=int(request.POST['month'])
                        hr=int(request.POST['hour'])
                        mi=int(request.POST['minute'])
                        curr_date=datetime.datetime.now()
                        yr=curr_date.year
                        date_given=''
                        try:
                            date_given=datetime.datetime(yr,mn,dt,hr,mi)
                            if date_given < curr_date:
                                error= 'This date cannot be given'
                            if date_given.month == curr_date.month:
                                if abs(date_given.day - curr_date.day) < 1:
                                    error= "You have to atleast give tomorrow's date."
                        except:
                            error='Please check the date you have entered.'
                    if error == '':
                        temp=tt1.objects.filter(Cell=Cell_obj)
                        temp=temp.filter(approved=True)
                        #print "First"
                        #print tt
                        chk, error = chkCells(temp, T, tt, tt1, 'I')
                        fliptt=fliptt1.objects.all()
                        if chk == False:
                            if(isflip=='1'):
                                for t in fliptt:
                                    if t.Cell.slot > 6:
                                        t.Cell.slot = t.Cell.slot-6
                                    else:
                                        t.Cell.slot = t.Cell.slot+6
                            fliptt=fliptt.filter(Cell=Cell_obj)
                            chk, error = chkCells(fliptt, T, tt, fliptt1, 'I')
                            print chk
                        if chk == False:
                            temp=tt2.objects.filter(Cell=Cell_obj)
                            temp=temp.filter(approved=True)
                            chk, error = chkCells(temp, T, tt, tt2, 'II')
                        if chk == False:
                            temp=tt3.objects.filter(Cell=Cell_obj)
                            temp=temp.filter(approved=True)
                            chk, error = chkCells(temp, T, tt, tt3, 'III')
                        if chk == False:
                            temp=tt4.objects.filter(Cell=Cell_obj)
                            temp=temp.filter(approved=True)
                            chk, error = chkCells(temp, T, tt, tt4, 'IV')
                    if chk==False and error== '':
                        if c_id == 'other':
                            T.Date=date_given
                        if user.Username == 'admin':
                            T.save()
                        else:
                            T.approved=False
                            T.save()
                            if tt == tt1:
                                Request.objects.create(user=user, t1=T)
                            if tt == tt2:
                                Request.objects.create(user=user, t2=T)
                            if tt == tt3:
                                Request.objects.create(user=user, t3=T)
                            if tt == tt4:
                                Request.objects.create(user=user, t4=T)
                            r=Request.objects.filter(user=user)
                            return render(request, 'myrequests.html', {'user':user, 'req':r})

                else:
                    error='Room not sufficient.'
        else:
            isflip = request.POST.get('batch','0')
    #print tt
    tt, tt_name, yr, courses1, courses2 = get(tt)
    #print yr
    rooms=Rooms.objects.all()
    table=tt.objects.filter(approved=True)
    if(tt==tt1):
        fliptt=fliptt1.objects.all()
        if(isflip=='1'):
           # raise http404
            for t in fliptt:
                if t.Cell.slot > 6:
                    t.Cell.slot = t.Cell.slot-5
                else:
                    if(t.Cell.slot==5):
                        t.Cell.slot = t.Cell.slot-4
                    elif(t.Cell.slot==1):
                        t.Cell.slot=t.Cell.slot+4
                    else:
                        t.Cell.slot=t.Cell.slot+6
            tt=fliptt
            table=tt
    done1=[]
    done2=[]
    delDateObj(request)
    count1, count2 = assignedCourses(request, table, courses1, courses2)
    i=0
    for c in courses1:
        if ((c.lecture == count1[i][0]) and (c.tutorial == count1[i][1]) and (c.practical == count1[i][2])):
            done1.append("1")
        else:
            done1.append("0")
        i+=1
    i=0
    i=0
    for c in courses2:
        if ((c.lecture == count2[i][0]) and (c.tutorial == count2[i][1]) and (c.practical == count2[i][2])):
            done2.append("1")
        else:
            done2.append("0")
        i+=1
    options = getFilterData(table)
    batch=isflip
    return render(request, 'timetable.html',{'user':user, 'days':days,'slots':slots,'dates':dates,'months':months,'hours':hours,
        'minutes':minutes, 'rooms':rooms,'courses1':courses1,'courses2':courses2, 'table':table,'error':error,'T':T,
        'tt_name':tt_name,'yr':yr, 'count1':count1, 'count2':count2, 'done1':done1, 'done2':done2, 'options':options, 'batch':batch, 'isstud':isstud})

def getFilterData(table):
    f1=[]
    f2=[]
    f3=[]
    f4=[]
    for t in table:
        if t.Course is not None:
            if t.Course.course_id not in f4:
                f4.append(t.Course.course_id)
            if t.Room.room_id not in f3:
                f3.append(t.Room.room_id)
            if t.Course.Teaching.all()[0].Name not in f1:
                f1.append(t.Course.Teaching.all()[0].Name)
            if t.Course.course_id[2].isdigit() == False:
                if t.Course.course_id[0:3] not in f2:
                    f2.append(t.Course.course_id[0:3])
            else:
                if t.Course.course_id[0:2] not in f2:
                    f2.append(t.Course.course_id[0:2])

    options = {'Professor':f1, 'Branch':f2, 'Rooms':f3, 'Course':f4}
    return options

def chkCells(temp, T, tt, ttn, yr):
    chk = False
    error = ''
    max_strength = Strengths.objects.get(year=yr).students_strength
    if len(temp)>0:
        for i in range(len(temp)):
            #course_name[0:2] only
            if (temp[i].Room == T.Room or (temp[i].Course!= None and temp[i].Course.Teaching.all()[0] == T.Course.Teaching.all()[0]) or temp[i].Course.course_id[0:2]==T.Course.course_id[0:2]):
                chk=True
                error=temp[i]
            print "chk:"
            print chk
            if tt == ttn:
                if temp[i].Course is not None:
                    if temp[i].Course.students_strength == max_strength:
                        chk=True
                        error=temp[i]

    return chk, error

def filterTT(request,yr,batch=None,isstud=None):
    if 'user' not in request.session.keys():
        return render(request, 'index.html',{'msg':False})
    user=request.session['user']
    if yr == '1':
        tt = tt1.objects.all()
        tt, tt_name, yr, courses1, courses2=get(tt1)
    elif yr == '2':
        tt = tt2.objects.all()
        tt, tt_name, yr, courses1, courses2=get(tt2)
    elif yr == '3':
        tt = tt3.objects.all()
        tt, tt_name, yr, courses1, courses2=get(tt3)
    else:
        tt = tt4.objects.all()
        tt, tt_name, yr, courses1, courses2=get(tt4)
    table=tt.objects.all()
    tt=table
    filter_prof=[]
    filter_rooms=[]
    filter_course=[]
    filter_branch=[]
    s=""
    opts = getFilterData(table)
    if request.method == 'POST':
        for p in opts['Professor']:
            if request.POST.get(p, ''):
                filter_prof.append(p)
        for p in opts['Course']:
            if request.POST.get(p, ''):
                filter_course.append(p)
        for p in opts['Rooms']:
            if request.POST.get(p, ''):
                filter_rooms.append(p)
        for p in opts['Branch']:
            if request.POST.get(p, ''):
                filter_branch.append(p)

        filtered = []
        tt_f=''
        for c in filter_course:
            course=Courses.objects.get(course_id=c)
            filtered.append(Q(Course=course))
        for r in filter_rooms:
            room=Rooms.objects.get(room_id=r)
            filtered.append(Q(Room=room))
        for p in filter_prof:
            prof=Professor.objects.get(Name=p)
            for t in tt:
                if t.Course.Teaching.all()[0] == prof:
                    filtered.append(Q(Course=t.Course))
        for b in filter_branch:
            for t in tt:
                if b in t.Course.course_id:
                    filtered.append(Q(Course=t.Course))
        if len(filtered) > 0:
            query = filtered.pop()
            for q in filtered:
                query |= q
#            print query
            tt_f=tt.filter(query)
            
        if(batch=='1'):
                for t in tt_f:
                    if t.Cell.slot > 6:
                        t.Cell.slot = t.Cell.slot-5
                    else:
                        if(t.Cell.slot==5):
                            t.Cell.slot = t.Cell.slot-4
                        elif(t.Cell.slot==1):
                            t.Cell.slot=t.Cell.slot+4
                        else:
                            t.Cell.slot=t.Cell.slot+6
##        for t in tt_f:
##                s+=str(t.Cell.day)+"--"+str(t.Cell.slot)+"\n"
##        print s
##        return HttpResponse(s)
        options = getFilterData(table)
        """if len(q_r) > 0:
            query = q_r.pop()
            for q in q_r:
                query |= q
            tt_r=tt.filter(query)
            for t in tt_r:
                s+=str(t.Cell.day)+"--"+str(t.Cell.slot)+"\n"
        """
        return render(request, 'timetable.html',{'user':user, 'days':days,'slots':slots,'dates':dates,'months':months,'hours':hours,
            'minutes':minutes, 'rooms':rooms,'courses1':courses1,'courses2':courses2, 'table':tt_f,'error':error,'T':T,
            'tt_name':tt_name,'yr':yr, 'options':options, 'batch':batch, 'isstud':isstud})
    else:
        options = getFilterData(table)
        return render(request, 'timetable.html',{'user':user, 'days':days,'slots':slots,'dates':dates,'months':months,'hours':hours,
            'minutes':minutes, 'rooms':rooms,'courses1':courses1,'courses2':courses2, 'table':table,'error':error,'T':T,
            'tt_name':tt_name,'yr':yr, 'options':options, 'batch':batch, 'isstud':isstud})


def my_timetable(request):
    if 'user' not in request.session.keys():
        return render(request,'index.html',{'msg':False})
    days={1:'Monday',2:'Tuesday',3:'Wednesday',4:'Thursday',5:'Friday',6:'Saturday',7:'Sunday'}
    slots={1:'8:00-9:00',2:'9:00-10:00',3:'10:00-11:00',4:'11:00-12:00',5:'12:00-1:00',6:'1:00-2:00',7:'2:00-3:00',8:'3:00-4:00',9:'4:00-5:00',10:'5:00-6:00',11:'6:00-7:00',12:'7:00-8:00',13:'8:00-9:00',14:'9:00-10:00',15:'10:00-11:00',16:'11:00-12:00'}
    usernm=request.session['user']
    user=Professor.objects.get(Username=usernm)
    t1=tt1.objects.exclude(Course=None)
    t2=tt2.objects.exclude(Course=None)
    t3=tt3.objects.exclude(Course=None)
    t4=tt4.objects.exclude(Course=None)
    all_t=[]
    for c in t1:
        all_t.append(c)
    for c in t2:
        all_t.append(c)
    for c in t3:
        all_t.append(c)
    for c in t4:
        all_t.append(c)
    all_tt=[]
    for a in all_t:
        prof=a.Course.Teaching.all()[0]
        if prof.Username == usernm:
            all_tt.append(a)
    delDateObj(request)
    return render(request, 'timetable.html',{'user':user, 'days':days,'slots':slots,'table':all_tt})

def delDateObj(request):
    tt=[tt1,tt2,tt3,tt4]
    curr_date=datetime.datetime.now()
    #date_given=datetime.datetime(yr,mn,dt,hr,mi)
    for t in tt:
        objs = t.objects.all()
        for o in objs:
            date=o.Date
            if date is not None:
                i=date.index(' ')
                time=date[i+1:]
                date=date[0:i]
                dates=date.split('-')
                times=time.split(':')
                found_date=datetime.datetime(int(dates[0]),int(dates[1]),int(dates[2]),int(times[0]),int(times[1]))
                if found_date < curr_date:
                    o.delete()

def assignedCourses(request, tt, courses1, courses2):
    count1=[]
    count2=[]
    i=0
    for c in courses1:
        count1.append([0,0,0])
        for t in tt:
            if t.Course == c:
                if t.isTutorial == 1:
                    count1[i][1]+=1
                elif t.Room.isLab == True:
                    count1[i][2]+=1
                else:
                    count1[i][0]+=1
        i+=1
    i=0
    for c in courses2:
        count2.append([0,0,0])
        for t in tt:
            if t.Course == c:
                if t.isTutorial == 1:
                    count2[i][1]+=1
                elif t.Room.isLab == True:
                    count2[i][2]+=1
                else:
                    count2[i][0]+=1
        i+=1
    return count1, count2

def autogen(request,yr):
    if 'user' not in request.session.keys() or request.session['user'] != 'admin':
        return render(request,'index.html',{'msg':False})
    sem='odd'
    if request.POST.get('generate',''):
        clr(request,yr)
        sem=request.POST['sem']
        tt=tt1
        sem_match=""
        if sem == "odd":
            sem_match="I"
        else:
            sem_match="II"
        if yr == "2":
            tt=tt2
            if sem == "odd":
                sem_match="III"
            else:
                sem_match="IV"
        if yr == "3":
            tt=tt3
            if sem == "odd":
                sem_match="V"
            else:
                sem_match="VI"
        if yr == "4":
            tt=tt4
            if sem == "odd":
                sem_match="VII"
            else:
                sem_match="VIII"
        cells1=Cell.objects.filter(slot__lte=5)
        cells1=cells1.exclude(day='saturday').exclude(day='sunday')
        cells2=Cell.objects.filter(slot=7)
        cells2=cells2.exclude(day='saturday').exclude(day='sunday')
        cells3=Cell.objects.filter(slot__lte=9)
        cells3=cells3.exclude(day='saturday').exclude(day='sunday')
        cells3=cells3.exclude(slot=6)
        #out=""
        #for c in cells2:
        #    out+=c.day+str(c.slot)+"\n"
        #return HttpResponse(out)
        courses1=Courses.objects.filter(semester=sem_match)
        courses1=courses1.exclude(Teaching=None)
        courses1=courses1.order_by("-students_strength")
        courses2=courses1.exclude(practical=0)
        courses3=courses1.exclude(tutorial=0)
        #out=""
        #for c in courses2:
        #    out+=c.course_id+" \n"
        #return HttpResponse(out)
        assign_prac(tt,cells2,courses2)
        assign(tt,cells1,courses1,'L')
        #assign(tt,cells3,courses3,'T')
        #cells1=Cell.objects.filter(slot__lte=9)
        #cells1=cells1.exclude(slot=6)
        #cells1=cells1.exclude(day='saturday').exclude(day='sunday')
        request.method=''
        return timetable(request,tt)
    else:
        username=request.session['user']
        User=Professor.objects.filter(Username=username)[0]
        return render(request,'welcome.html',{'user':User, 'message':''})

def get_others(a,b,c,d,cell):
    others=[]
    o1=a.objects.filter(Cell=cell)
    o2=b.objects.filter(Cell=cell)
    o3=c.objects.filter(Cell=cell)
    o4=d.objects.filter(Cell=cell)
    if len(o1)!=0:
        for o in o1:
            others.append(o)
    if len(o2)!=0:
        for o in o2:
            others.append(o)
    if len(o3)!=0:
        for o in o3:
            others.append(o)
    if len(o4)!=0:
        for o in o4:
            others.append(o)
    return others

#def assign_tut(tt,cells,courses):
#    for c in courses:
#        i=1
#        while(True):
#            i+=1
#            if(i>50):
#                break
#            cell=random.choice(cells)
#            rooms=Rooms.objects.all()
#            rooms=rooms.filter(room_strength__gte=c.students_strength)
#            rooms=rooms.exclude(isLab=1)


def assign_prac(tt,cells,courses):
    for c in courses:
        i=1
        checkin=0
        while(True):
            i+=1
            if(i>50):
                break
            cell=random.choice(cells)
            rooms=Rooms.objects.filter(isLab=1).filter(lab_type=c.course_id[0:2])
            room=random.choice(rooms)
            others=get_others(tt1,tt2,tt3,tt4,cell)
            change_room=False
            prof_busy=False
            if len(others)!=0:
                for o in others:
                    if o.Room.room_id==room.room_id:
                        change_room=True
                        break
                    o_prof=o.Course.Teaching.all()[0]
                    my_prof=c.Teaching.all()[0]
                    if my_prof.Email == o_prof.Email:
                        prof_busy=True
                        break
            if change_room==False and prof_busy==False:
                flag=False
                total=0
                if tt==tt1:
                    total=Strengths.objects.get(year='I').students_strength
                if tt==tt2:
                    total=Strengths.objects.get(year='II').students_strength
                if tt==tt3:
                    total=Strengths.objects.get(year='III').students_strength
                if tt==tt4:
                    total=Strengths.objects.get(year='IV').students_strength
                T_temp=tt.objects.filter(Cell=cell)
                if len(T_temp)!=0:
                    for t_c in T_temp:
                        c_id=t_c.Course.course_id
                        c_id=c_id[0:2]
                        if c_id==c.course_id[0:2]:
                            flag=True
                            break
                if flag==False:
                    d=cell.day
                    s=cell.slot
                    for i in range(c.practical):
                        T=tt()
                        cell=Cell.objects.get(day=d,slot=(s+i))
                        T.Cell=cell
                        T.Course=c
                        T.Room=room
                        T.isTutorial=0
                        T.save()
                    my_ss=c.students_strength
                    diff_allowed=int(my_ss*0.1)
                    if abs(c.students_strength-total)<diff_allowed:
                        checkin+=1
                        if checkin==3:
                            break
                        else:
                            continue
                    break

                else:
                    continue




def assign(tt,cells,courses,arg):
    for c in courses:
        if arg=='L':
            n=c.lecture
        else:
            n=c.tutorial
        for i in range(n):
            count=0
            while(True):
                count+=1
                if count>50:
                    break
                cell=random.choice(cells)
                #if(tt == tt1 and cell.slot == 1):
                #    continue
                cell_test=tt.objects.all()
                chnge=False
                for c_t in cell_test:
                    test_cell=c_t.Cell
                    today=test_cell.day
                    if today==cell.day and c_t.Course.course_id==c.course_id and c_t.Room.isLab==False:
                        chnge=True
                        break
                if chnge==True:
                    continue
                rooms=Rooms.objects.filter(isLab=False)
                rooms=rooms.filter(room_strength__gte=c.students_strength)
                s=cell.slot
                d=cell.day
                s=s-1
                t=s+1
                room=random.choice(rooms)
                chk_tt_cell=tt.objects.filter(Course=c)
                if len(chk_tt_cell)!=0 and chk_tt_cell[0].Room.isLab==False:
                    room=chk_tt_cell[0].Room
                elif s>0:
                    #return HttpResponse(d+str(s))
                    prev_cell=cells.filter(slot=s,day=d)[0]
                    tt_cell=tt.objects.filter(Cell=prev_cell)
                    if len(tt_cell)!=0:
                        for t_c in tt_cell:
                            c_id=t_c.Course.course_id
                            c_id=c_id[0:2]
                            if c_id==c.course_id[0:2]:
                                room=t_c.Room
                                break
                elif t>1 and t<=5:
                    next_cell=cells.filter(slot=t,day=d)[0]
                    tt_cell=tt.objects.filter(Cell=next_cell)
                    if len(tt_cell)!=0:
                        for t_c in tt_cell:
                            c_id=t_c.Course.course_id
                            c_id=c_id[0:2]
                            if c_id==c.course_id:
                                room=t_c.Room
                                break
                else:
                    min_s=c.students_strength
                    min_r=random.choice(rooms)
                    for i in range(2*len(rooms)):
                        room=random.choice(rooms)
                        diff=room.room_strength-c.students_strength
                        if diff<0:
                            continue;
                        else:
                            if diff < min_s:
                                min_s=diff
                                min_r=room
                    room=min_r
                others=get_others(tt1,tt2,tt3,tt4,cell)
                change_room=False
                prof_busy=False
                if len(others)!=0:
                    for o in others:
                        if o.Room.room_id==room.room_id:
                            change_room=True
                            break
                        o_prof=o.Course.Teaching.all()[0]
                        my_prof=c.Teaching.all()[0]
                        if my_prof.Email == o_prof.Email:
                            prof_busy=True
                            break
                if change_room==False and prof_busy==False:
                    flag=False
                    """T_temp=tt.objects.filter(Room=room)
                    if len(T_temp)!=0:
                        for t in T_temp:
                            if t.Course.course_id!=c.course_id:
                                flag=True
                                break"""
                    T_temp=tt.objects.filter(Cell=cell)
                    if len(T_temp)!=0:
                        for t_c in T_temp:
                            c_id=t_c.Course.course_id
                            c_id=c_id[0:2]
                            if c_id==c.course_id[0:2]:
                                flag=True
                                break
                            c_ss=t_c.Course.students_strength
                            my_ss=c.students_strength
                            diff_allowed=int(c_ss*0.1)
                            if abs(c_ss-my_ss)>diff_allowed:
                                flag=True
                                break
                            if tt==tt1:
                                total=Strengths.objects.get(year='I').students_strength
                            if tt==tt2:
                                total=Strengths.objects.get(year='II').students_strength
                            if tt==tt3:
                                total=Strengths.objects.get(year='III').students_strength
                            if tt==tt4:
                                total=Strengths.objects.get(year='IV').students_strength
                            if c_ss==total or my_ss==total:
                                flag=True
                                break
                    if flag==False:
                        T=tt()
                        T.Cell=cell
                        T.Course=c
                        T.Room=room
                        if arg=='T':
                            T.isTutorial=1
                        else:
                            T.isTutorial=0
                        T.save()
                        break
                    else:
                        continue
                #if change_room==True and prof_busy==False


def clr(request, yr):
    if yr == '1':
        t=tt1.objects.all()
        t.delete()
        tt=tt1
    if yr == '2':
        t=tt2.objects.all()
        t.delete()
        tt=tt2
    if yr == '3':
        t=tt3.objects.all()
        t.delete()
        tt=tt3
    if yr == '4':
        t=tt4.objects.all()
        t.delete()
        tt=tt4
    request.method=''
    return timetable(request,tt)

def gen_usrnm(request):
    import hashlib
    profs=Professor.objects.all()
    for p in profs:
        fn=p.Name.split(" ")[0].lower()
        br=p.Department.lower()
        p.Username=fn+"."+br
        psw=hashlib.sha1('root').hexdigest()
        p.Password=psw
        p.save()
    return HttpResponse("Sucess")
