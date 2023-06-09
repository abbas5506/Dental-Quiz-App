from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from . import forms
from . import models

from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.models import User
from django.contrib import messages

# Create your views here.
# For creating home dashboard of APP
def home(request):
    return render(request, 'home.html')

# For creating sign up page to get data from users
def register(request):
    message = None

    form = forms.RegisterUserForm
    if request.method == 'POST':
        form = forms.RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            message = "Data has been submitted Sucessfully!"

    return render(request, 'registration/register.html', {'form':form, message:'message'})

# To get all the categories from the models.py in DB
def all_Category(request):
    categoriesData = models.quizCategory.objects.all()
    return render(request, 'all_Category.html', {'data':categoriesData})

# To get all question according to categories from the models.py in DB
@login_required
def category_questions(request,cat_id):
    category = models.quizCategory.objects.get(id=cat_id)
    question = models.quizQuestions.objects.filter(category=category).order_by('id').first()
    return render(request, 'category-questions.html', {'question':question, 'category':category})

    # THIS IS FOR MULTIPLE QUESTIONS ON ONE PAGE
    #questions = models.quizQuestions.objects.filter(category=category)
    #return render(request, 'category-questions.html', {'data':questions, 'category':category})

@login_required
def submit_answer(request,cat_id,quest_id):
    if request.method == 'POST':
        user = request.user
        category = models.quizCategory.objects.get(id=cat_id)
        question = models.quizQuestions.objects.filter(category=category, id__gt=quest_id).exclude(id=quest_id).order_by('id').first()
        
        # If users select skip button so NOT SUBMITTED will be saved in DB
        if 'skip' in request.POST:
            quest = models.quizQuestions.objects.get(id=quest_id)
            user = request.user
            answer = 'Not Submitted'
            models.userSubmittedAnswers.objects.create(user=user, question=quest, right_answer=answer)
        
        # If users select submit button so RIGHT ANSWER will be saved in DB
        elif 'answer' in request.POST:
            quest = models.quizQuestions.objects.get(id=quest_id)
            user = request.user
            answer = request.POST['answer']
            models.userSubmittedAnswers.objects.create(user=user, question=quest, right_answer=answer)
        
        # If users haven't selected any option
        else:
            quest = models.quizQuestions.objects.get(id=quest_id)
            user = request.user
            answer = 'Not Submitted'
            models.userSubmittedAnswers.objects.create(user=user, question=quest, right_answer=answer)
        
        if question:
            return render(request, 'category-questions.html', {'question':question, 'category':category})
        else:
            # Fetch all the attempted and skipped submitted results
            result = models.userSubmittedAnswers.objects.filter(user=request.user)
            
            # Fetch all the skipped submitted results
            skipped = models.userSubmittedAnswers.objects.filter(user=request.user, right_answer='Not Submitted').count()
            
            # Fetch all the attempted submitted results
            attempted = models.userSubmittedAnswers.objects.filter(user=request.user).exclude(right_answer='Not Submitted').count()

            rightAns = 0
            percentage = 0
            if result:
                for row in result:
                    if row.question.right_option == row.right_answer:
                        rightAns +=1
                    # This is for the cathing of ZeroDivisionError
                    total = result.count()
                    if total > 0:
                        percentage = "{:.4f}%".format(round((rightAns*100) / result.count(), 4))
                    else:
                        percentage = "N/A"

            # This code is used to prevent user from submitting answers again
            # Generate the HTML for the results page
            html = render(request, 'result.html', {'result':result, 'total_skipped':skipped, 'total_attempted':attempted, 'rightAns':rightAns, 'percentage':percentage})

            # Redirect the user to the results page
            response = HttpResponse(html)
            response['Location'] = '/resultcard'
            response.status_code = 302
            return response

    else:
        return HttpResponse('Method is not Allowed!!!')

@login_required
def result(request):
    # Fetch all the attempted and skipped submitted results
    result = models.userSubmittedAnswers.objects.filter(user=request.user)
            
    # Fetch all the skipped submitted results
    skipped = models.userSubmittedAnswers.objects.filter(user=request.user, right_answer='Not Submitted').count()
            
    # Fetch all the attempted submitted results
    attempted = models.userSubmittedAnswers.objects.filter(user=request.user).exclude(right_answer='Not Submitted').count()

    rightAns = 0
    percentage = 0
    if result:
        for row in result:
            if row.question.right_option == row.right_answer:
                rightAns +=1
                # This is for the cathing of ZeroDivisionError
                total = result.count()
                if total > 0:
                    percentage = "{:.2f}%".format(round((rightAns*100) / result.count(), 2))
                else:
                    percentage = "N/A"

    return render(request, 'result.html', {'result':result, 'total_skipped':skipped, 'total_attempted':attempted, 'rightAns':rightAns, 'percentage':percentage})

@login_required
def resultcard(request):
    # Fetch all the attempted and skipped submitted results
    result = models.userSubmittedAnswers.objects.filter(user=request.user)
            
    # Fetch all the skipped submitted results
    skipped = models.userSubmittedAnswers.objects.filter(user=request.user, right_answer='Not Submitted').count()
            
    # Fetch all the attempted submitted results
    attempted = models.userSubmittedAnswers.objects.filter(user=request.user).exclude(right_answer='Not Submitted').count()

    rightAns = 0
    percentage = 0
    if result:
        for row in result:
            if row.question.right_option == row.right_answer:
                rightAns +=1
                # This is for the cathing of ZeroDivisionError
                total = result.count()
                if total > 0:
                    percentage = "{:.2f}%".format(round((rightAns*100) / result.count(), 2))
                else:
                    percentage = "N/A"

    return render(request, 'resultcard.html', {'result':result, 'total_skipped':skipped, 'total_attempted':attempted, 'rightAns':rightAns, 'percentage':percentage})

def password_reset_request(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = None

        if user:
            # Generate a token for the user
            token_generator = default_token_generator()
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = token_generator.make_token(user)

            # Build the password reset email
            subject = 'Password reset request'
            from_email = 'inximamkhan0@gmail.com'
            to_email = user.email
            context = {
                'user': user,
                'uid': uid,
                'token': token,
                'protocol': 'http',
                'domain': 'example.com',
            }
            message = render_to_string('password_reset_email.txt', context)

            # Send the email
            send_mail(subject, message, from_email, [to_email])

            # Render a success message to the user
            return render(request, 'password_reset_done.html')
        else:
            # Render an error message to the user
            return render(request, 'password_reset.html', {'error': 'Invalid email address'})
    else:
        # Render the password reset form
        return render(request, 'password_reset.html')

def portfolio(request):
    return render(request, 'portfolio.html')

