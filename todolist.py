from sqlalchemy import create_engine

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime, timedelta

from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///todo.db?check_same_thread=False')

Base = declarative_base()

class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String, default='default_value')
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.string_field

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

class Menu():

    def show_menu(self):
        print("1) Today's tasks\n"
              "2) Week's tasks\n"
              "3) All tasks\n"
              "4) Missed tasks\n"
              "5) Add task\n"
              "6) Delete task\n"
              "0) Exit")
        self.ask_for_action()

    def ask_for_action(self):
        action = int(input())
        self.start_activity(action)

    def print_tasks(self, rows):
        i = 0
        while i < len(rows):
            row_i = rows[i]
            deadline_day = row_i.deadline.day
            deadline_month = row_i.deadline.strftime('%b')

            print(f"{i+1}. {row_i.task}. {deadline_day} {deadline_month}")
            i += 1

    def start_activity(self, action):
        today = datetime.today()

        # Today's tasks
        if action == 1:
            today_day = today.day
            today_month = today.strftime('%b')
            print(f'Today: {today_day} {today_month}')

            rows = session.query(Table).filter(Table.deadline == today.date()).all()
            if len(rows) == 0:
                print("Nothing to do!")
                self.show_menu()
            else:
                self.print_tasks(rows)
                self.show_menu()

        # Week's tasks
        elif action == 2:
            days_from_today = 0
            while days_from_today < 7:
                weekday = today + timedelta(days_from_today)
                rows = session.query(Table).filter(Table.deadline == weekday.date()).all()

                weekday_day = weekday.day
                weekday_month = weekday.strftime('%b')

                days_of_week = {0: 'Monday',
                    1: 'Tuesday',
                    2: 'Wednesday',
                    3: 'Thursday',
                    4: 'Friday',
                    5: 'Saturday',
                    6: 'Sunday'}

                weekday_number = weekday.weekday()
                weekday_weekday = days_of_week[weekday_number]

                print(f'\n{weekday_weekday} {weekday_day} {weekday_month}')
                if len(rows) == 0:
                    print("Nothing to do!")
                    days_from_today += 1
                else:
                    self.print_tasks(rows)
                    days_from_today += 1

            self.show_menu()

        # All tasks
        elif action == 3:
            rows = session.query(Table).order_by(Table.deadline).all()

            today_day = today.day
            today_month = today.strftime('%b')
            print(f'Today: {today_day} {today_month}')

            if len(rows) == 0:
                print("Nothing to do!")
            else:
                self.print_tasks(rows)

            self.show_menu()

        # Missed tasks
        elif action == 4:
            rows = session.query(Table).filter(Table.deadline < today.date()).order_by(Table.deadline).all()

            print("Missed tasks:")
            if len(rows) == 0:
                print("Nothing is missed!")
            else:
                self.print_tasks(rows)
            print("")

            self.show_menu()

        # Add task
        elif action == 5:
            new_task = input('Enter task\n')
            new_task_deadline = input('Enter deadline\n')

            task_deadline = datetime.strptime(new_task_deadline, '%Y-%m-%d')

            new_row = Table(task = new_task, deadline = task_deadline)
            session.add(new_row)
            session.commit()
            print('The task has been added!')
            self.show_menu()

        # Delete task
        elif action == 6:
            rows = session.query(Table).order_by(Table.deadline).all()

            print("Choose the number of the task you want to delete:")
            if len(rows) == 0:
                print("Nothing to delete")
            else:
                self.print_tasks(rows)

            task_to_delete = int(input())
            specific_row = rows[task_to_delete-1]
            session.delete(specific_row)
            session.commit()
            print('The task has been deleted!')
            self.show_menu()

        else:
            print("Bye")
            return None

menu2 = Menu()
menu2.show_menu()
