try:
    import Tkinter as tk
    from Tkinter.scrolledtext import ScrolledText
except:
    import tkinter as tk
    from tkinter.scrolledtext import ScrolledText
from tkinter import *
import RPi.GPIO as GPIO
import time
from time import sleep
import random
import threading

# For Debugging - Colors the command line output for easy reading
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# GUI settings
class visuals:
    frame_borderwidth = 5
    label_font = 'helv 16'
    clock_font = 'ariel 18 bold'
    label_status_font = 'helv 24 bold'
    label_background = 'black'
    label_foreground = 'white'
    dark_grey = '#2b2d2f'
    x_padding = 5
    y_padding = 5
    frame_width = 275
    frame_height = 50
    on_btn_x_pos = 40
    off_btn_x_pos = 235


class App(Frame):
    def __init__(self, master = None):
        Frame.__init__(self, master)
        self.grid()
        self.master.title('RIG STATUS AND CONTROL')

        # -- Variable for rinse countdown --
        self.time_remaining = None

        # -- ROW ONE --
        # -- BLACK TANK STATUS FRAME --
        black_tank_status_parent_frame = Frame(master, width = visuals.frame_width, height = visuals.frame_height, bg = visuals.dark_grey, borderwidth = visuals.frame_borderwidth, highlightbackground = 'black', highlightcolor = 'black', highlightthickness = 5)
        black_tank_status_parent_frame.grid(row = 0, column = 0, sticky = W+E+N+S)
        black_tank_status_lbl_frame = Frame(black_tank_status_parent_frame, width = visuals.frame_width, height = visuals.frame_height, bg = visuals.dark_grey)
        black_tank_status_lbl_frame.grid(row = 0, column = 0, sticky = W+E+N+S)
        black_tank_status_frame = Frame(black_tank_status_parent_frame, width = visuals.frame_width, height = visuals.frame_height, bg = visuals.dark_grey)
        black_tank_status_frame.grid(row = 1, column = 0, sticky = W+E+N+S)
        self.black_tank_status_label = tk.Label(black_tank_status_lbl_frame, text = 'BLACK TANK STATUS', font = visuals.label_font, bg = visuals.dark_grey, fg = visuals.label_foreground)
        self.black_tank_status_label.place(x = visuals.frame_width / 2, y = visuals.frame_height / 2, anchor=CENTER)
        self.black_tank_status = tk.Label(black_tank_status_frame, text = 'OK', font = visuals.label_status_font, bg = visuals.dark_grey, fg = visuals.label_foreground)
        self.black_tank_status.place(x = visuals.frame_width / 2, y = visuals.frame_height / 2, anchor=CENTER)
        # -- BATHROOM STATUS FRAME --
        bathroom_tank_status_parent_frame = Frame(master, width = visuals.frame_width, height = visuals.frame_height, bg = visuals.dark_grey, borderwidth = visuals.frame_borderwidth, highlightbackground = 'black', highlightcolor = 'black', highlightthickness = 5)
        bathroom_tank_status_parent_frame.grid(row = 0, column = 1, sticky = W+E+N+S)
        bathroom_tank_status_lbl_frame = Frame(bathroom_tank_status_parent_frame, width = visuals.frame_width, height = visuals.frame_height, bg = visuals.dark_grey)
        bathroom_tank_status_lbl_frame.grid(row = 0, column = 0, sticky = W+E+N+S)
        bathroom_tank_status_frame = Frame(bathroom_tank_status_parent_frame, width = visuals.frame_width, height = visuals.frame_height, bg = visuals.dark_grey)
        bathroom_tank_status_frame.grid(row = 1, column = 0, sticky = W+E+N+S)
        self.bathroom_tank_status_label = tk.Label(bathroom_tank_status_lbl_frame, text = 'BATHROOM TANK STATUS', font = visuals.label_font, bg = visuals.dark_grey, fg = visuals.label_foreground)
        self.bathroom_tank_status_label.place(x = visuals.frame_width / 2, y = visuals.frame_height / 2, anchor=CENTER)
        self.bathroom_tank_status = tk.Label(bathroom_tank_status_frame, text = 'OK', font = visuals.label_status_font, bg = visuals.dark_grey, fg = visuals.label_foreground)
        self.bathroom_tank_status.place(x = visuals.frame_width / 2, y = visuals.frame_height / 2, anchor=CENTER)
        # -- KITCHEN STATUS FRAME --
        kitchen_status_parent_frame = Frame(master, width = visuals.frame_width, height = visuals.frame_height, bg = visuals.dark_grey, borderwidth = visuals.frame_borderwidth, highlightbackground = 'black', highlightcolor = 'black', highlightthickness = 5)
        kitchen_status_parent_frame.grid(row = 0, column = 2, sticky = W+E+N+S)
        kitchen_status_lbl_frame = Frame(kitchen_status_parent_frame, width = visuals.frame_width, height = visuals.frame_height, bg = visuals.dark_grey)
        kitchen_status_lbl_frame.grid(row = 0, column = 0, sticky = W+E+N+S)
        kitchen_status_frame = Frame(kitchen_status_parent_frame, width = visuals.frame_width, height = visuals.frame_height, bg = visuals.dark_grey)
        kitchen_status_frame.grid(row = 1, column = 0, sticky = W+E+N+S)
        self.kitchen_status_label = tk.Label(kitchen_status_lbl_frame, text = 'KITCHEN TANK STATUS', font = visuals.label_font, bg = visuals.dark_grey, fg = visuals.label_foreground)
        self.kitchen_status_label.place(x = visuals.frame_width / 2, y = visuals.frame_height / 2, anchor=CENTER)
        self.kitchen_tank_status = tk.Label(kitchen_status_frame, text = 'OK', font = visuals.label_status_font, bg = visuals.dark_grey, fg = visuals.label_foreground)
        self.kitchen_tank_status.place(x = visuals.frame_width / 2, y = visuals.frame_height / 2, anchor=CENTER)
        # -- ROW TWO --
        black_tank_valve_control_parent_frame = Frame(master, width = visuals.frame_width, height = visuals.frame_height, bg = visuals.dark_grey, borderwidth = visuals.frame_borderwidth, highlightbackground = 'black', highlightcolor = 'black', highlightthickness = 5)
        black_tank_valve_control_parent_frame.grid(row = 1, column = 0, sticky = W+E+N+S)
        black_tank_valve_control_lbl_frame = Frame(black_tank_valve_control_parent_frame, width = visuals.frame_width, height = visuals.frame_height, bg = visuals.dark_grey)
        black_tank_valve_control_lbl_frame.grid(row = 0, column = 0, sticky = W+E+N+S)
        self.black_tank_valve_control_lbl = Label(black_tank_valve_control_lbl_frame, text = 'BLACK TANK VALVE CONTROL', font = visuals.label_font, bg = visuals.dark_grey, fg = visuals.label_foreground)
        self.black_tank_valve_control_lbl.place(x = visuals.frame_width / 2, y = visuals.frame_height / 2, anchor=CENTER)
        black_tank_valve_control_btn_frame = Frame(black_tank_valve_control_parent_frame, width = visuals.frame_width, height = visuals.frame_height, bg = visuals.dark_grey)
        black_tank_valve_control_btn_frame.grid(row = 1, column = 0, sticky = W+E+N+S)
        self.black_tank_valve_btn_on = Button(black_tank_valve_control_btn_frame, width = 5, text = 'ON', font = visuals.label_font, bg = visuals.dark_grey, command = self.blackValveOn)
        self.black_tank_valve_btn_on.place(x = visuals.on_btn_x_pos, y = visuals.frame_height / 2, anchor=W)
        self.black_tank_valve_btn_off = Button(black_tank_valve_control_btn_frame, width = 5, text = 'OFF', font = visuals.label_font, bg = visuals.dark_grey, command = self.blackValveOff)
        self.black_tank_valve_btn_off.place(x = visuals.off_btn_x_pos, y = visuals.frame_height / 2, anchor=E)
        bath_tank_valve_control_parent_frame = Frame(master, width = visuals.frame_width, height = visuals.frame_height, bg = visuals.dark_grey, borderwidth = visuals.frame_borderwidth, highlightbackground = 'black', highlightcolor = 'black', highlightthickness = 5)
        bath_tank_valve_control_parent_frame.grid(row = 1, column = 1, sticky = W+E+N+S)
        bath_tank_valve_control_lbl_frame = Frame(bath_tank_valve_control_parent_frame, width = visuals.frame_width, height = visuals.frame_height, bg = visuals.dark_grey)
        bath_tank_valve_control_lbl_frame.grid(row = 0, column = 0, sticky = W+E+N+S)
        self.bath_tank_valve_control_lbl = Label(bath_tank_valve_control_lbl_frame, text = 'BATH TANK VALVE CONTROL', font = visuals.label_font, bg = visuals.dark_grey, fg = visuals.label_foreground)
        self.bath_tank_valve_control_lbl.place(x = visuals.frame_width / 2, y = visuals.frame_height / 2, anchor=CENTER)
        bath_tank_valve_control_btn_frame = Frame(bath_tank_valve_control_parent_frame, width = visuals.frame_width, height = visuals.frame_height, bg = visuals.dark_grey)
        bath_tank_valve_control_btn_frame.grid(row = 1, column = 0, sticky = W+E+N+S)
        self.bath_tank_valve_btn_on = Button(bath_tank_valve_control_btn_frame, width = 5, text = 'ON', font = visuals.label_font, bg = visuals.dark_grey, command = self.bathValveOn)
        self.bath_tank_valve_btn_on.place(x = visuals.on_btn_x_pos, y = visuals.frame_height / 2, anchor=W)
        self.bath_tank_valve_btn_off = Button(bath_tank_valve_control_btn_frame, width = 5, text = 'OFF', font = visuals.label_font, bg = visuals.dark_grey, command = self.bathValveOff)
        self.bath_tank_valve_btn_off.place(x = visuals.off_btn_x_pos, y = visuals.frame_height / 2, anchor=E)
        kitchen_tank_valve_control_parent_frame = Frame(master, width = visuals.frame_width, height = visuals.frame_height, bg = visuals.dark_grey, borderwidth = visuals.frame_borderwidth, highlightbackground = 'black', highlightcolor = 'black', highlightthickness = 5)
        kitchen_tank_valve_control_parent_frame.grid(row = 1, column = 2, sticky = W+E+N+S)
        kitchen_tank_valve_control_lbl_frame = Frame(kitchen_tank_valve_control_parent_frame, width = visuals.frame_width, height = visuals.frame_height, bg = visuals.dark_grey)
        kitchen_tank_valve_control_lbl_frame.grid(row = 0, column = 0, sticky = W+E+N+S)
        self.kitchen_tank_valve_control_lbl = Label(kitchen_tank_valve_control_lbl_frame, text = 'KITCHEN TANK VALVE CONTROL', font = visuals.label_font, bg = visuals.dark_grey, fg = visuals.label_foreground)
        self.kitchen_tank_valve_control_lbl.place(x = visuals.frame_width / 2, y = visuals.frame_height / 2, anchor=CENTER)
        kitchen_tank_valve_control_btn_frame = Frame(kitchen_tank_valve_control_parent_frame, width = visuals.frame_width, height = visuals.frame_height, bg = visuals.dark_grey)
        kitchen_tank_valve_control_btn_frame.grid(row = 1, column = 0, sticky = W+E+N+S)
        self.kitchen_tank_valve_btn_on = Button(kitchen_tank_valve_control_btn_frame, width = 5, text = 'ON', font = visuals.label_font, bg = visuals.dark_grey, command = self.kitchenValveOn)
        self.kitchen_tank_valve_btn_on.place(x = visuals.on_btn_x_pos, y = visuals.frame_height / 2, anchor=W)
        self.kitchen_tank_valve_btn_off = Button(kitchen_tank_valve_control_btn_frame, width = 5, text = 'OFF', font = visuals.label_font, bg = visuals.dark_grey, command = self.kitchenValveOff)
        self.kitchen_tank_valve_btn_off.place(x = visuals.off_btn_x_pos, y = visuals.frame_height / 2, anchor=E)
        # -- ROW THREE --
        black_tank_rinse_parent_frame = Frame(master, width = visuals.frame_width, height = visuals.frame_height, bg = visuals.dark_grey, borderwidth = visuals.frame_borderwidth, highlightbackground = 'black', highlightcolor = 'black', highlightthickness = 5)
        black_tank_rinse_parent_frame.grid(row = 2, column = 0, sticky = W+E+N+S)
        black_tank_rinse_lbl_frame = Frame(black_tank_rinse_parent_frame, width = visuals.frame_width, height = visuals.frame_height, bg = visuals.dark_grey)
        black_tank_rinse_lbl_frame.grid(row = 0, column = 0, sticky = W+E+N+S)
        self.black_tank_rinse_lbl = Label(black_tank_rinse_lbl_frame, text = 'BLACK TANK RINSE CONTROL', font = visuals.label_font, bg = visuals.dark_grey, fg = visuals.label_foreground)
        self.black_tank_rinse_lbl.place(x = visuals.frame_width / 2, y = visuals.frame_height / 2, anchor=CENTER)
        black_tank_rinse_btn_frame = Frame(black_tank_rinse_parent_frame, width = visuals.frame_width, height = visuals.frame_height, bg = visuals.dark_grey)
        black_tank_rinse_btn_frame.grid(row = 1, column = 0, sticky = W+E+N+S)
        self.black_tank_rinse_btn_on = Button(black_tank_rinse_btn_frame, width = 5, text = 'ON', font = visuals.label_font, bg = visuals.dark_grey, command = self.blackTankRinseOn)
        self.black_tank_rinse_btn_on.place(x = visuals.on_btn_x_pos, y = visuals.frame_height / 2, anchor=W)
        self.black_tank_rinse_btn_off = Button(black_tank_rinse_btn_frame, width = 5, text = 'OFF', font = visuals.label_font, bg = visuals.dark_grey, command = self.blackTankRinseOff)
        self.black_tank_rinse_btn_off.place(x = visuals.off_btn_x_pos, y = visuals.frame_height / 2, anchor=E)
        current_time_frame = Frame(master, width = visuals.frame_width, height = visuals.frame_height, bg = visuals.dark_grey, borderwidth = visuals.frame_borderwidth, highlightbackground = 'black', highlightcolor = 'black', highlightthickness = 5)
        current_time_frame.grid(row = 2, column = 1, sticky = W+E+N+S)
        display_frame = Frame(current_time_frame, width = visuals.frame_width, height = visuals.frame_height, bg = visuals.dark_grey)
        display_frame.grid(row = 0, column = 0, sticky = W+E+N+S)
        self.time_label = Label(display_frame, text = "time", width = visuals.frame_width, height = visuals.frame_height, font = visuals.clock_font, bg = visuals.dark_grey, fg = visuals.label_foreground)
        self.time_label.place(x = visuals.frame_width / 2, y = 25, anchor = CENTER)
        basement_heater_control_parent_frame = Frame(master, width = visuals.frame_width, height = visuals.frame_height, bg = visuals.dark_grey, borderwidth = visuals.frame_borderwidth, highlightbackground = 'black', highlightcolor = 'black', highlightthickness = 5)
        basement_heater_control_parent_frame.grid(row = 2, column = 2, sticky = W+E+N+S)
        basement_heater_control_lbl_frame = Frame(basement_heater_control_parent_frame, width = visuals.frame_width, height = visuals.frame_height, bg = visuals.dark_grey, )
        basement_heater_control_lbl_frame.grid(row = 0, column = 0, sticky = W+E+N+S)
        self.basement_heater_control_lbl = Label(basement_heater_control_lbl_frame, text = 'BASEMENT HEATER CONTROL', font = visuals.label_font, bg = visuals.dark_grey, fg = visuals.label_foreground)
        self.basement_heater_control_lbl.place(x = visuals.frame_width / 2, y = visuals.frame_height / 2, anchor = CENTER)
        basement_heater_control_btn_frame = Frame(basement_heater_control_parent_frame, width = visuals.frame_width, height = visuals.frame_height, bg = visuals.dark_grey)
        basement_heater_control_btn_frame.grid(row = 1, column = 0, sticky = W+E+N+S)
        self.basement_heater_btn_on = Button(basement_heater_control_btn_frame, width = 5, text = 'ON', font = visuals.label_font, bg = visuals.dark_grey, command = self.basementHeaterOn)
        self.basement_heater_btn_on.place(x = visuals.on_btn_x_pos, y = visuals.frame_height / 2, anchor=W)
        self.basement_heater_btn_off = Button(basement_heater_control_btn_frame, width = 5, text = 'OFF', font = visuals.label_font, bg = visuals.dark_grey, command = self.basementHeaterOff)
        self.basement_heater_btn_off.place(x = visuals.off_btn_x_pos, y = visuals.frame_height / 2, anchor=E)
        
        # --- ROW FOUR --
        open_frame = Frame(master, width = visuals.frame_width, height = visuals.frame_height, bg = visuals.dark_grey, borderwidth = visuals.frame_borderwidth, highlightbackground = 'black', highlightcolor = 'black', highlightthickness = 5)
        open_frame.grid(row = 3, column = 0, sticky = W+E+N+S)
        exit_button_frame = Frame(master, width = visuals.frame_width, height = visuals.frame_height, bg = visuals.dark_grey, borderwidth = visuals.frame_borderwidth, highlightbackground = 'black', highlightcolor = 'black', highlightthickness = 5)
        exit_button_frame.grid(row = 3, column = 1, sticky = W+E+N+S)
        exit_button_holder = Frame(exit_button_frame, width = visuals.frame_width, height = visuals.frame_height, bg = visuals.dark_grey)
        exit_button_holder.grid(row = 0, column = 0, sticky = W+E+N+S)
        self.exit_btn = Button(exit_button_frame, width = 5, text = 'EXIT', command = root.destroy)
        self.exit_btn.place(x = visuals.frame_width / 2, y = visuals.frame_height / 2, anchor = CENTER)
        basement_temperature_frame = Frame(master, width = visuals.frame_width, height = visuals.frame_height, bg = visuals.dark_grey, borderwidth = visuals.frame_borderwidth, highlightbackground = 'black', highlightcolor = 'black', highlightthickness = 5)
        basement_temperature_frame.grid(row = 3, column = 2, sticky = W+E+N+S)
        
    
        

    def buzz_on(self, pin = 25):
        self.update_status('Buzzer Activated', 'warning')
        # --- TODO ACTIVATE BUZZER --

    def buzz_off(self, pin = 25):
        self.update_status('Buzzer Deactivated', 'nominal')
        # --- TODO DEACTIVATE BUZZER --

    def blackValveOn(self, pin = None):
        self.update_status('Black Valve ON Button Pressed', 'user_action')
        # --- TODO SET GPIO --

        self.black_tank_valve_control_lbl.config(text = 'BLACK TANK VALVE OPEN')
        self.black_tank_valve_btn_on.config(state = 'disabled')
        self.black_tank_valve_btn_off.config(state = 'normal')

    def blackValveOff(self, pin = None):
        self.update_status('Black Valve OFF Button Pressed', 'user_action')
        # --- TODO SET GPIO --

        self.black_tank_valve_control_lbl.config(text = 'BLACK TANK VALVE CLOSED')
        self.black_tank_valve_btn_off.config(state = 'disabled')
        self.black_tank_valve_btn_on.config(state = 'normal')

    def bathValveOn(self, pin = None):
        self.update_status('Bath Valve ON Button Pressed', 'user_action')
        # --- TODO SET GPIO --

        self.bath_tank_valve_control_lbl.config(text = 'BATH TANK VALVE OPEN')
        self.bath_tank_valve_btn_on.config(state = 'disabled')
        self.bath_tank_valve_btn_off.config(state = 'normal')

    def bathValveOff(self, pin = None):
        self.update_status('Bath Valve OFF Button Pressed', 'user_action')
        # --- TODO SET GPIO --

        self.bath_tank_valve_control_lbl.config(text = 'BATH TANK VALVE CLOSED')
        self.bath_tank_valve_btn_off.config(state = 'disabled')
        self.bath_tank_valve_btn_on.config(state = 'normal')

    def kitchenValveOn(self, pin = None):
        self.update_status('Kitchen Valve ON Button Pressed', 'user_action')
        # --- TODO SET GPIO --

        self.kitchen_tank_valve_control_lbl.config(text = 'KITCHEN TANK VALVE OPEN')
        self.kitchen_tank_valve_btn_on.config(state = 'disabled')
        self.kitchen_tank_valve_btn_off.config(state = 'normal')

    def kitchenValveOff(self, pin = None):
        self.update_status('Kitchen Valve OFF Button Pressed', 'user_action')
        # --- TODO SET GPIO --

        self.kitchen_tank_valve_control_lbl.config(text = 'KITCHEN TANK VALVE CLOSED')
        self.kitchen_tank_valve_btn_off.config(state = 'disabled')
        self.kitchen_tank_valve_btn_on.config(state = 'normal')

    def blackTankRinseOn(self, pin = None):
        self.update_status('Black Rinse ON Button Pressed', 'user_action')
        # --- TODO SET GPIO --

        self.black_tank_rinse_lbl.config(text = 'BLACK RINSE ACTIVE: ')
        self.black_tank_rinse_btn_on.config(state = 'disabled')
        self.black_tank_rinse_btn_off.config(state = 'normal')
 
    def blackTankRinseOff(self, pin = None):
        self.update_status('Black Rinse OFF Button Pressed', 'user_action')
        # --- TODO SET GPIO --

        self.black_tank_rinse_lbl.config(text = 'BLACK TANK RINSE CONTROL')
        self.black_tank_rinse_btn_off.config(state = 'disabled')
        self.black_tank_rinse_btn_on.config(state = 'normal')

    def basementHeaterOn(self, pin = None):
        self.update_status('Basement Heater ON Pressed', 'user_action')
        # --- TODO SET GPIO --

        self.basement_heater_control_lbl.config(text = 'BASEMENT HEATER ACTIVE')
        self.basement_heater_btn_on.config(state = 'disabled')
        self.basement_heater_btn_off.config(state = 'normal')

    def basementHeaterOff(self, pin = None):
        self.update_status('Basement Heater OFF Pressed', 'user_action')
        # --- TODO SET GPIO --

        self.basement_heater_control_lbl.config(text = 'BASEMENT HEATER INACTIVE')
        self.basement_heater_btn_off.config(state = 'disabled')
        self.basement_heater_btn_on.config(state = 'normal')

    def kitchenTankLevel(self, LL3pin = 13):
        reading = 0

        # --- TESTING -- Replace with actual sensor value
        reading = random.randint(0,1)
        # --- END TESTING

        if reading == 0:
            self.buzz_off()
            self.kitchen_tank_status.config(text = 'OK', fg = 'green')
            self.update_status('KITCHEN TANK SENSOR REPORTING STATUS: OK', 'nominal')
        elif reading == 1:
            self.buzz_on()
            self.kitchen_tank_status.config(text = 'FULL', fg = 'red')
            self.update_status('KITCHEN TANK SENSOR REPORTING STATUS: FULL', 'error')
        self.kitchen_tank_status.after(2000, self.kitchenTankLevel)

    def bathTankLevel(self, LL2pin = 6):
        reading = 0

        # --- TESTING -- Replace with actual sensor value
        reading = random.randint(0,1)
        # --- END TESTING

        if reading == 0:
            self.buzz_off()
            self.bathroom_tank_status.config(text = 'OK', fg = 'green')
            self.update_status('BATH TANK SENSOR REPORTING STATUS: OK', 'nominal')
        elif reading == 1:
            self.buzz_on()
            self.bathroom_tank_status.config(text = 'FULL', fg = 'red')
            self.update_status('BATH TANK SENSOR REPORTING STATUS: FULL', 'error')
        self.bathroom_tank_status.after(2000, self.bathTankLevel)

    def blackTankLevel(self, LL1pin = 6):
        reading = 0

        # --- TESTING -- Replace with actual sensor value
        reading = random.randint(0,1)
        # --- END TESTING

        if reading == 0:
            self.buzz_off()
            self.black_tank_status.config(text = 'OK', fg = 'green')
            self.update_status('BLACK TANK REPORTING STATUS OK', 'nominal')
        elif reading == 1:
            self.buzz_on()
            self.black_tank_status.config(text = 'FULL', fg = 'red')
            self.update_status('BLACK TANK SENSOR REPORTING STATUS: FULL', 'error')
        self.black_tank_status.after(2000, self.blackTankLevel)


    def update_time(self):
        self.time_string = time.strftime('%I:%M:%S %p')
        self.time_label.config(text = self.time_string)
        self.time_label.after(200, self.update_time)

    
    def update_status(self, msg, sender):
        print(msg)


if __name__ == '__main__':

    root = Tk()
    app = App(root)
    app.update_time()
    app.kitchenTankLevel()
    app.bathTankLevel()
    app.blackTankLevel()
    root.mainloop()

