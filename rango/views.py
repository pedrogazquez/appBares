from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, render_to_response
import django
django.setup()
from rango.models import Bar,Tapa
from rango.forms import BarForm,TapaForm
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from rango.forms import UserForm, UserProfileForm
from datetime import datetime

def encode_url(str):
    return str.replace(' ', '_')

def decode_url(str):
    return str.replace('_', ' ')

def index(request):

	# Query the database for a list of ALL categories currently stored.
    # Order the categories by no. likes in descending order.
    # Retrieve the top 5 only - or all if less than 5.
    # Place the list in our context_dict dictionary which will be passed to the template engine.
	lista_bares = Bar.objects.order_by('-views')[:5]
	lista_tapas = Tapa.objects.order_by('-views')[:5]
	
	context_dict = {'bares': lista_bares,'tapas': lista_tapas}
	
	# Return a rendered response to send to the client.
	# We make use of the shortcut function to make our lives easier.
	# Note that the first parameter is the template we wish to use.

	return render(request, 'rango/index.html', context_dict)


def get_category_list(max_results=0, starts_with=''):
    cat_list = []
    if starts_with:
        cat_list = Bar.objects.filter(name__startswith=starts_with)
    else:
        cat_list = Bar.objects.all()

    if max_results > 0:
        if (len(cat_list) > max_results):
            cat_list = cat_list[:max_results]

    for cat in cat_list:
        cat.url = encode_url(cat.name)
    
    return cat_list

def about(request):
	# Request the context.
	context = RequestContext(request)
	context_dict = {}
	cat_list = get_category_list()
	context_dict['cat_list'] = cat_list
	# If the visits session varible exists, take it and use it.
	# If it doesn't, we haven't visited the site so set the count to zero.

	count = request.session.get('visits',0)

	context_dict['visit_count'] = count

	# Return and render the response, ensuring the count is passed to the template engine.
	return render_to_response('rango/about.html', context_dict , context)
	
def bar(request,bar_name_slug):
	# Create a context dictionary which we can pass to the template rendering engine.
	context_dict = {}
	
	try:
		# Can we find a category name slug with the given name?
		# If we can't, the .get() method raises a DoesNotExist exception.
		# So the .get() method returns one model instance or raises an exception.
		bar = Bar.objects.get(slug=bar_name_slug)
		context_dict['bar_name'] = bar.name

		# Retrieve all of the associated pages.
		# Note that filter returns >= 1 model instance.
		tapas = Tapa.objects.filter(bar=bar)

		# Adds our results list to the template context under name pages.
		context_dict['tapas'] = tapas
		# We also add the category object from the database to the context dictionary.
		# We'll use this in the template to verify that the category exists.
		context_dict['bar'] = bar
		bar.views += 1
		bar.save()
	except Bar.DoesNotExist:
		# We get here if we didn't find the specified category.
		# Don't do anything - the template displays the "no category" message for us.
		pass
	# Go render the response and return it to the client.
	return render(request, 'rango/bar.html', context_dict)
	
def grafico(request):
	context_dict = {}
	lista_bares = Bar.objects.order_by('-views')
	context_dict = {'bares': lista_bares}
	return render(request, 'rango/grafico.html', context_dict)

def listaBares(request):
	lista_bares = Bar.objects.order_by('-views')
	context_dict = {'bares': lista_bares}
	
	# Return a rendered response to send to the client.
	# We make use of the shortcut function to make our lives easier.
	# Note that the first parameter is the template we wish to use.

	return render(request, 'rango/listaBares.html', context_dict)
	
