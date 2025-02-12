from django.http import HttpResponse, Http404
from django.template import loader
import os
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import WeddingGuest, Family
from .forms import FamilyForm, WeddingGuestForm
import json
import openpyxl
from datetime import datetime

@login_required
def index(request):
    guest_id = request.session.get('guest_id')  # Retrieve guest ID from session
    if guest_id:
        guest = WeddingGuest.objects.get(id=guest_id)
        family = guest.family
        family_guests = family.guests.all()
        context = {'guest': guest, 'family': family, 'guests': family_guests}
        return render(request, 'p1/index.html', context)
    else:
        # Handle the case where no guest ID is in the session
        return redirect('/login/')
    # template = loader.get_template('p1/index.html')
    # guest = WeddingGuest.objects.get(user=request.user)
    # context = {'guest': guest}
    # return HttpResponse(template.render(context, request))

def login_view(request):
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        guest = authenticate(request, username=username, password=password)

        if guest is not None:
            request.session['guest_id'] = guest.id
            request.user = guest
            login(request, guest)
            return redirect("/")  # Redirect to the home page after login
        else:
            return render(request, "p1/login.html", {"error": "Invalid username or password"})

    return render(request, "p1/login.html")

def logout_view(request):
    logout(request)  # This will log the user out by clearing the session
    return redirect('login')

@login_required
def update_rsvp(request):
    if request.method == 'POST':
        form_data = json.loads(request.POST.get('form_data'))  # Get the form data
        updated_guests = []

        # Loop through the form data and update each guest
        for guest_data in form_data:
            guest = WeddingGuest.objects.get(id=guest_data['guest_id'])
            guest.rsvp_status = guest_data['rsvp_status'] == 'yes'
            guest.dietary_restrictions = None
            guest.first_name = guest_data['first_name']
            guest.last_name = guest_data['last_name']
            if 'dietary_restrictions' in guest_data and guest_data['dietary_restrictions']:
                guest.dietary_restrictions = guest_data['dietary_restrictions']

            guest.message = None
            if 'message' in guest_data and guest_data['message']:
                guest.message = guest_data['message']
            guest.is_rsvped = guest_data['is_rsvped']
            guest.staying_at_hotel = guest_data['staying_at_hotel'] == 'yes'
            guest.save()

            # Add the updated guest to the list to send back to the client
            updated_guests.append({
                'id': guest.id,
                'first_name': guest.first_name,
                'last_name': guest.last_name,
                'rsvp_status': guest.rsvp_status,
                'dietary_restrictions': guest.dietary_restrictions,
                'staying_at_hotel':guest.staying_at_hotel
            })

        # Send back the updated guest data to the client
        return JsonResponse({'updated_guests': updated_guests})

    return JsonResponse({'error': 'Invalid request method'}, status=400)

@login_required
def create_family_and_guest(request):
    families = Family.objects.all()
    if request.method == "POST":
        # Create or update the Family form
        family_form = FamilyForm(request.POST)
        guest_form = WeddingGuestForm(request.POST)

        # Check if the Family form is valid
        if family_form.is_valid():
            family_form.save()

        # Check if the WeddingGuest form is valid
        if guest_form.is_valid():
            guest = guest_form.save(commit=False)
            # guest.family = family
            guest.save()

        # Send a success response
        return JsonResponse({'status': 'success', 'message': 'Family and Wedding Guest created successfully!'})

    else:
        family_form = FamilyForm()
        guest_form = WeddingGuestForm()
        return render(request, 'p1/create_family_guest.html', {'family_form': family_form, 'guest_form': guest_form, 'families': families})

@login_required
def view_guests(request):
    rsvped_coming_guests = WeddingGuest.objects.filter(is_rsvped=True, rsvp_status=True)
    rsvped_not_coming_guests = WeddingGuest.objects.filter(is_rsvped=True, rsvp_status=False)
    non_rsvped_guests = WeddingGuest.objects.filter(is_rsvped=False)

    return render(request, 'p1/view_guests.html', {'rsvped_coming_guests': rsvped_coming_guests,
                                                         'rsvped_not_coming_guests': rsvped_not_coming_guests,
                                                         'non_rsvped_guests': non_rsvped_guests})

@login_required
def generate_excel(request):
    # Filter the records based on certain criteria
    records = WeddingGuest.objects.all()

    # Create a new Workbook
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = "Guest records"

    # Add headers to the Excel file
    sheet['A1'] = 'Name'
    sheet['B1'] = 'Dietary restrictions'
    sheet['C1'] = 'Message'
    sheet['D1'] = 'RSVP status'
    sheet['E1'] = 'Made the decision'

    # Fill in data for each record
    row_num = 2  # Start from the second row since the first row is for headers
    for record in records:
        sheet[f'A{row_num}'] = record.first_name + " " + record.last_name
        sheet[f'B{row_num}'] = record.dietary_restrictions
        sheet[f'C{row_num}'] = record.message
        sheet[f'D{row_num}'] = record.rsvp_status
        sheet[f'E{row_num}'] = record.is_rsvped
        row_num += 1

    current_datetime = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

    # Set the response to be a downloadable Excel file with the current date and time in the filename
    filename = f"active_records_{current_datetime}.xlsx"

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    # Save the workbook to the response object
    workbook.save(response)

    return response

