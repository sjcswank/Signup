#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import re
import cgi

# html boilerplate for the top of every page
page_header = """
<!DOCTYPE html>
<html>
<head>
    <title>Sign Up</title>
    <style type="text/css">
        .name_error {
            color: red;
        }

    </style>
</head>
<body>
    <h1>
        <a href="/">Sign Up</a>
    </h1>
"""

#form

form = """
<form method="post">
    <label>Username:
    <input type="text" name="username" min="4" max="20" value="%(username)s" required/>%(name_error_element)s</label>
    <br>
    <label>Password:
    <input type="password" name="password" min="8" max="20" required/>%(pass_error_element)s</label>
    <br>
    <label>Verify Password:
    <input type="password" name="verify" min="8" max="20" required/>%(ver_error_element)s</label>
    <br>
    <label>Email (optional):
    <input type="email" name="email" value="%(email)s"/>%(email_error_element)s</label>
    <br>
    <input type="submit" value="Sign Up"></input>
</form>
"""

# html boilerplate for the bottom of every page
page_footer = """
</body>
</html>
"""



#valid username 3-20 characters, letters, nums, underscore
USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return USER_RE.match(username)

#valid password 3-20 characters
PASS_RE = re.compile(r"^.{3,20}$")
def valid_pass(password):
    return PASS_RE.match(password)

#verified password, password and verify match
def pass_match(password, verify):
    return password == verify

#valid email alph+@+alpha+.+alpha
EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")
def valid_email(email):
    return not email or EMAIL_RE.match(email)

def escape_html(text):
    return cgi.escape(text, quote=True)



class MainHandler(webapp2.RequestHandler):
    def write_page(self, username="", name_error_element="", pass_error_element="", ver_error_element="", email="", email_error_element=""):
        response = page_header + form + page_footer
        self.response.out.write(response % {"username": escape_html(username),
                                            "name_error_element": name_error_element,
                                            "pass_error_element": pass_error_element,
                                            "ver_error_element": ver_error_element,
                                            "email": escape_html(email),
                                            "email_error_element": email_error_element})

    def get(self):

        nameError = self.request.get("name_error")
        name_error_element = "<p class='error'>" + name_error + "</p>" if nameError else ""

        passError = self.request.get("pass_error")
        pass_error_element = "<p class='error'>" + passError + "</p>" if passError else ""

        verError = self.request.get("ver_error")
        ver_error_element = "<p class='error'>" + verError + "</p>" if verError else ""

        emailError = self.request.get("email_error")
        email_error_element = "<p class='error'>" + emailError + "</p>" if emailError else ""

        self.write_page()



    def post(self):

        ver_username = self.request.get("username")
        if not valid_username(ver_username):
            name_error = "That is not a valid username."
        else:
            name_error = ""

        ver_password = self.request.get("password")
        if not valid_pass(ver_password):
            pass_error = "That is not a valid password."
        else:
            pass_error = ""

        ver_verify = self.request.get("verify")
        if not pass_match(ver_password, ver_verify):
            ver_error = "Passwords do not match."
        else:
            ver_error = ""

        ver_email = self.request.get("email")
        if not valid_email(ver_email):
            email_error = "That is not a valid email address."
        else:
            email_error = ""



        if (valid_username(ver_username) and valid_pass(ver_password) and pass_match(ver_password, ver_verify) and valid_email(ver_email)):
            self.redirect('/thanks?username=' + ver_username)
        else:
            self.write_page(ver_username, name_error, pass_error, ver_error, ver_email, email_error)


class Thanks(webapp2.RequestHandler):

    def get(self):
        username = self.request.get("username")

        welcome_element = """
        <h3>Welcome, %(username)s!</h3>
        <br>
        <p>Thank You for registering! Enjoy!</p>
        """

        response = page_header + welcome_element + page_footer
        self.response.out.write(response % {"username": escape_html(username)})




app = webapp2.WSGIApplication([
    ('/', MainHandler), ('/thanks', Thanks)
], debug=True)
