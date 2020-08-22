# PAIRED

Welcome to PAIRED! This study partner matching web application allows students to connect with other students and schedule work sessions. As many universities and schools transition to remote learning in the fall term, we wanted to create a platform that helps students study together.

## Getting Started

This web application was made with the CS50 IDE and written in Python, SQL, HTML, CSS, and JavaScript. After running Flask in the IDE, users are taken to the Paired website, where our five-table SQL database stores information on users' account data, personal information, availablility, and current enrolled courses.

## Using PAIRED

New users start by registering a new account under "REGISTER." After filling in a unique username, password, and confirming the password, users are then taken to the "LOG IN" page, where they log in with their new account. If the account is a new registration, the user will be redirected to fill in additional information like first and last name, email, graduation year, and house. These values are immediately added to the user_info table.

The user is directed to a personalized dashboard, where they are shown their personal information. Additional functionality includes adding and deleting courses and changing availability. Users can add at least one course to their dashboard by selecting the course department from the dropdown menu (i.e. Computer Science, Spanish, GenEd, etc.), typing in their course number (i.e. 50, S-AA, 1100), and adding any optional notes (i.e., section leader: Jane Doe, drill practice at 3 pm on Thursdays, class name: The Two Koreas).

"View availabilities" allows users to log the times and days of the week during which they're available to study. Similar to the popular scheduling web application "When2Meet," our interface allows users to click and drag to select half-hour slots, from 8AM to 12aM EST. Any saved changes are logged in the availabilities table. After pressing save, you will be redirected to your dashboard.

After adding courses and indicating availabilities, the user can "view partners, which will lead them to a dropdown menu. They can select any one of their courses and press "see matches," which will return a table of student names, years, and times, as well as a hyperlink to their email. If no other students are registered within the system to take the course, the program will return "no mutual availabilities at this time."

At any point, users may click "ABOUT" to learn more about us, or click our logo in the top left corner to go to the Homepage.

## A Tour of Our Directory

At the outset, our directory has three folders and six files:
- [FOLDER] static: image files and our CSS file.
- [FOLDER] templates: all of our html templates.
- [FOLDER] testing: Python files used to test code, unrelated to the implementation of the web application.
- application.py: Python file where we implemented various app routes to direct commands requesting access to different html pages. Depending on the html page summoned, "application.py" will return the page as well as different types of information stored from our SQL database.
- helpers.py: Python file where we implemented custom functions to help run "application.py" run more smoothly.
- database.db: our SQL database where we've stored our five tables.
- DESIGN.md: a markdown file detailing the design of our web app.
- README.md: a markdown file introducing our web app.

## Things to Improve

We plan to take this project beyond CS50 and host it for students to use during remote semesters. Before we launch, however, we need to edit the following things:
- make the availability tool functional
- condense the partners page to present one row per person and build the application to recognize consecutive time slots
- ask for gender pronouns from the user
- implement a favicon
- allow filters for the partners page (by class year, house, etc.)
- allow former students who have already taken class to be available for connecting with as well (alumni subsystem)
- streamline the partner matching table to eliminate redundant names

## Screenshots

<p align="center">

<img src="/static/home" alt="home"/>
<img src="/static/login" alt="login"/>
<img src="/static/dashboard" alt="dashboard"/>
<img src="/static/edit" alt="edit"/>
<img src="/static/partners" alt="partners"/>
<img src="/static/availability" alt="availability"/>

</p>