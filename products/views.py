import datetime

from django.shortcuts import render, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from .models import ProductCategory, Product, ProductImage
from basketapp.models import Basket


def products(request, product_vendor_code=None, category_pk=None):
    context = {}
    title = 'продукты'

    # upload product categories from DB
    product_categories = ProductCategory.objects.all()
    context.update({'product_categories': product_categories})

    # add basket
    if request.user.is_authenticated:
        basket = Basket.objects.filter(user=request.user)
    else:
        basket = []

    context.update({'basket': basket})

    # if refer from main menu=products
    if not category_pk and not product_vendor_code:
        category_pk = ProductCategory.objects.filter(name='все')[0].id

    # show category page
    if category_pk:
        category = get_object_or_404(ProductCategory, pk=category_pk)

        if category.name == 'все':
            cat_products = Product.objects.all().order_by('price')
        else:
            cat_products = Product.objects.filter(category__id=category_pk).order_by('price')

        context.update({
            'category': category,
            'products': cat_products,

        })

    # show product_detail page
    if product_vendor_code:

        p = get_object_or_404(Product, pk=product_vendor_code)
        imgs = ProductImage.objects.filter(product_id=p.id)

        ctx = {}
        ctx.update(p.__dict__)
        ctx.update({'images': imgs})
        context.update({'product_params': ctx, 'products': [p]})

    # upload related products from DB
    related_products = Product.get_featured_products(category_id=category_pk, filter_out=context['products'])

    context.update({'title': title,
                    'featured_categories': ['Похожие товары'],
                    'featured_products': related_products,
                    'visit_date': datetime.datetime.now()})

    return render(request, 'products.html', context)
