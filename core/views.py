from django.core.mail import message
from django.shortcuts import render,redirect

from .models import User




#---------login function----------------
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        get_user = User.objects.get(email=username, password=password)

        if get_user:
            request.session['is_admin'] = get_user.is_admin
            request.session['email']= get_user.email
            return redirect('home')

                


    return render(request, 'login.html')


#---------- home page -------------

def home(request):
    check_user=request.session.get('email')
    get_user = User.objects.get(email=check_user)
    all_user=User.objects.filter(is_admin=False)



    return render(request, 'home.html', {'get_user':get_user, 'all_user':all_user})


def logout(request):
    request.session.flush()
    return redirect('login')




import re
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import User  # Make sure your User model is imported

@csrf_exempt 
def chat_api(request):
    if request.method == 'POST':

        if not request.session.get('is_admin'):
            return JsonResponse({'reply': 'Access denied. Only admins can do this.'})
        
        message = request.POST.get('message', '').lower().strip()
        
        # 1. ADD USER 

        # Example format: "add user john@xyz.com phone +92332 password secretpass city New York"
        if 'add' in message:
                    email_match = re.search(r'([\w\.-]+@[\w\.-]+)', message)
                    phone_match = re.search(r'(?:phone|number)\s+(\+?\d{5,15})', message)
                    password_match = re.search(r'password\s+(\S+)', message)
                    city_match = re.search(r'city\s+(.+)', message)
        
                    if email_match and phone_match:
                        email = email_match.group(1)
                        phone = phone_match.group(1)
                        
                        # Use provided values, or defaults if admin forgot to type them
                        password = password_match.group(1) if password_match else 'defaultpassword123'
                        city = city_match.group(1).strip().title() if city_match else 'Unassigned'
        
                        if User.objects.filter(email=email).exists():
                            return JsonResponse({'reply': f'User {email} already exists.'})
        
                        # Creates the user and explicitly guarantees they are NOT an admin
                        User.objects.create(
                            email=email, 
                            phone_number=phone, 
                            password=password, 
                            city=city,
                            is_admin=False  
                        )
        
                        # CORRECTION 1: Return the SUCCESS message here!
                        return JsonResponse({'reply': f'Success! Added {email}. Phone: {phone}, Password: {password}, City: {city}.'})
        
                    # CORRECTION 2: The error message must be pushed out here, matching the indentation of the `if email_match...` block
                    return JsonResponse({'reply': 'To add a user, I need at least a valid email and phone number. Example: "add user a@b.com phone 123456 password mypass city London"'})
       
        # 2. REMOVE USER
        # Example: "can you remove the user john.smith@xyz.com"
        elif 'remove' in message or 'delete' in message:
            email_match = re.search(r'([\w\.-]+@[\w\.-]+)', message)
            
            if email_match:
                email = email_match.group(1)
                user = User.objects.filter(email=email).first()
                if user:
                    user.delete()
                    return JsonResponse({'reply': f'Success! Removed user {email}.'})
                return JsonResponse({'reply': f'Could not find the user {email} in the database.'})
            return JsonResponse({'reply': 'Please provide a valid email address to remove.'})



        elif 'update' in message:
            # First, find the target user's current email
            target_match = re.search(r'update.*?(?:user\s+)?([\w\.-]+@[\w\.-]+)', message)
            
            if target_match:
                target_email = target_match.group(1)
                user = User.objects.filter(email=target_email).first()
                
                if not user:
                    return JsonResponse({'reply': f"Could not find any user with the email '{target_email}'."})
                
                # Check for individual fields to update using "to [value]" syntax
                city_match = re.search(r'city\s+to\s+([a-zA-Z]+(?:\s+[a-zA-Z]+)?)', message) # Captures 1-2 words for city
                phone_match = re.search(r'(?:phone|number)\s+to\s+(\+?\d+)', message)
                password_match = re.search(r'password\s+to\s+(\S+)', message)
                email_match = re.search(r'email\s+to\s+([\w\.-]+@[\w\.-]+)', message)
                
                updated_fields = []
                
                if city_match:
                    user.city = city_match.group(1).title()
                    updated_fields.append(f"city to {user.city}")
                
                if phone_match:
                    user.phone_number = phone_match.group(1)
                    updated_fields.append(f"phone to {user.phone_number}")
                
                if password_match:
                    user.password = password_match.group(1)
                    updated_fields.append("password")
                
                if email_match:
                    new_email = email_match.group(1)
                    # Ensure the new email isn't already taken by someone else
                    if User.objects.filter(email=new_email).exists() and new_email != target_email:
                        return JsonResponse({'reply': f"Cannot update email: {new_email} is already in use by another user."})
                    user.email = new_email
                    updated_fields.append(f"email to {new_email}")
                
                # If at least one field was found and updated
                if updated_fields:
                    user.save()
                    updates_formatted = ', '.join(updated_fields)
                    return JsonResponse({'reply': f"Success! Updated {target_email}: {updates_formatted}."})
                
                return JsonResponse({'reply': f"Found {target_email}, but didn't catch what to update. Use format: 'city to [city]', 'phone to [number]', 'password to [pass]', or 'email to [email]'."})
            
            return JsonResponse({'reply': "Please specify who to update. Format: 'update [email] city to [new city]'"})

        # Fallback for unrecognized commands
        return JsonResponse({'reply': "I didn't understand. Try 'add user [email] with phone [number]', 'remove [email]', or 'update [name] city to [city]'."})
