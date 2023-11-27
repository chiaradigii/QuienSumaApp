from django.shortcuts import render
from .models import FutbolClubs
import googlemaps
import json

def geocode(request):
    clubs = FutbolClubs.objects.all()
    context = {
        'clubs':clubs,
    }
    return render(request, 'futbolClubs/geocode.html',context)

def geocode_club(request,pk):
    club = FutbolClubs.objects.get(id=pk)
    # check whether we have the data in the database that we need 
    if club.adress and club.country and club.zipcode and club.city != None: 
        # creating string of existing location data in database
        adress_string = str(club.adress)+", "+str(club.zipcode)+", "+str(club.city) +", "+str(club.country)

        # geocode the string
        gmaps = googlemaps.Client(key= settings.GOOGLE_API_KEY)
        intermediate = json.dumps(gmaps.geocode(str(adress_string))) 
        intermediate2 = json.loads(intermediate)
        latitude = intermediate2[0]['geometry']['location']['lat']
        longitude = intermediate2[0]['geometry']['location']['lng']
     
        # save the lat and long in our database
        club.latitude = latitude
        club.longitude = longitude
        club.save()
        return redirect('geocode')
    else:
        return redirect('geocode')
    return render(request, 'google/empty.html',context)