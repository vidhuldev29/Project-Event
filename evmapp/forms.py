from django import forms
from .models import decoration,entertainment,transportation,catering,cateringmenu,convention,photography,accommodation,GalleryImage,PreviousWorks,photos_collection,Convention_Booking,Catering_Booking,Decoration_Booking,Photography_Booking,Entertainment_Booking,Accommodation_Booking,Transportation_Booking
from django.core.validators import RegexValidator
from datetime import date
from django.forms import formset_factory
from django.forms.widgets import SelectDateWidget
from django.utils import timezone
from multiupload.fields import MultiFileField

class DecorationForm(forms.ModelForm):
    phone_number = forms.CharField(validators=[RegexValidator(r'^\d{10}$', 'Enter a valid phone number.')])
    class Meta:
        model = decoration
        fields = ['image', 'name', 'style', 'phone_number', 'price']
        widgets = {
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'style': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
        }
        help_texts = {
            'phone_number': 'Enter a valid 10-digit phone number.',
        }

class EntertainmentForm(forms.ModelForm):
    phone_number = forms.CharField(validators=[RegexValidator(r'^\d{10}$', 'Enter a valid phone number.')])

    class Meta:
        model = entertainment
        fields = ['image', 'name', 'category', 'phone_number', 'price']
        widgets = {
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
        }
        help_texts = {
            'phone_number': 'Enter a valid 10-digit phone number.',
        }


class TransportationForm(forms.ModelForm):
    bus = forms.BooleanField(required=False)
    traveller = forms.BooleanField(required=False)
    cars = forms.BooleanField(required=False)
    phone_number = forms.CharField(validators=[RegexValidator(r'^\d{10}$', 'Enter a valid phone number.')])

    class Meta:
        model = transportation
        fields = ['image', 'name', 'bus', 'traveller', 'cars', 'avg_km_charge', 'place', 'district', 'phone_number']
        widgets = {
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'bus': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'traveller': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'cars': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'avg_km_charge': forms.NumberInput(attrs={'class': 'form-control'}),
            'place': forms.TextInput(attrs={'class': 'form-control'}),
            'district': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
        }
        help_texts = {
            'phone_number': 'Enter a valid 10-digit phone number.',
        }


class CateringForm(forms.ModelForm):
    delivery = forms.BooleanField(required=False)
    service_staff = forms.BooleanField(required=False)
    phone_number = forms.CharField(validators=[RegexValidator(r'^\d{10}$', 'Enter a valid phone number.')])

    class Meta:
        model = catering
        fields = ['image', 'name', 'avg_menu_charge', 'delivery', 'service_staff', 'phone_number', 'location']
        widgets = {
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'avg_menu_charge':forms.NumberInput(attrs={'class': 'form-control'}),
            'delivery': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'service_staff': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
        }
        help_texts = {
            'phone_number': 'Enter a valid 10-digit phone number.',
        }

class CateringMenuForm(forms.ModelForm):
    class Meta:
        model = cateringmenu
        fields = ['catering', 'menu']
        widgets = {
            'catering': forms.Select(attrs={'class': 'form-control'}),
            'menu': forms.Textarea(attrs={'class': 'form-control',
                                          'rows': 10,
                                          'placeholder': 'Enter menu items and prices separated by a colon (:), with each item on a new line.'
                                          }),
        }


class ConventionForm(forms.ModelForm):
    class Meta:
        model = convention
        fields = ['image', 'name', 'seating', 'dining', 'parking', 'price', 'place', 'district']
        widgets = {
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'seating': forms.NumberInput(attrs={'class': 'form-control'}),
            'dining': forms.NumberInput(attrs={'class': 'form-control'}),
            'parking': forms.NumberInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'place': forms.TextInput(attrs={'class': 'form-control'}),
            'district': forms.TextInput(attrs={'class': 'form-control'}),
        }

