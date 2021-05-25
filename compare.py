import webapp2
import os
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
from myuser import MyUser
from eleveh import ELEVEH

JINJA_ENVIRONMENT = jinja2.Environment(
    loader = jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions = ['jinja2.ext.autoescape'],
    autoescape = True
)

class Compare(webapp2.RequestHandler):
	def get(self):
		keysCheckbox=[]
		ele = ELEVEH.query().fetch()
		for i in ele:
			keysCheckbox.append(i.key.urlsafe())

		template_values = {
			'ele' : ele,
			'keysCheckbox' : keysCheckbox
		}
		template = JINJA_ENVIRONMENT.get_template('compare.html')
		self.response.write(template.render(template_values))

	def post(self):
		high=[]
		low=[]
		allyears=[]
		allbatterysize=[]
		allwltprange=[]
		allcost=[]
		allpower=[]
		allrating=[]
		button = self.request.get('button')
		k=[]
		keysCheckbox=[]
		ele2=[]
		score=[]
		ele = ELEVEH.query().fetch()
		for i in ele:
			keysCheckbox.append(i.key.urlsafe())
		if button == 'Compare':
			keysToTake=self.request.get_all('c')
			if len(keysToTake) == 1:
				self.response.write('')
			elif len(keysToTake) > 1:
				for i in keysToTake:
					k = ndb.Key(urlsafe=i).get()
					ele2.append(k)
					if len(k.score) > 0:
						score.append(sum(k.score)/len(k.score))
						allrating.append(sum(k.score)/len(k.score))
					else:
						score.append('*')
					#find highest and lowest values for each property
					allyears.append(k.year)
					allbatterysize.append(k.batterySize)
					allwltprange.append(k.WLTPRange)
					allcost.append(k.cost)
					allpower.append(k.power)

				low.append(min(allyears))
				low.append(min(allbatterysize))
				low.append(min(allwltprange))
				low.append(min(allcost))
				low.append(min(allpower))
				if len(allrating) > 0:
					low.append(min(allrating))

				high.append(max(allyears))
				high.append(max(allbatterysize))
				high.append(max(allwltprange))
				high.append(max(allcost))
				high.append(max(allpower))
				if len(allrating) > 0:
					high.append(max(allrating))
			else:
				self.redirect('/')
		elif button=='Back':
			self.redirect('/')

		template_values = {
			'ele' : ele,
			'keys' : k,
			'score' : score,
			'ele2' : ele2,
			'keysCheckbox' : keysCheckbox,
			'low' : low,
			'high' : high
		}
		template = JINJA_ENVIRONMENT.get_template('compare.html')
		self.response.write(template.render(template_values))
