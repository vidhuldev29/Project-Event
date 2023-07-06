from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from .models import Admin,login,User,convention,GalleryImage,catering,cateringmenu,decoration,photography,PreviousWorks,accommodation,photos_collection,entertainment,transportation,Convention_Booking,Catering_Booking,Decoration_Booking,Photography_Booking,Entertainment_Booking,Accommodation_Booking,Transportation_Booking
from django.contrib import messages
from .forms import DecorationForm,EntertainmentForm,TransportationForm,CateringForm,CateringMenuForm,ConventionForm,ConventionGalleryForm,PhotographyForm,PreviousWorksForm,AccommodationForm,PhotosCollectionForm,ConventionBookingForm,CateringBookingForm,DecorationBookingForm,PhotographyBookingForm,EntertainmentBookingForm,AccommodationBookingForm,TransportationBookingForm
from django.db.models import Count
from django.http import JsonResponse
from django.contrib.sessions.models import Session
from datetime import date, timedelta
from django.db.models import F, Sum
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ObjectDoesNotExist
from django.forms import formset_factory,BaseFormSet
from django.core.exceptions import ValidationError
import os
from django.utils import timezone
from decimal import Decimal
import decimal


# Create your views here.
def admin_index(request):
    if 'id' in request.session:
        username = request.session['id']
        try:
            user = User.objects.get(username=username)
            # User is logged in as a regular user
            messages.error(request, 'You are not authorized to access the admin index page.')
            return redirect('index')
        except User.DoesNotExist:
            try:
                admin = Admin.objects.get(admin_username=username)
                # User is logged in as an admin
                return render(request, 'admin_index.html', {'username': username})
            except Admin.DoesNotExist:
                pass

        # User is not logged in or session is invalid
    messages.error(request, 'Please log in to access the admin index page.')
    return redirect('login')


def index(request):
    if 'id' in request.session:
        username = request.session['id']
        try:
            user = User.objects.get(username=username)
            # User is logged in and has a valid session
            return render(request, 'index.html', {'username': username})
        except User.DoesNotExist:
            pass

    # User is not logged in or session is invalid
    messages.error(request, 'Please log in to access the index page.')
    return redirect('login')

