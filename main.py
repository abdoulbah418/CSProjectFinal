import os
from os.path import exists
import click
from ics import Calendar, Event, DisplayAlarm, Todo
from datetime import datetime, timedelta
from prettytable import PrettyTable
import uuid

# this is the overarching command that houese the clases and reminder manafer and soon to be more managers
# this first cli() will be contruscting the calendar variable to be used by the other commands. this is very important as the ics file will be our database.
@click.group()
@click.option('--ics', type=click.Path(writable=True), required=True)
@click.pass_context
def cli(ctx, ics):
    """ Life Manager App """
    if not exists(ics):
        with open(ics, 'x') as ics_file:
            pass
    if os.stat(ics).st_size != 0:
        with open(ics, 'r') as ics_file:
            calendar = Calendar(ics_file.read())
    else:
        calendar = Calendar()
    ctx.obj = {
        "calendar": calendar,
        "ics_path": ics
    }


# this is the classes manager that will show, add, remove an later on do more
# it will be passing the context wiht teh clandear object insinde of it to the lower commands such as the show, add and reme and later on more.
@cli.group()
@click.pass_context
def classes(ctx):
    """ Classes Manager """
    pass


# this command print the currnt classes in the calnedar object in a pretty format!!!
@classes.command()
@click.pass_obj
def show(obj):
    x = PrettyTable()
    x.field_names = ["UID", "Name", "Begin Time", "End Time", "Description"]
    for event in obj['calendar'].events:
        x.add_row([event.uid, event.name, event.begin, event.end, event.description])
    click.echo(x)
        
# this command add a class toteh cladnerar and save ittot hte database and take the option flags name ngin and end to consturct the class event
@classes.command()
@click.option('--name', required=True)
@click.option('--begin', type=click.DateTime(), required=True)
@click.option('--end', type=click.DateTime(), required=True)
@click.pass_obj
def add(obj, name, begin, end):
    e = Event(name, begin, end, uid=str(uuid.uuid4()))
    obj['calendar'].events.add(e)
    save_ics(obj['calendar'], obj['ics_path'])


# this command remove a class with teh uid specificy to it e accuratly find the clss and remov. WHy uid, because names are not unique .
@classes.command()
@click.option('--uid', required=True)
@click.pass_obj
def remove(obj, uid):
    event_to_be_removed = None
    for event in obj['calendar'].events:
        if event.uid == uid:
            event_to_be_removed = event
    
    obj['calendar'].events.remove(event_to_be_removed)
    save_ics(obj['calendar'], obj['ics_path'])


# rmeinder command group that iwl house the show, add remove, command in it and hopefuly more :))))
@cli.group()
@click.pass_context
def reminders(ctx):
    """ Reminders """
    click.echo("reminders")


# this command print the currnt classes in the calnedar object in a pretty format!!!
@reminders.command()
@click.pass_obj
def show(obj):
    x = PrettyTable()
    x.field_names = ["UID", "Name", "Time", "Completed"]
    for todo in obj['calendar'].todos:
        x.add_row([todo.uid, todo.name, todo.dtstamp, todo.completed])
    click.echo(x)

# this command compeoted a atask that was add to teh reminders dtabase 
@reminders.command()
@click.option('--uid', required=True)
@click.pass_obj
def complete(obj, uid):
    todo_to_be_completed = None
    for todo in obj['calendar'].todos:
        if todo.uid == uid:
            todo_to_be_completed = todo
    if todo_to_be_completed == None:
        click.echo("Could not find the todo")
    else:
        todo_to_be_completed.completed = datetime.now()
        save_ics(obj['calendar'], obj['ics_path'])


# this command add a reminder toteh cladnerar and save ittot hte database and take the option flags name ngin and end to consturct the reminder event
@reminders.command()
@click.option('--name', required=True)
@click.option('--time', type=click.DateTime(), required=True)
@click.pass_obj
def add(obj, name, time):
    t = Todo(name=name, uid=str(uuid.uuid4()), due=time)
    obj['calendar'].todos.add(t)
    save_ics(obj['calendar'], obj['ics_path'])


# this command rmeoves!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! based on the uid provided to provide accuracy :)))):))):):):):)
@reminders.command()
@click.option('--uid', required=True)
@click.pass_obj
def remove(obj, uid):
    todo_to_be_removed = None
    for todo in obj['calendar'].todos:
        if todo.uid == uid:
            todo_to_be_removed = todo
    
    obj['calendar'].todos.remove(todo_to_be_removed)
    save_ics(obj['calendar'], obj['ics_path'])


# this is the save util ics that will save the infromation form teh add command for the clases manager and reminder manager!!!!
# ics is standard that have been improving with time thanks to the giants such as apple and google. TO have used another database will be extra uncessary work :)))!!
def save_ics(calendar, path):
    with open(path, 'w') as file:
        file.write(str(calendar))

if __name__ == '__main__':
    cli()