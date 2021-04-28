from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Fruit
from .forms import StockForm


@login_required
def stock_list(request):
    fruits = Fruit.objects.order_by("-updated_on")
    total_fruits = fruits.count()

    page = request.GET.get('page', 1)
    paginator = Paginator(fruits, 10)

    try:
        fruits = paginator.page(page)
    except PageNotAnInteger:
        fruits = paginator.page(1)
    except EmptyPage:
        fruits = paginator.page(paginator.num_pages)

    return render(
        request,
        "stock/stock_list.html",
        {
            "total_fruits": total_fruits,
            "fruits": fruits,
        }
    )


@login_required
def stock_create(request):
    if request.method == "POST":
        form = StockForm(request.POST)
        if form.is_valid():
            fruit = form.save(commit=False)
            fruit.name = fruit.name.lower()
            fruit.save()
            return redirect("stock_list")
    else:
        form = StockForm()
    return render(request, "stock/stock_create.html", {"form": form})


@login_required
def stock_delete(request, pk):
    fruit = get_object_or_404(Fruit, pk=pk)
    if request.method == "POST":
        fruit.delete()
    return redirect("stock_list")


@login_required
def stock_update(request, pk):
    fruit = get_object_or_404(Fruit, pk=pk)

    if request.method == "POST":
        form = StockForm(request.POST, instance=fruit)
        if form.is_valid():
            fruit = form.save()
            return redirect("stock_list")

    else:
        form = StockForm(instance=fruit)
    return render(request, "stock/stock_update.html", {"form": form})