class ConventionGalleryForm(forms.ModelForm):
    images = MultiFileField(max_num=100, min_num=1, max_file_size=1024*1024*5, required=True)

    class Meta:
        model = GalleryImage
        fields = ['convention', 'images']
        widgets = {
            'convention': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean_images(self):
        images = self.cleaned_data['images']
        if not images:
            raise forms.ValidationError("Please select at least one image.")
        return images


class PhotographyForm(forms.ModelForm):
    phone_number = forms.CharField(validators=[RegexValidator(r'^\d{10}$', 'Enter a valid phone number.')])

    class Meta:
        model = photography
        fields = ['image', 'name', 'phone_number', 'price', 'location']
        widgets = {
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
        }

        help_texts = {
            'phone_number': 'Enter a valid 10-digit phone number.',
        }

class PreviousWorksForm(forms.ModelForm):
    images = MultiFileField(max_num=100, min_num=1, max_file_size=1024*1024*5, required=True)

    class Meta:
        model = PreviousWorks
        fields = ['studio', 'images']
        widgets = {
            'studio': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean_images(self):
        images = self.cleaned_data['images']
        if not images:
            raise forms.ValidationError("Please select at least one image.")
        return images



class AccommodationForm(forms.ModelForm):
    class Meta:
        model = accommodation
        fields = ['image', 'name', 'restaurant', 'swimming_pool', 'campfire', 'fitness_center', 'price', 'place', 'district']
        widgets = {
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'restaurant': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'swimming_pool': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'campfire': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'fitness_center': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'place': forms.TextInput(attrs={'class': 'form-control'}),
            'district': forms.TextInput(attrs={'class': 'form-control'}),
        }

class PhotosCollectionForm(forms.ModelForm):
    images = MultiFileField(max_num=100, min_num=1, max_file_size=1024*1024*5, required=True)

    class Meta:
        model = photos_collection
        fields = ['hotel', 'images']
        widgets = {
            'hotel': forms.Select(attrs={'class': 'form-control'}),
            'images': forms.ClearableFileInput(attrs={'class': 'form-control-file', 'multiple': True}),
        }

    def clean_images(self):
        images = self.cleaned_data['images']
        if not images:
            raise forms.ValidationError("Please select at least one image.")
        return images







class ConventionBookingForm(forms.ModelForm):
    phone_number = forms.CharField(validators=[RegexValidator(r'^\d{10}$', 'Enter a valid phone number.')])
    date = forms.DateField(
        widget=SelectDateWidget(attrs={'class': 'form-control'}, empty_label=("Year", "Month", "Day")),
        help_text='You can only book the dates from tomorrow.'
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['date'].initial = date.today() + timezone.timedelta(days=1)

    def clean_date(self):
        selected_date = self.cleaned_data['date']
        today = date.today()
        if selected_date <= today:
            raise forms.ValidationError('Invalid date. Please choose a future date.')
        return selected_date

    class Meta:
        model = Convention_Booking
        fields = ['name','phone_number','convention_name','date','type']  # Include all fields from the model

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Enter your Name'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Enter your Phone Number'}),
            'convention_name': forms.Select(attrs={'class':  'form-control'}),
            'date': forms.SelectDateWidget(attrs={'class': 'form-control'},
                                           empty_label=("Year", "Month", "Day")),
            'type': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Enter type of your Event'}),
        }
        help_texts = {
            'phone_number': 'Enter a valid 10-digit phone number.',
        }

class CateringBookingForm(forms.ModelForm):
    phone_number = forms.CharField(validators=[RegexValidator(r'^\d{10}$', 'Enter a valid phone number.')])

    date = forms.DateField(
        widget=SelectDateWidget(attrs={'class': 'form-control'}, empty_label=("Year", "Month", "Day")),
        help_text='You can only book the dates from tomorrow.'
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['date'].initial = date.today() + timezone.timedelta(days=1)

    def clean_date(self):
        selected_date = self.cleaned_data['date']
        today = date.today()
        if selected_date <= today:
            raise forms.ValidationError('Invalid date. Please choose a future date.')
        return selected_date


    class Meta:
        model = Catering_Booking
        fields = ['name','phone_number','catering_name','guest','date','message','location']  # Include all fields from the model

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Enter your Name'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Enter your Phone Number'}),
            'catering_name': forms.Select(attrs={'class':  'form-control'}),
            'guest':forms.NumberInput(attrs={'class':  'form-control'}),
            'date': forms.SelectDateWidget(attrs={'class': 'form-control'},
                                           empty_label=("Year", "Month", "Day")),
            'message': forms.Textarea(attrs={'class': 'form-control', 'placeholder':'Enter message clarification'}),
            'location': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter location of the Event'}),

        }
        help_texts = {
            'phone_number': 'Enter a valid 10-digit phone number.',
        }

class DecorationBookingForm(forms.ModelForm):
    phone_number = forms.CharField(validators=[RegexValidator(r'^\d{10}$', 'Enter a valid phone number.')])

    date = forms.DateField(
        widget=SelectDateWidget(attrs={'class': 'form-control'}, empty_label=("Year", "Month", "Day")),
        help_text='You can only book the dates from tomorrow.'
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['date'].initial = date.today() + timezone.timedelta(days=1)

    def clean_date(self):
        selected_date = self.cleaned_data['date']
        today = date.today()
        if selected_date <= today:
            raise forms.ValidationError('Invalid date. Please choose a future date.')
        return selected_date


    class Meta:
        model = Decoration_Booking
        fields = ['name','phone_number','decoration_name','date','location']  # Include all fields from the model

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Enter your Name'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Enter your Phone Number'}),
            'decoration_name': forms.Select(attrs={'class':  'form-control'}),
            'date': forms.SelectDateWidget(attrs={'class': 'form-control'},
                                           empty_label=("Year", "Month", "Day")),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter location of the Event'}),

        }
        help_texts = {
            'phone_number': 'Enter a valid 10-digit phone number.',
        }

