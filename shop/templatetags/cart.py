from django import template

register = template.Library()


# to return if it is in cart or not
@register.filter(name = 'is_in_cart')
def is_in_cart(product, cart):
    keys = cart.keys()
    for id in keys:
        if int(id) == product.id:
            return True
    return False

# to return total quantity if a produc in the cart
@register.filter(name = 'cart_quantity')
def cart_quantity(product, cart):
    keys = cart.keys()
    for id in keys:
        if int(id) == product.id:
            return cart.get(id)
    return 0

# to return total price if the product
@register.filter(name='total_price')
def total_price(product, cart):
    return product.original_price * cart_quantity(product, cart)


# to get the total cart price
@register.filter(name='total_cart_price')
def total_cart_price(products, cart):
    sum = 0
    for product in products:
        sum += total_price(product, cart)
    return sum








