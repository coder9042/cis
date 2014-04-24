"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from cis_models.models import *
from django.test import Client

class myTest(TestCase):
    def setUp(self):
        Professor.objects.create(Name="ANUBHAV JOSHI",Designation="Student",Department="CSE",Email="anubhav.cs12@iitp.ac.in",PhoneExtension="0000",Username="admin",Password="root")
    def test_login(self):
        c=Client()
        r=c.post('/cis/login/',{'username':'admin','pass':'root'})
        #self.assertEqual(r.Context['msg'],'Wrong Username or Password')
    
