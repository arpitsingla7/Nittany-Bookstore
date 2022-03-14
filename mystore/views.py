from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Avg, Max, Min, Count
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Exists
from django.contrib import messages
from django.db.models import Q
from mystore import models
from mystore.models import registerdb, bookdb, managerdb, authordb, commentdb, ratingdb, trust, orderinfo, reqbook
from django.db.models import Sum
from .forms import CreateUserForm


def index(request):
    return render(request, 'mystore/index.html')


def register(request):
    if request.method == "POST":

        username = request.POST.get('username', 'm')
        firstname = request.POST.get('firstname', 'm')
        lastname = request.POST.get('lastname', 'm')
        address = request.POST.get('address', 'm')
        phone = request.POST.get('phone', 'm')
        password = request.POST.get('pass', 'm')

        if(username == 'm' or firstname == 'm' or lastname == 'm' or address == 'm' or phone == 'm' or password == 'm' or username == '' or firstname == '' or lastname == '' or address == '' or phone == '' or password == ''):
            messages.error(
                request, 'Error, either something is left empty or is invalid!')
            return render(request, 'mystore/register.html')
        else:
            ins = registerdb(username=username, firstname=firstname, lastname=lastname, phone=phone,
                             address=address, password=password)
            ins.save()
            return render(request, 'mystore/login.html')
    else:
        return render(request, 'mystore/register.html')


def loginpage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        all_customers = registerdb.objects.get(
            username=username, password=password)

        if (all_customers.username == username and all_customers.password == password):

            all_customers = registerdb.objects.filter(
                username=username).update(isactive=int(1))
            all_customers = registerdb.objects.get(username=username)
            context = {'all_customers': all_customers}
            print(all_customers)
            print(all_customers.userlevel)
            if (int(all_customers.userlevel) == 0):
                return render(request, "mystore/bookstorehpuser.html", context)
            else:
                return render(request, "mystore/bookstorehpmanager.html", context)
        else:
            messages.info(request, 'Username OR Password is incorrect')

    return render(request, 'mystore/login.html')


def logoutuser(request):
    username = request.POST.get('username')
    all_customers = registerdb.objects.get(isactive=1)
    username = all_customers.username
    registerdb.objects.filter(
        username=username).update(isactive=int(0))
    logout(request)
    return redirect('login')


# @login_required(login_url='login')
def bookstorehpuser(request):
    if request.method == 'POST':
        all_customers = registerdb.objects.get(isactive=1)
        userlevel = int(all_customers.userlevel)
        context = {'all_customers': all_customers}
        if (userlevel == 0):
            return render(request, 'mystore/bookstorehpuser.html', context)
        else:
            return render(request, 'mystore/bookstorehpmanager.html', context)

    ''' if request.method == "POST":
        print("this is post in user dashboard")
        username = request.post('username')
        print(username)

    all_customers = registerdb.objects.get(username__iexact=username)
    template = loader.get_template('mystore/bookstorehpuser.html')

    if all_customers:
        # return HttpResponse(template.render(context, request))
        return render(request, 'mystore/bookstorehpuser.html')

    else:

    return HttpResponse('<h1>the username doesnt exist</h1>')'''


# @login_required(login_url='login')
def bookstorehpmanager(request):
    if request.method == 'POST':
        all_customers = registerdb.objects.get(isactive=1)
        userlevel = int(all_customers.userlevel)
        context = {'all_customers': all_customers}

        if (userlevel == 0):
            return render(request, 'mystore/bookstorehpuser.html', context)
        else:
            return render(request, 'mystore/bookstorehpmanager.html', context)


# @login_required(login_url='login')
def browsebook(request):
    print('inside browsebook')
    sterm = request.GET.get('sterm', 'default')
    print(sterm)
    return render(request, "mystore/browsebook.html")


