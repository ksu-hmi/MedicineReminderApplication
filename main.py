import schedule
import time

from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.list import MDList, OneLineListItem
from plyer import notification
from database import ReminderDatabase


KV = '''
ScreenManager:
    MenuScreen:
    ReminderScreen:
    ListRemindersScreen:

<MenuScreen>:
    name: 'menu'

    MDLabel:
        text: "Medicine Reminder"
        halign: 'center'
        pos_hint: {'center_y': 0.8}
        font_style: 'H4'

    MDRaisedButton:
        text: "Set Reminder"
        pos_hint: {'center_x': 0.5, 'center_y': 0.6}
        on_release: app.show_reminder_screen()

    MDRaisedButton:
        text: "View Reminders"
        pos_hint: {'center_x': 0.5, 'center_y': 0.4}
        on_release: app.show_list_reminders_screen()

<ReminderScreen>:
    name: 'reminder'

    MDTextField:
        id: med_name
        hint_text: "Medication Name"
        pos_hint: {'center_x': 0.5, 'center_y': 0.7}
        size_hint_x: 0.8

    MDTextField:
        id: interval
        hint_text: "Reminder Interval (hours)"
        pos_hint: {'center_x': 0.5, 'center_y': 0.5}
        size_hint_x: 0.8
        input_filter: 'int'

    MDRaisedButton:
        text: "Set Reminder"
        pos_hint: {'center_x': 0.5, 'center_y': 0.3}
        on_release: app.set_reminder()

<ListRemindersScreen>:
    name: 'list_reminders'

    BoxLayout:
        orientation: 'vertical'
        
        ScrollView:
            MDList:
                id: reminder_list

    MDRaisedButton:
        text: "Back to Menu"
        pos_hint: {'center_x': 0.5, 'center_y': 0.1}
        on_release: app.show_menu_screen()
'''

class MenuScreen(Screen):
    pass

class ReminderScreen(Screen):
    pass

class ListRemindersScreen(Screen):
    pass

class ReminderApp(MDApp):
    def build(self):
        self.db = ReminderDatabase()
        return Builder.load_string(KV)

    def show_reminder_screen(self):
        self.root.current = 'reminder'

    def show_list_reminders_screen(self):
        self.load_reminders()
        self.root.current = 'list_reminders'

    def show_menu_screen(self):
        self.root.current = 'menu'

    def set_reminder(self):
        med_name = self.root.get_screen('reminder').ids.med_name.text
        interval = self.root.get_screen('reminder').ids.interval.text
        
        if med_name and interval.isdigit():
            interval = int(interval)
            self.db.add_reminder(med_name, interval)
            schedule.every(interval).hours.do(self.remind_user, med_name=med_name)
            self.show_dialog("Reminder set for {} every {} hours.".format(med_name, interval))
            self.root.current = 'menu'
        else:
            self.show_dialog("Please enter valid details.")

    def remind_user(self, med_name):
        notification.notify(
            title="Medication Reminder",
            message=f"It's time to take your {med_name}",
            timeout=10
        )

    def show_dialog(self, message):
        dialog = MDDialog(
            title="Reminder",
            text=message,
            size_hint=(0.8, 1),
            buttons=[
                MDRaisedButton(
                    text="OK",
                    on_release=lambda x: self.close_dialog(dialog)
                ),
            ],
        )
        dialog.open()

    def close_dialog(self, dialog):
        dialog.dismiss()

    def on_start(self):
        self.load_reminders()
        from threading import Thread
        Thread(target=self.run_schedule).start()

    def run_schedule(self):
        while True:
            schedule.run_pending()
            time.sleep(1)

    def load_reminders(self):
        reminder_list = self.root.get_screen('list_reminders').ids.reminder_list
        reminder_list.clear_widgets()

        reminders = self.db.get_reminders()
        for reminder in reminders:
            item = OneLineListItem(
                text=f"{reminder[1]} every {reminder[2]} hours",
                on_release=lambda x, r=reminder: self.edit_reminder(r)
            )
            reminder_list.add_widget(item)

    def edit_reminder(self, reminder):
        reminder_id, med_name, interval = reminder

        # Show dialog to edit or delete the reminder
        dialog = MDDialog(
            title="Edit Reminder",
            type="custom",
            content_cls=BoxLayout(orientation='vertical'),
            buttons=[
                MDRaisedButton(
                    text="Update",
                    on_release=lambda x: self.update_reminder(reminder_id, dialog)
                ),
                MDRaisedButton(
                    text="Delete",
                    on_release=lambda x: self.delete_reminder(reminder_id, dialog)
                ),
                MDRaisedButton(
                    text="Cancel",
                    on_release=lambda x: self.close_dialog(dialog)
                ),
            ],
        )

        dialog.content_cls.add_widget(MDTextField(
            id='edit_med_name',
            text=med_name,
            hint_text="Medication Name",
            pos_hint={'center_x': 0.5, 'center_y': 0.7},
            size_hint_x=0.8
        ))
        dialog.content_cls.add_widget(MDTextField(
            id='edit_interval',
            text=str(interval),
            hint_text="Reminder Interval (hours)",
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            size_hint_x=0.8,
            input_filter='int'
        ))

        dialog.open()

    def update_reminder(self, reminder_id, dialog):
        med_name = dialog.content_cls.ids.edit_med_name.text
        interval = dialog.content_cls.ids.edit_interval.text
        
        if med_name and interval.isdigit():
            interval = int(interval)
            self.db.update_reminder(reminder_id, med_name, interval)
            self.show_dialog("Reminder updated for {} every {} hours.".format(med_name, interval))
            self.load_reminders()
            self.root.current = 'list_reminders'
        else:
            self.show_dialog("Please enter valid details.")
        self.close_dialog(dialog)

    def delete_reminder(self, reminder_id, dialog):
        self.db.delete_reminder(reminder_id)
        self.show_dialog("Reminder deleted.")
        self.load_reminders()
        self.root.current = 'list_reminders'
        self.close_dialog(dialog)

if __name__ == "__main__":
    ReminderApp().run()
