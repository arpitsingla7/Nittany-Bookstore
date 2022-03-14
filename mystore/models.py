from django.db import models
from django.core.validators import MinLengthValidator
from django.core.validators import MaxLengthValidator
from django.db.models import UniqueConstraint

# Create your models here.

# **************registering users***************


class registerdb(models.Model):
    username = models.CharField(
        max_length=30, primary_key=True, blank=False, null=False, unique=True)
    firstname = models.CharField(max_length=30, blank=False, null=False)
    lastname = models.CharField(max_length=30, blank=False, null=False)
    phone = models.CharField(max_length=10, blank=False, null=False)
    address = models.CharField(max_length=100, blank=False, null=False)
    password = models.CharField(max_length=20, blank=False, null=False)
    userlevel = models.CharField(
        max_length=10, blank=False, null=False, default="0")
    isactive = models.IntegerField(default=0)

    # **************adding books***************


class bookdb(models.Model):
    isbn = models.CharField(max_length=13, primary_key=True, blank=False, validators=[
        MinLengthValidator(13)], null=False)
    title = models.CharField(max_length=150, blank=False, null=False)
    publisher = models.CharField(max_length=100, blank=False, null=False)
    language = models.CharField(max_length=20, blank=False, null=False)
    pubdate = models.DateField(
        auto_now_add=False, auto_now=False, blank=False, null=False)
    pages = models.PositiveIntegerField(blank=False, null=False)
    price = models.PositiveIntegerField(blank=False, null=False)
    subject = models.CharField(max_length=50, blank=False, null=False)
    currentstock = models.PositiveIntegerField(blank=False, null=False)
    keywordm = models.CharField(
        max_length=150, blank=False, default='null', null=False)
    author = models.CharField(
        max_length=150, blank=False, null=False, default='empty')


class commentdb(models.Model):
    username = models.ForeignKey(registerdb, on_delete=models.CASCADE)
    book = models.ForeignKey(bookdb, on_delete=models.CASCADE)
    text = models.TextField()
    date = models.DateField(auto_now_add=True)
    score = models.IntegerField(choices=((0, '0'), (1, '1'), (2, '2'), (3, '3'), (
        4, '4'), (5, '5'), (6, '6'), (7, '7'), (8, '8'), (9, '9'), (10, '10')), default='null')
    bookscore = models.IntegerField(default=0)

# comment usefullness rating to other customer's comment


class ratingdb(models.Model):
    rater = models.CharField(max_length=100)
    rating = models.PositiveIntegerField()
    user = models.ForeignKey(registerdb, on_delete=models.CASCADE)
    commentdb = models.ForeignKey(commentdb, on_delete=models.CASCADE)
    isbn = models.ForeignKey(bookdb, on_delete=models.CASCADE)

# trust rating table for other customers


class trust(models.Model):
    trustedby = models.ForeignKey(
        registerdb, on_delete=models.CASCADE, related_name='trustedby')
    trusting = models.ForeignKey(
        registerdb, on_delete=models.CASCADE, related_name='trusting')
    trustscore = models.IntegerField()


class orderinfo(models.Model):
    book = models.ForeignKey(bookdb, on_delete=models.CASCADE)
    customer = models.ForeignKey(registerdb, on_delete=models.CASCADE)
    order_date = models.DateField(auto_now_add=True)
    copies = models.PositiveIntegerField()
    amount = models.PositiveIntegerField()
    order_status = models.CharField(max_length=50, default='not delivered')


class reqbook(models.Model):
    isbn = models.CharField(max_length=13)
    title = models.CharField(max_length=150, blank=False, null=False)
    username = models.CharField(
        max_length=30)
    requeststatus = models.CharField(max_length=50, default='No Updates')

# not using the table, created by mistake


class authordb(models.Model):
    isbn = models.ForeignKey(bookdb, on_delete=models.CASCADE,
                             primary_key=True, blank=False, validators=[MinLengthValidator(13)], null=False, unique=True)
    author = models.CharField(
        max_length=100, blank=False, null=False, unique=True)

    class Meta:
        UniqueConstraint(fields=['isbn', 'author'], name='unique author')

        #unique_together = [['isbn', 'author']]


# **************registering managers***************


class managerdb(models.Model):
    username = models.ForeignKey(
        registerdb, on_delete=models.CASCADE, null=False)
    managerid = models.BigAutoField(primary_key=True, null=False)


# *************************************************************************************
