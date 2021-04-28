import re
import csv
import pytz
from datetime import datetime
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Sale, CsvUploadFile
from .forms import SaleCreateForm, SaleUpdateForm, CsvUploadForm
from stock.models import Fruit


@login_required
def sale_list(request):
    sales = Sale.objects.order_by("-sold_on")
    total_sales = sales.count()

    page = request.GET.get('page', 1)
    paginator = Paginator(sales, 10)

    try:
        sales = paginator.page(page)
    except PageNotAnInteger:
        sales = paginator.page(1)
    except EmptyPage:
        sales = paginator.page(paginator.num_pages)

    return render(
        request,
        "sales/sale_list.html",
        {
            "total_sales": total_sales,
            "sales": sales
        }
    )


@login_required
def sale_create(request):
    if request.method == "POST":
        form = SaleCreateForm(request.POST)
        if form.is_valid():

            sale = form.save(commit=False)
            sale.retrieve_fruit_price()
            sale.calculate_proceeds()

            # New record not saved if an identical sale record already exists
            if not Sale.objects.filter(
                fruit=sale.fruit,
                quantity=sale.quantity,
                proceeds=sale.proceeds,
                sold_on=sale.sold_on,
            ).exists():
                sale.save()

            return redirect("sale_list")
    else:
        form = SaleCreateForm()
    return render(request, "sales/sale_create.html", {"form": form})


@login_required
def sale_delete(request, pk):
    sale = get_object_or_404(Sale, pk=pk)
    if request.method == "POST":
        sale.delete()
    return redirect("sale_list")


@login_required
def sale_update(request, pk):
    sale = get_object_or_404(Sale, pk=pk)
    if request.method == "POST":
        form = SaleUpdateForm(request.POST, instance=sale)
        if form.is_valid():
            sale = form.save(commit=False)
            sale.calculate_proceeds()
            sale.save()
            return redirect("sale_list")
    else:
        form = SaleUpdateForm(instance=sale)
    return render(
        request, "sales/sale_update.html", {"form": form, "sale": sale}
    )


def convert_str_to_tz_aware_datetime(date_str):
    """
    Helper function for sale_upload().
    """

    # Convert str to timezone-naive datetime
    try:
        naive_datetime = datetime.strptime(date_str, "%Y-%m-%d %H:%M")
    except ValueError as e:
        print(e)

    # Convert timezone-naive datetime to timezone-aware datetime
    tokyo = pytz.timezone("Asia/Tokyo")
    aware_datetime = tokyo.localize(naive_datetime)

    return aware_datetime


def check_row_content(row):
    """
    Helper function for sale_upload(). Checks the elements included in
    each row of a csv file and the formatting thereof.
    """
    if len(row) != 4:
        return False

    # Check whether a corresponding Fruit object exists
    try:
        Fruit.objects.get(name=row[0])
    except Exception:
        return False

    if not row[1].isdigit():
        return False

    if not row[2].isdigit():
        return False

    # Check whether the datetime element has the correct format
    if not bool(re.match(r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}$", row[3])):
        return False

    # Check whether the datetime element is in the future
    sold_date = convert_str_to_tz_aware_datetime(row[3])
    if sold_date > timezone.now():
        return False

    # Check whether the same record already exists in the DB
    # Necessary to change to UTC time to compare with datetime in the DB
    utc_sold_date = sold_date.astimezone(pytz.utc)
    if Sale.objects.filter(
        fruit_name=row[0],
        quantity=row[1],
        proceeds=row[2],
        sold_on=utc_sold_date,
    ).exists():
        return False

    return True


def generate_sale_objects(file_content):
    """
    Helper function for sale_upload().
    Converts each row in a csv file into a Sale object.
    """
    for row in file_content:

        # Rows that don't pass the checks in check_row_content() are ignored
        verified = check_row_content(row)

        if verified:
            fruit = Fruit.objects.get(name=row[0])
            quantity = int(row[1])
            proceeds = int(row[2])
            fruit_price_when_sold = proceeds / quantity
            sold_on = convert_str_to_tz_aware_datetime(row[3])

            Sale.objects.create(
                fruit=fruit,
                quantity=quantity,
                proceeds=proceeds,
                fruit_price_when_sold=fruit_price_when_sold,
                sold_on=sold_on,
            )


@login_required
def sale_upload(request):
    if request.method == "POST":
        form = CsvUploadForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            csv_file = CsvUploadFile.objects.latest("uploaded_on")

            # Read in content from the CSV file
            file_content = []
            with open(csv_file.file_name.path, "r") as f:
                reader = csv.reader(f)
                for row in reader:
                    if row not in file_content:  # Duplicate rows are ignored
                        file_content.append(row)

            # Create Sale objects from the csv content
            generate_sale_objects(file_content)

            # Delete the uploaded csv file
            csv_file.delete()

            return redirect("sale_list")

    else:
        form = CsvUploadForm()
    return render(request, "sales/sale_upload.html", {"form": form})
