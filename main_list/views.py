from django.shortcuts import render, redirect, get_object_or_404
from . import models

# Create your views here.

def index(request):
    people = ['Mom', 'Dad', 'Court', 'Andrew', 'Eliza', 'Maggie', 'Hannah']

    people_with_counts = []
    for name in people:
        person=models.Person.objects.get(who=name)
        count = models.Item.objects.filter(who=person).count()
        people_with_counts.append({"who": name, "count": count})

    return render(request, "main_list/index.html", {"people_with_counts": people_with_counts})

def items(request, person_name):
    person = get_object_or_404(models.Person, who=person_name)
    items = models.Item.objects.filter(who=person)
    context={"person_name": person_name, "items": items}
    return render(request, "main_list/items.html", context)

def add_item(request, person_name=None):
    if request.method == "POST":
        name = request.POST.get("name")
        type_gift = request.POST.get("type_gift")
        price = request.POST.get("price")
        tagged_people_ids = request.POST.getlist("tagged_people")

        item = models.Item.objects.create(
            name=name,
            type_gift=type_gift,
            price=price
        )

        if person_name:
            person = models.Person.objects.get(who=person_name)
            item.who.add(person)
        
        for person_id in tagged_people_ids:
            person = models.Person.objects.get(id=person_id)
            item.who.add(person)

        if person_name:
            return redirect("main_list:items", person_name=person_name)
        elif tagged_people_ids:
            first_person = models.Person.objects.get(id=tagged_people_ids[0])
            return redirect("main_list:items", person_name=first_person.who)
        else:
            return redirect("main_list:index")
    
    people = models.Person.objects.all()
    context = {
        "person_name": person_name,
        "people": people
    }

    return render(request, "main_list/add_item.html", context)

def delete_item(request, item_id):
    item = get_object_or_404(models.Item, id=item_id)

    first_person = item.who.first()
    person_name = first_person.who if first_person else None

    item.delete()

    if person_name:
        return redirect("main_list:items", person_name=person_name)
    else:
        return redirect("main_list:index")
    
def calculator(request):
    items = models.Item.objects.all()
    
    # Get filter parameters
    people_filter = request.GET.getlist('people')
    type_filter = request.GET.getlist('type')
    
    # Apply filters
    if people_filter:
        items = items.filter(who__who__in=people_filter).distinct()
    
    if type_filter:
        items = items.filter(type_gift__in=type_filter)
    
    total = sum(item.price for item in items)
    
    # Get all people for filter dropdown
    all_people = models.Person.objects.all()
    
    context = {
        'items': items,
        'total': total,
        'all_people': all_people,
        'selected_people': people_filter,
        'selected_types': type_filter,
    }
    return render(request, 'main_list/calculator.html', context)