from django.shortcuts import render, redirect, get_object_or_404
from .models import Place
from .forms import NewPlaceForm, TripReviewForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib import messages

# Create your views here.
@login_required
def place_list(request):

    # if there is a request to add to the database, collect this data, save it locally
    # and if it is appropriate, save it to the database
    if request.method == "POST":
        form = NewPlaceForm(request.POST)
        place = form.save(commit=False) # create but dont save
        place.user = request.user #connect place to the user
        if form.is_valid():
            place.save()
            return redirect('place_list')
        
    #prints all of the places that the user has not visited, in alphabetical order     
    places = Place.objects.filter(user=request.user).filter(visited=False).order_by('name')
    new_place_form = NewPlaceForm()
    return render(request, 'travel_wishlist/wishlist.html', {'places': places, 'new_place_form': new_place_form})

@login_required
def places_visited(request):
    #this shows the list of visited locations (those with boolean visited == true)
    visited = Place.objects.filter(user=request.user).filter(visited=True)
    return render(request, 'travel_wishlist/visited.html', {'visited': visited})

@login_required
def place_was_visited(request, place_pk):
    # handles when the user clicks on button to mark a place as visited. checks for a code, gets a place object,
    # and saves it to say that it was visited
    if request.method == "POST":
        # pk = request.POST.get('pk')
        place = get_object_or_404(Place, pk=place_pk)
        print(place.user, request.user)
        if place.user == request.user: #checks if the user making the request is the currently logged in user
            place.visited = True
            place.save()
        else:
            return HttpResponseForbidden() #otherwise give them an error
        
    return redirect('place_list')

@login_required
def place_details(request, place_pk):
    # a view for the details of a place
    place = get_object_or_404(Place, pk=place_pk)

    if place.user != request.user:
        return HttpResponseForbidden()

    if request.method == 'POST':
        # if the user submits the form and everything looks good, the data is saved, otherwise gives and error
        form = TripReviewForm(request.POST, request.FILES, instance=place)
        if form.is_valid():
            form.save()
            messages.info(request, 'Trip information updated!')
        else:
            messages.error(request, form.errors)

        return render(request, 'travel_wishlist/place_detail.html', {'place':place})
    else:
        if place.visited:
            review_form = TripReviewForm(instance=place)
            return render(request, 'travel_wishlist/place_detail.html', {'place': place, 'review_form': review_form})
        else:
            return render(request, 'travel_wishlist/place_detail.html', {'place': place})

@login_required
def delete_place(request, place_pk):
    place = get_object_or_404(Place, pk=place_pk)
    if place.user == request.user:
        place.delete()
        return redirect('place_list')
    else:
        return HttpResponseForbidden()