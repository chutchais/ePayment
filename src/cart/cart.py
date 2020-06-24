from decimal import Decimal
from django.conf import settings
# from shop.models import Product
from django.db.models import Q,F
from tariff.models import Tariff

class Cart(object):
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            print ('New cart')
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
        # print('Initial Cart',cart)

    # def add(self, product, quantity=1, update_quantity=False):
    #     product_id = str(product.id)
    #     if product_id not in self.cart:
    #         self.cart[product_id] = {'quantity': 0, 'price': str(product.price)}
    #     if update_quantity:
    #         self.cart[product_id]['quantity'] = quantity
    #     else:
    #         self.cart[product_id]['quantity'] += quantity
    #     self.save()
    def add(self, container,category='E',size=40,full=True,oog=False, 
                quantity=1, update_quantity=False,con_type='DV',
                status='RGS'):
        container_number = str(container)
        if container_number not in self.cart:
            # Get teriff detail
            size = size.replace('.00','')
            # tariff_full_filters = {
            #     'full': full
            #    }
            con_size= 'size20' if int(size)==20 else 'size40' if int(size)==40 else 'size45'
            tariff ={}
            sum_price = 0

            if status == 'RGS':
                tariff_items = Tariff.objects.filter(   
                                Q(container_profile__category='B')|Q(container_profile__category=category),
                                container_profile__full=full,
                                container_profile__oog=oog,
                                container_profile__status = True,
                                status= True
                                ).order_by('seq')
                

                for x in tariff_items.values('title',con_size):
                    tariff[x['title']]=x[con_size]

                if len(tariff) > 0 :
                    sum_price = sum(v for k,v in tariff.items())

            # --End Tariff--
            self.cart[container_number] = {
                                'status' : status,
                                'container':container,
                                'quantity': 1,
                                'size' :    size,
                                'type' :    con_type, 
                                'price':    sum_price,
                                'full' :    full,
                                'oog'  :    oog,
                                'category': category,
                                'tariff' : tariff }
            # print(self.cart[container_number])
        # if update_quantity:
        #     self.cart[product_id]['quantity'] = quantity
        # else:
        #     self.cart[product_id]['quantity'] += quantity
        # print ('Cart add -- container_number')
        self.save()

    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def remove(self, container):
        container_number = str(container)
        if container_number in self.cart:
            del self.cart[container_number]
            self.save()

    def __iter__(self):
        container_ids = self.cart.keys()
        # yield 0
        # containers = Container.objects.filter(number__in=container_ids)
        # for container in containers:
        #     self.cart[str(container)]['booking'] = container

        for item in self.cart.values():
            # item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        print('Cart on clear :' , self.session[settings.CART_SESSION_ID])
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True
