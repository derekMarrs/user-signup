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
import cgi
import os
import re

# html boilerplate for the top of every page
page_header = """
<!DOCTYPE html>
<html>
<head>
    <title>Signup</title>
    <style type="text/css">
        .error {
            color: red;
        }
    </style>
</head>
<body>
"""

signup_header = "<h1>Signup</h1>"

signup_form = """
<form method="post">
    <table>
        <tr>
            <td><label for="username">Username</label></td>
            <td>
                <input name="username" type="text" value="%(entered_username)s" required>
                <td class="error">%(username)s</td>
            </td>
        </tr>
        <tr>
            <td><label for="password">Password</label></td>
            <td>
                <input name="password" type="password" required>
                <td class="error">%(password)s</td>
            </td>
        </tr>
        <tr>
            <td><label for="verify">Verify Password</label></td>
            <td>
                <input name="verify" type="password" required>
                <td class="error">%(verify)s</td>
            </td>
        </tr>
        <tr>
            <td><label for="email">Email (optional)</label></td>
            <td>
                <input name="email" type="email" value="%(entered_email)s">
                <td class="error">%(email)s</td>
            </td>
        </tr>
    </table>
    <input type="submit">
</form>
"""

# html boilerplate for the bottom of every page
page_footer = """
</body>
</html>
"""

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return username and USER_RE.match(username)

PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
    return password and PASS_RE.match(password)

EMAIL_RE  = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
def valid_email(email):
    return not email or EMAIL_RE.match(email)

class Signup(webapp2.RequestHandler):

    #def write_form(self, error_username="", error_password="", error_verify="", error_email=""):
        #self.response.out.write(page_header + signup_header + signup_form % {"username": error_username, "password": error_password, "verify": error_verify, "email": error_email} + page_footer)

    def get(self, error_username= "", error_password = "", error_verify = "", error_email = "", username = "", email = ""):
        self.response.out.write(page_header + signup_header + signup_form % {"username": error_username, "password": error_password, "verify": error_verify, "email": error_email, "entered_username": username, "entered_email": email} + page_footer)

    #def get(self):
        #self.write_form()

    def post(self):

        have_error = False
        username = self.request.get('username')
        password = self.request.get('password')
        verify = self.request.get('verify')
        email = self.request.get('email')

        params = dict(username = username,
                      email = email)

        error_username = ""
        error_password = ""
        error_verify = ""
        error_email = ""

        error = {"username": error_username, "password": error_password, "email": error_email, "verify": error_verify, "entered_username": username, "entered_email": email}

        if not valid_username(username):
            error['username'] = "That's not a valid username."
            have_error = True

        if not valid_password(password):
            error['password'] = "That wasn't a valid password."
            have_error = True
        elif password != verify:
            error['verify'] = "Your passwords didn't match."
            have_error = True

        if not valid_email(email):
            error['email'] = "That's not a valid email."
            have_error = True

        if have_error:



            content = page_header + signup_header + signup_form % error + page_footer
            self.response.write(content)
        else:
            self.redirect('/welcome?username=' + username)



class Welcome(webapp2.RequestHandler):
    def get(self):
        username = self.request.get("username")
        if valid_username(username) == False:
            self.redirect('/')

        welcome_message = "Welcome, " + username + "!"
        content = page_header + "<h1>" + welcome_message + "</h1>" + page_footer
        self.response.write(content)


app = webapp2.WSGIApplication([
    ('/', Signup),
    ('/welcome', Welcome)
], debug=True)
