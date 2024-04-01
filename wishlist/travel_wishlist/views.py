from django.shortcuts import render, redirect, get_object_or_404
from .models import Place
from .forms import NewPlaceForm

# Create your views here.
def place_list(request):

    # if there is a request to add to the database, collect this data, save it locally
    # and if it is appropriate, save it to the database
    if request.method == "POST":
        form = NewPlaceForm(request.POST)
        place = form.save()
        if form.is_valid():
            place.save()
            return redirect('place_list')
        
    #prints all of the places that the user has not visited, in alphabetical order     
    places = Place.objects.filter(visited=False).order_by('name')
    new_place_form = NewPlaceForm()
    return render(request, 'travel_wishlist/wishlist.html', {'places': places, 'new_place_form': new_place_form})

def places_visited(request):
    #this shows the list of visited locations (those with boolean visited == true)
    visited = Place.objects.filter(visited=True)
    return render(request, 'travel_wishlist/visited.html', {'visited': visited})

def place_was_visited(request, place_pk):
    # handles when the user clicks on button to mark a place as visited. checks for a code, gets a place object,
    # and saves it to say that it was visited
    if request.method == "POST":
        place = get_object_or_404(Place, pk=place_pk)
        place.visited = True
        place.save()
    
    return redirect('place_list')