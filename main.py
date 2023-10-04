import click
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, Table
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

# Define the association table for the many-to-many relationship between users and projects
user_project_association = Table(
    'user_project_association',  # Table name
    Base.metadata,  # Metadata object associated with the Base class
    Column('user_id', Integer, ForeignKey('users.id')),  # Foreign key to link users
    Column('project_id', Integer, ForeignKey('projects.id'))  # Foreign key to link projects
)

#Defines the User class as an SQLAlchemy model
class User(Base):
    __tablename__ = 'users' #Table name in the database
    id = Column(Integer, primary_key=True) #Primary key for the User table
    username = Column(String, unique=True) #Unique username for each User

    projects = relationship(
        "Project",  #Relationship with Project class
        secondary=user_project_association,  #Uses the user_project_association table
        back_populates="users"  #Defines the reverse relationship in the Project class
    )

    #Defines the one-to-many relationship between Project and User
    tasks = relationship("Task", back_populates="user")

#Defines the Project class as an SQLAlchemy model
class Project(Base):
    __tablename__ = 'projects' #Table name in the database
    id = Column(Integer, primary_key=True) #Primary key for Project
    name = Column(String) #Name of the project
    name = Column(String, unique=True)  #Unique project-name for each Project

    users = relationship(
        "User",  #Relationship with User class
        secondary=user_project_association,  #Uses the user_project_association table
        back_populates="projects"  #Defines the reverse relationship in the User class
    )

    #Defines the one-to-many relationship between Project and Task
    tasks = relationship("Task", back_populates="project")

#Defines the Task class as an SQLAlchemy model
class Task(Base):
    __tablename__ = 'tasks' #Table name in the database
    id = Column(Integer, primary_key=True) #Primary key for Task
    title = Column(String) #Title of the task
    description = Column(String) #Description of the task
    created_at = Column(DateTime, default=datetime.utcnow) #Timestamp when the task is created

    #Defines the foreign key to associate each task with the project
    project_id = Column(Integer, ForeignKey('projects.id'))

    #Defines the foreign key to associate each task with the user
    user_id = Column(Integer, ForeignKey('users.id'))  

    #Defines the many-to-one relationship between Task and Project
    project = relationship("Project", back_populates="tasks")

    #Defines the many-to-one relationship between Task and User
    user = relationship("User", back_populates="tasks")

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
@click.argument('usernames', nargs=-1, required=True)
def add_project(name, usernames):
    project = Project(name=name) #Creates a project instance

    for username in usernames:
        user = session.query(User).filter_by(username=username).first()
        if user:
            project.users.append(user)
        else:
            print(f'[red]User "{username}" not found.[/red]') #Prints an error message if the user is not found

    session.add(project) #Adds the Project instance to the session
    session.commit() #Commits the transaction to the database
    print(f'[green]Project "{name}" added for users: {", ".join(usernames)}[/green]') #Prints the success message

#Defines the command to add a task to the database
@cli.command()
@click.option('--title', prompt='Task title', help='Title of the task')
@click.option('--description', prompt='Task description', help='Description of the task')
@click.option('--project-name', prompt='Project name', help='Name of the project')
@click.option('--username', prompt='Username', help='Username of the user for whom the task is created')
def add_task(title, description, project_name, username):
    project = session.query(Project).filter_by(name=project_name).first() #Query for the project
    if project: #Checks if the project with the specified name exists in the database
        user = session.query(User).filter_by(username=username).first() #Attempts to fetch the user from the database using the provided username
        if user: #Checks if the user with the specified username exists in the database
            task = Task(title=title, description=description, project=project, user=user)  #Creates a new Task instance with the provided title, description, and associated project and user
            session.add(task) #Adds the newly created task to the session for database insertion
            session.commit() #Commits the changes to the database to save the new task
            print(f'[green]Task "{title}" added to project "{project_name}" for user "{username}".[/green]') #Prints the success message
        else:
            print(f'[red]User "{username}" not found.[/red]') #Prints an error message if the user is not found
    else:
        print(f'[red]Project "{project_name}" not found.[/red]') #Prints an error message if the project is not found

#Entry point for the command-line interface
if __name__ == '__main__':
    cli()