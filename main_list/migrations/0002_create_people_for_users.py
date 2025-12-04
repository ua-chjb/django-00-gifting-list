from django.db import migrations

def create_people_for_existing_users(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    Person = apps.get_model('main_list', 'Person')
    
    people_names = ['Mom', 'Dad', 'Court', 'Andrew', 'Ben', 'Eliza', 'Maggie', 'Phinney', 'Hannah']
    
    for user in User.objects.all():
        for name in people_names:
            Person.objects.get_or_create(user=user, who=name)

class Migration(migrations.Migration):

    dependencies = [
        ('main_list', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_people_for_existing_users),
    ]