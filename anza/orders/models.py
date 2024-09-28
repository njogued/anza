from django.db import models
from users.models import CustomUser
from products.models import Product

class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='orders')
    product = models.ManyToManyField(Product, through='OrderItem')
    status = models.CharField(max_length=50, choices=[('Pending', 'Pending'), ('Shipped', 'Shipped'), ('Delivered', 'Delivered')])
    delivery_address = models.CharField(max_length=100, default='Nairobi')
    delivery_date = models.DateField(default=None)
    payment_method = models.CharField(max_length=50, choices=[('Cash', 'Cash'), ('Card', 'Card'), ('Mobile Money', 'Mobile Money')])
    mobile_payment_number = models.CharField(max_length=50, default=None)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    archived = models.BooleanField(default=False)
    shipped_at = models.DateTimeField(null=True)
    delivered_at = models.DateTimeField(null=True)

    def __str__(self):
        return self.product.name + ' - ' + self.user.email
    
    def calculate_total(self):
        self.total_price = sum(item.price * item.quantity for item in self.orderitem_set.all())
        self.save()
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} of {self.product.name} in order {self.order.id}"
    
class Cart(models.Model):
    # need to validate that the user has only one active cart at a time
    # need to check if all items in cart are from the same shop
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='carts')
    items = models.ManyToManyField(Product, through='CartItem')
    total_price = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    archived = models.BooleanField(default=False)

    def __str__(self):
        return self.product.name + ' - ' + self.user.email
    
    def archive_and_create_order(self):
        self.archived = True
        self.save()
        order = Order.objects.create(user=self.user)
        for item in self.items.all():
            OrderItem.objects.create(order=order, product=item, quantity=item.quantity, price=item.price)
        order.calculate_total()
        return order
    
    def update_price_total(self, cart_item_price):
        self.update_price_total += cart_item_price

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} of {self.product.name} in cart {self.cart.id}"
    
    def calculate_price(self):
        self.price = self.product.price * self.quantity
        self.save()
        return self.price

    def save(self, *args, **kwargs):
        # Automatically calculate price on save
        if self.price is None:
            self.calculate_price()
        super().save(*args, **kwargs)

class Payment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50, choices=[('Pending', 'Pending'), ('Escrowed', 'Escrowed'), ('Completed', 'Completed'), ('Failed', 'Failed')])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    paid_at = models.DateTimeField(null=True)
    completed_at = models.DateTimeField(null=True)

    def __str__(self):
        return self.order + ' - ' + str(self.amount) + ' - ' + self.status