def rg(request):
    if request.method=='POST':
        a = request.POST['r1']
        b = request.POST['r2']
        c = request.POST['r3']
        d = request.POST['r4']
        e = request.POST['r5']
        f = request.POST['r6']
        try:
            data=User.objects.get(username=b)
        except Exception:
            User.objects.create(name=a, username=b, email=c, phone=d, password=f)
            return redirect('login')
        else:
            messages.error(request, 'Username already exists.')
            return redirect('rg')
    else:
        return render(request,'reg.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['l1']
        password = request.POST['l2']
        try:
            user = User.objects.get(username=username)
            if user.password == password:
                # Username and password match in User model
                login(request, user)
                request.session['id'] = username
                return redirect('index')  # Replace 'index' with the URL name of your index page
            else:
                # Incorrect password
                messages.error(request, 'Incorrect password')
                return redirect('login')
        except User.DoesNotExist:
            try:
                admin = Admin.objects.get(admin_username=username)
                if admin.password == password:
                    # Username and password match in Admin model
                    request.session['id'] = username
                    return redirect('admin_index')  # Replace 'admin_index' with the URL name of your admin's home page
                else:
                    # Incorrect password
                    messages.error(request, 'Incorrect password')
                    return redirect('login')
            except Admin.DoesNotExist:
                # User is neither in User model nor Admin model
                messages.error(request, 'Username incorrect')
                return redirect('login')
    else:
        if 'id' in request.session:
            return redirect('index')
        else:
            return render(request, 'login.html')

def logout_view(request):
    if request.method == 'POST':
        session_key = request.session.session_key
        if session_key:
            # Logout the user
            logout(request)
            # Delete the session
            request.session.delete(session_key)
            return JsonResponse({'status': 'success'})
    return redirect('login')


def forgot_password(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        try:
            user = User.objects.get(username=username, email=email)
            request.session['reset_username'] = username
            return redirect('reset_password')
        except ObjectDoesNotExist:
            message = 'Invalid username or email'
            return render(request, 'forgot_password.html', {'message': message})
    return render(request, 'forgot_password.html')

def reset_password(request):
    if 'reset_username' in request.session:
        username = request.session['reset_username']
        try:
            user = User.objects.get(username=username)
            if request.method == 'POST':
                password = request.POST.get('password')
                confirm_password = request.POST.get('confirm_password')
                if password == confirm_password:
                    user.password = password
                    user.save()
                    del request.session['reset_username']
                    messages.success(request, 'Password reset successfully!')
                    return redirect('reset_password')
                else:
                    messages.error(request, 'Passwords do not match')
            return render(request, 'password_reset.html')
        except User.DoesNotExist:
            messages.error(request, 'User does not exist')
            return redirect('forgot_password')
    else:
        return redirect('forgot_password')

def transportation_payment(request, booking_id):
    if 'id' in request.session:
        username = request.session['id']
        try:
            user = User.objects.get(username=username)
            # User is logged in and has a valid session
            booking = get_object_or_404(Transportation_Booking, id=booking_id)

            # Extract relevant data from the booking object
            payment_id = booking.id
            customer_name = booking.name
            phone_number = booking.phone_number
            travels_name = booking.travels_name.name
            km = booking.km

            booking_date = booking.date
            payment_amount = booking.travels_name.avg_km_charge
            subtotal = decimal.Decimal(payment_amount * km)
            gst = Decimal('0.18')
            grand_total = subtotal + (subtotal * gst)

            context = {
                'payment_id': payment_id,
                'customer_name': customer_name,
                'phone_number': phone_number,
                'travels_name': travels_name,
                'km': km,
                'booking_date': booking_date,
                'payment_amount': payment_amount,
                'subtotal': subtotal,
                'gst': gst,
                'grand_total': grand_total,
                'username': username,
            }

            return render(request, 'payment_transportation.html', context)
        except User.DoesNotExist:
            pass

    # User is not logged in or session is invalid
    messages.error(request, 'Please log in to access the about page.')
    return redirect('login')



def accommodation_payment(request, booking_id):
    if 'id' in request.session:
        username = request.session['id']
        try:
            user = User.objects.get(username=username)
            # User is logged in and has a valid session
            booking = get_object_or_404(Accommodation_Booking, id=booking_id)

            # Extract relevant data from the booking object
            payment_id = booking.id
            customer_name = booking.name
            phone_number = booking.phone_number
            hotel_name = booking.hotel_name.name
            rooms = booking.rooms
            booking_date = booking.date

            payment_amount = booking.hotel_name.price
            subtotal = payment_amount * rooms
            gst = Decimal('0.18')
            grand_total = subtotal + (subtotal * gst)

            context = {
                'payment_id': payment_id,
                'customer_name': customer_name,
                'phone_number': phone_number,
                'hotel_name': hotel_name,
                'rooms': rooms,
                'booking_date': booking_date,
                'payment_amount': payment_amount,
                'subtotal': subtotal,
                'gst': gst,
                'grand_total': grand_total,
                'username': username,
            }

            return render(request, 'payment_accommodation.html', context)

        except User.DoesNotExist:
            pass

    # User is not logged in or session is invalid
    messages.error(request, 'Please log in to access the about page.')
    return redirect('login')


def photography_payment(request, booking_id):
    if 'id' in request.session:
        username = request.session['id']
        try:
            user = User.objects.get(username=username)
            # User is logged in and has a valid session
            booking = get_object_or_404(Photography_Booking, id=booking_id)

            # Extract relevant data from the booking object
            payment_id = booking.id
            customer_name = booking.name
            phone_number = booking.phone_number
            studio_name = booking.studio_name.name
            booking_date = booking.date
            event_type = booking.event_type
            payment_amount = booking.studio_name.price
            subtotal = payment_amount
            gst = Decimal('0.18')
            grand_total = subtotal + (subtotal * gst)

            context = {
                'payment_id': payment_id,
                'customer_name': customer_name,
                'phone_number': phone_number,
                'studio_name': studio_name,
                'booking_date': booking_date,
                'event_type': event_type,
                'payment_amount': payment_amount,
                'subtotal': subtotal,
                'gst': gst,
                'grand_total': grand_total,
                'username': username,
            }

            return render(request, 'payment_photography.html', context)

        except User.DoesNotExist:
            pass

    # User is not logged in or session is invalid
    messages.error(request, 'Please log in to access the about page.')
    return redirect('login')

def entertainment_payment(request, booking_id):
    if 'id' in request.session:
        username = request.session['id']
        try:
            user = User.objects.get(username=username)
            # User is logged in and has a valid session
            booking = get_object_or_404(Entertainment_Booking, id=booking_id)

            # Extract relevant data from the booking object
            payment_id = booking.id
            customer_name = booking.name
            phone_number = booking.phone_number
            program_service_name = booking.program_service_name.name
            booking_date = booking.date
            payment_amount = booking.program_service_name.price
            subtotal = payment_amount
            gst = Decimal('0.18')
            grand_total = subtotal + (subtotal * gst)

            context = {
                'payment_id': payment_id,
                'customer_name': customer_name,
                'phone_number': phone_number,
                'program_service_name': program_service_name,
                'booking_date': booking_date,
                'payment_amount': payment_amount,
                'subtotal': subtotal,
                'gst': gst,
                'grand_total': grand_total,
                'username': username,
            }

            return render(request, 'payment_entertainment.html', context)

        except User.DoesNotExist:
            pass

    # User is not logged in or session is invalid
    messages.error(request, 'Please log in to access the about page.')
    return redirect('login')

def decoration_payment(request, booking_id):
    if 'id' in request.session:
        username = request.session['id']
        try:
            user = User.objects.get(username=username)
            # User is logged in and has a valid session
            booking = get_object_or_404(Decoration_Booking, id=booking_id)

            # Extract relevant data from the booking object
            payment_id = booking.id
            customer_name = booking.name
            phone_number = booking.phone_number
            decoration_name = booking.decoration_name.name
            booking_date = booking.date
            payment_amount = booking.decoration_name.price
            subtotal = payment_amount
            gst = Decimal('0.18')
            grand_total = subtotal + (subtotal * gst)

            context = {
                'payment_id': payment_id,
                'customer_name': customer_name,
                'phone_number': phone_number,
                'decoration_name': decoration_name,
                'booking_date': booking_date,
                'payment_amount': payment_amount,
                'subtotal': subtotal,
                'gst': gst,
                'grand_total': grand_total,
                'username': username,
            }

            return render(request, 'payment_decoration.html', context)

        except User.DoesNotExist:
            pass

    # User is not logged in or session is invalid
    messages.error(request, 'Please log in to access the about page.')
    return redirect('login')

def catering_payment(request, booking_id):
    if 'id' in request.session:
        username = request.session['id']
        try:
            user = User.objects.get(username=username)
            # User is logged in and has a valid session
            booking = get_object_or_404(Catering_Booking, id=booking_id)

            # Extract relevant data from the booking object
            payment_id = booking.id
            customer_name = booking.name
            phone_number = booking.phone_number
            catering_name = booking.catering_name.name
            avg_menu_charge = booking.catering_name.avg_menu_charge
            booking_date = booking.date
            guest_count = booking.guest
            payment_amount = decimal.Decimal(avg_menu_charge)
            subtotal = payment_amount * guest_count
            gst = Decimal('0.18')
            grand_total = subtotal + (subtotal * gst)

            context = {
                'payment_id': payment_id,
                'customer_name': customer_name,
                'phone_number': phone_number,
                'catering_name': catering_name,
                'avg_menu_charge': avg_menu_charge,
                'booking_date': booking_date,
                'guest_count': guest_count,
                'payment_amount': payment_amount,
                'subtotal': subtotal,
                'gst': gst,
                'grand_total': grand_total,
                'username': username,
            }

            return render(request, 'payment_catering.html', context)

        except User.DoesNotExist:
            pass

    # User is not logged in or session is invalid
    messages.error(request, 'Please log in to access the about page.')
    return redirect('login')

def convention_payment(request, booking_id):
    if 'id' in request.session:
        username = request.session['id']
        try:
            user = User.objects.get(username=username)
            # User is logged in and has a valid session
            booking = get_object_or_404(Convention_Booking, id=booking_id)

            # Extract relevant data from the booking object
            payment_id = booking.id
            customer_name = booking.name
            phone_number = booking.phone_number
            convention_name = booking.convention_name.name
            booking_date = booking.date
            event_type = booking.type
            payment_amount = booking.convention_name.price
            subtotal = payment_amount
            gst = Decimal('0.18')
            grand_total = subtotal + (subtotal * gst)

            context = {
                'payment_id': payment_id,
                'customer_name': customer_name,
                'phone_number': phone_number,
                'convention_name': convention_name,
                'booking_date': booking_date,
                'event_type': event_type,
                'payment_amount': payment_amount,
                'subtotal': subtotal,
                'gst': gst,
                'grand_total': grand_total,
                'username': username,
            }

            return render(request, 'payment_convention.html', context)
        except User.DoesNotExist:
            pass

    # User is not logged in or session is invalid
    messages.error(request, 'Please log in to access the about page.')
    return redirect('login')



def delete_transportation_booking(request, booking_id):
    booking = get_object_or_404(Transportation_Booking, id=booking_id)

    # Check if the booking is deletable based on the date
    today = date.today()
    deletable_date = booking.date - timedelta(days=3)

    if today <= deletable_date:
        if request.method == 'POST':
            booking.delete()
            messages.success(request, 'Travels booking has been deleted successfully.')
        else:
            messages.error(request, 'Invalid request to delete the travels booking.')
    else:
        messages.error(request, 'Travels booking cannot be deleted.')

    return redirect('booking')  # Replace 'booking' with the appropriate URL name


def delete_accommodation_booking(request, booking_id):
    booking = get_object_or_404(Accommodation_Booking, id=booking_id)

    # Check if the booking is deletable based on the date
    today = date.today()
    deletable_date = booking.date - timedelta(days=3)

    if today <= deletable_date:
        if request.method == 'POST':
            booking.delete()
            messages.success(request, 'Hotel booking has been deleted successfully.')
        else:
            messages.error(request, 'Invalid request to delete the hotel booking.')
    else:
        messages.error(request, 'Hotel booking cannot be deleted.')

    return redirect('booking')  # Replace 'booking' with the appropriate URL name

def delete_entertainment_booking(request, booking_id):
    booking = get_object_or_404(Entertainment_Booking, id=booking_id)

    # Check if the booking is deletable based on the date
    today = date.today()
    deletable_date = booking.date - timedelta(days=3)

    if today <= deletable_date:
        if request.method == 'POST':
            booking.delete()
            messages.success(request, 'Program Service booking has been deleted successfully.')
        else:
            messages.error(request, 'Invalid request to delete the program service booking.')
    else:
        messages.error(request, 'Program Service booking cannot be deleted.')

    return redirect('booking')  # Replace 'booking' with the appropriate URL name

def delete_photography_booking(request, booking_id):
    booking = get_object_or_404(Photography_Booking, id=booking_id)

    # Check if the booking is deletable based on the date
    today = date.today()
    deletable_date = booking.date - timedelta(days=3)

    if today <= deletable_date:
        if request.method == 'POST':
            booking.delete()
            messages.success(request, 'Studio booking has been deleted successfully.')
        else:
            messages.error(request, 'Invalid request to delete the studio booking.')
    else:
        messages.error(request, 'Studio booking cannot be deleted.')

    return redirect('booking')  # Replace 'booking' with the appropriate URL name

def delete_decoration_booking(request, booking_id):
    booking = get_object_or_404(Decoration_Booking, id=booking_id)

    # Check if the booking is deletable based on the date
    today = date.today()
    deletable_date = booking.date - timedelta(days=3)

    if today <= deletable_date:
        if request.method == 'POST':
            booking.delete()
            messages.success(request, 'Decoration booking has been deleted successfully.')
        else:
            messages.error(request, 'Invalid request to delete the decoration booking.')
    else:
        messages.error(request, 'Decoration booking cannot be deleted.')

    return redirect('booking')  # Replace 'booking' with the appropriate URL name


def delete_catering_booking(request, booking_id):
    booking = get_object_or_404(Catering_Booking, id=booking_id)

    # Check if the booking is deletable based on the date
    today = date.today()
    deletable_date = booking.date - timedelta(days=3)

    if today <= deletable_date:
        if request.method == 'POST':
            booking.delete()
            messages.success(request, 'Catering booking has been deleted successfully.')
        else:
            messages.error(request, 'Invalid request to delete the catering booking.')
    else:
        messages.error(request, 'Catering booking cannot be deleted.')

    return redirect('booking')  # Replace 'booking' with the appropriate URL name


def delete_convention_booking(request, booking_id):
    booking = get_object_or_404(Convention_Booking, id=booking_id)

    # Check if the booking is deletable based on the date
    today = date.today()
    deletable_date = booking.date - timedelta(days=3)

    if today <= deletable_date:
        if request.method == 'POST':
            booking.delete()
            messages.success(request, 'Convention booking has been deleted successfully.')
        else:
            messages.error(request, 'Invalid request to delete the convention booking.')
    else:
        messages.error(request, 'convention booking cannot be deleted.')

    return redirect('booking')


def transportation_booking(request):
    if 'id' in request.session:
        username = request.session['id']
        try:
            user = User.objects.get(username=username)
            if request.method == 'POST':
                transportation_booking_form = TransportationBookingForm(request.POST)
                if transportation_booking_form.is_valid():
                    booking = transportation_booking_form.save(commit=False)
                    booking.user = user  # Assign the logged-in user to the booking

                    # Check if the travel service is available on the selected date
                    selected_travel = booking.travels_name
                    selected_date = booking.date

                    # Count existing bookings for the same travel service and date
                    existing_bookings = Transportation_Booking.objects.filter(travels_name=selected_travel,
                                                                              date=selected_date).count()

                    if existing_bookings >= 2:
                        messages.error(request,
                                       'The travel service is fully booked on the selected date. Please choose another date.')
                        return redirect('transportation_booking')

                    booking.save()
                    messages.success(request, 'Booking Successful')
                    return redirect('transportation_booking')
            else:
                transportation_booking_form = TransportationBookingForm()
        except User.DoesNotExist:
            pass
    else:
        # User is not logged in or session is invalid
        messages.error(request, 'Please log in to book a travel service.')
        return redirect('login')

    return render(request, 'transportation_booking.html',
                  {'transportation_booking_form': transportation_booking_form, 'username': username})



def accommodation_booking(request):
    if 'id' in request.session:
        username = request.session['id']
        try:
            user = User.objects.get(username=username)
            total_rooms = 15
            selected_date = date.today() + timezone.timedelta(days=1)
            total_booked_rooms = Accommodation_Booking.objects.filter(date=selected_date).aggregate(
                total_booked_rooms=Sum('rooms'))['total_booked_rooms'] or 0
            available_rooms = total_rooms - total_booked_rooms

            if request.method == 'POST':
                accommodation_booking_form = AccommodationBookingForm(request.POST, available_rooms=available_rooms)
                if accommodation_booking_form.is_valid():
                    booking = accommodation_booking_form.save(commit=False)
                    booking.user = user  # Assign the logged-in user to the booking

                    # Check if the selected hotel has available rooms on the selected date


                    if available_rooms <= 0:
                        messages.info(request, 'No rooms available for booking on the selected date.')
                        return redirect('accommodation_booking')

                    requested_rooms = booking.rooms  # Extract the requested number of rooms

                    if requested_rooms > available_rooms:
                        messages.error(request,
                                       f'Only {available_rooms} room(s) available for booking on the selected date.')
                        return redirect('accommodation_booking')

                    if total_booked_rooms + requested_rooms > total_rooms:
                        messages.error(request, 'The hotel is fully booked on the selected date.')
                        return redirect('accommodation_booking')

                    booking.save()
                    messages.success(request, 'Booking Successful')
                    return redirect('accommodation_booking')

            else:
                accommodation_booking_form = AccommodationBookingForm(available_rooms=available_rooms)
        except User.DoesNotExist:
            pass
    else:
        # User is not logged in or session is invalid
        messages.error(request, 'Please log in to book accommodation.')
        return redirect('login')

    return render(request, 'accommodation_booking.html',
                  {'accommodation_booking_form': accommodation_booking_form, 'username': username})



def entertainment_booking(request):
    if 'id' in request.session:
        username = request.session['id']
        try:
            user = User.objects.get(username=username)
            if request.method == 'POST':
                entertainment_booking_form = EntertainmentBookingForm(request.POST)
                if entertainment_booking_form.is_valid():
                    booking = entertainment_booking_form.save(commit=False)
                    booking.user = user  # Assign the logged-in user to the booking

                    # Check if the program service is available on the selected date
                    selected_service = booking.program_service_name
                    selected_date = booking.date

                    conflicting_bookings = Entertainment_Booking.objects.filter(program_service_name=selected_service,
                                                                                date=selected_date)
                    if conflicting_bookings.exists():
                        messages.error(request,
                                       'This program service is not available on the selected date. Please choose another date.')
                        return redirect('entertainment_booking')

                    booking.save()
                    messages.success(request, 'Entertainment Booking Successful')
                    return redirect('entertainment_booking')
            else:
                entertainment_booking_form = EntertainmentBookingForm()
        except User.DoesNotExist:
            pass
    else:
        # User is not logged in or session is invalid
        messages.error(request, 'Please log in to book entertainment.')
        return redirect('login')

    return render(request, 'entertainment_booking.html',
                  {'entertainment_booking_form': entertainment_booking_form, 'username': username})



def photography_booking(request):
    if 'id' in request.session:
        username = request.session['id']
        try:
            user = User.objects.get(username=username)
            if request.method == 'POST':
                photography_booking_form = PhotographyBookingForm(request.POST)
                if photography_booking_form.is_valid():
                    booking = photography_booking_form.save(commit=False)
                    booking.user = user  # Assign the logged-in user to the booking

                    # Check if the studio is available on the selected date
                    selected_studio = booking.studio_name
                    selected_date = booking.date

                    conflicting_bookings = Photography_Booking.objects.filter(studio_name=selected_studio,
                                                                              date=selected_date)
                    if conflicting_bookings.exists():
                        messages.error(request,
                                       'This studio is not available on the selected date. Please choose another date.')
                        return redirect('photography_booking')

                    booking.save()
                    messages.success(request, 'Photography Booking Successful')
                    return redirect('photography_booking')
            else:
                photography_booking_form = PhotographyBookingForm()
        except User.DoesNotExist:
            pass
    else:
        # User is not logged in or session is invalid
        messages.error(request, 'Please log in to book photography.')
        return redirect('login')

    return render(request, 'photography_booking.html',
                  {'photography_booking_form': photography_booking_form, 'username': username})



def decoration_booking(request):
    if 'id' in request.session:
        username = request.session['id']
        try:
            user = User.objects.get(username=username)
            if request.method == 'POST':
                decoration_booking_form = DecorationBookingForm(request.POST)
                if decoration_booking_form.is_valid():
                    booking = decoration_booking_form.save(commit=False)
                    booking.user = user  # Assign the logged-in user to the booking

                    # Check if the decoration is available on the selected date
                    selected_decoration = booking.decoration_name
                    selected_date = booking.date

                    conflicting_bookings = Decoration_Booking.objects.filter(decoration_name=selected_decoration,
                                                                             date=selected_date)
                    if conflicting_bookings.exists():
                        messages.error(request,
                                       'This decoration is not available on the selected date. Please choose another date.')
                        return redirect('decoration_booking')

                    booking.save()
                    messages.success(request, 'Decoration Booking Successful')
                    return redirect('decoration_booking')
            else:
                decoration_booking_form = DecorationBookingForm()
        except User.DoesNotExist:
            pass
    else:
        # User is not logged in or session is invalid
        messages.error(request, 'Please log in to book a decoration.')
        return redirect('login')

    return render(request, 'decoration_booking.html',
                  {'decoration_booking_form': decoration_booking_form, 'username': username})


def catering_booking(request):
    if 'id' in request.session:
        username = request.session['id']
        try:
            user = User.objects.get(username=username)
            if request.method == 'POST':
                catering_booking_form = CateringBookingForm(request.POST)
                if catering_booking_form.is_valid():
                    booking = catering_booking_form.save(commit=False)
                    booking.user = user  # Assign the logged-in user to the booking

                    # Check if the catering service is available on the selected date
                    selected_catering = booking.catering_name
                    selected_date = booking.date

                    # Count existing bookings for the same catering service and date
                    existing_bookings = Catering_Booking.objects.filter(catering_name=selected_catering,
                                                                       date=selected_date).count()

                    if existing_bookings >= 3:
                        messages.error(request,
                                       'The catering service is fully booked on the selected date. Please choose another date.')
                        return redirect('catering_booking')

                    booking.save()
                    messages.success(request, 'Booking Successful')
                    return redirect('catering_booking')
            else:
                catering_booking_form = CateringBookingForm()
        except User.DoesNotExist:
            pass
    else:
        # User is not logged in or session is invalid
        messages.error(request, 'Please log in to book a catering service.')
        return redirect('login')

    return render(request, 'catering_booking.html',
                  {'catering_booking_form': catering_booking_form, 'username': username})


def convention_booking(request):
    if 'id' in request.session:
        username = request.session['id']
        try:
            user = User.objects.get(username=username)
            if request.method == 'POST':
                convention_booking_form = ConventionBookingForm(request.POST)
                if convention_booking_form.is_valid():
                    booking = convention_booking_form.save(commit=False)
                    booking.user = user  # Assign the logged-in user to the booking

                    # Check if the convention is available on the selected date
                    selected_convention = booking.convention_name
                    selected_date = booking.date

                    conflicting_bookings = Convention_Booking.objects.filter(convention_name=selected_convention, date=selected_date)
                    if conflicting_bookings.exists():
                        messages.error(request, 'This convention is not available on the selected date. Please choose another date.')
                        return redirect('convention_booking')

                    booking.save()
                    messages.success(request, 'Booking Successful')
                    return redirect('convention_booking')
            else:
                convention_booking_form = ConventionBookingForm()
        except User.DoesNotExist:
            pass
    else:
        # User is not logged in or session is invalid
        messages.error(request, 'Please log in to book a convention.')
        return redirect('login')

    return render(request, 'convention_booking.html', {'convention_booking_form': convention_booking_form, 'username': username})


def booking(request):
    if 'id' in request.session:
        username = request.session['id']
        try:
            user = User.objects.get(username=username)
            today_date = date.today()  # Get the current date

            convention_bookings = Convention_Booking.objects.filter(user=user)
            all_convention_bookings_passed = all(booking.date < today_date for booking in convention_bookings)

            catering_bookings = Catering_Booking.objects.filter(user=user)
            all_catering_bookings_passed = all(booking.date < today_date for booking in catering_bookings)

            decoration_bookings = Decoration_Booking.objects.filter(user=user)
            all_decoration_bookings_passed = all(booking.date < today_date for booking in decoration_bookings)

            photography_bookings = Photography_Booking.objects.filter(user=user)
            all_photography_bookings_passed = all(booking.date < today_date for booking in photography_bookings)

            entertainment_bookings = Entertainment_Booking.objects.filter(user=user)
            all_entertainment_bookings_passed = all(booking.date < today_date for booking in entertainment_bookings)

            accommodation_bookings = Accommodation_Booking.objects.filter(user=user)
            all_accommodation_bookings_passed = all(booking.date < today_date for booking in accommodation_bookings)

            transportation_bookings = Transportation_Booking.objects.filter(user=user)
            all_transportation_bookings_passed = all(booking.date < today_date for booking in transportation_bookings)

            return render(request, 'booking.html', {
                'convention_bookings': convention_bookings,
                'catering_bookings': catering_bookings,
                'decoration_bookings': decoration_bookings,
                'photography_bookings': photography_bookings,
                'entertainment_bookings': entertainment_bookings,
                'accommodation_bookings': accommodation_bookings,
                'transportation_bookings': transportation_bookings,
                'username': username,
                'today_date': today_date,
                'all_convention_bookings_passed': all_convention_bookings_passed,
                'all_catering_bookings_passed': all_catering_bookings_passed,
                'all_decoration_bookings_passed': all_decoration_bookings_passed,
                'all_photography_bookings_passed': all_photography_bookings_passed,
                'all_entertainment_bookings_passed': all_entertainment_bookings_passed,
                'all_accommodation_bookings_passed': all_accommodation_bookings_passed,
                'all_transportation_bookings_passed': all_transportation_bookings_passed,
            })
        except User.DoesNotExist:
            pass

    # User is not logged in or session is invalid
    messages.error(request, 'Please log in to view your bookings.')
    return redirect('login')


def admin_about(request):
    if 'id' in request.session:
        username = request.session['id']
        try:
            user = User.objects.get(username=username)
            # User is logged in as a regular user
            messages.error(request, 'You are not authorized to access the admin about page.')
            return redirect('index')
        except User.DoesNotExist:
            try:
                admin = Admin.objects.get(admin_username=username)
                # User is logged in as an admin
                return render(request, 'admin_about.html', {'username': username})
            except Admin.DoesNotExist:
                pass

        # User is not logged in or session is invalid
    messages.error(request, 'Please log in to access the admin about page.')
    return redirect('login')

def admin_booking(request):
    if 'id' in request.session:
        username = request.session['id']
        try:
            user = User.objects.get(username=username)
            # User is logged in as a regular user
            messages.error(request, 'You are not authorized to access the admin booking page.')
            return redirect('index')
        except User.DoesNotExist:
            try:
                admin = Admin.objects.get(admin_username=username)
                # User is logged in as an admin
                convention_bookings = Convention_Booking.objects.all()
                catering_bookings = Catering_Booking.objects.all()
                decoration_bookings = Decoration_Booking.objects.all()
                photography_bookings = Photography_Booking.objects.all()
                entertainment_bookings = Entertainment_Booking.objects.all()
                accommodation_bookings = Accommodation_Booking.objects.all()
                transportation_bookings = Transportation_Booking.objects.all()

                bookings = list(convention_bookings) + list(catering_bookings) + list(decoration_bookings) + list(
                    photography_bookings) + list(entertainment_bookings) + list(accommodation_bookings) + list(
                    transportation_bookings)

                return render(request, 'admin_booking.html', {
                    'bookings': bookings, 'username': username
                })
            except Admin.DoesNotExist:
                pass

        # User is not logged in or session is invalid
    messages.error(request, 'Please log in to access the admin booking page.')
    return redirect('login')


def booking_info(request, booking_id):
    if 'id' in request.session:
        username = request.session['id']
        try:
            user = User.objects.get(username=username)
            # User is logged in as a regular user
            messages.error(request, 'You are not authorized to access the admin booking info page.')
            return redirect('index')
        except User.DoesNotExist:
            try:
                admin = Admin.objects.get(admin_username=username)
                # User is logged in as an admin
                booking = None
                booking_type = None

                # Check each model to find the corresponding booking
                if Convention_Booking.objects.filter(id=booking_id).exists():
                    booking = get_object_or_404(Convention_Booking, id=booking_id)
                    booking_type = 'Convention_Booking'
                elif Catering_Booking.objects.filter(id=booking_id).exists():
                    booking = get_object_or_404(Catering_Booking, id=booking_id)
                    booking_type = 'Catering_Booking'
                elif Decoration_Booking.objects.filter(id=booking_id).exists():
                    booking = get_object_or_404(Decoration_Booking, id=booking_id)
                    booking_type = 'Decoration_Booking'
                elif Photography_Booking.objects.filter(id=booking_id).exists():
                    booking = get_object_or_404(Photography_Booking, id=booking_id)
                    booking_type = 'Photography_Booking'
                elif Entertainment_Booking.objects.filter(id=booking_id).exists():
                    booking = get_object_or_404(Entertainment_Booking, id=booking_id)
                    booking_type = 'Entertainment_Booking'
                elif Accommodation_Booking.objects.filter(id=booking_id).exists():
                    booking = get_object_or_404(Accommodation_Booking, id=booking_id)
                    booking_type = 'Accommodation_Booking'
                elif Transportation_Booking.objects.filter(id=booking_id).exists():
                    booking = get_object_or_404(Transportation_Booking, id=booking_id)
                    booking_type = 'Transportation_Booking'

                return render(request, 'booking_info.html', {
                    'booking': booking,
                    'booking_type': booking_type,
                    'username':username,
                })
            except Admin.DoesNotExist:
                pass

        # User is not logged in or session is invalid
    messages.error(request, 'Please log in to access the admin booking info page.')
    return redirect('login')




def admin_delete_booking(request, booking_id):
    if request.method == 'POST':
        booking = None

        # Check each model to find the corresponding booking
        if Convention_Booking.objects.filter(id=booking_id).exists():
            booking = get_object_or_404(Convention_Booking, id=booking_id)
        elif Catering_Booking.objects.filter(id=booking_id).exists():
            booking = get_object_or_404(Catering_Booking, id=booking_id)
        elif Decoration_Booking.objects.filter(id=booking_id).exists():
            booking = get_object_or_404(Decoration_Booking, id=booking_id)
        elif Photography_Booking.objects.filter(id=booking_id).exists():
            booking = get_object_or_404(Photography_Booking, id=booking_id)
        elif Entertainment_Booking.objects.filter(id=booking_id).exists():
            booking = get_object_or_404(Entertainment_Booking, id=booking_id)
        elif Accommodation_Booking.objects.filter(id=booking_id).exists():
            booking = get_object_or_404(Accommodation_Booking, id=booking_id)
        elif Transportation_Booking.objects.filter(id=booking_id).exists():
            booking = get_object_or_404(Transportation_Booking, id=booking_id)

        if booking:
            # Delete the booking
            booking.delete()

    return redirect('admin_booking')


def manage_transportation(request):
    if 'id' in request.session:
        username = request.session['id']
        try:
            user = User.objects.get(username=username)
            # User is logged in as a regular user
            messages.error(request, 'You are not authorized to access the admin index page.')
            return redirect('index')
        except User.DoesNotExist:
            try:
                admin = Admin.objects.get(admin_username=username)
                # User is logged in as an admin
                transportations = transportation.objects.all()
                return render(request, 'manage_transportation.html', {'transportations': transportations,'username': username})
            except Admin.DoesNotExist:
                pass

        # User is not logged in or session is invalid
    messages.error(request, 'Please log in to access the admin index page.')
    return redirect('login')

def transportation_info(request, id):
    if 'id' in request.session:
        username = request.session['id']
        try:
            user = User.objects.get(username=username)
            # User is logged in as a regular user
            messages.error(request, 'You are not authorized to access the transportation info page.')
            return redirect('index')
        except User.DoesNotExist:
            try:
                admin = Admin.objects.get(admin_username=username)
                # User is logged in as an admin
                transportations = get_object_or_404(transportation, pk=id)
                return render(request, 'transportation_info.html', {'transportations': transportations,'username': username})
            except Admin.DoesNotExist:
                pass

        # User is not logged in or session is invalid
    messages.error(request, 'Please log in to access the transportation info page.')
    return redirect('login')

def edit_transportation(request, id):
    if 'id' in request.session:
        username = request.session['id']
        try:
            user = User.objects.get(username=username)
            # User is logged in as a regular user
            messages.error(request, 'You are not authorized to access the edit transportation page.')
            return redirect('index')
        except User.DoesNotExist:
            try:
                admin = Admin.objects.get(admin_username=username)
                # User is logged in as an admin
                transportations = get_object_or_404(transportation, pk=id)
                edit_transportation_form = TransportationForm(request.POST or None, instance=transportations)
                if edit_transportation_form.is_valid():
                    edit_transportation_form.save()
                    return redirect('manage_transportation')
                return render(request, 'edit_transportation.html', {'transportations': transportations,
                                                                    'edit_transportation_form': edit_transportation_form,'username': username})
            except Admin.DoesNotExist:
                pass

        # User is not logged in or session is invalid
    messages.error(request, 'Please log in to access the edit transportation page.')
    return redirect('login')

def delete_transportation(request, id):
    transportations = transportation.objects.get(pk=id)
    transportations.delete()
    return redirect('manage_transportation')
def add_transportation(request):
    if 'id' in request.session:
        username = request.session['id']
        try:
            user = User.objects.get(username=username)
            # User is logged in as a regular user
            messages.error(request, 'You are not authorized to access the add transportation page.')
            return redirect('index')
        except User.DoesNotExist:
            try:
                admin = Admin.objects.get(admin_username=username)
                # User is logged in as an admin
                if request.method == 'POST':
                    transportation_form = TransportationForm(request.POST, request.FILES)
                    if transportation_form.is_valid():
                        name = transportation_form.cleaned_data['name']
                        if transportation.objects.filter(name=name).exists():
                            messages.error(request, 'A travels with the same name already exists.')
                        else:
                            transportation_form.save()
                            messages.success(request, 'Travels created successfully.')
                        return redirect('add_transportation')
                else:
                    transportation_form = TransportationForm()
                return render(request, 'add_transportation.html', {'transportation_form': transportation_form,'username': username})
            except Admin.DoesNotExist:
                pass

        # User is not logged in or session is invalid
    messages.error(request, 'Please log in to access the add transportation page.')
    return redirect('login')



def manage_accommodation(request):
    if 'id' in request.session:
        username = request.session['id']
        try:
            user = User.objects.get(username=username)
            # User is logged in as a regular user
            messages.error(request, 'You are not authorized to access the manage accommodation page.')
            return redirect('index')
        except User.DoesNotExist:
            try:
                admin = Admin.objects.get(admin_username=username)
                # User is logged in as an admin
                accommodations = accommodation.objects.all()
                return render(request, 'manage_accommodation.html', {'accommodations': accommodations,'username': username})
            except Admin.DoesNotExist:
                pass

        # User is not logged in or session is invalid
    messages.error(request, 'Please log in to access the manage accommodation page.')
    return redirect('login')

def accommodation_info(request, id):
    if 'id' in request.session:
        username = request.session['id']
        try:
            user = User.objects.get(username=username)
            # User is logged in as a regular user
            messages.error(request, 'You are not authorized to access the accommodation info page.')
            return redirect('index')
        except User.DoesNotExist:
            try:
                admin = Admin.objects.get(admin_username=username)
                # User is logged in as an admin
                accommodations = get_object_or_404(accommodation, pk=id)
                photos_collection_images = accommodations.photos_collection_images.all()
                return render(request, 'accommodation_info.html',
                              {'accommodations': accommodations, 'photos_collection_images': photos_collection_images,'username': username})
            except Admin.DoesNotExist:
                pass

        # User is not logged in or session is invalid
    messages.error(request, 'Please log in to access the accommodation info page.')
    return redirect('login')


def edit_accommodation(request, id):
    if 'id' in request.session:
        username = request.session['id']
        try:
            user = User.objects.get(username=username)
            # User is logged in as a regular user
            messages.error(request, 'You are not authorized to access the edit accommodation page.')
            return redirect('index')
        except User.DoesNotExist:
            try:
                admin = Admin.objects.get(admin_username=username)
                # User is logged in as an admin
                accommodations = get_object_or_404(accommodation, id=id)
                photos_collection_images = accommodations.photos_collection_images.all()

                if request.method == 'POST':
                    accommodation_form = AccommodationForm(request.POST, instance=accommodations)
                    if accommodation_form.is_valid():
                        accommodation_form.save()

                    # Delete selected images
                    delete_images = request.POST.getlist('delete_images')
                    for image_id in delete_images:
                        image = photos_collection.objects.get(id=image_id)
                        image.delete()

                    messages.success(request, 'Hotel updated successfully.')
                    return redirect('edit_accommodation', id=id)
                else:
                    accommodation_form = AccommodationForm(instance=accommodations)

                context = {
                    'accommodations': accommodations,
                    'accommodation_form': accommodation_form,
                    'photos_collection_images': photos_collection_images,
                    'username': username,
                }

                return render(request, 'edit_accommodation.html', context=context)
            except Admin.DoesNotExist:
                pass

    # User is not logged in or session is invalid
    messages.error(request, 'Please log in to access the edit accommodation page.')
    return redirect('login')




def delete_accommodation(request, id):
    accommodations = accommodation.objects.get(pk=id)
    accommodations.delete()
    return redirect('manage_accommodation')
def add_accommodation(request):
    if 'id' in request.session:
        username = request.session['id']
        try:
            user = User.objects.get(username=username)
            # User is logged in as a regular user
            messages.error(request, 'You are not authorized to access the add accommodation page.')
            return redirect('index')
        except User.DoesNotExist:
            try:
                admin = Admin.objects.get(admin_username=username)
                # User is logged in as an admin
                if request.method == 'POST':
                    accommodation_form = AccommodationForm(request.POST, request.FILES)
                    if accommodation_form.is_valid():
                        name = accommodation_form.cleaned_data['name']
                        if accommodation.objects.filter(name=name).exists():
                            messages.error(request, 'A hotel with the same name already exists.')
                        else:
                            accommodation_form.save()
                            messages.success(request, 'Accommodation created successfully.')
                        return redirect('add_accommodation')
                else:
                    accommodation_form = AccommodationForm()
                return render(request, 'add_accommodation.html', {'accommodation_form': accommodation_form,'username': username})
            except Admin.DoesNotExist:
                pass

        # User is not logged in or session is invalid
    messages.error(request, 'Please log in to access the add accommodation page.')
    return redirect('login')

def add_accommodation_photos(request):
    if 'id' in request.session:
        username = request.session['id']
        try:
            user = User.objects.get(username=username)
            # User is logged in as a regular user
            messages.error(request, 'You are not authorized to access the add photos collections page.')
            return redirect('index')
        except User.DoesNotExist:
            try:
                admin = Admin.objects.get(admin_username=username)
                # User is logged in as an admin

                if request.method == 'POST':
                    form = PhotosCollectionForm(request.POST, request.FILES)
                    if form.is_valid():
                        hotel_id = form.cleaned_data['hotel'].id
                        try:
                            hotel_instance = accommodation.objects.get(id=hotel_id)
                            images = request.FILES.getlist('images')
                            for image in images:
                                photos_collection.objects.create(hotel=hotel_instance, image=image)
                            messages.success(request, 'Photos collections added successfully.')
                            return redirect('add_accommodation_photos')
                        except accommodation.DoesNotExist:
                            messages.error(request, 'Selected hotel does not exist.')
                            return redirect('index')
                    else:
                        messages.error(request, 'Form is invalid.')
                else:
                    form = PhotosCollectionForm()
                return render(request, 'add_accommodation_photos.html', {'form': form, 'username': username})
            except Admin.DoesNotExist:
                pass

    # User is not logged in or session is invalid
    messages.error(request, 'Please log in to access the add photos collections page.')
    return redirect('login')



def manage_entertainment(request):
    if 'id' in request.session:
        username = request.session['id']
        try:
            user = User.objects.get(username=username)
            # User is logged in as a regular user
            messages.error(request, 'You are not authorized to access the manage entertainment page.')
            return redirect('index')
        except User.DoesNotExist:
            try:
                admin = Admin.objects.get(admin_username=username)
                # User is logged in as an admin
                entertainments = entertainment.objects.all()
                return render(request, 'manage_entertainment.html', {'entertainments': entertainments,'username': username})
            except Admin.DoesNotExist:
                pass

        # User is not logged in or session is invalid
    messages.error(request, 'Please log in to access the manage entertainment page.')
    return redirect('login')

def entertainment_info(request, id):
    if 'id' in request.session:
        username = request.session['id']
        try:
            user = User.objects.get(username=username)
            # User is logged in as a regular user
            messages.error(request, 'You are not authorized to access the entertainment info page.')
            return redirect('index')
        except User.DoesNotExist:
            try:
                admin = Admin.objects.get(admin_username=username)
                # User is logged in as an admin
                entertainments = get_object_or_404(entertainment, pk=id)
                return render(request, 'entertainment_info.html', {'entertainments': entertainments,'username': username})
            except Admin.DoesNotExist:
                pass

        # User is not logged in or session is invalid
    messages.error(request, 'Please log in to access the entertainment info page.')
    return redirect('login')

def edit_entertainment(request, id):
    if 'id' in request.session:
        username = request.session['id']
        try:
            user = User.objects.get(username=username)
            # User is logged in as a regular user
            messages.error(request, 'You are not authorized to access the edit entertainment page.')
            return redirect('index')
        except User.DoesNotExist:
            try:
                admin = Admin.objects.get(admin_username=username)
                # User is logged in as an admin
                entertainments = get_object_or_404(entertainment, pk=id)
                entertainment_edit_form = EntertainmentForm(request.POST or None, instance=entertainments)
                if entertainment_edit_form.is_valid():
                    entertainment_edit_form.save()
                    return redirect('manage_entertainment')
                return render(request, 'edit_entertainment.html',
                              {'entertainments': entertainments, 'entertainment_edit_form': entertainment_edit_form,'username': username})
            except Admin.DoesNotExist:
                pass

        # User is not logged in or session is invalid
    messages.error(request, 'Please log in to access the edit entertainment page.')
    return redirect('login')

def delete_entertainment(request, id):
    entertainments = entertainment.objects.get(pk=id)
    entertainments.delete()
    return redirect('manage_entertainment')
def add_entertainment(request):
    if 'id' in request.session:
        username = request.session['id']
        try:
            user = User.objects.get(username=username)
            # User is logged in as a regular user
            messages.error(request, 'You are not authorized to access the add entertainment page.')
            return redirect('index')
        except User.DoesNotExist:
            try:
                admin = Admin.objects.get(admin_username=username)
                # User is logged in as an admin
                if request.method == 'POST':
                    entertainment_form = EntertainmentForm(request.POST, request.FILES)
                    if entertainment_form.is_valid():
                        name = entertainment_form.cleaned_data['name']
                        if entertainment.objects.filter(name=name).exists():
                            messages.error(request, 'A program service with the same name already exists.')
                        else:
                            entertainment_form.save()
                            messages.success(request, 'Program Service created successfully.')
                        return redirect('add_entertainment')
                else:
                    entertainment_form = EntertainmentForm()
                return render(request, 'add_entertainment.html', {'entertainment_form': entertainment_form,'username': username})
            except Admin.DoesNotExist:
                pass

        # User is not logged in or session is invalid
    messages.error(request, 'Please log in to access the add entertainment page.')
    return redirect('login')



def manage_photography(request):
    if 'id' in request.session:
        username = request.session['id']
        try:
            user = User.objects.get(username=username)
            # User is logged in as a regular user
            messages.error(request, 'You are not authorized to access the manage photography page.')
            return redirect('index')
        except User.DoesNotExist:
            try:
                admin = Admin.objects.get(admin_username=username)
                # User is logged in as an admin
                photographers = photography.objects.all()
                return render(request, 'manage_photography.html', {'photographers': photographers,'username': username})
            except Admin.DoesNotExist:
                pass

        # User is not logged in or session is invalid
    messages.error(request, 'Please log in to access the manage photography page.')
    return redirect('login')

def photography_info(request, id):
    if 'id' in request.session:
        username = request.session['id']
        try:
            user = User.objects.get(username=username)
            # User is logged in as a regular user
            messages.error(request, 'You are not authorized to access the photogrphy info page.')
            return redirect('index')
        except User.DoesNotExist:
            try:
                admin = Admin.objects.get(admin_username=username)
                # User is logged in as an admin
                photographers = get_object_or_404(photography, pk=id)
                previous_works_images = photographers.previous_works_images.all()
                return render(request, 'photography_info.html',
                              {'photographers': photographers, 'previous_works_images': previous_works_images,'username': username})
            except Admin.DoesNotExist:
                pass

        # User is not logged in or session is invalid
    messages.error(request, 'Please log in to access the photogrphy info page.')
    return redirect('login')


def edit_photography(request, id):
    if 'id' in request.session:
        username = request.session['id']
        try:
            user = User.objects.get(username=username)
            # User is logged in as a regular user
            messages.error(request, 'You are not authorized to access the edit photography page.')
            return redirect('index')
        except User.DoesNotExist:
            try:
                admin = Admin.objects.get(admin_username=username)
                # User is logged in as an admin
                photographers = get_object_or_404(photography, id=id)
                previous_works_images = photographers.previous_works_images.all()

                if request.method == 'POST':
                    photography_form = PhotographyForm(request.POST, instance=photographers)
                    if photography_form.is_valid():
                        photography_form.save()

                    # Delete selected images
                    delete_images = request.POST.getlist('delete_images')
                    for image_id in delete_images:
                        image = PreviousWorks.objects.get(id=image_id)
                        image.delete()

                    messages.success(request, 'Studio updated successfully.')
                    return redirect('edit_photography', id=id)
                else:
                    photography_form = PhotographyForm(instance=photographers)

                context = {
                    'photographers': photographers,
                    'photography_form': photography_form,
                    'previous_works_images': previous_works_images,
                    'username': username,
                }

                return render(request, 'edit_photography.html', context=context)
            except Admin.DoesNotExist:
                pass

    # User is not logged in or session is invalid
    messages.error(request, 'Please log in to access the edit photography page.')
    return redirect('login')



def delete_photography(request, id):
    photographers = photography.objects.get(pk=id)
    photographers.delete()
    return redirect('manage_photography')
def add_photography(request):
    if 'id' in request.session:
        username = request.session['id']
        try:
            user = User.objects.get(username=username)
            # User is logged in as a regular user
            messages.error(request, 'You are not authorized to access the add photography page.')
            return redirect('index')
        except User.DoesNotExist:
            try:
                admin = Admin.objects.get(admin_username=username)
                # User is logged in as an admin
                if request.method == 'POST':
                    photography_form = PhotographyForm(request.POST, request.FILES)
                    if photography_form.is_valid():
                        name = photography_form.cleaned_data['name']
                        if photography.objects.filter(name=name).exists():
                            messages.error(request, 'A studio with the same name already exists.')
                        else:
                            photography_form.save()
                            messages.success(request, 'Studio created successfully.')
                        return redirect('add_photography')
                else:
                    photography_form = PhotographyForm()
                return render(request, 'add_photography.html', {'photography_form': photography_form,'username': username})
            except Admin.DoesNotExist:
                pass

        # User is not logged in or session is invalid
    messages.error(request, 'Please log in to access the add photography page.')
    return redirect('login')

def add_photography_works(request):
    if 'id' in request.session:
        username = request.session['id']
        try:
            user = User.objects.get(username=username)
            # User is logged in as a regular user
            messages.error(request, 'You are not authorized to access the add previous works page.')
            return redirect('index')
        except User.DoesNotExist:
            try:
                admin = Admin.objects.get(admin_username=username)
                # User is logged in as an admin

                if request.method == 'POST':
                    form = PreviousWorksForm(request.POST, request.FILES)
                    if form.is_valid():
                        studio_id = form.cleaned_data['studio'].id
                        try:
                            studio_instance = photography.objects.get(id=studio_id)
                            images = request.FILES.getlist('images')
                            for image in images:
                                PreviousWorks.objects.create(studio=studio_instance, image=image)
                            messages.success(request, 'Previous works added successfully.')
                            return redirect('add_photography_works')
                        except photography.DoesNotExist:
                            messages.error(request, 'Selected studio does not exist.')
                            return redirect('index')
                    else:
                        messages.error(request, 'Form is invalid.')
                else:
                    form = PreviousWorksForm()
                return render(request, 'add_photography_works.html', {'form': form, 'username': username})
            except Admin.DoesNotExist:
                pass

    # User is not logged in or session is invalid
    messages.error(request, 'Please log in to access the add previous works page.')
    return redirect('login')



def manage_decoration(request):
    if 'id' in request.session:
        username = request.session['id']
        try:
            user = User.objects.get(username=username)
            # User is logged in as a regular user
            messages.error(request, 'You are not authorized to access the manage decoration page.')
            return redirect('index')
        except User.DoesNotExist:
            try:
                admin = Admin.objects.get(admin_username=username)
                # User is logged in as an admin
                decorations = decoration.objects.all()
                return render(request, 'manage_decoration.html', {'decorations': decorations,'username': username})
            except Admin.DoesNotExist:
                pass

        # User is not logged in or session is invalid
    messages.error(request, 'Please log in to access the manage decoration page.')
    return redirect('login')

def decoration_info(request, id):
    if 'id' in request.session:
        username = request.session['id']
        try:
            user = User.objects.get(username=username)
            # User is logged in as a regular user
            messages.error(request, 'You are not authorized to access the decoration info page.')
            return redirect('index')
        except User.DoesNotExist:
            try:
                admin = Admin.objects.get(admin_username=username)
                # User is logged in as an admin
                decorations = get_object_or_404(decoration, pk=id)
                return render(request, 'decoration_info.html', {'decorations': decorations, 'username': username})
            except Admin.DoesNotExist:
                pass

        # User is not logged in or session is invalid
    messages.error(request, 'Please log in to access the decoration info page.')
    return redirect('login')

def edit_decoration(request, id):
    if 'id' in request.session:
        username = request.session['id']
        try:
            user = User.objects.get(username=username)
            # User is logged in as a regular user
            messages.error(request, 'You are not authorized to access the edit decoration page.')
            return redirect('index')
        except User.DoesNotExist:
            try:
                admin = Admin.objects.get(admin_username=username)
                # User is logged in as an admin
                decorations = get_object_or_404(decoration, pk=id)
                edit_decoration_form = DecorationForm(request.POST or None, instance=decorations)
                if edit_decoration_form.is_valid():
                    edit_decoration_form.save()
                    return redirect('manage_decoration')
                return render(request, 'edit_decoration.html',
                              {'decorations': decorations, 'edit_decoration_form': edit_decoration_form, 'username': username})
            except Admin.DoesNotExist:
                pass

        # User is not logged in or session is invalid
    messages.error(request, 'Please log in to access the edit decoration page.')
    return redirect('login')

def delete_decoration(request, id):
    decorations = decoration.objects.get(pk=id)
    decorations.delete()
    return redirect('manage_decoration')
def add_decoration(request):
    if 'id' in request.session:
        username = request.session['id']
        try:
            user = User.objects.get(username=username)
            # User is logged in as a regular user
            messages.error(request, 'You are not authorized to access the add decoration page.')
            return redirect('index')
        except User.DoesNotExist:
            try:
                admin = Admin.objects.get(admin_username=username)
                # User is logged in as an admin
                if request.method == 'POST':
                    decoration_form = DecorationForm(request.POST, request.FILES)
                    if decoration_form.is_valid():
                        name = decoration_form.cleaned_data['name']
                        if decoration.objects.filter(name=name).exists():
                            messages.error(request, 'A decoration with the same name already exists.')
                        else:
                            decoration_form.save()
                            messages.success(request, 'Decoration created successfully.')
                        return redirect('add_decoration')
                else:
                    decoration_form = DecorationForm()
                return render(request, 'add_decoration.html', {'decoration_form': decoration_form,'username': username})
            except Admin.DoesNotExist:
                pass

        # User is not logged in or session is invalid
    messages.error(request, 'Please log in to access the add decoration page.')
    return redirect('login')



def manage_catering(request):
    if 'id' in request.session:
        username = request.session['id']
        try:
            user = User.objects.get(username=username)
            # User is logged in as a regular user
            messages.error(request, 'You are not authorized to access the admin index page.')
            return redirect('index')
        except User.DoesNotExist:
            try:
                admin = Admin.objects.get(admin_username=username)
                # User is logged in as an admin
                caterings = catering.objects.all()
                return render(request, 'manage_catering.html', {'caterings': caterings,'username': username})
            except Admin.DoesNotExist:
                pass

        # User is not logged in or session is invalid
    messages.error(request, 'Please log in to access the admin index page.')
    return redirect('login')


def catering_info(request, id):
    if 'id' in request.session:
        username = request.session['id']
        try:
            user = User.objects.get(username=username)
            # User is logged in as a regular user
            messages.error(request, 'You are not authorized to access the catering info page.')
            return redirect('index')
        except User.DoesNotExist:
            try:
                admin = Admin.objects.get(admin_username=username)
                # User is logged in as an admin
                caterings = get_object_or_404(catering, pk=id)
                catering_menu = caterings.catering_menu.get()  # assuming there is only one catering menu object per catering service
                menu_list = catering_menu.get_menu_list()
                return render(request, 'catering_info.html', {'caterings': caterings, 'menu_list': menu_list,'username': username})
            except Admin.DoesNotExist:
                pass

        # User is not logged in or session is invalid
    messages.error(request, 'Please log in to access the catering info page.')
    return redirect('login')

def edit_catering(request, id):
    if 'id' in request.session:
        username = request.session['id']
        try:
            user = User.objects.get(username=username)
            # User is logged in as a regular user
            messages.error(request, 'You are not authorized to access the edit catering page.')
            return redirect('index')
        except User.DoesNotExist:
            try:
                admin = Admin.objects.get(admin_username=username)
                # User is logged in as an admin
                # Get the catering object to be edited
                caterings = get_object_or_404(catering, pk=id)
                catering_menu = caterings.catering_menu.all()

                if request.method == 'POST':
                    catering_form = CateringForm(request.POST, instance=caterings)
                    catering_menu_forms = [CateringMenuForm(request.POST, request.FILES, instance=menu) for menu in
                                           catering_menu]

                    if catering_form.is_valid() and all([form.is_valid() for form in catering_menu_forms]):
                        caterings = catering_form.save()
                        for form in catering_menu_forms:
                            form.save()
                        messages.success(request, 'Catering updated successfully.')
                        return redirect('edit_catering', id=id)
                else:
                    catering_form = CateringForm(instance=caterings)
                    catering_menu_forms = [CateringMenuForm(instance=image) for image in catering_menu]

                context = {
                    'caterings': caterings,
                    'catering_form': catering_form,
                    'catering_menu_forms': catering_menu_forms,
                    'username': username,
                }

                return render(request, 'edit_catering.html', context=context)
            except Admin.DoesNotExist:
                pass

        # User is not logged in or session is invalid
    messages.error(request, 'Please log in to access the edit catering page.')
    return redirect('login')


def delete_catering(request, id):
    caterings = catering.objects.get(pk=id)
    caterings.delete()
    return redirect('manage_catering')
def add_catering(request):
    if 'id' in request.session:
        username = request.session['id']
        try:
            user = User.objects.get(username=username)
            # User is logged in as a regular user
            messages.error(request, 'You are not authorized to access the add catering page.')
            return redirect('index')
        except User.DoesNotExist:
            try:
                admin = Admin.objects.get(admin_username=username)
                # User is logged in as an admin
                if request.method == 'POST':
                    catering_form = CateringForm(request.POST, request.FILES)
                    if catering_form.is_valid():
                        name = catering_form.cleaned_data['name']
                        if catering.objects.filter(name=name).exists():
                            messages.error(request, 'A catering with the same name already exists.')
                        else:
                            catering_form.save()
                            messages.success(request, 'Catering created successfully.')
                        return redirect('add_catering')
                else:
                    catering_form = CateringForm()
                return render(request, 'add_catering.html', {'catering_form': catering_form,'username': username})
            except Admin.DoesNotExist:
                pass

        # User is not logged in or session is invalid
    messages.error(request, 'Please log in to access the add catering page.')
    return redirect('login')

def add_catering_menu(request):
    if 'id' in request.session:
        username = request.session['id']
        try:
            user = User.objects.get(username=username)
            # User is logged in as a regular user
            messages.error(request, 'You are not authorized to access the add catering menu page.')
            return redirect('index')
        except User.DoesNotExist:
            try:
                admin = Admin.objects.get(admin_username=username)
                # User is logged in as an admin
                if request.method == 'POST':
                    catering_menu_form = CateringMenuForm(request.POST)
                    if catering_menu_form.is_valid():
                        catering_menu_form.save()
                        messages.success(request, 'Menu added successfully.')
                        return redirect(
                            'add_catering_menu')  # replace 'home' with the name of your desired redirect URL
                else:
                    catering_menu_form = CateringMenuForm()
                return render(request, 'add_catering_menu.html', {'catering_menu_form': catering_menu_form,'username': username})
            except Admin.DoesNotExist:
                pass

        # User is not logged in or session is invalid
    messages.error(request, 'Please log in to access the add catering menu page.')
    return redirect('login')


def manage_convention(request):
    if 'id' in request.session:
        username = request.session['id']
        try:
            user = User.objects.get(username=username)
            # User is logged in as a regular user
            messages.error(request, 'You are not authorized to access the manage convention page.')
            return redirect('index')
        except User.DoesNotExist:
            try:
                admin = Admin.objects.get(admin_username=username)
                # User is logged in as an admin
                conventions = convention.objects.all()
                return render(request, 'manage_convention.html', {'conventions': conventions,'username': username})
            except Admin.DoesNotExist:
                pass

        # User is not logged in or session is invalid
    messages.error(request, 'Please log in to access the manage convention page.')
    return redirect('login')

def convention_info(request, id):
    if 'id' in request.session:
        username = request.session['id']
        try:
            user = User.objects.get(username=username)
            # User is logged in as a regular user
            messages.error(request, 'You are not authorized to access the convention info page.')
            return redirect('index')
        except User.DoesNotExist:
            try:
                admin = Admin.objects.get(admin_username=username)
                # User is logged in as an admin
                conventions = get_object_or_404(convention, pk=id)
                gallery_images = conventions.gallery_images.all()
                return render(request, 'convention_info.html',
                              {'conventions': conventions, 'gallery_images': gallery_images, 'username': username})
            except Admin.DoesNotExist:
                pass

        # User is not logged in or session is invalid
    messages.error(request, 'Please log in to access the convention info page.')
    return redirect('login')


def edit_convention(request, id):
    if 'id' in request.session:
        username = request.session['id']
        try:
            user = User.objects.get(username=username)
            # User is logged in as a regular user
            messages.error(request, 'You are not authorized to access the edit convention page.')
            return redirect('index')
        except User.DoesNotExist:
            try:
                admin = Admin.objects.get(admin_username=username)
                # User is logged in as an admin
                conventions = get_object_or_404(convention, id=id)
                gallery_images = conventions.gallery_images.all()

                if request.method == 'POST':
                    convention_form = ConventionForm(request.POST, instance=conventions)
                    if convention_form.is_valid():
                        convention_form.save()

                    # Delete selected images
                    delete_images = request.POST.getlist('delete_images')
                    for image_id in delete_images:
                        image = GalleryImage.objects.get(id=image_id)
                        image.delete()

                    messages.success(request, 'Convention updated successfully.')
                    return redirect('edit_convention', id=id)
                else:
                    convention_form = ConventionForm(instance=conventions)

                context = {
                    'conventions': conventions,
                    'convention_form': convention_form,
                    'gallery_images': gallery_images,
                    'username': username,
                }

                return render(request, 'edit_convention.html', context=context)
            except Admin.DoesNotExist:
                pass

    # User is not logged in or session is invalid
    messages.error(request, 'Please log in to access the edit convention page.')
    return redirect('login')


def delete_convention(request, id):
    conventions = convention.objects.get(pk=id)
    conventions.delete()
    return redirect('manage_convention')
def add_convention(request):
    if 'id' in request.session:
        username = request.session['id']
        try:
            user = User.objects.get(username=username)
            # User is logged in as a regular user
            messages.error(request, 'You are not authorized to access the add convention page.')
            return redirect('index')
        except User.DoesNotExist:
            try:
                admin = Admin.objects.get(admin_username=username)
                # User is logged in as an admin
                if request.method == 'POST':
                    convention_form = ConventionForm(request.POST, request.FILES)
                    if convention_form.is_valid():
                        name = convention_form.cleaned_data['name']
                        if convention.objects.filter(name=name).exists():
                            messages.error(request, 'A convention with the same name already exists.')
                        else:
                            convention_form.save()
                            messages.success(request, 'Convention created successfully.')
                        return redirect('add_convention')
                else:
                    convention_form = ConventionForm()
                return render(request, 'add_convention.html', {'convention_form': convention_form, 'username': username})
            except Admin.DoesNotExist:
                pass

        # User is not logged in or session is invalid
    messages.error(request, 'Please log in to access the add convention page.')
    return redirect('login')




class ConventionGalleryFormSet(BaseFormSet):
    def clean(self):
        for form in self.forms:
            if form.cleaned_data and not form.cleaned_data.get('image'):
                raise ValidationError('Please select at least one image per form.')

def add_convention_gallery(request):
    if 'id' in request.session:
        username = request.session['id']
        try:
            user = User.objects.get(username=username)
            # User is logged in as a regular user
            messages.error(request, 'You are not authorized to access the add convention gallery page.')
            return redirect('index')
        except User.DoesNotExist:
            try:
                admin = Admin.objects.get(admin_username=username)
                # User is logged in as an admin

                if request.method == 'POST':
                    form = ConventionGalleryForm(request.POST, request.FILES)
                    if form.is_valid():
                        convention_id = form.cleaned_data['convention'].id
                        try:
                            convention_instance = convention.objects.get(id=convention_id)
                            images = request.FILES.getlist('images')
                            for image in images:
                                GalleryImage.objects.create(convention=convention_instance, image=image)
                            messages.success(request, 'Gallery added successfully.')
                            return redirect('add_convention_gallery')
                        except convention.DoesNotExist:
                            messages.error(request, 'Selected convention does not exist.')
                            return redirect('index')
                    else:
                        messages.error(request, 'Form is invalid.')
                else:
                    form = ConventionGalleryForm()
                return render(request, 'add_convention_gallery.html', {'form': form, 'username': username})
            except Admin.DoesNotExist:
                pass

    # User is not logged in or session is invalid
    messages.error(request, 'Please log in to access the add convention gallery page.')
    return redirect('login')





def manage_user(request):
    if 'id' in request.session:
        username = request.session['id']
        try:
            user = User.objects.get(username=username)
            # User is logged in as a regular user
            messages.error(request, 'You are not authorized to access the manage user page.')
            return redirect('index')
        except User.DoesNotExist:
            try:
                admin = Admin.objects.get(admin_username=username)
                # User is logged in as an admin
                user = User.objects.all()
                return render(request, 'manage_user.html', {'user': user,'username': username})
            except Admin.DoesNotExist:
                pass

        # User is not logged in or session is invalid
    messages.error(request, 'Please log in to access the manage user page.')
    return redirect('login')

def user_info(request, username):
    if 'id' in request.session:
        usernameid = request.session['id']
        try:
            user = User.objects.get(username=usernameid)
            # User is logged in as a regular user
            messages.error(request, 'You are not authorized to access the user info page.')
            return redirect('index')
        except User.DoesNotExist:
            try:
                admin = Admin.objects.get(admin_username=usernameid)
                # User is logged in as an admin
                user = get_object_or_404(User, username=username)
                return render(request, 'user_info.html', {'user': user, 'username': admin})
            except Admin.DoesNotExist:
                pass

        # User is not logged in or session is invalid
    messages.error(request, 'Please log in to access the user info page.')
    return redirect('login')

def delete_user(request, username):
    user = User.objects.get(username=username)
    user.delete()
    return redirect('manage_user')






def transportationview(request):
    if 'id' in request.session:
        username = request.session['id']
        try:
            user = User.objects.get(username=username)
            # User is logged in and has a valid session
            travels_list = transportation.objects.all()
            return render(request, 'transportation.html', {'travels_list': travels_list,'username': username})
        except User.DoesNotExist:
            pass

    # User is not logged in or session is invalid
    messages.error(request, 'Please log in to access the travels list page.')
    return redirect('login')


def accommodatonview(request):
    if 'id' in request.session:
        username = request.session['id']
        try:
            user = User.objects.get(username=username)
            # User is logged in and has a valid session
            hotels_list = accommodation.objects.all()
            return render(request, 'accommodation.html', {'hotels_list': hotels_list,'username': username})
        except User.DoesNotExist:
            pass

    # User is not logged in or session is invalid
    messages.error(request, 'Please log in to access the hotels list page.')
    return redirect('login')


def photoview(request,id):
    if 'id' in request.session:
        username = request.session['id']
        try:
            user = User.objects.get(username=username)
            # User is logged in and has a valid session
            hotel = get_object_or_404(accommodation, id=id)
            photos = photos_collection.objects.filter(hotel=hotel)
            return render(request, 'photos_collection.html', {'studio': hotel, 'photos': photos,'username': username})
        except User.DoesNotExist:
            pass

    # User is not logged in or session is invalid
    messages.error(request, 'Please log in to access the hotel photos page.')
    return redirect('login')


def entertainmentview(request):
    if 'id' in request.session:
        username = request.session['id']
        try:
            user = User.objects.get(username=username)
            # User is logged in and has a valid session
            ent_serv_list = entertainment.objects.all()
            return render(request, 'entertainment.html', {'ent_serv_list': ent_serv_list,'username': username})
        except User.DoesNotExist:
            pass

    # User is not logged in or session is invalid
    messages.error(request, 'Please log in to access the program service list page.')
    return redirect('login')

def photographyview(request):
    if 'id' in request.session:
        username = request.session['id']
        try:
            user = User.objects.get(username=username)
            # User is logged in and has a valid session
            studio_list = photography.objects.all()
            return render(request, 'photography.html', {'studio_list': studio_list,'username': username})
        except User.DoesNotExist:
            pass

    # User is not logged in or session is invalid
    messages.error(request, 'Please log in to access the studio list page.')
    return redirect('login')


def worksview(request,id):
    if 'id' in request.session:
        username = request.session['id']
        try:
            user = User.objects.get(username=username)
            # User is logged in and has a valid session
            studio = get_object_or_404(photography, id=id)
            previous_works_images = PreviousWorks.objects.filter(studio=studio)
            return render(request, 'previous_works.html',{'studio': studio, 'previous_works_images': previous_works_images,'username': username})
        except User.DoesNotExist:
            pass

    # User is not logged in or session is invalid
    messages.error(request, 'Please log in to access the previous works page.')
    return redirect('login')

def decorationview(request):
    if 'id' in request.session:
        username = request.session['id']
        try:
            user = User.objects.get(username=username)
            # User is logged in and has a valid session
            decoration_list = decoration.objects.all()
            return render(request, 'decoration.html', {'decoration_list': decoration_list,'username': username})
        except User.DoesNotExist:
            pass

    # User is not logged in or session is invalid
    messages.error(request, 'Please log in to access the decoration list page.')
    return redirect('login')


def cateringview(request):
    if 'id' in request.session:
        username = request.session['id']
        try:
            user = User.objects.get(username=username)
            # User is logged in and has a valid session
            catering_list = catering.objects.all()
            return render(request, 'catering.html', {'catering_list': catering_list,'username': username})
        except User.DoesNotExist:
            pass

    # User is not logged in or session is invalid
    messages.error(request, 'Please log in to access the catering list page.')
    return redirect('login')


def cateringmenuview(request, catering_id):
    if 'id' in request.session:
        username = request.session['id']
        try:
            user = User.objects.get(username=username)
            # User is logged in and has a valid session
            cat_list = get_object_or_404(catering, pk=catering_id)
            menu = cateringmenu.objects.filter(catering=cat_list)
            menu_list = []
            if menu:
                menu_list = menu[0].get_menu_list()
            return render(request, 'catering_menu.html', {'cat_list': cat_list, 'menu_list': menu_list,'username': username})
        except User.DoesNotExist:
            pass

    # User is not logged in or session is invalid
    messages.error(request, 'Please log in to access the catering menu page.')
    return redirect('login')


def conventionview(request):
    if 'id' in request.session:
        username = request.session['id']
        try:
            user = User.objects.get(username=username)
            # User is logged in and has a valid session
            conlist = convention.objects.all()
            return render(request, 'convention.html', {'conlist': conlist,'username': username})
        except User.DoesNotExist:
            pass

    # User is not logged in or session is invalid
    messages.error(request, 'Please log in to access the convention list page.')
    return redirect('login')



def galleryview(request,id):
    if 'id' in request.session:
        username = request.session['id']
        try:
            user = User.objects.get(username=username)
            # User is logged in and has a valid session
            conv = get_object_or_404(convention, id=id)
            gallery_images = GalleryImage.objects.filter(convention=conv)
            return render(request, 'gallery.html', {'g': conv, 'gallery_images': gallery_images,'username': username})
        except User.DoesNotExist:
            pass

    # User is not logged in or session is invalid
    messages.error(request, 'Please log in to access the convention gallery page.')
    return redirect('login')




def services(request):
    if 'id' in request.session:
        username = request.session['id']
        try:
            user = User.objects.get(username=username)
            # User is logged in and has a valid session
            return render(request, 'services.html', {'username': username})
        except User.DoesNotExist:
            pass

    # User is not logged in or session is invalid
    messages.error(request, 'Please log in to access the services page.')
    return redirect('login')


def about(request):
    if 'id' in request.session:
        username = request.session['id']
        try:
            user = User.objects.get(username=username)
            # User is logged in and has a valid session
            return render(request, 'about.html', {'username': username})
        except User.DoesNotExist:
            pass

    # User is not logged in or session is invalid
    messages.error(request, 'Please log in to access the about page.')
    return redirect('login')

