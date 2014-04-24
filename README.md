Central Information System
==========================

Central Information System(CIS) is an online timetable system for managing the
day-to-day academic and non-academic activities.

What is CIS
-----------

More specifically to design and develop a simple and intuitive system
which shall cater to the needs of the institute. The system shall provide
features to the user of the institute to stay connected to the college
activities at all times and also be able to make/request changes.
Using this anyone can know about any activities going in any part of the
campus from anywhere and all he needs is an internet connection. The interface
of the software is easy to use and self-explanatory.

Features
--------

CIS comes with lot of functional as well as UI features to make user experience
not only good but better. The software aims to provide lots of functionalities
and use cases keeping in mind that the complexity user has to face is kept
minimum. CIS is focused to provide the users all of the functionalities along 
with better UX.

With **CIS** you can:

- Manage Rooms: Add/Remove
- Manage Professor: Add/Edit/Remove
- Manage Courses: Add/Edit/Remove
- Manage Timetable: Create/Edit/Autogenerate/Filter/Clear
- Make Appointments
- Make Requests


To run and use this software, one needs to install **Python** and **Django** and then
run *manage.py*.

You have to add users and student strength. Admin will have username `admin`.
Rest everything can be done after being logged in as admin.

There is also cell initial data that needs to be added in the database. Its given
in `cell.txt`, you need to add it for all days in the Cell table that is formed in the
database after syncdb.
It is being worked upon that this happens by default, but its not implemented yet.
After doing the above, do the following:

For Windows:
- Open cmd
- Navigate to the cis folder.
- python manage.py syncdb.
- python manage.py runserver [port_number].
- Open the 127.0.0.1:port/cis/home in browser.

For Unix:
- Open Terminal
- Navigate to the cis folder.
- ./manage.py syncdb.
- ./manage.py runserver [port_number].
- Open the 127.0.0.1:port/cis/home in browser.

Also the *settings.py* has to be added accordingly, since this has not been deployed
yet and is meant for local use.