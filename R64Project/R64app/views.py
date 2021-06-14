from django.contrib import messages
from django.contrib.auth import authenticate
from django.core.mail import send_mail, EmailMessage
from django.shortcuts import render, redirect, get_object_or_404
from django.template import loader
from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.hashers import check_password
from django.views.decorators.csrf import csrf_exempt

from .models import *


@csrf_exempt
def index(request):
   if request.method == 'POST':
      form = AuthenticationForm(request=request, data=request.POST)
      if form.is_valid():
         username = form.cleaned_data.get('username')
         password = form.cleaned_data.get('password')
         user = authenticate(username=username, password=password)
         if user is not None:
            if user.is_active:
               request.session['SUK'] = username
               return redirect('dashboard')
            else:
               messages.error(request, "The User has been deactivated by the Admin.")
               return redirect(request.META['HTTP_REFERER'])
         else:
            messages.error(request, "invalid username or password.")
            return redirect(request.META['HTTP_REFERER'])
      else:
         messages.error(request, "invalid username or password.")
         return redirect(request.META['HTTP_REFERER'])
   elif request.session.get('SUK'):
      return redirect('dashboard')
   form = AuthenticationForm()
   return render(request=request,
                 template_name="page-login.html",
                 context={"form": form})


def logout(request):
    try:
        del request.session['SUK']
    except KeyError:
        pass

    return redirect(index)

@csrf_exempt
def dashboard(request):
   if request.session.get('SUK'):
      username = request.session['SUK']
      trecieve = 0
      tgive = 0
      recieve = Cash.objects.all().filter(reciever__username__exact=username)
      give = Cash.objects.all().filter(giver__username__exact=username)
      if recieve:
         for r in recieve:
             trecieve = trecieve + r.amount

      if give:
         for g in give:
             tgive = tgive + g.amount

      context = {'trecieve': trecieve,
                 'tgive': tgive,
                 'username': username}

      return render(request, 'dashboard.html', context)

   else:
      return redirect(index)

@csrf_exempt
def single_entry(request):
   if request.session.get('SUK'):
      username = request.session['SUK']
      if request.method == 'POST':
         rec = get_object_or_404(User, username=username)
         try:
          giv = get_object_or_404(User, username=request.POST.get('giver'))
          create_cash = Cash()
          create_cash.reciever = rec
          create_cash.giver = giv
          create_cash.amount = int(request.POST.get('amount'))
          if request.POST.get('event') == "":
             messages.error(request, "please fill all the required fields/something went wrong")
             return redirect(request.META['HTTP_REFERER'])
          create_cash.event = request.POST.get('event')
          create_cash.save()
          messages.success(request, "Success")
          return redirect(request.META['HTTP_REFERER'])
         except:
            messages.error(request, "please fill all the required fields/something went wrong")
            return redirect(request.META['HTTP_REFERER'])
      else:
         users = User.objects.all().exclude(username__exact=username)
         return render(request, 'entry.html', {'users': users})
   else:
       return redirect(index)

@csrf_exempt
def selectUser(request):
   if request.session.get('SUK'):
      username = request.session['SUK']
      if request.method == 'POST':
         return redirect(hisab_kitab)
      users = User.objects.all().exclude(username__exact=username)
      return render(request, 'selectUser.html', {'users': users})
   else:
      return redirect(index)

@csrf_exempt
def selectbulkUser(request):
   if request.session.get('SUK'):
      username = request.session['SUK']
      if request.method == 'POST':
         no = request.POST.get('no')
         if not no:
            messages.error(request, "please fill all the required fields/something went wrong")
            return redirect(request.META['HTTP_REFERER'])

         return redirect(bulkentry, {'no': no})
      users = User.objects.all().exclude(username__exact=username)
      return render(request, 'selectbulkUser.html', {'users': users})
   else:
      return redirect(index)


@csrf_exempt
def bulkentry(request):
   if request.session.get('SUK'):
      username = request.session['SUK']
      err = 0
      no = request.POST.get('no')
      list = []
      try:
       for i in range(int(no)):
         list.append(i+1)
      except:
         pass

      if request.method == 'POST' and no:
         users = User.objects.all().exclude(username__exact=username)
         return render(request, 'bulkentry.html', {'no': list, 'count': len(list), 'users': users})

      elif request.method == 'POST' and request.POST.get('count'):
         data = request.POST.dict()
         if data.get("event") == "":
            messages.error(request, "please fill all the required fields/something went wrong")
            return redirect(request.META['HTTP_REFERER'])
         try:
          amnt = int(data.get("amount"))
          eve = data.get("event")
          p = int(request.POST.get('count'))
          am = amnt/p
         except:
          messages.error(request, "please fill all the required fields/something went wrong")
          return redirect(request.META['HTTP_REFERER'])

         for i in range(int(request.POST.get('count'))):
             user = data.get("giver"+str(i+1))
             rec = get_object_or_404(User, username=username)
             try:
              giv = get_object_or_404(User, username=user)
             except:
              messages.error(request, "please fill all the required fields/something went wrong")
              return redirect(request.META['HTTP_REFERER'])
             create_cash = Cash()
             create_cash.reciever = rec
             create_cash.giver = giv
             create_cash.amount = am
             create_cash.event = eve
             try:
                create_cash.save()
             except:
                messages.error(request, "please fill all the required fields/something went wrong")
                return redirect(request.META['HTTP_REFERER'])


         messages.success(request, "Success")
         return redirect(request.META['HTTP_REFERER'])
      else:
         return redirect(selectbulkUser)
   else:
       return redirect(index)


