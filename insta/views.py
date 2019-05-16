from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
import datetime as dt
from .models import
from .forms import 
from .email import send_welcome_email
from django.contrib.auth.decorators import login_required
# Create your views here.
