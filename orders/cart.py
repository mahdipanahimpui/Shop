

CART_SESSION_ID = 'card'

class Cart:
    def __init__(self, request):
        self.session = request.session
        session_cart = self.session.get(CART_SESSION_ID)

        if not session_cart:
            session_cart = self.session[CART_SESSION_ID] = {}
        
        self.cart = session_cart

    
    def add(self, product, quantity):
        product_id = product.id

        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0, 'price': product.price}

        self.cart[product_id]['quantity'] += quantity
        self.save_session()


    def save_session(self):
        self.session.modified = True