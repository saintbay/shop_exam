from django.shortcuts import render, redirect, get_object_or_404
from app.forms import SignUpForm
from .models import Product, ProductCategory
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
import pprint
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from .models import Product  # Импортируйте вашу модель товара
from .cart import Cart  # Импортируйте свою модель/класс корзины
# def home(request):
#     return render(request, 'home.html')

# class SignUp(CreateView):
#     model = CustomUser
#     form_class = SignUpForm
#     template_name = 'signup.html'
#     success_url = reverse_lazy('home')
#     def form_valid(self, form):
#         user = form.save(commit=False)
#         user.password = make_password(form.cleaned_data.get('password'))
#         user.save()
#         login(self.request, user)
#         return redirect(self.success_url)

def home2(request):
    all_products = Product.objects.all()
    if request.method == 'POST':
        text = request.POST.get('text', None)
        product_id = request.POST.get('product', None)
        product = Product.objects.get(id=product_id)
        return render(request, 'home.html', {'products': all_products})    
    return render(request, 'home.html', {'products': all_products})

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        cart = Cart(request)
        cart.add(product, quantity)

        messages.success(request, f'{product.name} добавлен в корзину.')
        return redirect('cart')  
    return redirect('product_detail', product_id=product.id)  # Вернуться на страницу товара
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

def home(request):
    username = request.user.username if request.user.is_authenticated else None
    return render(request, 'home.html', {'username': username})
def catalog_view(request):
    products = Product.objects.all()  # Получаем все продукты
    return render(request, 'catalog.html', {'products': products})

# Страница продукта
def product_detail_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)  # Получаем продукт по id или выводим 404
    return render(request, 'product_detail.html', {'product': product})

# Страница корзины (пока просто статичная, позже можно добавить логику)
@login_required
def cart_view(request):
    return render(request, 'cart.html')

# Личный кабинет
@login_required
def profile_view(request):
    return render(request, 'profile.html')

# Поиск товаров
def search_view(request):
    query = request.GET.get('q', '')  # Получаем поисковый запрос
    products = Product.objects.filter(name__icontains=query)  # Ищем продукты по имени
    return render(request, 'search_results.html', {'products': products, 'query': query})