def register(request):
    # Request the context.
    context = RequestContext(request)
    cat_list = get_category_list()
    context_dict = {}
    context_dict['cat_list'] = cat_list
    # Boolean telling us whether registration was successful or not.
    # Initially False; presume it was a failure until proven otherwise!
    registered = False

    # If HTTP POST, we wish to process form data and create an account.
    if request.method == 'POST':
        # Grab raw form data - making use of both FormModels.
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        # Two valid forms?
        if user_form.is_valid() and profile_form.is_valid():
            # Save the user's form data. That one is easy.
            user = user_form.save()

            # Now a user account exists, we hash the password with the set_password() method.
            # Then we can update the account with .save().
            user.set_password(user.password)
            user.save()

            # Now we can sort out the UserProfile instance.
            # We'll be setting values for the instance ourselves, so commit=False prevents Django from saving the instance automatically.
            profile = profile_form.save(commit=False)
            profile.user = user

            # Profile picture supplied? If so, we put it in the new UserProfile.
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            # Now we save the model instance!
            profile.save()

            # We can say registration was successful.
            registered = True

        # Invalid form(s) - just print errors to the terminal.
        else:
            print user_form.errors, profile_form.errors

    # Not a HTTP POST, so we render the two ModelForms to allow a user to input their data.
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    context_dict['user_form'] = user_form
    context_dict['profile_form']= profile_form
    context_dict['registered'] = registered

    # Render and return!
    return render_to_response(
        'registration/register.html',
        context_dict,
        context)	

@login_required
def add_category(request):
    # Get the context from the request.
    context = RequestContext(request)
    cat_list = get_category_list()
    context_dict = {}
    context_dict['cat_list'] = cat_list
    
    # A HTTP POST?
    if request.method == 'POST':
        form = BarForm(request.POST)

        # Have we been provided with a valid form?
        if form.is_valid():
            # Save the new category to the database.
            form.save(commit=True)

            # Now call the index() view.
            # The user will be shown the homepage.
            return index(request)
        else:
	        # The supplied form contained errors - just print them to the terminal.
            print form.errors
    else:
        # If the request was not a POST, display the form to enter details.
        form = BarForm()

    # Bad form (or form details), no form supplied...
    # Render the form with error messages (if any).
    context_dict['form'] = form
    return render_to_response('rango/add_category.html', context_dict, context)

@login_required
def add_page(request,bar_name_slug):
	
	try:
		bar = Bar.objects.get(slug=bar_name_slug)
	except bar.DoesNotExist:
		bar = None

	if request.method == 'POST':
		form = TapaForm(request.POST)
		if form.is_valid():
			if bar:
				tapa = form.save(commit=False)
				tapa.bar = bar
				tapa.views = 0
				tapa.save()
				# probably better to use a redirect here.
				return listaBares(request)
		else:
			print form.errors
	else:
		form = TapaForm()
	
	context_dict = {'form':form, 'bar': bar}

	return render(request, 'rango/add_page.html', context_dict)
	

def meGusta(request,tapa_title):
	tapa = Tapa.objects.get(nombre=tapa_title)
	tapa.views += 1
	tapa.save()
	return render(request, 'rango/about.html')

def user_login(request):
    # Obtain our request's context.
    context = RequestContext(request)
    cat_list = get_category_list()
    context_dict = {}
    context_dict['cat_list'] = cat_list

    # If HTTP POST, pull out form data and process it.
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Attempt to log the user in with the supplied credentials.
        # A User object is returned if correct - None if not.
        user = authenticate(username=username, password=password)

        # A valid user logged in?
        if user is not None:
            # Check if the account is active (can be used).
            # If so, log the user in and redirect them to the homepage.
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/rango/')
            # The account is inactive; tell by adding variable to the template context.
            else:
                context_dict['disabled_account'] = True
                return render_to_response('registration/login.html', context_dict, context)
        # Invalid login details supplied!
        else:
            print "Invalid login details: {0}, {1}".format(username, password)
            context_dict['bad_details'] = True
            return render_to_response('registration/login.html', context_dict, context)

    # Not a HTTP POST - most likely a HTTP GET. In this case, we render the login form for the user.
    else:
        return render_to_response('registration/login.html', context_dict, context)

		
# Only allow logged in users to logout - add the @login_required decorator!
@login_required
def user_logout(request):
    # As we can assume the user is logged in, we can just log them out.
    logout(request)

    # Take the user back to the homepage.
    return HttpResponseRedirect('/rango/')
	
@login_required
def profile(request):
	context = RequestContext(request)
	cat_list = get_category_list()
	context_dict = {'cat_list': cat_list}
	u = User.objects.get(username=request.user)

	try:
		up = UserProfile.objects.get(user=u)
	except:
		up = None

	context_dict['user'] = u
	context_dict['userprofile'] = up
	return render_to_response('rango/profile.html', context_dict, context)