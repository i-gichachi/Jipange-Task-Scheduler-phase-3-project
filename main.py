import click
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from rich import print

engine = create_engine('sqlite:///task_manager.db')
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    # Define the one-to-many relationship between User and Project
    projects = relationship("Project", back_populates="user")

class Project(Base):
    __tablename__ = 'projects'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))
    # Define the many-to-one relationship between Project and User
    user = relationship("User", back_populates="projects")
    tasks = relationship("Task", back_populates="project")

class Task(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    project_id = Column(Integer, ForeignKey('projects.id'))
    project = relationship("Project", back_populates="tasks")

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


Base.metadata.create_all(engine)

@click.group()
def cli():
    pass

@cli.command()
@click.option('--username', prompt='Username', help='Username of the user')
def add_user(username):
    user = User(username=username)
    session.add(user)
    session.commit()
    print(f'[green]User "{username}" added.[/green]')

@cli.command()
@click.option('--name', prompt='Project name', help='Name of the project')
@click.option('--username', prompt='Username', help='Username of the user')
def add_project(name, username):
    user = session.query(User).filter_by(username=username).first()
    if user:
        project = Project(name=name, user=user)
        session.add(project)
        session.commit()
        print(f'[green]Project "{name}" added for user "{username}".[/green]')
    else:
        print(f'[red]User "{username}" not found.[/red]')

@cli.command()
@click.option('--title', prompt='Task title', help='Title of the task')
@click.option('--description', prompt='Task description', help='Description of the task')
@click.option('--project-name', prompt='Project name', help='Name of the project')
def add_task(title, description, project_name):
    project = session.query(Project).filter_by(name=project_name).first()
    if project:
        task = Task(title=title, description=description, project=project)
        session.add(task)
        session.commit()
        print(f'[green]Task "{title}" added to project "{project_name}".[/green]')
    else:
        print(f'[red]Project "{project_name}" not found.[/red]')

if __name__ == '__main__':
    cli()