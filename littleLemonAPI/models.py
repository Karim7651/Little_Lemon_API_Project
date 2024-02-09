from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Category(models.Model):
    slug=models.SlugField()
    title=models.CharField(max_length=255,db_index=True)
    def __str__(self):
        return self.title

class MenuItem(models.Model):
    title = models.CharField(max_length=255,db_index=True)
    price = models.DecimalField(max_digits=6,decimal_places=2,db_index=True)
    featured = models.BooleanField(db_index=True)
    category = models.ForeignKey(Category,on_delete=models.PROTECT)
    def __str__(self):
        return f"{self.title} - {self.price}"
    
class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    menuitem = models.ForeignKey(MenuItem,on_delete=models.CASCADE)
    quantity = models.SmallIntegerField
    unit_price = models.DecimalField(max_digits=6,decimal_places=2)
    price = models.DecimalField(max_digits=6,decimal_places=2)
    
    class Meta:
        unique_together=('menuitem','user') #user can add item only once to his cart
    def __str__(self):
        return f"{self.user.username}'s Cart - {self.menuitem.title}"
        
class Order(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    delivery_crew = models.ForeignKey(User,on_delete=models.SET_NULL,related_name='delivery_crew',null=True) #since user and del.crew refer to the same Table we have to make foreign key that way
    status = models.BooleanField(db_index=True,default=0)
    total = models.DecimalField(max_digits=6,decimal_places=2)
    date = models.DateField(db_index=True)
    def __str__(self):
        return f"Order by {self.user.username} on {self.date}"
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    menuitem = models.ForeignKey(MenuItem,on_delete=models.CASCADE)
    quantity = models.SmallIntegerField()
    unit_price = models.DecimalField(max_digits=6,decimal_places=2)
    price = models.DecimalField(max_digits=6,decimal_places=2)
    
    def save(self, *args, **kwargs):
        # Calculate the total price before saving
        self.price = self.unit_price * self.quantity
        super().save(*args, **kwargs)
    
    class meta:
        unique_together=('order','menuitem') #menu item can be added once only in the same orderItem with quantity
        
    def __str__(self):
        return f"Item: {self.menuitem.title} - Quantity: {self.quantity} - Price: {self.price}"

        