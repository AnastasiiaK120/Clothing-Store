from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages

from .models import Category, Product, Review
from .forms import ReviewForm
from cart.forms import CartAddProductForm


def front(request):
    products = Product.objects.all()[:8]
    return render(request, 'product/front.html', {'products': products})


def product_list(request):
    categories = Category.objects.all()
    products = Product.objects.all()

    active_category = request.GET.get('category', '')

    if active_category:
        products = products.filter(category__slug=active_category)

    return render(request, 'product/shop.html', {'categories': categories, 'active_category': active_category, 'products': products})


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)

    if request.method == 'POST':
        # rating = request.POST.get('rating', 3)
        # content = request.POST.get('content', '')
        #
        # if content:
        #     reviews = Review.objects.filter(author=request.user, product=product)
        #
        #     if reviews.count() > 0:
        #         review = reviews.first()
        #         review.rating = rating
        #         review.content = content
        #         review.save()
        #     else:
        #         review = Review.objects.create(
        #             product=product,
        #             rating=rating,
        #             text=content,
        #             author=request.user
        #         )
        #
        #     return redirect('listings:product', slug=slug)
        review_form = ReviewForm(request.POST)

        if review_form.is_valid():
            cf = review_form.cleaned_data
            # author_name = 'Anonymous'
            author = request.user
            # if request.user.is_authenticated:
            #     author_name = request.user.first_name

            Review.objects.create(product=product, author=author, text=cf['text'], rating=cf['rating'])
        return redirect('listings:product', slug=slug)
    else:
        review_form = ReviewForm()
        cart_product_form = CartAddProductForm()

    return render(request, 'product/product_detail.html', {'product': product, 'review_form': review_form, 'cart_product_form': cart_product_form})
    # return render(request, 'product/product_detail.html',
    #               {'product': product})


def submit_review(request, product):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        try:
            reviews = Review.objects.get(user__id=request.user.id, product=product)
            form = ReviewForm(request.POST, instance=reviews)
            form.save()
            messages.success(request, 'Thank you! Your review has been updated.')
            return redirect(url)
        except Review.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = Review()
                data.subject = form.cleaned_data['subject']
                data.rating = form.cleaned_data['rating']
                data.review = form.cleaned_data['review']
                data.ip = request.META.get('REMOTE_ADDR')
                data.product = product
                data.user_id = request.user.id
                data.save()
                messages.success(request, 'Thank you! Your review has been submitted.')
                return redirect(url)