# @login_required(login_url='login')
def search(request):
    sterm = request.GET['sterm']
    searchby = request.GET['searchby']
    orderby = request.GET['orderby']

    if (searchby == 'author'):

        if (orderby == 'year'):
            all_books = bookdb.objects.filter(
                author__icontains=sterm).order_by('-pubdate')
            bookscore = commentdb.objects.filter(
                book=all_books).aggregate(Avg('bookscore'))

            context = {'all_books': all_books,
                       'bookscore': bookscore}

            return render(request, "mystore/browsebook.html", context)

        elif (orderby == 'score'):
            all_books = bookdb.objects.filter(
                author__icontains=sterm).order_by('-score')
            context = {'all_books': all_books}

            return render(request, "mystore/browsebook.html", context)

        else:
            all_books = bookdb.objects.filter(author__icontains=sterm)
            context = {'all_books': all_books}

            return render(request, "mystore/browsebook.html", context)

    elif (searchby == 'publisher'):
        if (orderby == 'year'):
            all_books = bookdb.objects.filter(
                publisher__icontains=sterm).order_by('-pubdate')
            context = {'all_books': all_books}

            return render(request, "mystore/browsebook.html", context)

        elif (orderby == 'score'):
            all_books = bookdb.objects.filter(
                publisher__icontains=sterm).order_by('-score')
            context = {'all_books': all_books}

            return render(request, "mystore/browsebook.html", context)

        else:
            all_books = bookdb.objects.filter(publisher__icontains=sterm)
            context = {'all_books': all_books}

            return render(request, "mystore/browsebook.html", context)

    elif (searchby == 'title'):
        if (orderby == 'year'):
            all_books = bookdb.objects.filter(
                title__icontains=sterm).order_by('-pubdate')
            context = {'all_books': all_books}

            return render(request, "mystore/browsebook.html", context)

        elif (orderby == 'score'):
            all_books = bookdb.objects.filter(
                title__icontains=sterm).order_by('-score')
            context = {'all_books': all_books}

            return render(request, "mystore/browsebook.html", context)

        else:
            all_books = bookdb.objects.filter(title__icontains=sterm)
            context = {'all_books': all_books}

            return render(request, "mystore/browsebook.html", context)

    elif (searchby == 'language'):
        if (orderby == 'year'):
            all_books = bookdb.objects.filter(
                language__icontains=sterm).order_by('-pubdate')
            context = {'all_books': all_books}

            return render(request, "mystore/browsebook.html", context)

        elif (orderby == 'score'):
            all_books = bookdb.objects.filter(
                language__icontains=sterm).order_by('-score')
            context = {'all_books': all_books}

            return render(request, "mystore/browsebook.html", context)

        else:
            all_books = bookdb.objects.filter(language__icontains=sterm)
            context = {'all_books': all_books}

            return render(request, "mystore/browsebook.html", context)

    else:
        return render(request, "mystore/browsebook.html")


# @login_required(login_url='login')
def browsecustomer(request):
    all_customers = registerdb.objects.all()
    template = loader.get_template('mystore/browsecustomer.html')
    context = {
        'all_customers': all_customers,
    }

    return HttpResponse(template.render(context, request))


# @login_required(login_url='login')
def customerprofile(request, username):
    all_customers = registerdb.objects.get(username__iexact=username)
    all_comments = commentdb.objects.filter(username=username)
    trusting = registerdb.objects.get(username=username)
    totaltrust = trust.objects.filter(trusting=trusting, trustscore=1).count()

    totalnottrust = trust.objects.filter(
        trusting=trusting, trustscore=0).count()

    template = loader.get_template('mystore/customerprofile.html')
    context = {
        'all_customers': all_customers,
        'all_comments': all_comments,
        'totaltrust': totaltrust,
        'totalnottrust': totalnottrust,
    }

    return HttpResponse(template.render(context, request))