class PhotographyBookingForm(forms.ModelForm):
    phone_number = forms.CharField(validators=[RegexValidator(r'^\d{10}$', 'Enter a valid phone number.')])

    date = forms.DateField(
        widget=SelectDateWidget(attrs={'class': 'form-control'}, empty_label=("Year", "Month", "Day")),
        help_text='You can only book the dates from tomorrow.'
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['date'].initial = date.today() + timezone.timedelta(days=1)

    def clean_date(self):
        selected_date = self.cleaned_data['date']
        today = date.today()
        if selected_date <= today:
            raise forms.ValidationError('Invalid date. Please choose a future date.')
        return selected_date

    class Meta:
        model = Photography_Booking
        fields = ['name','phone_number','studio_name','event_type','date']  # Include all fields from the model

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Enter your Name'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Enter your Phone Number'}),
            'studio_name': forms.Select(attrs={'class':  'form-control'}),
            'event_type':forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Enter your Event type'}),
            'date': forms.SelectDateWidget(attrs={'class': 'form-control'},
                                           empty_label=("Year", "Month", "Day")),

        }
        help_texts = {
            'phone_number': 'Enter a valid 10-digit phone number.',
        }

class EntertainmentBookingForm(forms.ModelForm):
    phone_number = forms.CharField(validators=[RegexValidator(r'^\d{10}$', 'Enter a valid phone number.')])

    date = forms.DateField(
        widget=SelectDateWidget(attrs={'class': 'form-control'}, empty_label=("Year", "Month", "Day")),
        help_text='You can only book the dates from tomorrow.'
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['date'].initial = date.today() + timezone.timedelta(days=1)

    def clean_date(self):
        selected_date = self.cleaned_data['date']
        today = date.today()
        if selected_date <= today:
            raise forms.ValidationError('Invalid date. Please choose a future date.')
        return selected_date


    class Meta:
        model = Entertainment_Booking
        fields = ['name','phone_number','program_service_name','date','location']  # Include all fields from the model

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Enter your Name'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Enter your Phone Number'}),
            'program_service_name': forms.Select(attrs={'class':  'form-control'}),
            'date': forms.SelectDateWidget(attrs={'class': 'form-control'},
                                           empty_label=("Year", "Month", "Day")),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter location of the Event'}),

        }
        help_texts = {
            'phone_number': 'Enter a valid 10-digit phone number.',
        }

class AccommodationBookingForm(forms.ModelForm):
    phone_number = forms.CharField(validators=[RegexValidator(r'^\d{10}$', 'Enter a valid phone number.')])
    rooms = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Number of rooms'}),
        min_value=1,
        help_text='Enter the number of rooms required (maximum 15). Available rooms: %(available_rooms)s.'
    )
    date = forms.DateField(
        widget=SelectDateWidget(attrs={'class': 'form-control'}, empty_label=("Year", "Month", "Day")),
        help_text='You can only book the dates from tomorrow.'
    )

    def __init__(self, *args, **kwargs):
        available_rooms = kwargs.pop('available_rooms', None)
        super().__init__(*args, **kwargs)
        self.fields['date'].initial = date.today() + timezone.timedelta(days=1)
        self.fields['rooms'].help_text = self.fields['rooms'].help_text % {'available_rooms': available_rooms}

    def clean_date(self):
        selected_date = self.cleaned_data['date']
        today = date.today()
        if selected_date <= today:
            raise forms.ValidationError('Invalid date. Please choose a future date.')
        return selected_date


    class Meta:
        model = Accommodation_Booking
        fields = ['name','phone_number','hotel_name','rooms','date']  # Include all fields from the model

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Enter your Name'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Enter your Phone Number'}),
            'hotel_name': forms.Select(attrs={'class':  'form-control'}),
            'date': forms.SelectDateWidget(attrs={'class': 'form-control'},
                                           empty_label=("Year", "Month", "Day")),

        }
        help_texts = {
            'phone_number': 'Enter a valid 10-digit phone number.',
        }


class TransportationBookingForm(forms.ModelForm):
    phone_number = forms.CharField(validators=[RegexValidator(r'^\d{10}$', 'Enter a valid phone number.')])

    date = forms.DateField(
        widget=SelectDateWidget(attrs={'class': 'form-control'}, empty_label=("Year", "Month", "Day")),
        help_text='You can only book the dates from tomorrow.'
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['date'].initial = date.today() + timezone.timedelta(days=1)

    def clean_date(self):
        selected_date = self.cleaned_data['date']
        today = date.today()
        if selected_date <= today:
            raise forms.ValidationError('Invalid date. Please choose a future date.')
        return selected_date

    class Meta:
        model = Transportation_Booking
        fields = ['name', 'phone_number', 'travels_name', 'km', 'date', 'message', 'location']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your Name'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your Phone Number'}),
            'travels_name': forms.Select(attrs={'class': 'form-control'}),
            'km':forms.NumberInput(attrs={'class': 'form-control'}),
            'date': forms.SelectDateWidget(attrs={'class': 'form-control'}, empty_label=("Year", "Month", "Day")),
            'message': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter message clarification'}),
            'location': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter location'}),
        }

        help_texts = {
            'phone_number': 'Enter a valid 10-digit phone number.',
        }

