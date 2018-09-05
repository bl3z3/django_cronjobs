from datetime import timedelta

from django.core.mail import send_mail
from django.core.management import BaseCommand
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.template.loader import get_template
from django.template import Context

def email_tardy_users():
	two_weeks_ago = now() - timedelta(days=14)
	tardy_users = User.objects.filter(last_login__lt=two_weeks_ago)

	print("Found " + str(len(tardy_users)) + " users")

	for user in tardy_users:
		template = get_template('login_reminder.txt')
		context = {
			"username": user.username,
		}

		content = template.render(context)
		send_mail(
			'You have not logged in in two weeks - can we help?',
			content,
			'your app <hi@local.host>',
			[user.email],
		)

class Command(BaseCommand):
	def handle(self, *args, **options):
		print("Email tardy users")
		email_tardy_users()