from django import forms
from .models import HostelStay
from .models import PaymentHistory
from django import forms
from .models import HostelStay,ChatMessage

class HostelJoinForm(forms.ModelForm):
    profile_picture = forms.ImageField(required=False, widget=forms.FileInput(attrs={'accept': 'image/*'}))
    class Meta:
        model = HostelStay
        fields = ['profile_picture','location','priority1', 'priority2', 'priority3', 'share','hosteltype', 'gender', 'house_address', 'parent_mobile', 'your_mobile', 'guardian_no']

        widgets = {
            'location': forms.Select(attrs={'class': 'form-control'}),
            'share': forms.Select(attrs={'class': 'form-control'}),  # Corrected 'share' instead of 'share_type'
            'hosteltype':forms.Select(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'house_address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'parent_mobile': forms.TextInput(attrs={'class': 'form-control'}),
            'your_mobile': forms.TextInput(attrs={'class': 'form-control'}),  # Corrected 'your_mobile' instead of 'user_mobile'
            'guardian_no': forms.TextInput(attrs={'class': 'form-control'}),  # Corrected 'guardian_no' instead of 'guardian_mobile'
        }


class PaymentForm(forms.ModelForm):
    class Meta:
        model = PaymentHistory
        fields = ['amount_paid', 'payment_proof']

class ChatForm(forms.ModelForm):
    class Meta:
        model = ChatMessage
        fields = ['message']