from django.views import View
from django.shortcuts import render, redirect, HttpResponseRedirect
from store.models.customer import Customer
from django.contrib.auth.hashers import check_password
from django.contrib import messages

class Login(View):
    return_url = None
    def get(self, request):
        Login.return_url = request.GET.get('return_url')
        return render(request, 'login.html')

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        customer = Customer.get_customer_by_email(email)
        values = {
            'email': email,
            'password': password
        }
        error_message = None
        if customer:
            flag = check_password(password, customer.password)
            if flag:
                request.session['customer'] = customer.id
                messages.success(request, f'You have successfully logged in!!! Happy Shopping.')
                if Login.return_url:
                    return HttpResponseRedirect(Login.return_url)
                else:
                    Login.return_url = None
                    return redirect('homepage')
            else:
                error_message = 'Email or Password invalid!! Please try again.'
        else:
            error_message = 'Email or Password invalid!! Please try again.'
        return render(request, 'login.html', {'error': error_message, 'values': values})

def logout(request):
    #request.session.clear()
    messages.warning(request, f'You have successfully logged out!!! Please come back and see us soon.')
    del request.session['customer']
    return redirect('login')