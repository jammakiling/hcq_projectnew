from django.shortcuts import render, redirect
from .models import Purchase, PurchaseItem
from .forms import PurchaseForm, PurchaseItemFormSet
from suppliers.models import Supplier
from inventory.models import Inventory

def add_purchase(request):
    if request.method == "POST":
        purchase_form = PurchaseForm(request.POST)
        formset = PurchaseItemFormSet(request.POST)

        if purchase_form.is_valid() and formset.is_valid():
            # Save the purchase (main record)
            purchase = purchase_form.save()

            total_cost = 0  # Initialize total cost

            # Calculate the total cost based on the quantity and price of each item
            for form in formset:
                purchase_item = form.save(commit=False)
                purchase_item.purchase = purchase  # Associate item with this purchase
                purchase_item.save()  # Save purchase item

                total_cost += purchase_item.quantity * purchase_item.price  # Add item cost to total

            purchase.total_cost = total_cost  # Update the total cost of the purchase
            purchase.save()  # Save the purchase with the updated total cost

            return redirect('purchase_detail', pk=purchase.pk)  # Redirect to purchase details view

    else:
        purchase_form = PurchaseForm()
        formset = PurchaseItemFormSet(queryset=PurchaseItem.objects.none())  # Empty formset for new items

    # Fetch the list of suppliers and inventories for the dropdowns
    suppliers = Supplier.objects.all()
    inventories = Inventory.objects.all()

    return render(request, 'purchases/add_purchase.html', {
        'purchase_form': purchase_form,
        'formset': formset,
        'suppliers': suppliers,  # Pass suppliers to the template
        'inventories': inventories,  # Pass inventories to the template
    })

def purchase_index(request):
    # Fetch all purchases and pass to the template
    purchases = Purchase.objects.all()
    return render(request, 'purchases/index.html', {'purchases': purchases})
