import sys

from PyQt5 import QtCore, QtGui, QtWidgets

from . import config
from .computer import Computer
from .config import BLANK


class ControlRegister:
    def __init__(self, central_widget, name, *digits):
        
        self.central_widget = central_widget
        self.name = name
        self.verb_35_timer = QtCore.QTimer()
        self.digits = [
            digits[0],
            digits[1],
        ]
    
    def set_tooltip(self, tooltip):
        
        for digit in self.digits:
            digit.set_tooltip(tooltip)
    
    def start_verb_35_blink(self):
        
        if self.name != "program":
            self.digits[0].start_blink()
            self.digits[1].start_blink()
        else:
            self.display("88")
        
        self.verb_35_timer.singleShot(5000, self.stop_verb_35_blink)
    
    def stop_verb_35_blink(self):
        self.digits[0].stop_blink()
        self.digits[1].stop_blink()
        if self.name == "program":
            self.display(BLANK)
        else:
            self.display("88")
        for annunciator in gui_instance.annunciators.values():
            annunciator.off()
    
    def stop_blink(self):
        self.digits[0].stop_blink()
        self.digits[1].stop_blink()
    
    def display(self, data):
        
        self.digits[0].display(data[0])
        if len(data) > 1:
            self.digits[1].display(data[1])
    
    def blank(self):
        """ Blanks the whole control register.
        :return: None
        """
        
        self.display(BLANK)
    
    def start_blink(self):
        self.digits[0].start_blink()
        self.digits[1].start_blink()


class DataRegister:
    def __init__(self, central_widget, sign_digit, *digits):
        
        self.central_widget = central_widget
        self.digits = [
            sign_digit,
            digits[0],
            digits[1],
            digits[2],
            digits[3],
            digits[4],
        
        ]
        self.display(["b", 10, 10, 10, 10, 10])
    
    def blank(self):
        
        """Blanks (clears) the whole data register."""
        self.display(["b", 10, 10, 10, 10, 10])
    
    def set_tooltip(self, tooltip):
        
        for digit in self.digits:
            digit.set_tooltip(tooltip)
    
    def display(self, data):
        
        """displays the data given, sending the call thru to gui"""
        
        # if input data is a string, need to do some further processing
        if isinstance(data, str):
            # if any chars are b, need to change this value to 10 cause thats what Digit class expects for blank
            # create list without the sign digit
            chars = []
            # perform the substitution
            for char in data:
                if char == "b":
                    chars.append(10)
                else:
                    chars.append(char)
            data = [chars[0], int(chars[1]), int(chars[2]), int(chars[3]), int(chars[4]), int(chars[5])]
        
        # some value length checks
        # value_length = len(value)
        # if value_length > 6:
        #     utils.log("Too many digits passed to display(), got {} digits".format(value_length), log_level="ERROR")
        #     return
        # elif value_length == 5:
        #     utils.log("display() received only 5 digits, assuming sign is blank", log_level="WARNING")
        #
        # elif value_length < 5:
        #     utils.log("display() received {} digits, padding with zeros to the left".format(value_length),
        #               log_level="WARNING")
        #     value.zfill(5)
        
        self.digits[0].display(data[0])
        self.digits[1].display(data[1])
        self.digits[2].display(data[2])
        self.digits[3].display(data[3])
        self.digits[4].display(data[4])
        self.digits[5].display(data[5])


