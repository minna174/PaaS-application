import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
from create import Create
import os
from myuser import MyUser
from eleveh import ELEVEH
import math

JINJA_ENVIRONMENT = jinja2.Environment(
loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
extensions=['jinja2.ext.autoescape'],
autoescape=True
)

class Information(webapp2.RequestHandler):
	def get(self):
		self.response.headers['Content-Type'] = 'text/html'
		user=users.get_current_user()
		if user:
			showButtons=1
		else:
			showButtons=None
		name = self.request.get('name')
		manufacturer = self.request.get('manufacturer')
		year = int(self.request.get('year'))
		ele=ELEVEH.query(ELEVEH.name==name, ELEVEH.manufacturer==manufacturer, ELEVEH.year==year)

		k1=ELEVEH.query(ELEVEH.name==name).fetch(keys_only=True)
		k2=ELEVEH.query(ELEVEH.manufacturer==manufacturer).fetch(keys_only=True)
		k3=ELEVEH.query(ELEVEH.year==int(year)).fetch(keys_only=True)
		k=ndb.get_multi(set(k1).intersection(k2).intersection(k3))
		if len(k) > 0:
			k=k[0].key

		reviews=reversed(ele.fetch()[0].review)
		if len(ele.fetch()[0].review) == 0:
			reviews = []
		list1=ele.fetch()[0].score
		score='Nothing found'
		if len(list1) > 0:
			score=sum(list1)/len(list1)
		template_values = {
			'ele' : ele,
			'_key' : k.urlsafe(),
			'reviews' : reviews,
			'score' : score,
			'showButtons' : showButtons
		}
		template = JINJA_ENVIRONMENT.get_template('information.html')
		self.response.write(template.render(template_values))

	def post(self):
		self.response.headers['Content-Type'] = 'text/html'
		button = self.request.get('button')
		user = users.get_current_user()
		if user:
			key=self.request.get('_key_')
			key=ndb.Key(urlsafe=key)
			ele=key.get()
			if ele == None:
				self.redirect('/')

			if button == 'Edit Ev':
				newname = self.request.get('name').strip()
				newmanufacturer = self.request.get('manufacturer').strip()
				newyear = int(math.floor(float(self.request.get('year').strip())))
				newbatterySize = float(self.request.get('batterySize').strip())
				newWLTPRange = float(self.request.get('WLTPRange').strip())
				newcost = float(self.request.get('cost').strip())
				newpower = float(self.request.get('power').strip())
				if newname and newmanufacturer:
					otherele=ELEVEH.query(ELEVEH.name==newname, ELEVEH.manufacturer==newmanufacturer, ELEVEH.year==newyear).fetch(keys_only=True)
					if otherele:
						if otherele[0] == key:
							#
							ele.name=newname
							ele.manufacturer=newmanufacturer
							ele.year=newyear
							ele.batterySize=newbatterySize
							ele.WLTPRange=newWLTPRange
							ele.cost=newcost
							ele.power=newpower
							ele.put()
							self.redirect('/')
						else:
							template_values = {
			                    'error' : 'This EV already exists with same details (name, manufacturer, year)'
			                }
							template = JINJA_ENVIRONMENT.get_template('error.html')
							self.response.write(template.render(template_values))
					else:
						#
						ele.name=newname
						ele.manufacturer=newmanufacturer
						ele.year=newyear
						ele.batterySize=newbatterySize
						ele.WLTPRange=newWLTPRange
						ele.cost=newcost
						ele.power=newpower
						ele.put()
						self.redirect('/')
				else:
					template_values = {
	                    'error' : 'Please check the input fields'
	                }
					template = JINJA_ENVIRONMENT.get_template('error.html')
					self.response.write(template.render(template_values))
			elif button == 'Delete Ev':
				key.delete()
				self.redirect('/')
			elif button == 'Add review and score':
				review=self.request.get('review').strip()
				if len(review) > 1000:
					template_values = {
	                    'error' : 'Review should contain maximum 1000 characters'
	                }
					template = JINJA_ENVIRONMENT.get_template('error.html')
					self.response.write(template.render(template_values))
				else:
					score=int(math.floor(float(self.request.get('rating'))))
					if len(review) > 0:
						ele.review.append(review)
					if score:
						ele.score.append(int(score))
					ele.put()
					self.redirect('/information?name=' + ele.name + '&manufacturer=' + ele.manufacturer + '&year=' + str(ele.year))
		if button == 'Back':
			self.redirect('/')
