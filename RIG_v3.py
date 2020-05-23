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

        # VARIABLES
        self.abort_black_rinse = False
        self.open_img = PhotoImage(file = 'assets/open.gif')
        self.closed_img = PhotoImage(file = 'assets/closed.gif')

        # GPIO SETUP
        self.GPIO_black_tank_sensor = 5
        self.GPIO_bathroom_tank_sensor = 6
        self.GPIO_kitchen_tank_sensor = 13
        self.GPIO_basement_heater_sensor = 19 # Does this return a temperature value?
        self.GPIO_black_tank_valve = 26
        self.GPIO_bathroom_tank_valve = 12
        self.GPIO_kitchen_tank_valve = 16
        self.GPIO_heater_switch = 21
        self.GPIO_black_tank_rinse_valve = 20
        self.GPIO_alarm_silence = 25

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.GPIO_black_tank_sensor, GPIO.IN)    #input for black tank liquid level
        GPIO.setup(self.GPIO_bathroom_tank_sensor, GPIO.IN)    #input for bathroom tank liquid level
        GPIO.setup(self.GPIO_kitchen_tank_sensor, GPIO.IN)   #input for kitchen tank liquid level
        GPIO.setup(self.GPIO_basement_heater_sensor, GPIO.IN)   #input for basement heater
        GPIO.setup(self.GPIO_black_tank_valve, GPIO.OUT)  #relay control to open/close black tank valve
        GPIO.setup(self.GPIO_bathroom_tank_valve, GPIO.OUT)  #relay control to open/close bathroom tank valve
        GPIO.setup(self.GPIO_kitchen_tank_valve, GPIO.OUT)  #relay control to open/close kitchen tank valve
        GPIO.setup(self.GPIO_heater_switch, GPIO.OUT)  #relay control to turn heater power on/off
        GPIO.setup(self.GPIO_black_tank_rinse_valve, GPIO.OUT)  #relay turn on/off black tank rinse valve
        GPIO.setup(self.GPIO_alarm_silence, GPIO.OUT)  #output to turn  tank acknoledgw/silence full alarm

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
        black_tank_valve_status_lbl_frame = Frame(black_tank_valve_control_parent_frame, width = visuals.frame_width, height = visuals.frame_height, bg = visuals.dark_grey)
        black_tank_valve_status_lbl_frame.grid(row = 1, column = 0, sticky = W+E+N+S)
        self.black_tank_valve_control_status_lbl = Label(black_tank_valve_status_lbl_frame, image = self.closed_img, font = visuals.label_font, bg = visuals.dark_grey, fg = visuals.label_foreground)
        self.black_tank_valve_control_status_lbl.place(x = visuals.frame_width / 2, y = visuals.frame_height / 2, anchor=CENTER)
        black_tank_valve_control_btn_frame = Frame(black_tank_valve_control_parent_frame, width = visuals.frame_width, height = visuals.frame_height, bg = visuals.dark_grey)
        black_tank_valve_control_btn_frame.grid(row = 2, column = 0, sticky = W+E+N+S)
        self.black_tank_valve_btn_on = Button(black_tank_valve_control_btn_frame, width = 5, text = 'OPEN', font = visuals.label_font, bg = visuals.dark_grey, command = self.blackValveOpen)
        self.black_tank_valve_btn_on.place(x = visuals.on_btn_x_pos, y = visuals.frame_height / 2, anchor=W)
        self.black_tank_valve_btn_off = Button(black_tank_valve_control_btn_frame, width = 5, text = 'CLOSE', font = visuals.label_font, bg = visuals.dark_grey, command = self.blackValveClosed)
        self.black_tank_valve_btn_off.place(x = visuals.off_btn_x_pos, y = visuals.frame_height / 2, anchor=E)
        bath_tank_valve_control_parent_frame = Frame(master, width = visuals.frame_width, height = visuals.frame_height, bg = visuals.dark_grey, borderwidth = visuals.frame_borderwidth, highlightbackground = 'black', highlightcolor = 'black', highlightthickness = 5)
        bath_tank_valve_control_parent_frame.grid(row = 1, column = 1, sticky = W+E+N+S)
        bath_tank_valve_control_lbl_frame = Frame(bath_tank_valve_control_parent_frame, width = visuals.frame_width, height = visuals.frame_height, bg = visuals.dark_grey)
        bath_tank_valve_control_lbl_frame.grid(row = 0, column = 0, sticky = W+E+N+S)
        self.bath_tank_valve_control_lbl = Label(bath_tank_valve_control_lbl_frame, text = 'BATH TANK VALVE CONTROL', font = visuals.label_font, bg = visuals.dark_grey, fg = visuals.label_foreground)
        self.bath_tank_valve_control_lbl.place(x = visuals.frame_width / 2, y = visuals.frame_height / 2, anchor=CENTER)
        bath_tank_valve_status_lbl_frame = Frame(bath_tank_valve_control_parent_frame, width = visuals.frame_width, height = visuals.frame_height, bg = visuals.dark_grey)
        bath_tank_valve_status_lbl_frame.grid(row = 1, column = 0, sticky = W+E+N+S)
        self.bath_tank_valve_control_status_lbl = Label(bath_tank_valve_status_lbl_frame, image = self.closed_img, font = visuals.label_font, bg = visuals.dark_grey, fg = visuals.label_foreground)
        self.bath_tank_valve_control_status_lbl.place(x = visuals.frame_width / 2, y = visuals.frame_height / 2, anchor=CENTER)
        bath_tank_valve_control_btn_frame = Frame(bath_tank_valve_control_parent_frame, width = visuals.frame_width, height = visuals.frame_height, bg = visuals.dark_grey)
        bath_tank_valve_control_btn_frame.grid(row = 2, column = 0, sticky = W+E+N+S)
        self.bath_tank_valve_btn_on = Button(bath_tank_valve_control_btn_frame, width = 5, text = 'OPEN', font = visuals.label_font, bg = visuals.dark_grey, command = self.bathValveOn)
        self.bath_tank_valve_btn_on.place(x = visuals.on_btn_x_pos, y = visuals.frame_height / 2, anchor=W)
        self.bath_tank_valve_btn_off = Button(bath_tank_valve_control_btn_frame, width = 5, text = 'CLOSE', font = visuals.label_font, bg = visuals.dark_grey, command = self.bathValveOff)
        self.bath_tank_valve_btn_off.place(x = visuals.off_btn_x_pos, y = visuals.frame_height / 2, anchor=E)
        kitchen_tank_valve_control_parent_frame = Frame(master, width = visuals.frame_width, height = visuals.frame_height, bg = visuals.dark_grey, borderwidth = visuals.frame_borderwidth, highlightbackground = 'black', highlightcolor = 'black', highlightthickness = 5)
        kitchen_tank_valve_control_parent_frame.grid(row = 1, column = 2, sticky = W+E+N+S)
        kitchen_tank_valve_control_lbl_frame = Frame(kitchen_tank_valve_control_parent_frame, width = visuals.frame_width, height = visuals.frame_height, bg = visuals.dark_grey)
        kitchen_tank_valve_control_lbl_frame.grid(row = 0, column = 0, sticky = W+E+N+S)
        self.kitchen_tank_valve_control_lbl = Label(kitchen_tank_valve_control_lbl_frame, text = 'KITCHEN TANK VALVE CONTROL', font = visuals.label_font, bg = visuals.dark_grey, fg = visuals.label_foreground)
        self.kitchen_tank_valve_control_lbl.place(x = visuals.frame_width / 2, y = visuals.frame_height / 2, anchor=CENTER)
        kitchen_tank_valve_status_lbl_frame = Frame(kitchen_tank_valve_control_parent_frame, width = visuals.frame_width, height = visuals.frame_height, bg = visuals.dark_grey)
        kitchen_tank_valve_status_lbl_frame.grid(row = 1, column = 0, sticky = W+E+N+S)
        self.kitchen_tank_valve_control_status_lbl = Label(kitchen_tank_valve_status_lbl_frame, image = self.closed_img, font = visuals.label_font, bg = visuals.dark_grey, fg = visuals.label_foreground)
        self.kitchen_tank_valve_control_status_lbl.place(x = visuals.frame_width / 2, y = visuals.frame_height / 2, anchor=CENTER)
        kitchen_tank_valve_control_btn_frame = Frame(kitchen_tank_valve_control_parent_frame, width = visuals.frame_width, height = visuals.frame_height, bg = visuals.dark_grey)
        kitchen_tank_valve_control_btn_frame.grid(row = 2, column = 0, sticky = W+E+N+S)
        self.kitchen_tank_valve_btn_on = Button(kitchen_tank_valve_control_btn_frame, width = 5, text = 'OPEN', font = visuals.label_font, bg = visuals.dark_grey, command = self.kitchenValveOn)
        self.kitchen_tank_valve_btn_on.place(x = visuals.on_btn_x_pos, y = visuals.frame_height / 2, anchor=W)
        self.kitchen_tank_valve_btn_off = Button(kitchen_tank_valve_control_btn_frame, width = 5, text = 'CLOSE', font = visuals.label_font, bg = visuals.dark_grey, command = self.kitchenValveOff)
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

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.HIGH)

    def buzz_off(self, pin = 25):
        self.update_status('Buzzer Deactivated', 'nominal')
        
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.LOW)


        """
        self.GPIO_black_tank_sensor = 5
        self.GPIO_bathroom_tank_sensor = 6
        self.GPIO_kitchen_tank_sensor = 13
        self.GPIO_basement_heater_sensor = 19 # Does this return a temperature value?
        self.GPIO_black_tank_valve = 26
        self.GPIO_bathroom_tank_valve = 12
        self.GPIO_kitchen_tank_valve = 16
        self.GPIO_heater_switch = 21
        self.GPIO_black_tank_rinse_valve = 20
        self.GPIO_alarm_silence = 25
        """




    def blackValveOpen(self, pin = None):
        self.update_status('Black Valve ON Button Pressed', 'user_action')
        
        GPIO.output(self.GPIO_black_tank_valve, 1)
        sleep(0.6)
        GPIO.output(self.GPIO_black_tank_valve, 0)

        self.black_tank_valve_control_status_lbl.config(image = self.open_img)
        self.black_tank_valve_btn_on.config(state = 'disabled')
        self.black_tank_valve_btn_off.config(state = 'normal')

    def blackValveClosed(self, pin = None):
        self.update_status('Black Valve OFF Button Pressed', 'user_action')
        
        GPIO.output(self.GPIO_black_tank_valve, 1)
        sleep(0.6)
        GPIO.output(self.GPIO_black_tank_valve, 0)

        self.black_tank_valve_control_status_lbl.config(image = self.closed_img)
        self.black_tank_valve_btn_off.config(state = 'disabled')
        self.black_tank_valve_btn_on.config(state = 'normal')

    def bathValveOn(self, pin = None):
        self.update_status('Bath Valve ON Button Pressed', 'user_action')
        
        GPIO.output(self.GPIO_bathroom_tank_valve, 1)
        sleep(0.6)
        GPIO.output(self.GPIO_bathroom_tank_valve, 0)

        self.bath_tank_valve_control_status_lbl.config(image = self.open_img)
        self.bath_tank_valve_btn_on.config(state = 'disabled')
        self.bath_tank_valve_btn_off.config(state = 'normal')

    def bathValveOff(self, pin = None):
        self.update_status('Bath Valve OFF Button Pressed', 'user_action')
        
        GPIO.output(self.GPIO_bathroom_tank_valve, 1)
        sleep(0.6)
        GPIO.output(self.GPIO_bathroom_tank_valve, 0)

        self.bath_tank_valve_control_status_lbl.config(image = self.closed_img)
        self.bath_tank_valve_btn_off.config(state = 'disabled')
        self.bath_tank_valve_btn_on.config(state = 'normal')

    def kitchenValveOn(self, pin = None):
        self.update_status('Kitchen Valve ON Button Pressed', 'user_action')
        
        GPIO.output(self.GPIO_kitchen_tank_valve, 1)
        sleep(0.6)
        GPIO.output(self.GPIO_kitchen_tank_valve, 0)

        self.kitchen_tank_valve_control_status_lbl.config(image = self.open_img)
        self.kitchen_tank_valve_btn_on.config(state = 'disabled')
        self.kitchen_tank_valve_btn_off.config(state = 'normal')

    def kitchenValveOff(self, pin = None):
        self.update_status('Kitchen Valve OFF Button Pressed', 'user_action')
        
        GPIO.output(self.GPIO_kitchen_tank_valve, 1)
        sleep(0.6)
        GPIO.output(self.GPIO_kitchen_tank_valve, 0)

        self.kitchen_tank_valve_control_status_lbl.config(image = self.closed_img)
        self.kitchen_tank_valve_btn_off.config(state = 'disabled')
        self.kitchen_tank_valve_btn_on.config(state = 'normal')

    def blackTankRinseOn(self):
        '''
        Black tank valve needs to be open before the rinse process begins.  Is there a way to confirm 
        that the valve is open?
        '''
        self.update_status('Black Rinse ON Button Pressed', 'user_action')
        
        # Open the black tank valve before opening the rinse valve
        self.blackValveOpen()

        GPIO.ouput(self.GPIO_black_tank_rinse_valve, 1)
        sleep(0.6)
        GPIO.ouput(self.GPIO_black_tank_rinse_valve, 0)

        self.black_tank_rinse_btn_on.config(state = 'disabled')
        self.black_tank_rinse_btn_off.config(state = 'normal')
        self.start_countdown()
     
    def blackTankRinseOff(self):
        self.update_status('Black Rinse OFF Button Pressed', 'user_action')
        
        GPIO.ouput(self.GPIO_black_tank_rinse_valve, 1)
        sleep(0.6)
        GPIO.ouput(self.GPIO_black_tank_rinse_valve, 0)

        self.black_tank_rinse_lbl.config(text = 'BLACK TANK RINSE CONTROL')
        self.black_tank_rinse_btn_off.config(state = 'disabled')
        self.black_tank_rinse_btn_on.config(state = 'normal')
        self.stop_countdown()

    def basementHeaterOn(self):
        self.update_status('Basement Heater ON Pressed', 'user_action')
        
        GPIO.output(self.GPIO_heater_switch, 1)
        sleep(0.6)
        GPIO.output(self.GPIO_heater_switch, 0)

        self.basement_heater_control_lbl.config(text = 'BASEMENT HEATER ACTIVE')
        self.basement_heater_btn_on.config(state = 'disabled')
        self.basement_heater_btn_off.config(state = 'normal')

    def basementHeaterOff(self):
        self.update_status('Basement Heater OFF Pressed', 'user_action')
        
        GPIO.output(self.GPIO_heater_switch, 1)
        sleep(0.6)
        GPIO.output(self.GPIO_heater_switch, 0)

        self.basement_heater_control_lbl.config(text = 'BASEMENT HEATER INACTIVE')
        self.basement_heater_btn_off.config(state = 'disabled')
        self.basement_heater_btn_on.config(state = 'normal')

    def kitchenTankLevel(self, LL3Pin = 13):
        reading = 0

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(LL3Pin, GPIO.OUT)
        GPIO.output(LL3Pin, GPIO.LOW)
        sleep(0.1)
        GPIO.setup(LL3Pin, GPIO.IN)

        if GPIO.input(LL3Pin) == GPIO.LOW:
            reading = 0
        else:
            reading = 1

        if reading == 0:
            self.buzz_off()
            self.kitchen_tank_status.config(text = 'OK', fg = 'green')
            self.update_status('KITCHEN TANK SENSOR REPORTING STATUS: OK', 'nominal')
        elif reading == 1:
            self.buzz_on()
            self.kitchen_tank_status.config(text = 'FULL', fg = 'red')
            self.update_status('KITCHEN TANK SENSOR REPORTING STATUS: FULL', 'error')
        self.kitchen_tank_status.after(2000, self.kitchenTankLevel)

    def bathTankLevel(self, LL2Pin = 6):
        reading = 0

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(LL2Pin, GPIO.OUT)
        GPIO.output(LL2Pin, GPIO.LOW)
        time.sleep(.1)
        GPIO.setup(LL2Pin, GPIO.IN)

        if GPIO.input(LL2Pin) == GPIO.LOW:
            reading = 0
        else:
            reading = 1

        if reading == 0:
            self.buzz_off()
            self.bathroom_tank_status.config(text = 'OK', fg = 'green')
            self.update_status('BATH TANK SENSOR REPORTING STATUS: OK', 'nominal')
        elif reading == 1:
            self.buzz_on()
            self.bathroom_tank_status.config(text = 'FULL', fg = 'red')
            self.update_status('BATH TANK SENSOR REPORTING STATUS: FULL', 'error')
        self.bathroom_tank_status.after(2000, self.bathTankLevel)

    def blackTankLevel(self, LL1Pin = 5):
        reading = 0

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(LL1Pin, GPIO.OUT)
        GPIO.output(LL1Pin, GPIO.LOW)
        time.sleep(.1)
        GPIO.setup(LL1Pin, GPIO.IN)

        if GPIO.input(LL1Pin) == GPIO.LOW:
            reading = 0
        else:
            reading = 1

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

    def countdown(self, remaining = 360):
        for i in range(remaining, 0, -1):
            if self.abort_black_rinse == True:
                return
            else:
                print(i)
                minutes, seconds = divmod(i, 60)
                self.black_tank_rinse_lbl.config(text = 'Rinse Active: {:1d}:{:02d}'.format(minutes, seconds))
                sleep(1)

        self.blackTankRinseOff() 
        self.black_tank_rinse_lbl.config(text = 'BLACK TANK RINSE CONTROL')

    def start_countdown(self):
        self.timer = threading.Thread(target = self.countdown)
        self.timer.start()

    def stop_countdown(self):
        self.abort_black_rinse = True
        self.black_tank_rinse_lbl.config(text = 'BLACK TANK RINSE CONTROL')
        self.timer.join()
  
    def update_status(self, msg, sender):
        pass
        #print(msg)

    def system_status(self):
        # initialize all controls and set labels to appropriate state
        '''
        will need to loop through the GPIO signals and get the state of each
        in the meantime just assume all are closed to complete testing of the interface
        '''

        valve_status_images = [self.black_tank_valve_control_status_lbl, self.bath_tank_valve_control_status_lbl, self.kitchen_tank_valve_control_status_lbl]
        valve_off_btns = [self.black_tank_valve_btn_off, self.bath_tank_valve_btn_off, self.kitchen_tank_valve_btn_off]

        for img in valve_status_images:
            img.config(image = self.closed_img)
        for btn in valve_off_btns:
            btn.config(state = 'disabled')

        


if __name__ == '__main__':

    root = Tk()
    app = App(root)
    app.system_status()

    app.update_time()
    app.kitchenTankLevel()
    app.bathTankLevel()
    app.blackTankLevel()
    root.mainloop()

