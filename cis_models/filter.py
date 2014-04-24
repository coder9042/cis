from django.shortcuts import render
from django.http import HttpResponse
from cis_models.models import *
from django.db.models import Q
import random, datetime
#from timetable import *


course1=[]
course2=[]
days={}
slots={}
dates=range(1,32)
months=[]
hours=range(1,24)
minutes=range(0,60,5)
rooms=[]
days={1:'Monday',2:'Tuesday',3:'Wednesday',4:'Thursday',5:'Friday',6:'Saturday',7:'Sunday'}
slots={1:'8:00-9:00',2:'9:00-10:00',3:'10:00-11:00',4:'11:00-12:00',5:'12:00-1:00',6:'1:00-2:00',7:'2:00-3:00',8:'3:00-4:00',9:'4:00-5:00',10:'5:00-6:00',11:'6:00-7:00',12:'7:00-8:00',13:'8:00-9:00',14:'9:00-10:00',15:'10:00-11:00',16:'11:00-12:00'}
dates=range(1,32)
months=[]
curr=datetime.datetime.now()
months.append(curr.month)
months.append(curr.month +1)
hours=range(1,24)
minutes=range(0,60,5)
error=''
T=''
tt_name=''
courses=Courses.objects.filter(Q(semester='I') | Q(semester='II'))
courses1=courses.filter(semester='I')
courses2=courses.filter(semester='II')

def get(tt):
    from django.http import Http404
    if tt == tt1:
        courses=Courses.objects.filter(Q(semester='I') | Q(semester='II'))
        courses1=courses.filter(semester='I')
        courses2=courses.filter(semester='II')
        tt_name='tt1'
        yr=1
            
    if tt == tt2:
        courses=Courses.objects.filter(Q(semester='III') | Q(semester='IV'))
        courses1=courses.filter(semester='III')
        courses2=courses.filter(semester='IV')
        tt_name='tt2'
        yr=2
    if tt == tt3:
        courses=Courses.objects.filter(Q(semester='V') | Q(semester='VI'))
        courses1=courses.filter(semester='V')
        courses2=courses.filter(semester='VI')
        tt_name='tt3'
        yr=3
    if tt == tt4:
        courses=Courses.objects.filter(Q(semester='VII') | Q(semester='VIII'))
        courses1=courses.filter(semester='VII')
        courses2=courses.filter(semester='VIII')
        tt_name='tt4'
        yr=4
    courses1=courses1.exclude(Teaching=None)
    courses2=courses2.exclude(Teaching=None)
    courses1=courses1.order_by('course_id')
    courses2=courses2.order_by('course_id')
    return tt, tt_name, yr, courses1, courses2
rooms=Rooms.objects.all()
done1=[]
done2=[]

