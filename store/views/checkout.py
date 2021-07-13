from django.views import View
from django.contrib import messages
from django.shortcuts import redirect
from store.models.product import Product
from store.models.orders import Order
from store.models.customer import Customer

class CheckOut(View):
    def post(self, request):
        customer = request.session.get('customer')
        if not customer:
            messages.warning(request, f'You to have login to check out, please login now.')
            return redirect('login')
        else:
            address = request.POST.get('address')
            phone = request.POST.get('phone')
            cart = request.session.get('cart')
            products = Product.get_products_by_id(list(cart.keys()))
            for product in products:
                order = Order(customer=Customer(id = customer),
                              product = product,
                              price = product.price,
                              quantity = cart.get(str(product.id)),
                              address = address,
                              phone = phone
                            )
                request.session['cart'] = {}
                order.placeOrder()
            messages.success(request, f'Thank you for purchasing!!! Please click on Orders tab to view your orders.')
            return redirect('cart')

