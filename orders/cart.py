

CART_SESSION_ID = 'card'

class Cart:
    def __init__(self, request):
        self.session = request.session
        session_cart = self.session.get(CART_SESSION_ID)

        if not session_cart:
            session_cart = self.session[CART_SESSION_ID] = {}
        
        self.cart = session_cart