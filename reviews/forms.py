from django.forms import ModelForm
from restaurants.models import Restaurant
from models import Review
from django import forms

stars = (
    ('1' , 1),
    ('2' , 2),
    ('3' , 3),
    ('4' , 4),
    ('5' , 5),
)

class ReviewForm(ModelForm) :
    class Meta:
        model = Review
        fields = ['restaurant', 'stars', 'contents']
        labels = {
            'stars' : _('평점'),
            'contents' : _('리뷰')
        }
        widgets = {
            'restaurant' : forms.HiddenInput(),
            'stars' : forms.Select(choices = stars)            
        }