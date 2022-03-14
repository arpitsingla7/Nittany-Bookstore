# I have created this file- Arpit
from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    # params = {'name': 'Arpit', 'place': 'USA'}

    return render(request, 'index.html')

    #  return HttpResponse(" <h1>homepage</h1> <a href = "">back</a> ")


def login(request):
   # dj_username = request.GET.get('username', 'default')
   # dj_password = request.POST.get('pass', 'default')

    #params = {'username': dj_username, 'password': dj_password}
    return render(request, 'login.html')


def register(request):
    dj_username = request.POST.get('username', 'default')
    dj_firstname = request.POST.get('firstname', 'default')
    dj_lastname = request.POST.get('lastname', 'default')
    dj_address = request.POST.get('address', 'default')
    dj_phone = request.POST.get('phone', 'default')
    dj_password = request.POST.get('pass', 'default')

    return render(request, 'register.html')
 #   return HttpResponse(" <h1> Register Page </h1> ")


def bookstorehpuser(request):

    # check if the login username and passowrd exist in the user table or manager table
    # then return the page accordingly
    return render(request, 'bookstorehpuser.html')


def bookstorehpmanager(request):
    return render(request, 'bookstorehpmanager.html')


def browsebook(request):
    return render(request, "browsebook.html")


def browsecustomer(request):
    return render(request, "browsecustomer.html")


def recommendedbooks(request):
    return render(request, "recommendedbooks.html")


def degreeofseprsearch(request):
    return render(request, "degreeofseprsearch.html")


def stockmanage(request):
    return render(request, "stockmanage.html")


def bookmanage(request):
    return render(request, "bookmanage.html")


def addbook(request):
    return render(request, "addbook.html")


def statistics(request):
    return render(request, "statistics.html")


def bookstatistics(request):
    return render(request, "bookstatistics.html")


def userstatistics(request):
    return render(request, "userstatistics.html")


def managerdata(request):
    return render(request, "managerdata.html")


def addmanager(request):
    return render(request, "addmanager.html")


def bookinfo(request):
    return render(request, "bookinfo.html")


def customerinfo(request):
    return render(request, "customerinfo.html")


def customerprofile(request):
    return render(request, "customerprofile.html")