def addtrust(request, username):
    if request.method == 'POST':
        trustscore = int(request.POST.get('trustscore', '3'))
        trusting = registerdb.objects.get(username=username)
        trustedby = registerdb.objects.get(isactive=1)
        trustedbyu = trustedby.username
        alreadypresent = int(trust.objects.filter(
            trusting=trusting, trustedby=trustedby).count())

        if ((trustscore == 1 or trustscore == 0) and trustedbyu != username):

            if (alreadypresent == 0):

                trustscore = int(request.POST.get('trustscore', '3'))

                ins = trust(trustedby=trustedby, trusting=trusting,
                            trustscore=trustscore)
                ins.save()
            else:
                trustscore = int(request.POST.get('trustscore', '3'))
                trust.objects.filter(
                    trustedby=trustedby, trusting=trusting,).update(trustscore=trustscore)

            all_customers = registerdb.objects.get(username__iexact=username)
            all_comments = commentdb.objects.filter(username=username)

            totaltrust = trust.objects.filter(
                trusting=trusting, trustscore=1).count()

            totalnottrust = trust.objects.filter(
                trusting=trusting, trustscore=0).count()

            template = loader.get_template('mystore/customerprofile.html')
            context = {
                'all_customers': all_customers,
                'all_comments': all_comments,
                'totaltrust': totaltrust,
                'totalnottrust': totalnottrust,
            }
            messages.success(
                request, 'you have successfully updated the trust rating ')

            return HttpResponse(template.render(context, request))

        else:
            messages.error(
                request, 'trust rating not valid OR you are giving trust rating to yourself OR you have already trusted this user')

            all_customers = registerdb.objects.get(username__iexact=username)
            all_comments = commentdb.objects.filter(username=username)

            totaltrust = trust.objects.filter(
                trusting=trusting, trustscore=1).count()

            totalnottrust = trust.objects.filter(
                trusting=trusting, trustscore=0).count()

            template = loader.get_template('mystore/customerprofile.html')
            context = {
                'all_customers': all_customers,
                'all_comments': all_comments,
                'totaltrust': totaltrust,
                'totalnottrust': totalnottrust,
            }

            return HttpResponse(template.render(context, request))


# @login_required(login_url='login')
def degreeofseprsearch(request):
    return render(request, "mystore/degreeofseprsearch.html")


# @login_required(login_url='login')
def stockmanage(request):
    all_books = bookdb.objects.all()
    template = loader.get_template('mystore/stockmanage.html')
    context = {
        'all_books': all_books,
    }

    return HttpResponse(template.render(context, request))


# @login_required(login_url='login')
def bookmanage(request, isbn):

    if request.method == "POST":
        newstock = request.POST.get('newstock', 'default')
        all_books = bookdb.objects.filter(
            isbn=isbn).update(currentstock=int(newstock))

        all_books = bookdb.objects.get(isbn__iexact=isbn)
        bookscore = commentdb.objects.filter(
            book=isbn).aggregate(Avg('bookscore'))
        template = loader.get_template('mystore/bookmanage.html')
        context = {
            'all_books': all_books,
            'bookscore': bookscore,
        }

        return HttpResponse(template.render(context, request))

    else:
        all_books = bookdb.objects.get(isbn__iexact=isbn)
        bookscore = commentdb.objects.filter(
            book=isbn).aggregate(Avg('bookscore'))
        template = loader.get_template('mystore/bookmanage.html')
        context = {
            'all_books': all_books,
            'bookscore': bookscore,
        }

        return HttpResponse(template.render(context, request))


# @login_required(login_url='login')
def addbook(request):

    if request.method == "POST":
        print("inside post")
        temp = request.POST.get('isbn', 'default')
        print(temp)
        if (temp == 'default'):
            print("inside if of post")
            return render(request, "mystore/addbook.html")

        else:
            print("inside else of post")
            isbn = request.POST.get('isbn', 'default')
            title = request.POST.get('title', 'default')
            publisher = request.POST.get('publisher', 'default')
            language = request.POST.get('language', 'default')
            price = request.POST.get('price', '0')
            pubdate = request.POST.get('date', '2021-04-28')
            pages = request.POST.get('pages', '0')
            keywordm = request.POST.get('keywords', 'default')
            subject = request.POST.get('subject', 'default')
            currentstock = request.POST.get('stock', '0')
            author = request.POST.get('author', 'default')

            print(isbn)
            # if request.POST['username'] == '':
            #   return render(request, 'mystore/register.html', {'error': 'Please fill all the fileds '})

            ins = bookdb(isbn=isbn, title=title, publisher=publisher, language=language,
                         pubdate=pubdate, pages=pages, price=price, subject=subject, currentstock=currentstock, keywordm=keywordm, author=author)
            ins.save()
            print("the data has been saved")
            return render(request, "mystore/addbook.html")


# @login_required(login_url='login')
def managerdata(request):
    all_customers = registerdb.objects.all()
    template = loader.get_template('mystore/managerdata.html')
    context = {
        'all_customers': all_customers,
    }

    return HttpResponse(template.render(context, request))


# @login_required(login_url='login')
def addmanager(request, username):
    all_customers = registerdb.objects.get(username__iexact=username)
    template = loader.get_template('mystore/addmanager.html')
    context = {
        'all_customers': all_customers,
    }

    return HttpResponse(template.render(context, request))


