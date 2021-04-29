import dateutil.relativedelta
from django.utils import timezone
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from sales.models import Sale


class Row:
    """
    Class representing a row in the table to be displayed on the stats page,
    including sales details data per day and per month.
    """

    def __init__(self, date, proceeds, sales, details, details_str):
        self.date = date
        self.proceeds = proceeds
        self.sales = sales
        # Dict for holding details information
        self.details = details
        # Above dict converted to a string
        self.details_str = details_str


def calculate_total_proceeds(sales):
    proceeds = [sale.proceeds for sale in sales]
    return sum(proceeds)


def get_sales_for_period(sales, period):
    """
    Note regarding "time" in the code below:
    Within code used in a Django view (i.e. this file), time is represented as
    datetime objects that are UTC timezone-aware. However, in order to get and
    sort Sale objects correctly for outputting in the statistics template, it
    is necessary to convert the Sale.sold_on values from UTC time to JPT time
    and then to compare these with the local time according to JPY timezone.
    """

    # Get local time in JPT (i.e. JPT timezone aware datetime obj)
    now = timezone.localtime(timezone.now())

    if period == "days":
        # Get start point (minus two days from the current day)
        now_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
        start = now_day - dateutil.relativedelta.relativedelta(days=2)
    else:
        # Get start point (start of the current month minus two months)
        now_month = now.replace(
            day=1, hour=0, minute=0, second=0, microsecond=0
        )
        start = now_month - dateutil.relativedelta.relativedelta(months=2)

    target_sales = []

    for sale in sales:
        sold_on_jpt = timezone.localtime(sale.sold_on)  # Convert to JPT
        if sold_on_jpt >= start:
            target_sales.append(sale)

    return target_sales


def sort_sales_by_day(sales):

    # Get current day in local JPT timezone
    now_day = timezone.localtime(timezone.now()).date()
    one_day_b4 = now_day - dateutil.relativedelta.relativedelta(days=1)
    two_days_b4 = now_day - dateutil.relativedelta.relativedelta(days=2)

    row1 = Row(date=now_day, proceeds=0, sales=[], details={}, details_str="")
    row2 = Row(
        date=one_day_b4, proceeds=0, sales=[], details={}, details_str=""
    )
    row3 = Row(
        date=two_days_b4, proceeds=0, sales=[], details={}, details_str=""
    )

    for sale in sales:

        sold_on_jpt = timezone.localtime(sale.sold_on).date()  # Convert to JPT

        if sold_on_jpt == now_day:
            row1.sales.append(sale)
        elif sold_on_jpt == one_day_b4:
            row2.sales.append(sale)
        else:
            row3.sales.append(sale)

    return [row1, row2, row3]


def sort_sales_by_month(sales):

    # Get start of current month in local JPT timezone
    now = timezone.localtime(timezone.now())

    now_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    one_month_b4 = now_month - dateutil.relativedelta.relativedelta(months=1)
    two_month_b4 = now_month - dateutil.relativedelta.relativedelta(months=2)

    row1 = Row(
        date=now_month, proceeds=0, sales=[], details={}, details_str=""
    )
    row2 = Row(
        date=one_month_b4, proceeds=0, sales=[], details={}, details_str=""
    )
    row3 = Row(
        date=two_month_b4, proceeds=0, sales=[], details={}, details_str=""
    )

    for sale in sales:

        sold_on_jpt = timezone.localtime(sale.sold_on)  # Convert to JPT

        if sold_on_jpt >= now_month:
            row1.sales.append(sale)
        elif sold_on_jpt >= one_month_b4 and sale.sold_on < now_month:
            row2.sales.append(sale)
        else:
            row3.sales.append(sale)

    return [row1, row2, row3]


def build_sales_details(sales):

    sorted_sales = []

    for row in sales:
        if row.sales:

            # Get total proceeds for this row
            all_proceeds = [sale.proceeds for sale in row.sales]
            row.proceeds = sum(all_proceeds)

            # Build the details dict
            # key = fruit name (str), val = [proceeds (int), quantity (int)]
            all_fruit_names = [sale.fruit_name for sale in row.sales]
            unique_fruit_names = set(all_fruit_names)
            for name in unique_fruit_names:
                row.details[name] = []

            # Get total proceeds and quantity for each fruit in this row
            for name in unique_fruit_names:
                total_proceeds = 0
                quantity = 0
                for sale in row.sales:
                    if sale.fruit_name == name:
                        total_proceeds += sale.proceeds
                        quantity += sale.quantity
                row.details[name].append(total_proceeds)
                row.details[name].append(quantity)

            # Sort the details dict according in descending order of proceeds
            sorted_details = dict(
                sorted(
                    row.details.items(),
                    key=lambda item: item[1],
                    reverse=True,
                )
            )
            row.details = sorted_details

            # Convert the details dict into a str
            # format() used to insert commas into long numbers
            for entry in row.details:
                row.details_str += (
                    entry.capitalize()
                    + ": ¥"
                    + "{:,}".format(row.details[entry][0])
                    + " ("
                    + "{:,}".format(row.details[entry][1])
                    + "), "
                )
            # Remove trailing comma and space
            row.details_str = row.details_str[:-2]

        sorted_sales.append(row)

    return sorted_sales


@login_required
def stats_list(request):

    sales = Sale.objects.all()

    total_proceeds = calculate_total_proceeds(sales)

    # Get sales for most recent three days
    day_sales = get_sales_for_period(sales, "days")
    day_sales = sort_sales_by_day(day_sales)
    day_sales = build_sales_details(day_sales)

    # Get sales for most recent three months
    month_sales = get_sales_for_period(sales, "month")
    month_sales = sort_sales_by_month(month_sales)
    month_sales = build_sales_details(month_sales)

    return render(
        request,
        "stats/stats_list.html",
        {
            "total_proceeds": total_proceeds,
            "month_sales": month_sales,
            "day_sales": day_sales,
        },
    )
