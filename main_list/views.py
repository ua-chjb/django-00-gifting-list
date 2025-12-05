from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from . import models

def signup(request):
    if request.method == "POST":     
        form = UserCreationForm(request.POST)
        if form.is_valid():           
            user = form.save()
            login(request, user)

            # for name, _ in models.Person.person_enum:
            #     models.Person.objects.create(user=user, who=name)

            return redirect("main_list:index")
    else:
        form = UserCreationForm()
    return render(request, "registration/signup.html", {"form": form})

@login_required
def years(request):
    years = models.Item.objects.filter(user=request.user).values_list("year", flat=True).distinct().order_by("-year")
    context = {"years": years}

    return render(request, "main_list/years.html", context)

@login_required
def index(request, year):
    people = models.Person.objects.filter(user=request.user)

    people_with_counts = []
    for name in people:
        count = models.Item.objects.filter(who=name, user=request.user, year=year).count()
        people_with_counts.append({"who": name, "count": count})

    context = {
        "people_with_counts": people_with_counts,
        "year": year
    }

    return render(request, "main_list/index.html", context)

@login_required
def items(request, year, person_name):
    person = get_object_or_404(models.Person, who=person_name, user=request.user)
    items = models.Item.objects.filter(who=person, user=request.user, year=year)
    context={
        "person_name": person_name, 
        "items": items,
        "year": year
    }
    return render(request, "main_list/items.html", context)

@login_required
def add_item(request, year, person_name=None):
    if request.method == "POST":
        name = request.POST.get("name")
        type_gift = request.POST.get("type_gift")
        price = request.POST.get("price")
        tagged_people_data = request.POST.getlist("tagged_people")

        item = models.Item.objects.create(
            user=request.user,
            year=year,
            name=name,
            type_gift=type_gift,
            price=price
        )

        for data in tagged_people_data:
            try:
                person_id = int(data)
                person = models.Person.objects.get(id=person_id, user=request.user)
                item.who.add(person)
            except (ValueError, models.Person.DoesNotExist):
                person, _ = models.Person.objects.get_or_create(
                    user=request.user,
                    who=data
                )
                item.who.add(person)

        if person_name:
            return redirect("main_list:items", person_name=person_name)
        elif tagged_people_data:
            first_data = tagged_people_data[0]
            try:
                person_id = int(first_data)
                first_person = models.Person.objects.get(id=person_id, user=request.user)
            except (ValueError, models.Person.DoesNotExist):
                first_person = models.Person.objects.get(user=request.user, who=first_data)
            return redirect("main_list:items", year=year, person_name=first_person.who)
        else:
            return redirect("main_list:index", year=year)
            
    people = models.Person.objects.filter(user=request.user)
    context = {
        "person_name": person_name,
        "people": people,
        "year": year
    }

    return render(request, "main_list/add_item.html", context)

@login_required
def delete_item(request, item_id):
    item = get_object_or_404(models.Item, id=item_id)

    year = item.year
    first_person = item.who.first()
    person_name = first_person.who if first_person else None

    item.delete()

    if person_name:
        return redirect("main_list:items", year=year, person_name=person_name)
    else:
        return redirect("main_list:index", year=year)

@login_required
def calculator(request, year):
    items = models.Item.objects.filter(user=request.user, year=year)
    
    people_filter = request.GET.getlist('people')
    type_filter = request.GET.getlist('type')
    
    if people_filter:
        items = items.filter(who__who__in=people_filter).distinct()
    
    if type_filter:
        items = items.filter(type_gift__in=type_filter)
    
    total = sum(item.price for item in items)
    
    all_people = models.Person.objects.filter(user=request.user)
    
    context = {
        'items': items,
        'total': total,
        'all_people': all_people,
        'selected_people': people_filter,
        'selected_types': type_filter,
        "year": year
    }
    return render(request, 'main_list/calculator.html', context)