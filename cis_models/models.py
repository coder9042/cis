from django.db import models

class Strengths(models.Model):
    year=models.CharField(max_length=5)
    students_strength=models.IntegerField(max_length=11)

class Professor(models.Model):
    Name=models.CharField(max_length=60)
    Designation=models.CharField(max_length=60)
    Department=models.CharField(max_length=60)
    Email=models.CharField(max_length=60, unique=True)
    PhoneExtension=models.IntegerField(max_length=60, unique=True)
    Username=models.CharField(max_length=60, blank=True, null=True)
    Password=models.CharField(max_length=60, blank=True, null=True)
    Last_Login=models.CharField(max_length=60, blank=True, null=True)

class Students(models.Model):
    Username=models.CharField(max_length=60, blank=True, null=True)
    Password=models.CharField(max_length=60, blank=True, null=True)
    Email=models.CharField(max_length=60, unique=True)
    Department=models.CharField(max_length=3)
    Last_Login=models.CharField(max_length=60, blank=True, null=True)

class Courses(models.Model):
    course_id=models.CharField(max_length=30, unique=True)
    course_name=models.CharField(max_length=60)
    lecture=models.IntegerField(max_length=11)
    tutorial=models.IntegerField(max_length=11)
    practical=models.IntegerField(max_length=11)
    credit=models.IntegerField(max_length=11)
    semester=models.CharField(max_length=30)
    elective_group_number=models.IntegerField(max_length=11)
    students_strength=models.IntegerField(max_length=11)
    branch_number=models.IntegerField(max_length=11)
    Teaching=models.ManyToManyField(Professor)
    time_added=models.CharField(max_length=60)


class Rooms(models.Model):
    room_id=models.CharField(max_length=60, unique=True)
    room_strength=models.IntegerField(max_length=11)
    projector=models.IntegerField(max_length=11)
    conference=models.IntegerField(max_length=11)
    isLab=models.BooleanField()
    lab_type=models.CharField(max_length=2)
    time_added=models.CharField(max_length=60)

class Cell(models.Model):
    slot=models.IntegerField(max_length=60)
    day=models.CharField(max_length=60)

class tt1(models.Model):
    Cell=models.ForeignKey(Cell)
    Course=models.ForeignKey(Courses, null=True, blank=True)
    isTutorial=models.IntegerField(max_length=1,null=True,blank=True)
    Room=models.ForeignKey(Rooms)
    Extra=models.CharField(max_length=60, null=True, blank=True)
    Link=models.URLField(max_length=100 , null=True, blank=True)
    Date=models.CharField(max_length=100, null=True, blank=True)
    approved=models.BooleanField(default=True)

class fliptt1(tt1):
    class Meta:
        proxy = True

class tt2(models.Model):
    Cell=models.ForeignKey(Cell)
    Course=models.ForeignKey(Courses, null=True, blank=True)
    isTutorial=models.IntegerField(max_length=1,null=True,blank=True)
    Room=models.ForeignKey(Rooms)
    Extra=models.CharField(max_length=60, null=True, blank=True)
    Link=models.URLField(max_length=100 , null=True, blank=True)
    Date=models.CharField(max_length=100, null=True, blank=True)
    approved=models.BooleanField(default=True)

class tt3(models.Model):
    Cell=models.ForeignKey(Cell)
    Course=models.ForeignKey(Courses, null=True, blank=True)
    isTutorial=models.IntegerField(max_length=1,null=True,blank=True)
    Room=models.ForeignKey(Rooms)
    Extra=models.CharField(max_length=60, null=True, blank=True)
    Link=models.URLField(max_length=100 , null=True, blank=True)
    Date=models.CharField(max_length=100, null=True, blank=True)
    approved=models.BooleanField(default=True)

class tt4(models.Model):
    Cell=models.ForeignKey(Cell)
    Course=models.ForeignKey(Courses, null=True, blank=True)
    isTutorial=models.IntegerField(max_length=1,null=True,blank=True)
    Room=models.ForeignKey(Rooms)
    Extra=models.CharField(max_length=60, null=True, blank=True)
    Link=models.URLField(max_length=100 , null=True, blank=True)
    Date=models.CharField(max_length=100, null=True, blank=True)
    approved=models.BooleanField(default=True)

class resetTable(models.Model):
    prof=models.ForeignKey(Professor, blank=True, null=True)
    stud=models.ForeignKey(Students, blank=True, null=True)
    hex_code=models.CharField(max_length=100)
    c=models.CharField(max_length=100)

class Request(models.Model):
    user=models.ForeignKey(Professor)
    t1=models.ForeignKey(tt1, null=True, default=None)
    t2=models.ForeignKey(tt2, null=True, default=None)
    t3=models.ForeignKey(tt3, null=True, default=None)
    t4=models.ForeignKey(tt4, null=True, default=None)

class appointment(models.Model):
    professor=models.ForeignKey(Professor)
    student=models.ForeignKey(Students)
    confirmed=models.IntegerField()
    Month=models.IntegerField()
    Day=models.IntegerField()
    Hour=models.IntegerField()
    Minute=models.IntegerField()