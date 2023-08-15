#### context_processors is used to available a variable in all templates like <request>, <messages>


from .cart import Cart


def cart_context_processor(request):
    # in templates just key is used
    return {'cart': Cart(request)}


# add 'orders.context_processors.cart_context_processors' in context_processors of TEMPLATES in settings
 