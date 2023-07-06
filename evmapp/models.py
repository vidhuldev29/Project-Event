from django.db import models
from django.core.validators import RegexValidator
from datetime import date, timedelta

# Create your models here.

class User(models.Model):
    name = models.CharField(max_length=25)
    username = models.CharField(max_length=25,primary_key=True)
    email = models.EmailField()
    phone = models.CharField(max_length=10, validators=[RegexValidator(r'^\d{10}$', 'Enter a valid phone number.')])
    password = models.CharField(max_length=20)
    confirmpassword = models.CharField(max_length=20)

    def __str__(self):
        return self.username

class Admin(models.Model):
    admin_username = models.CharField(max_length=25,primary_key=True)
    password = models.CharField(max_length=20)
    def __str__(self):
        return self.admin_username

class login(models.Model):
    username=models.CharField(max_length=25)
    password=models.CharField(max_length=20)
    def __str__(self):
        return self.username



class convention(models.Model):
    image = models.FileField()
    name = models.CharField(max_length=100)
    seating = models.IntegerField()
    dining = models.IntegerField()
    parking = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    place = models.CharField(max_length=100)
    district = models.CharField(max_length=25)

    def __str__(self):
        return self.name


class GalleryImage(models.Model):
    convention = models.ForeignKey(convention, on_delete=models.CASCADE, related_name='gallery_images', null=True)
    image = models.ImageField(upload_to='gallery')

    def __str__(self):
        return f"Gallery image of {self.convention.name}"


class catering(models.Model):
    image=models.FileField()
    name=models.CharField(max_length=100)
    avg_menu_charge=models.FloatField(null=True)
    delivery = models.BooleanField(default=False)
    service_staff = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=10, validators=[RegexValidator(r'^\d{10}$', 'Enter a valid phone number.')])
    location=models.CharField(max_length=1000)
    def __str__(self):
        return self.name

class cateringmenu(models.Model):
    catering = models.ForeignKey(catering, on_delete=models.CASCADE, related_name='catering_menu')
    menu = models.TextField()

    def get_menu_list(self):
        """
        Returns a list of tuples representing the menu items and their prices.
        """
        menu_items = self.menu.split('\n')
        menu_list = []
        for item in menu_items:
            if item.strip():
                item_split = item.strip().split(':')
                if len(item_split) == 2:
                    item_name = item_split[0].strip()
                    item_price = item_split[1].strip()
                    menu_list.append((item_name, item_price))
        return menu_list

    def __str__(self):
        return f"Menu for {self.catering.name}"

class decoration(models.Model):
    image = models.FileField()
    name = models.CharField(max_length=100)
    style = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=10, validators=[RegexValidator(r'^\d{10}$', 'Enter a valid phone number.')])
    price = models.DecimalField(max_digits=8, decimal_places=2)
    def __str__(self):
        return self.name

class photography(models.Model):
    image = models.FileField()
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=10, validators=[RegexValidator(r'^\d{10}$', 'Enter a valid phone number.')])
    price = models.IntegerField()
    location=models.CharField(max_length=1000)
    def __str__(self):
        return self.name

class PreviousWorks(models.Model):
    studio = models.ForeignKey(photography, on_delete=models.CASCADE, related_name='previous_works_images')
    image = models.ImageField(upload_to='previous_works')

    def __str__(self):
        return f"Previous works images of {self.studio.name}"


class accommodation(models.Model):
    image = models.FileField()
    name = models.CharField(max_length=100)
    restaurant=models.BooleanField(default=False)
    swimming_pool=models.BooleanField(default=False)
    campfire=models.BooleanField(default=False)
    fitness_center=models.BooleanField(default=False)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    place = models.CharField(max_length=100)
    district = models.CharField(max_length=25)
    def __str__(self):
        return self.name

class photos_collection(models.Model):
    hotel = models.ForeignKey(accommodation, on_delete=models.CASCADE, related_name='photos_collection_images')
    image = models.ImageField(upload_to='photos_collection')

    def __str__(self):
        return f"Photos of {self.hotel.name}"


class entertainment(models.Model):
    image = models.FileField()
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=10, validators=[RegexValidator(r'^\d{10}$', 'Enter a valid phone number.')])
    price = models.DecimalField(max_digits=8, decimal_places=2)
    def __str__(self):
        return self.name