class Key(QtWidgets.QPushButton):
    def __init__(self, central_widget, name, image, geometry):
        
        super().__init__(central_widget)
        
        self.setGeometry(geometry)
        self.setObjectName(name)
        self.icon = QtGui.QIcon()
        self.icon.addPixmap(QtGui.QPixmap(config.IMAGES_DIR + image), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setIcon(self.icon)
        self.setIconSize(QtCore.QSize(65, 65))
        self.clicked.connect(self.charin)
        self.setText("")
        self.key_handler_function = None  # will hold the function to run for keypress events
    
    def charin(self):
        key_handler_function(self.objectName())
    
    def register_key_handler(self, key_handler_function):
        self.key_handler_function = key_handler_function

class Annunciator(QtWidgets.QLabel):
    def __init__(self, central_widget, name, image_on, image_off, geometry):
        
        super().__init__(central_widget)
        self.setGeometry(geometry)
        self.setObjectName(name)
        self.pixmaps = {
            "on": QtGui.QPixmap(config.IMAGES_DIR + image_on),
            "off": QtGui.QPixmap(config.IMAGES_DIR + image_off),
        }
        self.setText("")
        self.is_lit = False
        self.requested_state = False
        self.blink_timer = QtCore.QTimer()
        self.blink_timer.timeout.connect(self.invert)
        self.off()
    
    def start_blink(self, interval=500):
        """ Starts the annunciator blinking.
        :param interval: the blink interval
        :return: None
        """
        
        self.blink_timer.start(interval)
    
    def stop_blink(self):
        """ Stops the annunciator blinking.
        :return: None
        """
        
        self.blink_timer.stop()
        self.off()
    
    def invert(self):
        """ Blinks indicator """
        
        if self.is_lit:
            self.off()
        else:
            self.on()
    
    def on(self):
        self.is_lit = True
        image = self.pixmaps["on"]
        self.setPixmap(image)
    
    def off(self):
        self.is_lit = False
        image = self.pixmaps["off"]
        self.setPixmap(image)


class SignDigit(QtWidgets.QLabel):
    def __init__(self, central_widget, name, geometry):
        super().__init__(central_widget)
        self.setGeometry(geometry)
        self.setObjectName(name)
        self.digit_pixmaps = {
            "+": QtGui.QPixmap(config.IMAGES_DIR + "PlusOn.jpg"),
            "-": QtGui.QPixmap(config.IMAGES_DIR + "MinusOn.jpg"),
            "b": QtGui.QPixmap(config.IMAGES_DIR + "PlusMinusOff.jpg"),
            10: QtGui.QPixmap(config.IMAGES_DIR + "PlusMinusOff.jpg"),  # for compatibility with digits
        }
        self.setText("")
        self.display("b")
    
    def set_tooltip(self, tooltip):
        self.setToolTip(tooltip)
    
    def display(self, digit_to_display):
        # get pixmap
        image = self.digit_pixmaps[digit_to_display]
        # change picture
        self.setPixmap(image)


class Digit(QtWidgets.QLabel):
    def __init__(self, central_widget, name, geometry):
        super().__init__(central_widget)
        self.setGeometry(geometry)
        self.setObjectName(name)
        self.digit_pixmaps = [
            QtGui.QPixmap(config.IMAGES_DIR + "7Seg-0.jpg"),
            QtGui.QPixmap(config.IMAGES_DIR + "7Seg-1.jpg"),
            QtGui.QPixmap(config.IMAGES_DIR + "7Seg-2.jpg"),
            QtGui.QPixmap(config.IMAGES_DIR + "7Seg-3.jpg"),
            QtGui.QPixmap(config.IMAGES_DIR + "7Seg-4.jpg"),
            QtGui.QPixmap(config.IMAGES_DIR + "7Seg-5.jpg"),
            QtGui.QPixmap(config.IMAGES_DIR + "7Seg-6.jpg"),
            QtGui.QPixmap(config.IMAGES_DIR + "7Seg-7.jpg"),
            QtGui.QPixmap(config.IMAGES_DIR + "7Seg-8.jpg"),
            QtGui.QPixmap(config.IMAGES_DIR + "7Seg-9.jpg"),
            QtGui.QPixmap(config.IMAGES_DIR + "7SegOff.jpg"),  # 10 means blank
        ]
        self.is_blinking_lit = True
        self.current_display = None
        self.value_to_blink = None
        self.blink_timer = QtCore.QTimer()
        self.blink_timer.timeout.connect(self.flip)
        self.setText("")
        self.display(10)
        self.last_value = None
        self.is_blinking = False
    
    def set_tooltip(self, tooltip):
        self.setToolTip(tooltip)
    
    def start_blink(self):
        
        """ Starts the digit blinking.
        :return: None
        """
        self.is_blinking_lit = False
        self.is_blinking = True
        self.display(10)
        self.blink_timer.start(500)
    
    def stop_blink(self):
        self.is_blinking = False
        self.blink_timer.stop()
    
    def flip(self):
        
        """alternates the digit between a value and blank ie to flash the digit."""
        
        # digit displaying the number, switch to blank
        if self.is_blinking_lit:
            self.display(10)
            self.is_blinking_lit = False
        else:
            # digit displaying blank, change to number
            self.display(self.last_value)
            self.is_blinking_lit = True
    
    def display(self, number_to_display):
        
        """displays a given digit"""
        
        # first cast number_to_display to int
        number_to_display = int(number_to_display)
        
        # if we are flashing, only need to change stored digit
        if self.is_blinking:
            if self.is_blinking_lit:
                self.last_value = number_to_display
        else:
            # stores the last value displayed, in case we need to flash
            self.last_value = self.current_display
            
            # store the value we shall be displaying
            self.current_display = number_to_display
            # now get image filename and display it
            image = self.digit_pixmaps[number_to_display]
            self.setPixmap(image)



class GUI:
    """This class represents the GUI. It contains the DSKY and its elements."""
    
    def __init__(self, main_window):
        
        """Class constructor."""
        
        self.input_source = None  # will be set later by register_input()
        self.main_window = main_window
        self.main_window.setObjectName("main_window")
        self.main_window.resize(572, 658)
        
        self.verb_noun_flash_timer = QtCore.QTimer()
        self.verb_noun_flash_timer.timeout.connect(self._flash_verb_noun)
        
        # init icon
        self.icon = QtGui.QIcon()
        self.icon.addPixmap(QtGui.QPixmap(config.IMAGES_DIR + "icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.main_window.setWindowIcon(self.icon)
        
        # init central widget
        self.centralwidget = QtWidgets.QWidget(self.main_window)
        self.centralwidget.setObjectName("centralwidget")
        
        # create frame borders for left and right frames
        # left:
        self.left_frame_left_border = QtWidgets.QLabel(self.centralwidget)
        self.left_frame_bottom_border = QtWidgets.QLabel(self.centralwidget)
        self.left_frame_right_border = QtWidgets.QLabel(self.centralwidget)
        self.left_frame_top_border = QtWidgets.QLabel(self.centralwidget)
        
        # right:
        self.right_frame_right_border = QtWidgets.QLabel(self.centralwidget)
        self.right_frame_bottom_border = QtWidgets.QLabel(self.centralwidget)
        self.right_frame_top_border = QtWidgets.QLabel(self.centralwidget)
        self.right_frame_left_border = QtWidgets.QLabel(self.centralwidget)
        
        # indicators that are usually on for display purposes:
        self.lighting_prog = QtWidgets.QLabel(self.centralwidget)
        self.lighting_verb = QtWidgets.QLabel(self.centralwidget)
        self.lighting_noun = QtWidgets.QLabel(self.centralwidget)
        
        # seperators:
        self.lighting_sep_bar_1 = QtWidgets.QLabel(self.centralwidget)
        self.lighting_sep_bar_2 = QtWidgets.QLabel(self.centralwidget)
        self.lighting_sep_bar_3 = QtWidgets.QLabel(self.centralwidget)
        
        # other gui stuff
        self.menubar = QtWidgets.QMenuBar(self.main_window)
        self.action_about = QtWidgets.QAction(self.main_window)
        self.action_alarm_codes = QtWidgets.QAction(self.main_window)
        self.action_programs = QtWidgets.QAction(self.main_window)
        self.action_nouns = QtWidgets.QAction(self.main_window)
        self.action_verbs = QtWidgets.QAction(self.main_window)
        self.action_quit = QtWidgets.QAction(self.main_window)
        self.action_show_log = QtWidgets.QAction(self.main_window)
        self.action_settings = QtWidgets.QAction(self.main_window)
        self.menu_help = QtWidgets.QMenu(self.menubar)
        self.menu_file = QtWidgets.QMenu(self.menubar)
        
        self.static_display_3 = QtWidgets.QLabel(self.centralwidget)
        self.static_display_2 = QtWidgets.QLabel(self.centralwidget)
        self.static_display_1 = QtWidgets.QLabel(self.centralwidget)
        
        # annunciators:
        self.annunciators = {
            "uplink_acty": Annunciator(
                self.centralwidget,
                name="uplink_acty",
                image_off="UplinkActyOff.jpg",
                image_on="UplinkActyOn.jpg",
                geometry=QtCore.QRect(58, 28, 84, 40)),
            "temp": Annunciator(
                self.centralwidget,
                name="temp",
                image_off="TempOff.jpg",
                image_on="TempOn.jpg",
                geometry=QtCore.QRect(150, 28, 84, 40)),
            "no_att": Annunciator(
                self.centralwidget,
                name="no_att",
                image_off="NoAttOff.jpg",
                image_on="NoAttOn.jpg",
                geometry=QtCore.QRect(58, 76, 84, 40)),
            "gimbal_lock": Annunciator(
                self.centralwidget,
                name="gimbal_lock",
                image_off="GimbalLockOff.jpg",
                image_on="GimbalLockOn.jpg",
                geometry=QtCore.QRect(150, 76, 84, 40)),
            "stby": Annunciator(
                self.centralwidget,
                name="stby",
                image_off="StbyOff.jpg",
                image_on="StbyOn.jpg",
                geometry=QtCore.QRect(58, 125, 84, 40)),
            "prog": Annunciator(
                self.centralwidget,
                name="prog",
                image_off="ProgOff.jpg",
                image_on="ProgOn.jpg",
                geometry=QtCore.QRect(150, 125, 84, 40)),
            "key_rel": Annunciator(
                self.centralwidget,
                name="key_rel",
                image_off="KeyRelOff.jpg",
                image_on="KeyRelOn.jpg",
                geometry=QtCore.QRect(58, 174, 84, 40)),
            "restart": Annunciator(
                self.centralwidget,
                name="key_rel",
                image_off="RestartOff.jpg",
                image_on="RestartOn.jpg",
                geometry=QtCore.QRect(150, 174, 84, 40)),
            "opr_err": Annunciator(
                self.centralwidget,
                name="opr_err",
                image_off="OprErrOff.jpg",
                image_on="OprErrOn.jpg",
                geometry=QtCore.QRect(58, 223, 84, 40)),
            "tracker": Annunciator(
                self.centralwidget,
                name="tracker",
                image_off="TrackerOff.jpg",
                image_on="TrackerOn.jpg",
                geometry=QtCore.QRect(150, 223, 84, 40)),
            "blank1": Annunciator(
                self.centralwidget,
                name="blank_1",
                image_off="BlankOff.jpg",
                image_on="BlankOn.jpg",
                geometry=QtCore.QRect(58, 272, 84, 40)),
            "blank2": Annunciator(
                self.centralwidget,
                name="blank_2",
                image_off="BlankOff.jpg",
                image_on="BlankOn.jpg",
                geometry=QtCore.QRect(150, 272, 84, 40)),
            "blank3": Annunciator(
                self.centralwidget,
                name="blank_3",
                image_off="BlankOff.jpg",
                image_on="BlankOn.jpg",
                geometry=QtCore.QRect(58, 321, 84, 40)),
            "blank4": Annunciator(
                self.centralwidget,
                name="blank_4",
                image_off="BlankOff.jpg",
                image_on="BlankOn.jpg",
                geometry=QtCore.QRect(150, 321, 84, 40)),
            "comp_acty": Annunciator(
                self.centralwidget,
                name="comp_acty",
                image_off="CompActyOff.jpg",
                image_on="CompActyOn.jpg",
                geometry=QtCore.QRect(324, 22, 64, 64)),
        }
        
        self.control_registers = {
            "program": ControlRegister(self.centralwidget,
                                       "program",
                                       Digit(self.centralwidget,
                                             name="control_register:program:1",
                                             geometry=QtCore.QRect(452, 46, 32, 45)),
                                       Digit(self.centralwidget,
                                             name="control_register:program:2",
                                             geometry=QtCore.QRect(484, 46, 32, 45))),
            "verb": ControlRegister(self.centralwidget,
                                    "verb",
                                    Digit(self.centralwidget,
                                          name="control_register:verb:1",
                                          geometry=QtCore.QRect(324, 129, 32, 45)),
                                    Digit(self.centralwidget,
                                          name="control_register:verb:2",
                                          geometry=QtCore.QRect(356, 129, 32, 45))),
            "noun": ControlRegister(self.centralwidget,
                                    "noun",
                                    Digit(self.centralwidget,
                                          name="control_register:noun:1",
                                          geometry=QtCore.QRect(452, 129, 32, 45)),
                                    Digit(self.centralwidget,
                                          name="control_register:noun:2",
                                          geometry=QtCore.QRect(484, 129, 32, 45))),
        }
        
        self.data_registers = {
            1: DataRegister(self.centralwidget,
                            SignDigit(self.centralwidget,
                                      name="data_register:1:sign",
                                      geometry=QtCore.QRect(324, 193, 32, 45)),  # sign
                            Digit(self.centralwidget,
                                  name="data_register:1:1",
                                  geometry=QtCore.QRect(356, 193, 32, 45)),
                            Digit(self.centralwidget,
                                  name="data_register:1:2",
                                  geometry=QtCore.QRect(388, 193, 32, 45)),
                            Digit(self.centralwidget,
                                  name="data_register:1:3",
                                  geometry=QtCore.QRect(420, 193, 32, 45)),
                            Digit(self.centralwidget,
                                  name="data_register:1:4",
                                  geometry=QtCore.QRect(452, 193, 32, 45)),
                            Digit(self.centralwidget,
                                  name="data_register:1:5",
                                  geometry=QtCore.QRect(484, 193, 32, 45))),
            2: DataRegister(self.centralwidget,
                            SignDigit(self.centralwidget,
                                      name="data_register:2:sign",
                                      geometry=QtCore.QRect(324, 257, 32, 45)),  # sign
                            Digit(self.centralwidget,
                                  name="data_register:2:1",
                                  geometry=QtCore.QRect(356, 257, 32, 45)),
                            Digit(self.centralwidget,
                                  name="data_register:2:2",
                                  geometry=QtCore.QRect(388, 257, 32, 45)),
                            Digit(self.centralwidget,
                                  name="data_register:2:3",
                                  geometry=QtCore.QRect(420, 257, 32, 45)),
                            Digit(self.centralwidget,
                                  name="data_register:2:4",
                                  geometry=QtCore.QRect(452, 257, 32, 45)),
                            Digit(self.centralwidget,
                                  name="data_register:2:5",
                                  geometry=QtCore.QRect(484, 257, 32, 45))),
            3: DataRegister(self.centralwidget,
                            SignDigit(self.centralwidget,
                                      name="data_register:3:sign",
                                      geometry=QtCore.QRect(324, 321, 32, 45)),  # sign
                            Digit(self.centralwidget,
                                  name="data_register:3:1",
                                  geometry=QtCore.QRect(356, 321, 32, 45)),
                            Digit(self.centralwidget,
                                  name="data_register:3:2",
                                  geometry=QtCore.QRect(388, 321, 32, 45)),
                            Digit(self.centralwidget,
                                  name="data_register:3:3",
                                  geometry=QtCore.QRect(420, 321, 32, 45)),
                            Digit(self.centralwidget,
                                  name="data_register:3:4",
                                  geometry=QtCore.QRect(452, 321, 32, 45)),
                            Digit(self.centralwidget,
                                  name="data_register:3:5",
                                  geometry=QtCore.QRect(484, 321, 32, 45)))
        }
        
        def get_output_widgets(self):
            
            """returns the objects that are output objects"""
            
            return self.annunciators, self.control_registers, self.data_registers
        
        self.keyboard = {
            "verb":   Key(self.centralwidget,
                          name="V",
                          image="VerbUp.jpg",
                          geometry=QtCore.QRect(6, 430, 75, 75)),
            "noun":   Key(self.centralwidget,
                          name="N",
                          image="NounUp.jpg",
                          geometry=QtCore.QRect(6, 510, 75, 75)),
            "plus":   Key(self.centralwidget,
                          name="+",
                          image="PlusUp.jpg",
                          geometry=QtCore.QRect(88, 390, 75, 75)),
            "minus":   Key(self.centralwidget,
                           name="-",
                           image="MinusUp.jpg",
                           geometry=QtCore.QRect(88, 470, 75, 75)),
            0:         Key(self.centralwidget,
                           name="0",
                           image="0Up.jpg",
                           geometry=QtCore.QRect(88, 550, 75, 75)),
            1:         Key(self.centralwidget,
                           name="1",
                           image="1Up.jpg",
                           geometry=QtCore.QRect(170, 550, 75, 75)),
            2:         Key(self.centralwidget,
                           name="2",
                           image="2Up.jpg",
                           geometry=QtCore.QRect(252, 550, 75, 75)),
            3:         Key(self.centralwidget,
                           name="3",
                           image="3Up.jpg",
                           geometry=QtCore.QRect(335, 550, 75, 75)),
            4:         Key(self.centralwidget,
                           name="4",
                           image="4Up.jpg",
                           geometry=QtCore.QRect(170, 470, 75, 75)),
            5:         Key(self.centralwidget,
                           name="5",
                           image="5Up.jpg",
                           geometry=QtCore.QRect(252, 470, 75, 75)),
            6:         Key(self.centralwidget,
                           name="6",
                           image="6Up.jpg",
                           geometry=QtCore.QRect(335, 470, 75, 75)),
            7:         Key(self.centralwidget,
                           name="7",
                           image="7Up.jpg",
                           geometry=QtCore.QRect(170, 390, 75, 75)),
            8:         Key(self.centralwidget,
                           name="8",
                           image="8Up.jpg",
                           geometry=QtCore.QRect(252, 390, 75, 75)),
            9:         Key(self.centralwidget,
                           name="9",
                           image="9Up.jpg",
                           geometry=QtCore.QRect(335, 390, 75, 75)),
            "clr":     Key(self.centralwidget,
                           name="C",
                           image="ClrUp.jpg",
                           geometry=QtCore.QRect(418, 470, 75, 75)),
            "pro":     Key(self.centralwidget,
                           name="P",
                           image="ProUp.jpg",
                           geometry=QtCore.QRect(418, 390, 75, 75)),
            "key_rel": Key(self.centralwidget,
                           name="K",
                           image="KeyRelUp.jpg",
                           geometry=QtCore.QRect(418, 550, 75, 75)),
            "entr":    Key(self.centralwidget,
                           name="E",
                           image="EntrUp.jpg",
                           geometry=QtCore.QRect(496, 411, 75, 75)),
            "rset":    Key(self.centralwidget,
                           name="R",
                           image="RsetUp.jpg",
                           geometry=QtCore.QRect(496, 491, 75, 75)),
        }
        
        self.setup_ui(self.main_window)

    def register_input(output_function):
        """ regesters the given function as the output, qtpy will then use this as input to display"""
        self.input_source = output_function
    
    def set_verb_noun_flash(self, state_to_set):
        if state_to_set == "on":
            self.control_registers["verb"].start_blink()
            self.control_registers["noun"].start_blink()
        elif state_to_set == "off":
            self.control_registers["verb"].stop_blink()
            self.control_registers["noun"].stop_blink()
        else:
            print("Didn't understand your command, do you want me to flash or what?")
    
    def _flash_verb_noun(self):
        pass
    
    def setup_ui(self, main_window):
        
        self.left_frame_left_border.setGeometry(QtCore.QRect(42, 14, 8, 360))
        self.left_frame_left_border.setText("")
        self.left_frame_left_border.setPixmap(QtGui.QPixmap(config.IMAGES_DIR + "FrameVerticalL.jpg"))
        self.left_frame_left_border.setObjectName("left_frame_left_border")
        
        self.left_frame_bottom_border.setGeometry(QtCore.QRect(50, 362, 211, 16))
        self.left_frame_bottom_border.setText("")
        self.left_frame_bottom_border.setPixmap(QtGui.QPixmap(config.IMAGES_DIR + "FrameHorizontal.jpg"))
        self.left_frame_bottom_border.setObjectName("left_frame_bottom_border")
        
        self.left_frame_right_border.setGeometry(QtCore.QRect(242, 14, 8, 360))
        self.left_frame_right_border.setText("")
        self.left_frame_right_border.setPixmap(QtGui.QPixmap(config.IMAGES_DIR + "FrameVerticalL.jpg"))
        self.left_frame_right_border.setObjectName("left_frame_right_border")
        
        self.left_frame_top_border.setGeometry(QtCore.QRect(50, 10, 211, 16))
        self.left_frame_top_border.setText("")
        self.left_frame_top_border.setPixmap(QtGui.QPixmap(config.IMAGES_DIR + "FrameHorizontal.jpg"))
        self.left_frame_top_border.setObjectName("left_frame_top_border")
        
        self.right_frame_right_border.setGeometry(QtCore.QRect(516, 14, 8, 360))
        self.right_frame_right_border.setText("")
        self.right_frame_right_border.setPixmap(QtGui.QPixmap(config.IMAGES_DIR + "FrameVerticalL.jpg"))
        self.right_frame_right_border.setObjectName("right_frame_right_border")
        
        self.right_frame_bottom_border.setGeometry(QtCore.QRect(324, 362, 211, 16))
        self.right_frame_bottom_border.setText("")
        self.right_frame_bottom_border.setPixmap(QtGui.QPixmap(config.IMAGES_DIR + "FrameHorizontal.jpg"))
        self.right_frame_bottom_border.setObjectName("right_frame_bottom_border")
        
        self.right_frame_top_border.setGeometry(QtCore.QRect(324, 10, 201, 16))
        self.right_frame_top_border.setText("")
        self.right_frame_top_border.setPixmap(QtGui.QPixmap(config.IMAGES_DIR + "FrameHorizontal.jpg"))
        self.right_frame_top_border.setObjectName("right_frame_top_border")
        
        self.right_frame_left_border.setGeometry(QtCore.QRect(316, 14, 8, 360))
        self.right_frame_left_border.setText("")
        self.right_frame_left_border.setPixmap(QtGui.QPixmap(config.IMAGES_DIR + "FrameVerticalL.jpg"))
        self.right_frame_left_border.setObjectName("right_frame_left_border")
        
        self.lighting_prog.setGeometry(QtCore.QRect(452, 22, 64, 24))
        self.lighting_prog.setText("")
        self.lighting_prog.setPixmap(QtGui.QPixmap(config.IMAGES_DIR + "rProgOn.jpg"))
        self.lighting_prog.setObjectName("lighting_prog")
        
        self.lighting_verb.setGeometry(QtCore.QRect(324, 105, 64, 24))
        self.lighting_verb.setText("")
        self.lighting_verb.setPixmap(QtGui.QPixmap(config.IMAGES_DIR + "VerbOn.jpg"))
        self.lighting_verb.setObjectName("lighting_verb")
        self.lighting_noun.setGeometry(QtCore.QRect(452, 105, 64, 24))
        self.lighting_noun.setText("")
        self.lighting_noun.setPixmap(QtGui.QPixmap(config.IMAGES_DIR + "NounOn.jpg"))
        self.lighting_noun.setObjectName("lighting_noun")
        self.lighting_sep_bar_1 = QtWidgets.QLabel(self.centralwidget)
        self.lighting_sep_bar_1.setGeometry(QtCore.QRect(324, 174, 192, 19))
        self.lighting_sep_bar_1.setText("")
        self.lighting_sep_bar_1.setPixmap(QtGui.QPixmap(config.IMAGES_DIR + "SeparatorOn.jpg"))
        self.lighting_sep_bar_1.setObjectName("lighting_sep_bar_1")
        self.lighting_sep_bar_2.setGeometry(QtCore.QRect(324, 238, 192, 19))
        self.lighting_sep_bar_2.setText("")
        self.lighting_sep_bar_2.setPixmap(QtGui.QPixmap(config.IMAGES_DIR + "SeparatorOn.jpg"))
        self.lighting_sep_bar_2.setObjectName("lighting_sep_bar_2")
        self.lighting_sep_bar_3.setGeometry(QtCore.QRect(324, 302, 192, 19))
        self.lighting_sep_bar_3.setText("")
        self.lighting_sep_bar_3.setPixmap(QtGui.QPixmap(config.IMAGES_DIR + "SeparatorOn.jpg"))
        self.lighting_sep_bar_3.setObjectName("lighting_sep_bar_3")
        
        self.static_display_1.setGeometry(QtCore.QRect(388, 22, 64, 152))
        self.static_display_1.setText("")
        self.static_display_1.setPixmap(QtGui.QPixmap(config.IMAGES_DIR + "CenterBlock.jpg"))
        self.static_display_1.setScaledContents(True)
        self.static_display_1.setObjectName("static_display_1")
        self.static_display_2.setGeometry(QtCore.QRect(452, 89, 64, 19))
        self.static_display_2.setText("")
        self.static_display_2.setPixmap(QtGui.QPixmap(config.IMAGES_DIR + "ShortHorizontal.jpg"))
        self.static_display_2.setObjectName("static_display_2")
        self.static_display_3.setGeometry(QtCore.QRect(324, 86, 64, 19))
        self.static_display_3.setText("")
        self.static_display_3.setPixmap(QtGui.QPixmap(config.IMAGES_DIR + "ShortHorizontal.jpg"))
        self.static_display_3.setObjectName("static_display_3")
        self.static_display_2.raise_()
        self.static_display_3.raise_()
        self.left_frame_left_border.raise_()
        self.left_frame_bottom_border.raise_()
        self.left_frame_right_border.raise_()
        self.left_frame_top_border.raise_()
        self.right_frame_right_border.raise_()
        self.right_frame_bottom_border.raise_()
        self.right_frame_top_border.raise_()
        self.right_frame_left_border.raise_()
        self.lighting_prog.raise_()
        
        for key in self.annunciators:
            self.annunciators[key].raise_()
        
        # for register in self.control_registers:
        #     for digit in self.control_registers[register]:
        #         self.control_registers[register][digit].raise_()
        
        # for register in self.data_registers:
        #     for digit in self.data_registers[register]:
        #         self.data_registers[register][digit].raise_()
        
        # misc setup
        self.lighting_verb.raise_()
        self.lighting_noun.raise_()
        
        self.lighting_sep_bar_1.raise_()
        self.lighting_sep_bar_2.raise_()
        self.lighting_sep_bar_3.raise_()
        
        self.static_display_1.raise_()
        
        main_window.setCentralWidget(self.centralwidget)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 572, 21))
        self.menubar.setObjectName("menubar")
        self.menu_file.setObjectName("menu_file")
        self.menu_help.setObjectName("menu_help")
        main_window.setMenuBar(self.menubar)
        self.action_settings.setEnabled(True)
        self.action_settings.setObjectName("action_settings")
        self.action_show_log.setObjectName("action_show_log")
        self.action_quit.setObjectName("action_quit")
        self.action_verbs.setObjectName("action_verbs")
        self.action_nouns.setObjectName("action_nouns")
        self.action_programs.setObjectName("action_programs")
        self.action_alarm_codes.setObjectName("action_alarm_codes")
        self.action_about.setObjectName("action_about")
        self.menu_file.addAction(self.action_settings)
        self.menu_file.addAction(self.action_show_log)
        self.menu_file.addSeparator()
        self.menu_file.addAction(self.action_quit)
        self.menu_help.addAction(self.action_verbs)
        self.menu_help.addAction(self.action_nouns)
        self.menu_help.addAction(self.action_programs)
        self.menu_help.addAction(self.action_alarm_codes)
        self.menu_help.addSeparator()
        self.menu_help.addAction(self.action_about)
        self.menubar.addAction(self.menu_file.menuAction())
        self.menubar.addAction(self.menu_help.menuAction())
        
        # self.retranslateUi(main_window)
        QtCore.QMetaObject.connectSlotsByName(main_window)
        
        # def retranslateUi(self, main_window):
        #     _translate = QtCore.QCoreApplication.translate
        #     main_window.setWindowTitle(_translate("main_window", "basaGC"))
        #     self.menu_file.setTitle(_translate("main_window", "&File"))
        #     self.menu_help.setTitle(_translate("main_window", "&Help"))
        #     self.action_settings.setText(_translate("main_window", "&Settings..."))
        #     self.action_show_log.setText(_translate("main_window", "Show &Log..."))
        #     self.action_quit.setText(_translate("main_window", "&Quit"))
        #     self.action_verbs.setText(_translate("main_window", "&Verbs..."))
        #     self.action_nouns.setText(_translate("main_window", "&Nouns..."))
        #     self.action_programs.setText(_translate("main_window", "&Programs"))
        #     self.action_alarm_codes.setText(_translate("main_window", "&Alarm Codes..."))
        #     self.action_about.setText(_translate("main_window", "Abou&t..."))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main_window = QtWidgets.QMainWindow()
    ui = GUI(main_window)
    computer = Computer(ui)
    main_window.show()
    sys.exit(app.exec_())
