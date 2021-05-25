from google.appengine.ext import ndb
class MyUser(ndb.Model):
    # email address of this User
    email_address=ndb.StringProperty()