class transportation(models.Model):
    image = models.FileField()
    name = models.CharField(max_length=100)
    bus = models.BooleanField(default=False)
    traveller = models.BooleanField(default=False)
    cars = models.BooleanField(default=False)
    avg_km_charge=models.FloatField(null=True)
    place = models.CharField(max_length=25)
    district = models.CharField(max_length=25)
    phone_number = models.CharField(max_length=10, validators=[RegexValidator(r'^\d{10}$', 'Enter a valid phone number.')])
    def __str__(self):
        return self.name


class Convention_Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name=models.CharField(max_length=25)
    phone_number = models.CharField(max_length=10, validators=[RegexValidator(r'^\d{10}$', 'Enter a valid phone number.')])
    convention_name = models.ForeignKey(convention, on_delete=models.CASCADE)
    date=models.DateField()
    type=models.CharField(max_length=100)
    def __str__(self):
        return self.name

    def is_deletable(self):
        today = date.today()
        deletable_date = self.date - timedelta(days=3)
        print(f"Today's Date: {today}")
        print(f"Deletable Date: {deletable_date}")
        return today <= deletable_date

class Catering_Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=25)
    phone_number = models.CharField(max_length=10, validators=[RegexValidator(r'^\d{10}$', 'Enter a valid phone number.')])
    catering_name = models.ForeignKey(catering, on_delete=models.CASCADE)
    guest=models.IntegerField(null=True)
    date=models.DateField()
    message=models.TextField()
    location=models.TextField()
    def __str__(self):
        return self.name

    def is_deletable(self):
        today = date.today()
        deletable_date = self.date - timedelta(days=3)
        print(f"Today's Date: {today}")
        print(f"Deletable Date: {deletable_date}")
        return today <= deletable_date

class Decoration_Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=25)
    phone_number = models.CharField(max_length=10, validators=[RegexValidator(r'^\d{10}$', 'Enter a valid phone number.')])
    decoration_name = models.ForeignKey(decoration, on_delete=models.CASCADE)
    date=models.DateField()
    location=models.TextField()
    def __str__(self):
        return self.name

    def is_deletable(self):
        today = date.today()
        deletable_date = self.date - timedelta(days=3)
        print(f"Today's Date: {today}")
        print(f"Deletable Date: {deletable_date}")
        return today <= deletable_date

class Photography_Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=25)
    phone_number = models.CharField(max_length=10, validators=[RegexValidator(r'^\d{10}$', 'Enter a valid phone number.')])
    studio_name = models.ForeignKey(photography, on_delete=models.CASCADE)
    event_type=models.CharField(max_length=250,null=True)
    date=models.DateField()
    def __str__(self):
        return self.name

    def is_deletable(self):
        today = date.today()
        deletable_date = self.date - timedelta(days=3)
        print(f"Today's Date: {today}")
        print(f"Deletable Date: {deletable_date}")
        return today <= deletable_date

class Entertainment_Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=25)
    phone_number = models.CharField(max_length=10, validators=[RegexValidator(r'^\d{10}$', 'Enter a valid phone number.')])
    program_service_name = models.ForeignKey(entertainment, on_delete=models.CASCADE)
    date=models.DateField()
    location=models.TextField()
    def __str__(self):
        return self.name

    def is_deletable(self):
        today = date.today()
        deletable_date = self.date - timedelta(days=3)
        print(f"Today's Date: {today}")
        print(f"Deletable Date: {deletable_date}")
        return today <= deletable_date

class Accommodation_Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=25)
    phone_number = models.CharField(max_length=10, validators=[RegexValidator(r'^\d{10}$', 'Enter a valid phone number.')])
    hotel_name = models.ForeignKey(accommodation, on_delete=models.CASCADE)
    rooms=models.IntegerField()
    date=models.DateField()
    def __str__(self):
        return self.name

    def is_deletable(self):
        today = date.today()
        deletable_date = self.date - timedelta(days=3)
        print(f"Today's Date: {today}")
        print(f"Deletable Date: {deletable_date}")
        return today <= deletable_date

class Transportation_Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=25)
    phone_number = models.CharField(max_length=10, validators=[RegexValidator(r'^\d{10}$', 'Enter a valid phone number.')])
    travels_name = models.ForeignKey(transportation, on_delete=models.CASCADE)
    km=models.IntegerField(null=True)
    date = models.DateField()
    message=models.TextField()
    location = models.TextField()
    def __str__(self):
        return self.name

    def is_deletable(self):
        today = date.today()
        deletable_date = self.date - timedelta(days=3)
        print(f"Today's Date: {today}")
        print(f"Deletable Date: {deletable_date}")
        return today <= deletable_date
