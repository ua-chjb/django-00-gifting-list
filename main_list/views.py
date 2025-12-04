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

            for name, _ in models.Person.person_enum:
                models.Person.objects.create(user=user, who=name)

            return redirect("main_list:index")
    else:
        form = UserCreationForm()
    return render(request, "registration/signup.html", {"form": form})

@login_required
def index(request):
    people = models.Person.objects.filter(user=request.user)

    people_with_counts = []
    for name in people:
        count = models.Item.objects.filter(who=name, user=request.user).count()
        people_with_counts.append({"who": name, "count": count})

    return render(request, "main_list/index.html", {"people_with_counts": people_with_counts})

@login_required
def items(request, person_name):
    person = get_object_or_404(models.Person, who=person_name, user=request.user)
    items = models.Item.objects.filter(who=person, user=request.user)
    context={
        "person_name": person_name, 
        "items": items
    }
    return render(request, "main_list/items.html", context)

@login_required
def add_item(request, person_name=None):
    if request.method == "POST":
        name = request.POST.get("name")
        type_gift = request.POST.get("type_gift")
        price = request.POST.get("price")
        tagged_people_ids = request.POST.getlist("tagged_people")

        item = models.Item.objects.create(
            user=request.user,
            name=name,
            type_gift=type_gift,
            price=price
        )

        if person_name:
            person = models.Person.objects.get(who=person_name, user=request.user)
            item.who.add(person)
        
        for person_id in tagged_people_ids:
            person = models.Person.objects.get(id=person_id, user=request.user)
            item.who.add(person)

        if person_name:
            return redirect("main_list:items", person_name=person_name)
        elif tagged_people_ids:
            first_person = models.Person.objects.get(id=tagged_people_ids[0], user=request.user)
            return redirect("main_list:items", person_name=first_person.who)
        else:
            return redirect("main_list:index")
    
    people = models.Person.objects.filter(user=request.user)
    context = {
        "person_name": person_name,
        "people": people
    }

    return render(request, "main_list/add_item.html", context)

@login_required
def delete_item(request, item_id):
    item = get_object_or_404(models.Item, id=item_id)

    first_person = item.who.first()
    person_name = first_person.who if first_person else None

    item.delete()

    if person_name:
        return redirect("main_list:items", person_name=person_name)
    else:
        return redirect("main_list:index")

@login_required
def calculator(request):
    print(f"Current user: {request.user.username}")  # Debug
    items = models.Item.objects.filter(user=request.user)
    print(f"Items count: {items.count()}")  # Debug
    
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
    }
    return render(request, 'main_list/calculator.html', context)