import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
from create import Create
import os
from myuser import MyUser
from eleveh import ELEVEH
from information import Information
from compare import Compare
import math

JINJA_ENVIRONMENT = jinja2.Environment(
loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
extensions=['jinja2.ext.autoescape'],
autoescape=True
)

class MainPage(webapp2.RequestHandler):
    def get(self):

        self.response.headers['Content-type']='text/html'
        url=''
        url_string=''
        ele = None
        user=users.get_current_user()
        myuser=None

        if user:
            url=users.create_logout_url(self.request.uri)
            url_string='logout'

            myuser_key=ndb.Key('MyUser',user.email())
            myuser=myuser_key.get()
            if myuser == None:
                myuser= MyUser(id=user.email(),email_address=user.email())
                myuser.put()
        else:
            url= users.create_login_url(self.request.uri)
            url_string= 'login'

        button = self.request.get('button')
        if button == 'Query ev':
            year = 0
            name= self.request.get('name').strip()
            manufacturer = self.request.get('manufacturer').strip()
            minyear = self.request.get('minyear').strip()
            minbatterySize=self.request.get('minbatterySize').strip()
            minWLTPRange=self.request.get('minWLTPRange').strip()
            mincost=self.request.get('mincost').strip()
            minpower=self.request.get('minpower').strip()
            maxyear = self.request.get('maxyear').strip()
            maxbatterySize=self.request.get('maxbatterySize').strip()
            maxWLTPRange=self.request.get('maxWLTPRange').strip()
            maxcost=self.request.get('maxcost').strip()
            maxpower=self.request.get('maxpower').strip()

            ele = ELEVEH.query()
            ele2 = ele
            ele3 = ELEVEH.query().fetch(keys_only=True)
            i = 0
            z = 0

            if name != '':
                i=1
                z=1
                elea = ele.filter(ELEVEH.name == name).fetch(keys_only=True)
                ele3=set(ele3).intersection(elea)
            if manufacturer != '':
                i=1
                z=1
                eleb = ele.filter(ELEVEH.manufacturer == manufacturer).fetch(keys_only=True)
                ele3=set(ele3).intersection(eleb)
            if minyear != '' or maxyear != '':
                i=1
                if minyear != '' and maxyear != '':
                    z=1
                    elec = ele.filter(ELEVEH.year >= int(math.floor(float(minyear)))).fetch(keys_only=True)
                    eled = ele.filter(ELEVEH.year <= int(math.floor(float(maxyear)))).fetch(keys_only=True)
                    ele3 = set(ele3).intersection(elec)
                    ele3 = set(ele3).intersection(eled)
            if minbatterySize != '' or maxbatterySize != '':
                i=1
                if minbatterySize != '' and maxbatterySize != '':
                    z=1
                    elee = ele.filter(ELEVEH.batterySize >= float(minbatterySize)).fetch(keys_only=True)
                    elef = ele.filter(ELEVEH.batterySize <= float(maxbatterySize)).fetch(keys_only=True)
                    ele3 = set(ele3).intersection(elee)
                    ele3 = set(ele3).intersection(elef)
            if minWLTPRange != '' or maxWLTPRange != '':
                i=1
                if minWLTPRange != '' and maxWLTPRange != '':
                    z=1
                    eleg = ele.filter(ELEVEH.WLTPRange >= float(minWLTPRange)).fetch(keys_only=True)
                    eleh = ele.filter(ELEVEH.WLTPRange <= float(maxWLTPRange)).fetch(keys_only=True)
                    ele3 = set(ele3).intersection(eleg)
                    ele3 = set(ele3).intersection(eleh)
            if mincost != '' or maxcost != '':
                i=1
                if mincost != '' and maxcost != '':
                    z=1
                    elei = ele.filter(ELEVEH.cost >= float(mincost)).fetch(keys_only=True)
                    elej = ele.filter(ELEVEH.cost <= float(maxcost)).fetch(keys_only=True)
                    ele3 = set(ele3).intersection(elei)
                    ele3 = set(ele3).intersection(elej)
            if minpower != '' or maxpower != '':
                i=1
                if minpower != '' and maxpower != '':
                    z=1
                    elek = ele.filter(ELEVEH.power >= float(minpower)).fetch(keys_only=True)
                    elel = ele.filter(ELEVEH.power <= float(maxpower)).fetch(keys_only=True)
                    ele3 = set(ele3).intersection(elek)
                    ele3 = set(ele3).intersection(elel)

            if z==1:
                ele=ndb.get_multi(ele3)
            elif i==1 and z==0:
                ele=None
            elif i==0:
                ele = ele2
                ele = ele.fetch()

        template_values= {
            'url': url,
            'url_string': url_string,
            'user': user,
            'myuser': myuser,
            'ele' : ele
        }
        template= JINJA_ENVIRONMENT.get_template('main.html')
        self.response.write(template.render(template_values))

    def post(self):
        button = self.request.get('button')
        if button == 'Create Ev':
            self.redirect('/create')
        elif button == 'Compare Ev':
            self.redirect('/compare')

app = webapp2.WSGIApplication([('/',MainPage),
('/create',Create),
('/information', Information),
('/compare', Compare)
],debug=True)
