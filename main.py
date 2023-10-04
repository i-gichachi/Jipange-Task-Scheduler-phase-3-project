import click
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from rich import print

#Creates an SQLite database engine and binds it to 'task_manager.db'
engine = create_engine('sqlite:///task_manager.db')

#Creates a base class for declarative SQLAlchemy models
Base = declarative_base()

#Creates a session factory to interact with the database
Session = sessionmaker(bind=engine)

#Creates a session object for database operations
session = Session()

#Defines the User class as an SQLAlchemy model
class User(Base):
    __tablename__ = 'users' #Table name in the database
    id = Column(Integer, primary_key=True) #Primary key for the User table
    username = Column(String, unique=True) #Unique username for each User

    #Defines the one-to-many relationship between User and Project
    projects = relationship("Project", back_populates="user")

#Defines the Project class as an SQLAlchemy model
class Project(Base):
    __tablename__ = 'projects' #Table name in the database
    id = Column(Integer, primary_key=True) #Primary key for Project
    name = Column(String) #Name of the project

    #Defines the foreign key to associate each project with a user
    user_id = Column(Integer, ForeignKey('users.id'))

    #Defines the many-to-one relationship between Project and User
    user = relationship("User", back_populates="projects")

    #Defines the one-to-many relationship between Project and Task
    tasks = relationship("Task", back_populates="project")

#Defines the Task class as an SQLAlchemy model
class Task(Base):
    __tablename__ = 'tasks' #Table name in the database
    id = Column(Integer, primary_key=True) #Primary key for Task
    title = Column(String) #Title of the task
    description = Column(String) #Description of the task
    created_at = Column(DateTime, default=datetime.utcnow) #Timestamp when the task is created

    #Defines the foreign key to associate each task with a project
    project_id = Column(Integer, ForeignKey('projects.id'))

    #Defines the many-to-one relationship between Task and Proj
    project = relationship("Project", back_populates="tasks")

#Defines the Stack class for managing a stack of items
class Stack:
    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if not self.is_empty():
            return self.items.pop()
        else:
            return None

    def is_empty(self):
        return len(self.items) == 0

#Creates the database tables based on the defined models
Base.metadata.create_all(engine)

#Defines the command-line interface using Click
@click.group()
def cli():
    pass

#Defines the command to add a user to the database
@cli.command()
@click.option('--username', prompt='Username', help='Username of the user')
def add_user(username):
    user = User(username=username) #Creates the User instance
    session.add(user) #Adds the User instance to the session
    session.commit() #Commits the transaction to the database
    print(f'[green]User "{username}" added.[/green]') #Prints the success message

#Defines the command to add a project to the database
@cli.command()
@click.option('--name', prompt='Project name', help='Name of the project')
@click.option('--username', prompt='Username', help='Username of the user')
def add_project(name, username):
    user = session.query(User).filter_by(username=username).first() #Query for the user
    if user:
        project = Project(name=name, user=user) #Creates the Project instance associated with the user
        session.add(project) #Adds the Project instance to the session
        session.commit() #Commits the transaction to the database
        print(f'[green]Project "{name}" added for user "{username}".[/green]') #Prints the success message
    else:
        print(f'[red]User "{username}" not found.[/red]') #Prints an error message if the user is not found

#Defines the command to add a task to the database
@cli.command()
@click.option('--title', prompt='Task title', help='Title of the task')
@click.option('--description', prompt='Task description', help='Description of the task')
@click.option('--project-name', prompt='Project name', help='Name of the project')
def add_task(title, description, project_name):
    project = session.query(Project).filter_by(name=project_name).first() #Query for the project
    if project:
        task = Task(title=title, description=description, project=project) #Creates the Task instance associated with the project
        session.add(task) #Adds the Task instance to the session
        session.commit() #Commits the transaction to the database
        print(f'[green]Task "{title}" added to project "{project_name}".[/green]') #Prints the success message
    else:
        print(f'[red]Project "{project_name}" not found.[/red]') #Prints an error message if the project is not found

#Entry point for the command-line interface
if __name__ == '__main__':
    cli()