from django.db import models
from suppliers.models import Supplier
from inventory.models import Inventory

class Purchase(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name='purchases')
    date = models.DateTimeField(auto_now_add=True)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Purchase from {self.supplier.name} on {self.date}"

class PurchaseItem(models.Model):
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE, related_name='items')
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE, related_name='purchase_items')
    quantity = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)  # Price is optional here

    def __str__(self):
        return f"{self.inventory.product.product_name} ({self.quantity})"

    def save(self, *args, **kwargs):
        if not self.price:
            self.price = self.inventory.product.purchase_price  # Automatically get the purchase price from the inventory
        super().save(*args, **kwargs)
