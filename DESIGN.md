# PAIRED Design

## Beginning Ideas

This website was inspired by a comment on a post from Facebook group "Overheard At Harvard." In this group, where Harvard students can post humorous and often out-of-context statements said by their classmates, one comment under an academics-related post during quarantine read something along the lines of "someone should make a pset partner finding app for their cs50 project." Austin, Diana and I all had varying degrees of comfort with using different languages, so we put our skills together to create a dynamic web application that could help our fellow classmates at Harvard with online learning this fall.

## Back-End

### SQL and Javascript

The first few stages of development consisted of implementing an effective database system. To achieve functionality, we set up five tables:
- users: unique id numbers for users (id), usernames (username), and password hashes (hash) make up the structure used to identify user sessions.
- user_info: users.id, first (first) and last (last) names, email addresses (email), graduating class year (year), and house or dorm (house) all allow users to save profile details when interacting with other users.
- courses: users.id, course department or subject (dept), course number (number), and an optional "notes to self" column (addinfo) make up information on the courses users want to be paired for.
- availability: users.id and unique id numbers for timeslots (slot_id) make up the table that saves information on when users are available to study together with potential partners.
- times: availability.slot_id and actual timeslots (time) make up a static table that connects a slot's id to a day and a half-hour (there are 224 slots — one for every half-hour from 8:00 am EST to 12:00 am EST).

The "users" table, through the "register.html" and "deactivate.html" files, allow the web app
to create and delete users. The "courses" table, through the "add.html" and "delete.html" files,
allow the web app to create and delete courses for each user. Both were implemented fairly easily
with simple Python and Flask elements.

The "availabilities" table was by far the most difficult to implement, and we still have errors with it. Using JS, we made an 8x32-cell table responsive to the dragging feature found in the popular scheduling web app "When2Meet." We played around with fetch() and $.ajax to send the
information of a user's individual availabilities, which were indicated by shading in cells on the table, to Flask. We have assigned each <td> in the table to a unique id, which corresponds to its slot_id in the "times" table in database.db. We theniterated through each of the id values,
checking to see whether the cell's background has been shaded to green. If it is, the id will be appended via push() to an initially empty array called availability[] and then sent via fetch() POST option to the /availability route in Flask. This is where we stumbled into some errors with
appending the ids. For now, we have manually inserted into the "times" table a few availabilities for each user so that the partner matching demo is functional, but we seek to repair the "availabilities.html" and /availabilities route so that users can repeatedly fill out and update their
availability in the table and have the SQL table be updated accordingly.

### Python and Flask

In the "application.py" file, the app routes implemented are detailed as follows:
- /login: [GET] quits current user's session, allows new user to log in; [POST] receives account information and checks with the "users" table to see if the user should be let into the rest of the web application.
- /logout: quits current user's session and returns the user to the home page.
- /register: [GET] allows new user to make an account; [POST] checks if inputted information is new to the "users" table and inserts into it.
- /index: returns the user to the home page.
- /about: returns the user to the about page.
- /dashboard: collects the following information and sends it to the dashboard page: current session's user's unique id, their first and last names, their email address, their graduating class year, their house or dorm, and their courses
- /edit: [GET] allows the user to edit personal information; [POST] collects and saves the following information (after checking for uniqueness) into the "user_info" table: current session user's first and last names, their email address, their graduating class year, their house or dorm, and their courses.
- /availability:
- /add:
- /delete:
- /partners:
- /deactivate:
- /password:

In the "helpers.py" file, the custom functions* implemented are:
- apology(): posts error messages in the form of modifications of the "apology.html" file.
- login_required(): checks if a user has logged into their account in order to grant access to certain HTML pages. Of the HTML pages, only "about.html", "login.html", "register.html", and "index.html" are accessible without this function being called prior to establishing an app route.
*Both were sourced from Problem Set 9 earlier in CS50's course.

## Front-End

### HTML, CSS, and UI/UX

For a tree view of all our functional pages and their accessibility, see below:
- home
- about
- register
    - edit
        - dashboard
            - see below
- log in
    - about
    - dashboard
        - edit
            - (change) password
            - deactivate (account)
        - availability
        - partners
            - pairs
        - add (course)
        - delete (course)
    - log out

Every page named after a verb or action, when successfully carried out, redirects to the dashboard.
Our apology pages (error warnings) all provide a back button to return the previous page in the user's history.

Our home page has an animated feature of having the header be individually typed out, thanks to a special CSS class design sourced from Creative Block's implementation. We also used Bootstrap for a variety of features in our forms and buttons, particularly the "required" feature for input tags in HTML that allowed us to save save in "application.py" and only implement the apology() function when necessary.

Our "layout.html" and "styles.css" files allow us to maintain a consistent user interface throughout the entire web application: namely, a beige and seafoam color palette, the Abril Fatface accent font, clean white tables, and more stylistic design choices that follow current trends in UI today.

As for the UX, we missed the chance to implement elements like gender pronouns, a questionnaire-style form that collects information on what kind of student/learner a user is for more efficient partner matching, and capacities for former students who have already taken some courses to interact with current students and give advice (like an alumni subsystem).