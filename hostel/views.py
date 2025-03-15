from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.models import auth
from .models import Feature,Announcement,Outing
from .models import HostelStay,PaymentHistory,ChatMessage
from .forms import HostelJoinForm,PaymentForm,ChatForm
from datetime import date
from django.core.paginator import Paginator
from django.utils import timezone
import datetime
def index(request):
    return render(request, 'index.html')
def logout(request):
    auth.logout(request)
    return redirect('index')

@login_required
def profile(request):
    user = request.user
    stay = HostelStay.objects.filter(user=request.user).first()
    if request.method == "POST":
        if "payment_proof" in request.FILES:  # If user is submitting payment proof
            form = PaymentForm(request.POST, request.FILES)
            if form.is_valid():
                payment = form.save(commit=False)
                payment.user = user
                payment.save()
                return redirect("profile")  # Refresh the page after submission
        else:  # If user is applying for hostel stay
            # form = HostelJoinForm(request.POST, request.FILES)
            # if form.is_valid():
            #     hostel_stay = form.save(commit=False)
            #     hostel_stay.user = user
            #     hostel_stay.status = "pending"  # Mark application as pending
            #     hostel_stay.save()
            #     return redirect("profile")  # Refresh page
            form = HostelJoinForm(request.POST, request.FILES)  # ✅ Include request.FILES
            if form.is_valid():
                hostel_stay = form.save(commit=False)
                hostel_stay.user = user
                hostel_stay.status = "pending"
    
                # Debugging: Check if the file is received
                if 'profile_picture' in request.FILES:
                    print("DEBUG: Image received in request.FILES ->", request.FILES['profile_picture'])
                else:
                    print("DEBUG: No image received in request.FILES")

                hostel_stay.save()
                print(f"DEBUG: Saved profile picture -> {hostel_stay.profile_picture}")  # ✅ Debugging
                return redirect("profile")
            else:
                print("DEBUG: Form errors ->", form.errors)

    amount_due = 0
    payment_history = []
    payment_form = PaymentForm()

    if stay:
        print(f"DEBUG: User {request.user.username} - Status: '{stay.status}'") 
        if stay.status == "approved":
            if stay.check_in:  # ✅ Ensure check_in is not None
                today = date.today()
                months_due = (today.year - stay.check_in.year) * 12 + (today.month - stay.check_in.month)
                total_due = months_due * 7000

                total_paid = sum(
                    payment.amount_paid for payment in PaymentHistory.objects.filter(user=user, verified=True)
                )
                amount_due = max(total_due - total_paid, 0)
                payment_history = PaymentHistory.objects.filter(user=user).order_by('-payment_date')
                print(f"DEBUG: Payment history for {user.username}: {payment_history.count()} records found.")

            else:
                amount_due = 0

            return render(request, 'profile.html', {
                'stay': stay,
                'amount_due': amount_due,
                'payment_history': payment_history,
                'payment_form': payment_form,
            })

        elif stay.status == "pending":
            return render(request, 'profile.html', {'stay': stay})

        else:
            form = HostelJoinForm()
            return render(request, 'profile.html', {'form': form, 'stay': stay})

    form = HostelJoinForm()
    return render(request, 'profile.html', {'form': form, 'stay': None})


def features(request):
    all_features = Feature.objects.all()
    return render(request, 'features.html',{'features': all_features})
def anouncements(request):
    announcements_list = Announcement.objects.all().order_by('-created_at')  # Fetch all announcements (latest first)
    paginator = Paginator(announcements_list, 15)  # Show 15 announcements per page
    
    page_number = request.GET.get('page')  # Get the current page number from the request
    page_obj = paginator.get_page(page_number)  # Get the announcements for the requested page

    return render(request, 'announce.html', {'page_obj': page_obj})

@login_required
def help(request):
    user = request.user
    messages = ChatMessage.objects.filter(user=request.user).order_by('-created_at')
    paginator = Paginator(messages, 15)  # 15 messages per page
    page_number = request.GET.get('page')
    chat_messages = paginator.get_page(page_number)

    if request.method == 'POST':
        form = ChatForm(request.POST)
        if form.is_valid():
            chat_message = form.save(commit=False)
            chat_message.user = request.user
            chat_message.save()
            return redirect('help')
    else:
        form = ChatForm()

    return render(request, 'help.html', {'chat_messages': chat_messages, 'form': form,'user':user})

@login_required
def outing(request):
    outings = Outing.objects.filter(user=request.user).order_by('-outtime')
    stay = HostelStay.objects.filter(user=request.user).first()
    return render(request, 'outing.html', {'outings': outings, 'stay': stay})

@login_required
def outing_request(request):
    if request.method == "POST":
        outtype=request.POST.get("outtype")
        outdate = request.POST.get("outdate")
        outtime=request.POST.get("outtime")
        indate=request.POST.get("indate")
        intime = request.POST.get("intime")
        reason = request.POST.get("reason")

        # ✅ Convert Strings to Python Date & Time Objects
        outdate = datetime.datetime.strptime(outdate, "%Y-%m-%d").date()
        outtime = datetime.datetime.strptime(outtime, "%I:%M %p").time()  # AM/PM Format
        indate = datetime.datetime.strptime(indate, "%Y-%m-%d").date()
        intime = datetime.datetime.strptime(intime, "%I:%M %p").time()  # AM/PM Format

        Outing.objects.create(
            user=request.user,
            outtype=outtype,
            outdate=outdate,
            outtime=outtime,
            indate=indate,
            intime=intime,
            reason=reason,
            approved=False,  # Admin needs to approve
        )
        return redirect("outing")  # Redirect to outing history page

    return render(request, 'outing_request.html')