@csrf_exempt
def hisab_kitab(request):
   if request.session.get('SUK'):
      username = request.session['SUK']
      if request.method == 'POST':
         trecieve = 0
         tgive = 0
         user2 = request.POST.get('payeer')
         if user2 == " ":
            messages.error(request, "please fill all the required fields/something went wrong")
            return redirect(request.META['HTTP_REFERER'])
         have_to_reciever = Cash.objects.all().filter(reciever__username__exact=username, giver__username__exact=user2).order_by('-cash_id')
         have_to_give = Cash.objects.all().filter(reciever__username__exact=user2, giver__username__exact=username).order_by('-cash_id')

         if have_to_reciever:
            for r in have_to_reciever:
               trecieve = trecieve + r.amount

         if have_to_give:
            for g in have_to_give:
               tgive = tgive + g.amount

         context = {
            'have_to_recieve': have_to_reciever,
            'have_to_give': have_to_give,
            'trecieve': trecieve,
            'tgive': tgive,
            'user2': user2
                   }
         return render(request, 'cash-online.html', context)
      else:
         return redirect(selectUser)
   else:
       return redirect(index)


def history(request):
      if request.session.get('SUK'):
            username = request.session['SUK']
            reciever_history = History.objects.all().filter(reciever__username=username).order_by('-history_id')
            give_history = History.objects.all().filter(giver__username=username).order_by('-history_id')

            context = {
               'reciever_history': reciever_history,
               'give_history': give_history
            }
            return render(request, 'trxhistory.html', context)
      else:
         return redirect(index)


def markpaid(request, key_id):
   if request.session.get('SUK'):
      idd = key_id
      obj = get_object_or_404(Cash, cash_id=idd)

      his = History()
      his.reciever = obj.reciever
      his.giver = obj.giver
      his.amount = obj.amount
      his.event = obj.event
      his.save()

      obj.delete()
      messages.success(request, "Successfully Paid")
      return redirect(selectUser)
   else:
       return redirect(index)


def mark_all_paid(request, user2):
   if request.session.get('SUK'):
      username = request.session['SUK']
      t = 0
      try:
       cash = Cash.objects.all().filter(reciever__username__exact=username, giver__username__exact=user2)
       obj = get_object_or_404(User, username__exact=username)
       obj2 = get_object_or_404(User, username__exact=user2)
       for am in cash:
           t = t + am.amount

       his = History()
       his.reciever = obj
       his.giver = obj2
       his.amount = t
       his.event = "All Payment Paid"
       his.save()

       Cash.objects.all().filter(reciever__username__exact=username, giver__username__exact=user2).delete()
       messages.success(request, "All Cash are Paid")
       return redirect(selectUser)
      except:
         messages.error(request, "Something went wrong")
         return redirect(selectUser)
   else:
       return redirect(index)


@csrf_exempt
def changepassword(request):
   if request.session.get('SUK'):
      username = request.session['SUK']
      if request.method == 'POST':

         u = User.objects.filter(username__exact=username)
         data = request.POST.dict()
         op = data.get("lastpassword")
         np1 = data.get("newpassword1")
         np2 = data.get("newpassword2")
         if op and np1 and np2:
            for p in u:
               if check_password(op, p.password):
                  if np1 == np2:
                     p.set_password(np1)
                     p.save()
                     messages.success(request, "Your password has been changed successfully!.")
                     return redirect(request.META['HTTP_REFERER'])
                  else:
                     messages.error(request, "new password and confirm new password didn't match!.")
                     return redirect(request.META['HTTP_REFERER'])
               else:
                  messages.error(request, "Your old password is wrong. Please type correct one!.")
                  return redirect(request.META['HTTP_REFERER'])
         else:
            messages.error(request, "Invalid form filled!.")
            return redirect(request.META['HTTP_REFERER'])

      else:
         return render(request, 'changepassword.html')
   else:
      return redirect(index)


def dashboardR(request):
   if request.session.get('SUK'):
      return redirect(dashboard)
   else:
      return redirect(index)