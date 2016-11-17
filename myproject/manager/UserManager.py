import json
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from datetime import datetime, timedelta

from ..models import DPUser


@csrf_exempt
def userRequest(request, user_id=None):
	if request.method == "POST":
		return createUser(request)
	else:
		return getUser(request, user_id)

@csrf_exempt
def createUser(request):
	first_name = request.POST.get('first_name','')
	last_name = request.POST.get('last_name','')
	username = request.POST.get('username','')

	user = None
	existing_users = DPUser.objects.filter(username=username)

	print first_name, last_name, username
	print len(existing_users)
	if len(existing_users) > 0:
		# Player Exists!
		user = existing_users[0]
		errorMessage = "Error! Player with this username already exists."

		return HttpResponse(json.dumps({'success': False, "error":errorMessage}), content_type="application/json")

	if user is None:
		user = DPUser()

	user.first_name = first_name
	user.last_name = last_name
	user.email = email

	user.save()

	response_data = user.getResponseData()

	return HttpResponse(json.dumps(response_data), content_type="application/json")


@csrf_exempt
def getUser(request, user_id):
	response_data = {}
	
	if user_id:
		users = DPUser.objects.filter(id=user_id)

		if len(users)>0:
			user = users[0]
			response_data = user.getResponseData()

		else:
			errorMessage = "Error! This user doesn't exist."
			response_data = {'success': False, "error":errorMessage}

	return HttpResponse(json.dumps(response_data), content_type="application/json")