def changeaccess(request, username):
    if request.method == "POST":
        accesslevel = request.POST.get('accesslevel', 'default')
        if accesslevel == '1' or accesslevel == '0':
            all_customers = registerdb.objects.filter(
                username=username).update(userlevel=accesslevel)

        else:
            messages.error(request, 'please input a valid value')

            all_customers = registerdb.objects.get(username__iexact=username)
            template = loader.get_template('mystore/addmanager.html')
            context = {
                'all_customers': all_customers,
            }

            return HttpResponse(template.render(context, request))

    return redirect('managerdata')


# @login_required(login_url='login')
def bookinfo(request, isbn):

    all_books = bookdb.objects.get(isbn__iexact=isbn)
    all_comments = commentdb.objects.filter(book=isbn)
    bookscore = commentdb.objects.filter(
        book=isbn).aggregate(Avg('bookscore'))

    rater = registerdb.objects.get(isactive=int(1)).username

    stockpresent = (all_books.currentstock)

    if stockpresent > 0:
        say = 'Y'

    else:
        say = 'N'

    totalrating = ratingdb.objects.filter(
        isbn=all_books).aggregate(Sum('user', distinct='True'))

    template = loader.get_template('mystore/bookinfo.html')
    print(totalrating)
    context = {
        'all_books': all_books,
        'all_comments': all_comments,
        'bookscore': bookscore,
        'totalrating': totalrating,
        'say': say
    }

    return HttpResponse(template.render(context, request))


'''if request.method == 'GET':
        m = int(request.get['m'])
        comments = int(commentdb.objects.filter(book=isbn).count())
        if(m < comments):
            all_comments = commentdb.objects.filter(book=isbn).order_by('-')


        else:
            messages.error(request, 'm is too large or invalid')

        all_comments = commentdb.objects.filter()
        context = {'all_books': all_books}

        return render(request, "mystore/browsebook.html", context)
'''


def addcomment(request, isbn):
    if request.method == 'POST':
        commenter1 = registerdb.objects.get(isactive=int(1))
        commenter = commenter1.username
        presentcomm = int(commentdb.objects.filter(
            username=commenter, book=isbn).count())

        if(presentcomm == 0):
            bookscore = int(request.POST.get('bookscore', 'n'))
            if (bookscore < int(11) and bookscore >= int(0)):
                text = request.POST.get('usercomment', '')
                bookscore = request.POST.get('bookscore', 'n')
                book = bookdb.objects.get(isbn=isbn)
                username = registerdb.objects.get(username=commenter)
                ins = commentdb(text=text, username=username,
                                book=book, bookscore=bookscore, score=int(0))
                ins.save()

                all_books = bookdb.objects.get(isbn__iexact=isbn)
                all_comments = commentdb.objects.filter(book=isbn)
                bookscore = commentdb.objects.filter(
                    book=isbn).aggregate(Avg('bookscore'))
                template = loader.get_template('mystore/bookinfo.html')
                context = {
                    'all_books': all_books,
                    'all_comments': all_comments,
                    'bookscore': bookscore,
                }

                return HttpResponse(template.render(context, request))

            else:
                all_books = bookdb.objects.get(isbn__iexact=isbn)
                all_comments = commentdb.objects.filter(book=isbn)
                bookscore = commentdb.objects.filter(
                    book=isbn).aggregate(Avg('bookscore'))
                template = loader.get_template('mystore/bookinfo.html')
                context = {
                    'all_books': all_books,
                    'all_comments': all_comments,
                    'bookscore': bookscore,
                }
                messages.error(request, 'score box is not valid')

                return HttpResponse(template.render(context, request))
        else:
            all_books = bookdb.objects.get(isbn__iexact=isbn)
            all_comments = commentdb.objects.filter(book=isbn)
            bookscore = commentdb.objects.filter(
                book=isbn).aggregate(Avg('bookscore'))
            template = loader.get_template('mystore/bookinfo.html')
            context = {
                'all_books': all_books,
                'all_comments': all_comments,
                'bookscore': bookscore,
            }
            messages.error(
                request, 'you have already commented once on this book')

            return HttpResponse(template.render(context, request))


