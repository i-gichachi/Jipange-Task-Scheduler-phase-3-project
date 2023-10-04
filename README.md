
## Jipange Task-Scheduler

## Author
i-gichachi

## Description
Jipange Task Scheduler is a tool, for managing tasks via the command line. It enables users to create and organize tasks into projects as assign them to specific users. The application utilizes SQLAlchemy, for efficient database management Click for a command line interface and Rich to provide a user terminal output.

## Setup Instructions
Follow these steps to set up and run the Jipange Task Scheduler on your local machine:

1. Prerequisites
    Python 3.10 or higher Pipenv (for managing Python dependencies)

2. Clone the repository: git@github.com:i-gichachi/Jipange-Task-Scheduler-phase-3-project.git

3. Navigate to the project directory: cd Jiandikishe-Task-Scheduler

4. Navigate to the project directory: pipenv install

5. Activate the Pipenv shell: pipenv shell

6. Start using the Jipange Task Scheduler by running commands like:

        Add a user: python main.py add_user
        Add a project: python main.py add_project
        Add a task: python main.py add_task

7. Run unit tests: python test.py

## Technologies Used
    Python
    SQLAlchemy
    Click
    Rich

## Project Setup
1. main.py: Contains the main application code, including database models, CLI commands, and database setup.
2. test.py: Includes unit tests for the Stack class.
3. Pipfile and Pipfile.lock: Manage Python dependencies.
4. .gitignore: Specifies files and directories to be ignored by Git.
5. task_manager.db: SQLite database file to store user, project, and task data.
