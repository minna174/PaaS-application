import webapp2
import jinja2
import os
from google.appengine.api import users
from google.appengine.ext import ndb
from eleveh import ELEVEH
import math

JINJA_ENVIRONMENT = jinja2.Environment(
loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
extensions=['jinja2.ext.autoescape'],
autoescape=True
)
#ElecVehicle

class Create(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] ='text/html'
        user=users.get_current_user()
        button=self.request.get('button')
        if button == 'Back':
            self.redirect('/')
        if user:
            template_values = {
            }
            template = JINJA_ENVIRONMENT.get_template('create.html')
            self.response.write(template.render(template_values))
        else:
            self.redirect('/')

    def post(self):
        action = self.request.get('button')
        user=users.get_current_user()
        key = ndb.Key('ELEVEH', 'default')
        ele = key.get()
        if ele == None:
            ele = ELEVEH()
        if action == 'Create':
            if user:
                ele.name=self.request.get('name').strip()
                ele.manufacturer=self.request.get('manufacturer').strip()
                ele.year=int(math.floor(float(self.request.get('year').strip())))
                ele.batterySize=float(self.request.get('batterySize').strip())
                ele.WLTPRange=float(self.request.get('WLTPRange').strip())
                ele.cost=float(self.request.get('cost').strip())
                ele.power=float(self.request.get('power').strip())

                data=ELEVEH.query()
                Ename=data.filter(ELEVEH.name==ele.name).fetch(keys_only=True)
                Emanufacturer=data.filter(ELEVEH.manufacturer==ele.manufacturer).fetch(keys_only=True)
                Eyear=data.filter(ELEVEH.year==ele.year).fetch(keys_only=True)
                contains=ndb.get_multi(set(Ename).intersection(Emanufacturer).intersection(Eyear))
                if contains:
                    template_values = {
                        'error' : 'This EV already exists with same details (name, manufacturer, year)'
                    }
                    template = JINJA_ENVIRONMENT.get_template('error.html')
                    self.response.write(template.render(template_values))
                else:
                    ele.put()
                    self.redirect('/')
            else:
                template_values = {
                    'error' : 'You are not logged in'
                }
                template = JINJA_ENVIRONMENT.get_template('error.html')
                self.response.write(template.render(template_values))