def editcomment(request, username, isbn):
    # username is the persons's comment
    if request.method == 'POST':
        editor = registerdb.objects.get(isactive=int(1))
        editor = editor.username

        if(username == editor):
            editcomment = request.POST.get('editcomment')
            editor = registerdb.objects.get(isactive=int(1))
            book = bookdb.objects.get(isbn=isbn)
            all_customers = commentdb.objects.filter(
                username=editor, book=book).update(text=editcomment)

            return customerprofile(request, username)

        else:
            messages.error(request, 'You cannot change this comment!')
            return customerprofile(request, username)


def deletecomment(request, username, isbn):
    # username is the persons's comment
    if request.method == 'POST':
        editor = registerdb.objects.get(isactive=int(1))
        editor = editor.username

        if(username == editor):
            editor = registerdb.objects.get(isactive=int(1))
            book = bookdb.objects.get(isbn=isbn)
            all_customers = commentdb.objects.filter(
                username=editor, book=book).delete()
            messages.success(
                request, 'You have successfully deleted the comment')
            return customerprofile(request, username)

        else:
            messages.error(
                request, 'You dont have the authority to delete this comment!')
            return customerprofile(request, username)


def changebookscore(request, username, isbn):
    # username is the persons's comment
    if request.method == 'POST':
        editor = registerdb.objects.get(isactive=int(1))
        editor = editor.username
        bookscore = int(request.POST.get('bookscore'))
        if(username == editor and bookscore <= 10 and bookscore >= 0):
            bookscore = request.POST.get('bookscore')
            editor = registerdb.objects.get(isactive=int(1))
            book = bookdb.objects.get(isbn=isbn)
            all_customers = commentdb.objects.filter(
                username=editor, book=book).update(bookscore=int(bookscore))
            messages.success(request, 'Book score successfully changed')
            return customerprofile(request, username)

        else:
            messages.error(
                request, 'either you dont have the authority to change the bookscore or its out of range (1-10)!')
            return customerprofile(request, username)


def addusefullness(request, username, isbn):
    passisbn = isbn
    if request.method == 'POST':
        rater = registerdb.objects.get(isactive=int(1))
        rater = rater.username

        rating = int(request.POST.get('rating'))

        if(username != rater and (rating == 1 or rating == 2 or rating == 3)):

            rating = int(request.POST.get('rating'))
            user = registerdb.objects.get(username=username)
            isbn = bookdb.objects.get(isbn=isbn)
            commentdbv = commentdb.objects.get(book=isbn, username=user)

            mcount = int(ratingdb.objects.filter(isbn=isbn, commentdb=commentdbv,
                                                 rater=rater, user=user).count())
            if (mcount == 0):
                ins = ratingdb(isbn=isbn, commentdb=commentdbv,
                               rater=rater, rating=rating, user=user)
                ins.save()
            else:
                ratingdb.objects.filter(isbn=isbn, commentdb=commentdbv,
                                        rater=rater, user=user).update(rating=rating)

            messages.success(
                request, 'Successfully update the usefullness rating')
            return bookinfo(request, passisbn)

        else:
            messages.error(
                request, 'Error, either you are giving yourself a rating or the rating is out of bounds')
            return bookinfo(request, passisbn)

    return render(request, "mystore/customerinfo.html")


def orderhistory(request):

    customer = registerdb.objects.get(isactive=int(1))
    all_orders = orderinfo.objects.filter(customer=customer)

    template = loader.get_template('mystore/orderhistory.html')
    context = {
        'all_orders': all_orders,
    }

    return HttpResponse(template.render(context, request))


def orderplace(request, isbn):
    if request.method == 'POST':
        copies = int(request.POST.get('quantity'))
        book = bookdb.objects.get(isbn=isbn)
        stock = int(book.currentstock) - copies
        if (copies > 0 and stock > 0):
            customer = registerdb.objects.get(isactive=int(1))
            book = bookdb.objects.get(isbn=isbn)
            stock = int(book.currentstock) - copies
            bookdb.objects.filter(isbn=isbn).update(currentstock=stock)
            tamount = copies * (book.price)
            order_status = 'not delivered'

            ins = orderinfo(customer=customer, book=book, amount=tamount,
                            copies=copies, order_status=order_status)
            ins.save()

            return orderhistory(request)

        else:
            return HttpResponse('<h1>quantity ordered is not valid! Either enter a positive quanity or order less quantity</h1>')


