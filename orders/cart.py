from home.models import Product

CART_SESSION_ID = 'cart'

class Cart:
    def __init__(self, request):
        self.session = request.session
        session_cart = self.session.get(CART_SESSION_ID)

        if not session_cart:
            session_cart = self.session[CART_SESSION_ID] = {}
        
        self.cart = session_cart

    
    def add(self, product, quantity):
        product_id = str(product.id)

        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0, 'price': product.price}

        self.cart[product_id]['quantity'] += quantity
        self.save_session() 


    def save_session(self):
        self.session.modified = True


    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids) # using field lookup get all product with product_ids

        temp_cart = self.cart.copy()

        for product in products:
            item = temp_cart[str(product.id)]
            temp_cart[str(product.id)]['product_name'] = product.name
            temp_cart[str(product.id)]['total_price'] = item['price'] * item['quantity']
            temp_cart[str(product.id)]['product_id'] = product.id

        for item in temp_cart.values():
            yield item


    def total_price(self):
        return sum(item['price'] * item['quantity'] for item in self.cart.values())
    

    def cart_item_remvoe(self, product_id):
        product_id = str(product_id)
        if product_id in self.cart:
            del self.cart[product_id]
            # print(f'cart: {id(self.cart)},    session:  {id(self.session.get(CART_SESSION_ID))}')
            self.save_session()
            # print(f'cart: {self.cart}, session: {self.session.get(CART_SESSION_ID)}')

            #### the self.cart and self.session.get(CART_SESSION_ID) point to the same dict(object)


    def is_epmty(self):
        return not len(self.cart)


            
    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

        