# @login_required(login_url='login')


def recommendedbooks(request):
    print('inside reccc')
    customer = registerdb.objects.get(isactive=int(1))
    all_orders = orderinfo.objects.filter(
        Q(customer=customer)).distinct()

    books = orderinfo.objects.filter(customer=customer)

    other_orders = orderinfo.objects.exclude(
        Q(customer=customer)).distinct()

    template = loader.get_template('mystore/recommendedbooks.html')
    context = {
        'all_orders': all_orders,
    }

    return HttpResponse(template.render(context, request))


# @login_required(login_url='login')
def statistics(request):
    return render(request, "mystore/statistics.html")


# @login_required(login_url='login')
def bookstatistics(request):
    orderby = request.POST.get('orderby')

    if request.method == 'POST':
        mval = int(request.POST.get('mval'))

        if mval > 0:
            allorders = orderinfo.objects.filter()

            print()

    return render(request, "mystore/bookstatistics.html")


# @login_required(login_url='login')
def userstatistics(request):
    ''' if request.method == 'POST':
         mval = int(request.POST.get('mval'))
         trustc = int(trust.objects.filter(trustscore=1).count())
         trustnotc = int(trust.objects.filter(trustscore=0).count()'''

    return render(request, "mystore/userstatistics.html")


def deliverystatus(request):

    if request.method == 'POST':
        all_orders = orderinfo.objects.filter(
            Q(order_status='not delivered') | Q(order_status='pending') | Q(order_status='delivered'))

        template = loader.get_template('mystore/deliverystatus.html')
        context = {
            'all_orders': all_orders,
        }

    return HttpResponse(template.render(context, request))


def changestatus(request, id):

    if request.method == 'POST':
        statuschange = request.POST.get('statuschange')

        orderinfo.objects.filter(id=id).update(order_status=statuschange)
        return deliverystatus(request)

    # return HttpResponse(template.render(context, request))


def deletebook(request, isbn):

    if request.method == 'POST':
        bookdb.objects.filter(isbn=isbn).delete()
        messages.success(
            request, 'You have successfully deleted the book')

        all_books = bookdb.objects.all()
        template = loader.get_template('mystore/stockmanage.html')
        context = {
            'all_books': all_books,
        }

        return HttpResponse(template.render(context, request))

    return HttpResponse(template.render(context, request))


def requestbook(request):

    username = registerdb.objects.get(isactive=int(1)).username
    all_books = reqbook.objects.filter(username=username)
    template = loader.get_template('mystore/requestbook.html')
    context = {
        'all_books': all_books,
    }

    return HttpResponse(template.render(context, request))


def requestbutton(request):
    if request.method == 'POST':
        isbn = request.POST.get('isbn')
        leng = len(str(isbn))
        username = registerdb.objects.get(isactive=int(1)).username
        isbn = request.POST.get('isbn', 'default')
        coun = reqbook.objects.filter(isbn=isbn, username=username).count()

        if(leng > 0 and coun == 0):
            username = registerdb.objects.get(isactive=int(1)).username
            isbn = request.POST.get('isbn', 'default')
            title = request.POST.get('title', 'default')
            requeststatus = 'No Updates'
            ins = reqbook(username=username, isbn=isbn,
                          title=title, requeststatus=requeststatus)
            ins.save()

            all_books = reqbook.objects.filter(username=username)
            template = loader.get_template('mystore/requestbook.html')
            context = {
                'all_books': all_books,
            }

            return HttpResponse(template.render(context, request))
        else:
            messages.error(
                request, 'one of the fields is not valid or you have already requested the book')
            all_books = reqbook.objects.all()
            template = loader.get_template('mystore/requestbook.html')
            context = {
                'all_books': all_books,
            }

            return HttpResponse(template.render(context, request))


def changereqstatus(request, id):

    if request.method == 'POST':
        statuschange = request.POST.get('statuschange')

        reqbook.objects.filter(id=id).update(requeststatus=statuschange)
        return requestbstatus(request)


def requestbstatus(request):
    all_books = reqbook.objects.all()
    template = loader.get_template('mystore/requestbstatus.html')
    context = {
        'all_books': all_books,
    }

    return HttpResponse(template.render(context, request))
