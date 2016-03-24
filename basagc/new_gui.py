# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'basaGC.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Digit(QtWidgets.QLabel):

    def __init__(self, central_widget):
        super().__init__(self, central_widget)


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(572, 658)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../images/icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setAutoFillBackground(False)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.left_frame_left_border = QtWidgets.QLabel(self.centralwidget)
        self.left_frame_left_border.setGeometry(QtCore.QRect(42, 14, 8, 360))
        self.left_frame_left_border.setText("")
        self.left_frame_left_border.setPixmap(QtGui.QPixmap("../images/FrameVerticalL.jpg"))
        self.left_frame_left_border.setObjectName("left_frame_left_border")
        self.left_frame_bottom_border = QtWidgets.QLabel(self.centralwidget)
        self.left_frame_bottom_border.setGeometry(QtCore.QRect(50, 362, 211, 16))
        self.left_frame_bottom_border.setText("")
        self.left_frame_bottom_border.setPixmap(QtGui.QPixmap("../images/FrameHorizontal.jpg"))
        self.left_frame_bottom_border.setObjectName("left_frame_bottom_border")
        self.left_frame_right_border = QtWidgets.QLabel(self.centralwidget)
        self.left_frame_right_border.setGeometry(QtCore.QRect(242, 14, 8, 360))
        self.left_frame_right_border.setText("")
        self.left_frame_right_border.setPixmap(QtGui.QPixmap("../images/FrameVerticalL.jpg"))
        self.left_frame_right_border.setObjectName("left_frame_right_border")
        self.left_frame_top_border = QtWidgets.QLabel(self.centralwidget)
        self.left_frame_top_border.setGeometry(QtCore.QRect(50, 10, 211, 16))
        self.left_frame_top_border.setText("")
        self.left_frame_top_border.setPixmap(QtGui.QPixmap("../images/FrameHorizontal.jpg"))
        self.left_frame_top_border.setObjectName("left_frame_top_border")
        self.right_frame_right_border = QtWidgets.QLabel(self.centralwidget)
        self.right_frame_right_border.setGeometry(QtCore.QRect(516, 14, 8, 360))
        self.right_frame_right_border.setText("")
        self.right_frame_right_border.setPixmap(QtGui.QPixmap("../images/FrameVerticalL.jpg"))
        self.right_frame_right_border.setObjectName("right_frame_right_border")
        self.right_frame_bottom_border = QtWidgets.QLabel(self.centralwidget)
        self.right_frame_bottom_border.setGeometry(QtCore.QRect(324, 362, 211, 16))
        self.right_frame_bottom_border.setText("")
        self.right_frame_bottom_border.setPixmap(QtGui.QPixmap("../images/FrameHorizontal.jpg"))
        self.right_frame_bottom_border.setObjectName("right_frame_bottom_border")
        self.right_frame_top_border = QtWidgets.QLabel(self.centralwidget)
        self.right_frame_top_border.setGeometry(QtCore.QRect(324, 10, 201, 16))
        self.right_frame_top_border.setText("")
        self.right_frame_top_border.setPixmap(QtGui.QPixmap("../images/FrameHorizontal.jpg"))
        self.right_frame_top_border.setObjectName("right_frame_top_border")
        self.right_frame_left_border = QtWidgets.QLabel(self.centralwidget)
        self.right_frame_left_border.setGeometry(QtCore.QRect(316, 14, 8, 360))
        self.right_frame_left_border.setText("")
        self.right_frame_left_border.setPixmap(QtGui.QPixmap("../images/FrameVerticalL.jpg"))
        self.right_frame_left_border.setObjectName("right_frame_left_border")
        self.lighting_prog = QtWidgets.QLabel(self.centralwidget)
        self.lighting_prog.setGeometry(QtCore.QRect(452, 22, 64, 24))
        self.lighting_prog.setText("")
        self.lighting_prog.setPixmap(QtGui.QPixmap("../images/rProgOn.jpg"))
        self.lighting_prog.setObjectName("lighting_prog")
        self.annunciator_comp_acty = QtWidgets.QLabel(self.centralwidget)

        self.ctrl_reg_prog_d1 = QtWidgets.QLabel(self.centralwidget)
        self.ctrl_reg_prog_d1.setGeometry(QtCore.QRect(452, 46, 32, 45))
        self.ctrl_reg_prog_d1.setText("")
        self.ctrl_reg_prog_d1.setPixmap(QtGui.QPixmap("../images/7SegOff.jpg"))
        self.ctrl_reg_prog_d1.setObjectName("ctrl_reg_prog_d1")
        self.ctrl_reg_prog_d2 = QtWidgets.QLabel(self.centralwidget)
        self.ctrl_reg_prog_d2.setGeometry(QtCore.QRect(484, 46, 32, 45))
        self.ctrl_reg_prog_d2.setText("")
        self.ctrl_reg_prog_d2.setPixmap(QtGui.QPixmap("../images/7SegOff.jpg"))
        self.ctrl_reg_prog_d2.setObjectName("ctrl_reg_prog_d2")
        self.lighting_verb = QtWidgets.QLabel(self.centralwidget)
        self.lighting_verb.setGeometry(QtCore.QRect(324, 105, 64, 24))
        self.lighting_verb.setText("")
        self.lighting_verb.setPixmap(QtGui.QPixmap("../images/VerbOn.jpg"))
        self.lighting_verb.setObjectName("lighting_verb")
        self.lighting_noun = QtWidgets.QLabel(self.centralwidget)
        self.lighting_noun.setGeometry(QtCore.QRect(452, 105, 64, 24))
        self.lighting_noun.setText("")
        self.lighting_noun.setPixmap(QtGui.QPixmap("../images/NounOn.jpg"))
        self.lighting_noun.setObjectName("lighting_noun")
        self.ctrl_reg_verb_d1 = QtWidgets.QLabel(self.centralwidget)
        self.ctrl_reg_verb_d1.setGeometry(QtCore.QRect(324, 129, 32, 45))
        self.ctrl_reg_verb_d1.setText("")
        self.ctrl_reg_verb_d1.setPixmap(QtGui.QPixmap("../images/7SegOff.jpg"))
        self.ctrl_reg_verb_d1.setObjectName("ctrl_reg_verb_d1")
        self.ctrl_reg_verb_d2 = QtWidgets.QLabel(self.centralwidget)
        self.ctrl_reg_verb_d2.setGeometry(QtCore.QRect(356, 129, 32, 45))
        self.ctrl_reg_verb_d2.setText("")
        self.ctrl_reg_verb_d2.setPixmap(QtGui.QPixmap("../images/7SegOff.jpg"))
        self.ctrl_reg_verb_d2.setObjectName("ctrl_reg_verb_d2")
        self.ctrl_reg_noun_d1 = QtWidgets.QLabel(self.centralwidget)
        self.ctrl_reg_noun_d1.setGeometry(QtCore.QRect(452, 129, 32, 45))
        self.ctrl_reg_noun_d1.setText("")
        self.ctrl_reg_noun_d1.setPixmap(QtGui.QPixmap("../images/7SegOff.jpg"))
        self.ctrl_reg_noun_d1.setObjectName("ctrl_reg_noun_d1")
        self.ctrl_reg_noun_d2 = QtWidgets.QLabel(self.centralwidget)
        self.ctrl_reg_noun_d2.setGeometry(QtCore.QRect(484, 129, 32, 45))
        self.ctrl_reg_noun_d2.setText("")
        self.ctrl_reg_noun_d2.setPixmap(QtGui.QPixmap("../images/7SegOff.jpg"))
        self.ctrl_reg_noun_d2.setObjectName("ctrl_reg_noun_d2")
        self.lighting_sep_bar_1 = QtWidgets.QLabel(self.centralwidget)
        self.lighting_sep_bar_1.setGeometry(QtCore.QRect(324, 174, 192, 19))
        self.lighting_sep_bar_1.setText("")
        self.lighting_sep_bar_1.setPixmap(QtGui.QPixmap("../images/SeparatorOn.jpg"))
        self.lighting_sep_bar_1.setObjectName("lighting_sep_bar_1")
        self.data_reg_1_plus_minus = QtWidgets.QLabel(self.centralwidget)
        self.data_reg_1_plus_minus.setGeometry(QtCore.QRect(324, 193, 32, 45))
        self.data_reg_1_plus_minus.setText("")
        self.data_reg_1_plus_minus.setPixmap(QtGui.QPixmap("../images/PlusMinusOff.jpg"))
        self.data_reg_1_plus_minus.setObjectName("data_reg_1_plus_minus")
        self.lighting_sep_bar_2 = QtWidgets.QLabel(self.centralwidget)
        self.lighting_sep_bar_2.setGeometry(QtCore.QRect(324, 238, 192, 19))
        self.lighting_sep_bar_2.setText("")
        self.lighting_sep_bar_2.setPixmap(QtGui.QPixmap("../images/SeparatorOn.jpg"))
        self.lighting_sep_bar_2.setObjectName("lighting_sep_bar_2")
        self.data_reg_2_plus_minus = QtWidgets.QLabel(self.centralwidget)
        self.data_reg_2_plus_minus.setGeometry(QtCore.QRect(324, 257, 32, 45))
        self.data_reg_2_plus_minus.setText("")
        self.data_reg_2_plus_minus.setPixmap(QtGui.QPixmap("../images/PlusMinusOff.jpg"))
        self.data_reg_2_plus_minus.setObjectName("data_reg_2_plus_minus")
        self.lighting_sep_bar_3 = QtWidgets.QLabel(self.centralwidget)
        self.lighting_sep_bar_3.setGeometry(QtCore.QRect(324, 302, 192, 19))
        self.lighting_sep_bar_3.setText("")
        self.lighting_sep_bar_3.setPixmap(QtGui.QPixmap("../images/SeparatorOn.jpg"))
        self.lighting_sep_bar_3.setObjectName("lighting_sep_bar_3")
        self.data_reg_3_plus_minus = QtWidgets.QLabel(self.centralwidget)
        self.data_reg_3_plus_minus.setGeometry(QtCore.QRect(324, 321, 32, 45))
        self.data_reg_3_plus_minus.setText("")
        self.data_reg_3_plus_minus.setPixmap(QtGui.QPixmap("../images/PlusMinusOff.jpg"))
        self.data_reg_3_plus_minus.setObjectName("data_reg_3_plus_minus")
        self.data_reg_1_d1 = QtWidgets.QLabel(self.centralwidget)
        self.data_reg_1_d1.setGeometry(QtCore.QRect(356, 193, 32, 45))
        self.data_reg_1_d1.setText("")
        self.data_reg_1_d1.setPixmap(QtGui.QPixmap("../images/7SegOff.jpg"))
        self.data_reg_1_d1.setObjectName("data_reg_1_d1")
        self.data_reg_1_d2 = QtWidgets.QLabel(self.centralwidget)
        self.data_reg_1_d2.setGeometry(QtCore.QRect(388, 193, 32, 45))
        self.data_reg_1_d2.setText("")
        self.data_reg_1_d2.setPixmap(QtGui.QPixmap("../images/7SegOff.jpg"))
        self.data_reg_1_d2.setObjectName("data_reg_1_d2")
        self.data_reg_1_d3 = QtWidgets.QLabel(self.centralwidget)
        self.data_reg_1_d3.setGeometry(QtCore.QRect(420, 193, 32, 45))
        self.data_reg_1_d3.setText("")
        self.data_reg_1_d3.setPixmap(QtGui.QPixmap("../images/7SegOff.jpg"))
        self.data_reg_1_d3.setObjectName("data_reg_1_d3")
        self.data_reg_1_d4 = QtWidgets.QLabel(self.centralwidget)
        self.data_reg_1_d4.setGeometry(QtCore.QRect(452, 193, 32, 45))
        self.data_reg_1_d4.setText("")
        self.data_reg_1_d4.setPixmap(QtGui.QPixmap("../images/7SegOff.jpg"))
        self.data_reg_1_d4.setObjectName("data_reg_1_d4")
        self.data_reg_1_d5 = QtWidgets.QLabel(self.centralwidget)
        self.data_reg_1_d5.setGeometry(QtCore.QRect(484, 193, 32, 45))
        self.data_reg_1_d5.setText("")
        self.data_reg_1_d5.setPixmap(QtGui.QPixmap("../images/7SegOff.jpg"))
        self.data_reg_1_d5.setObjectName("data_reg_1_d5")
        self.data_reg_2_d3 = QtWidgets.QLabel(self.centralwidget)
        self.data_reg_2_d3.setGeometry(QtCore.QRect(420, 257, 32, 45))
        self.data_reg_2_d3.setText("")
        self.data_reg_2_d3.setPixmap(QtGui.QPixmap("../images/7SegOff.jpg"))
        self.data_reg_2_d3.setObjectName("data_reg_2_d3")
        self.data_reg_2_d1 = QtWidgets.QLabel(self.centralwidget)
        self.data_reg_2_d1.setGeometry(QtCore.QRect(356, 257, 32, 45))
        self.data_reg_2_d1.setText("")
        self.data_reg_2_d1.setPixmap(QtGui.QPixmap("../images/7SegOff.jpg"))
        self.data_reg_2_d1.setObjectName("data_reg_2_d1")
        self.data_reg_2_d4 = QtWidgets.QLabel(self.centralwidget)
        self.data_reg_2_d4.setGeometry(QtCore.QRect(452, 257, 32, 45))
        self.data_reg_2_d4.setText("")
        self.data_reg_2_d4.setPixmap(QtGui.QPixmap("../images/7SegOff.jpg"))
        self.data_reg_2_d4.setObjectName("data_reg_2_d4")
        self.data_reg_2_d2 = QtWidgets.QLabel(self.centralwidget)
        self.data_reg_2_d2.setGeometry(QtCore.QRect(388, 257, 32, 45))
        self.data_reg_2_d2.setText("")
        self.data_reg_2_d2.setPixmap(QtGui.QPixmap("../images/7SegOff.jpg"))
        self.data_reg_2_d2.setObjectName("data_reg_2_d2")
        self.data_reg_2_d5 = QtWidgets.QLabel(self.centralwidget)
        self.data_reg_2_d5.setGeometry(QtCore.QRect(484, 257, 32, 45))
        self.data_reg_2_d5.setText("")
        self.data_reg_2_d5.setPixmap(QtGui.QPixmap("../images/7SegOff.jpg"))
        self.data_reg_2_d5.setObjectName("data_reg_2_d5")
        self.data_reg_3_d3 = QtWidgets.QLabel(self.centralwidget)
        self.data_reg_3_d3.setGeometry(QtCore.QRect(420, 321, 32, 45))
        self.data_reg_3_d3.setText("")
        self.data_reg_3_d3.setPixmap(QtGui.QPixmap("../images/7SegOff.jpg"))
        self.data_reg_3_d3.setObjectName("data_reg_3_d3")
        self.data_reg_3_d1 = QtWidgets.QLabel(self.centralwidget)
        self.data_reg_3_d1.setGeometry(QtCore.QRect(356, 321, 32, 45))
        self.data_reg_3_d1.setText("")
        self.data_reg_3_d1.setPixmap(QtGui.QPixmap("../images/7SegOff.jpg"))
        self.data_reg_3_d1.setObjectName("data_reg_3_d1")
        self.data_reg_3_d4 = QtWidgets.QLabel(self.centralwidget)
        self.data_reg_3_d4.setGeometry(QtCore.QRect(452, 321, 32, 45))
        self.data_reg_3_d4.setText("")
        self.data_reg_3_d4.setPixmap(QtGui.QPixmap("../images/7SegOff.jpg"))
        self.data_reg_3_d4.setObjectName("data_reg_3_d4")
        self.data_reg_3_d2 = QtWidgets.QLabel(self.centralwidget)
        self.data_reg_3_d2.setGeometry(QtCore.QRect(388, 321, 32, 45))
        self.data_reg_3_d2.setText("")
        self.data_reg_3_d2.setPixmap(QtGui.QPixmap("../images/7SegOff.jpg"))
        self.data_reg_3_d2.setObjectName("data_reg_3_d2")
        self.data_reg_3_d5 = QtWidgets.QLabel(self.centralwidget)
        self.data_reg_3_d5.setGeometry(QtCore.QRect(484, 321, 32, 45))
        self.data_reg_3_d5.setText("")
        self.data_reg_3_d5.setPixmap(QtGui.QPixmap("../images/7SegOff.jpg"))
        self.data_reg_3_d5.setObjectName("data_reg_3_d5")
        self.static_display_1 = QtWidgets.QLabel(self.centralwidget)
        self.static_display_1.setGeometry(QtCore.QRect(388, 22, 64, 152))
        self.static_display_1.setText("")
        self.static_display_1.setPixmap(QtGui.QPixmap("../images/CenterBlock.jpg"))
        self.static_display_1.setScaledContents(True)
        self.static_display_1.setObjectName("static_display_1")
        self.static_display_2 = QtWidgets.QLabel(self.centralwidget)
        self.static_display_2.setGeometry(QtCore.QRect(452, 89, 64, 19))
        self.static_display_2.setText("")
        self.static_display_2.setPixmap(QtGui.QPixmap("../images/ShortHorizontal.jpg"))
        self.static_display_2.setObjectName("static_display_2")
        self.static_display_3 = QtWidgets.QLabel(self.centralwidget)
        self.static_display_3.setGeometry(QtCore.QRect(324, 86, 64, 19))
        self.static_display_3.setText("")
        self.static_display_3.setPixmap(QtGui.QPixmap("../images/ShortHorizontal.jpg"))
        self.static_display_3.setObjectName("static_display_3")
        self.annunciator_uplink_acty = QtWidgets.QLabel(self.centralwidget)
        self.annunciator_uplink_acty.setGeometry(QtCore.QRect(58, 28, 84, 40))
        self.annunciator_uplink_acty.setText("")
        self.annunciator_uplink_acty.setPixmap(QtGui.QPixmap("../images/UplinkActyOff.jpg"))
        self.annunciator_uplink_acty.setObjectName("annunciator_uplink_acty")
        self.annunciator_temp = QtWidgets.QLabel(self.centralwidget)
        self.annunciator_temp.setGeometry(QtCore.QRect(150, 28, 84, 40))
        self.annunciator_temp.setText("")
        self.annunciator_temp.setPixmap(QtGui.QPixmap("../images/TempOff.jpg"))
        self.annunciator_temp.setObjectName("annunciator_temp")
        self.annunciator_no_att = QtWidgets.QLabel(self.centralwidget)
        self.annunciator_no_att.setGeometry(QtCore.QRect(58, 76, 84, 40))
        self.annunciator_no_att.setText("")
        self.annunciator_no_att.setPixmap(QtGui.QPixmap("../images/NoAttOff.jpg"))
        self.annunciator_no_att.setObjectName("annunciator_no_att")
        self.annunciator_gimbal_lock = QtWidgets.QLabel(self.centralwidget)
        self.annunciator_gimbal_lock.setGeometry(QtCore.QRect(150, 76, 84, 40))
        self.annunciator_gimbal_lock.setText("")
        self.annunciator_gimbal_lock.setPixmap(QtGui.QPixmap("../images/GimbalLockOff.jpg"))
        self.annunciator_gimbal_lock.setObjectName("annunciator_gimbal_lock")
        self.annunciator_stby = QtWidgets.QLabel(self.centralwidget)
        self.annunciator_stby.setGeometry(QtCore.QRect(58, 125, 84, 40))
        self.annunciator_stby.setText("")
        self.annunciator_stby.setPixmap(QtGui.QPixmap("../images/StbyOff.jpg"))
        self.annunciator_stby.setObjectName("annunciator_stby")
        self.annunciator_prog = QtWidgets.QLabel(self.centralwidget)
        self.annunciator_prog.setGeometry(QtCore.QRect(150, 125, 84, 40))
        self.annunciator_prog.setText("")
        self.annunciator_prog.setPixmap(QtGui.QPixmap("../images/ProgOff.jpg"))
        self.annunciator_prog.setObjectName("annunciator_prog")
        self.annunciator_key_rel = QtWidgets.QLabel(self.centralwidget)
        self.annunciator_key_rel.setGeometry(QtCore.QRect(58, 174, 84, 40))
        self.annunciator_key_rel.setText("")
        self.annunciator_key_rel.setPixmap(QtGui.QPixmap("../images/KeyRelOff.jpg"))
        self.annunciator_key_rel.setObjectName("annunciator_key_rel")
        self.annunciator_restart = QtWidgets.QLabel(self.centralwidget)
        self.annunciator_restart.setGeometry(QtCore.QRect(150, 174, 84, 40))
        self.annunciator_restart.setText("")
        self.annunciator_restart.setPixmap(QtGui.QPixmap("../images/RestartOff.jpg"))
        self.annunciator_restart.setObjectName("annunciator_restart")
        self.annunciator_opr_err = QtWidgets.QLabel(self.centralwidget)
        self.annunciator_opr_err.setGeometry(QtCore.QRect(58, 223, 84, 40))
        self.annunciator_opr_err.setText("")
        self.annunciator_opr_err.setPixmap(QtGui.QPixmap("../images/OprErrOff.jpg"))
        self.annunciator_opr_err.setObjectName("annunciator_opr_err")
        self.annunciator_tracker = QtWidgets.QLabel(self.centralwidget)
        self.annunciator_tracker.setGeometry(QtCore.QRect(150, 223, 84, 40))
        self.annunciator_tracker.setText("")
        self.annunciator_tracker.setPixmap(QtGui.QPixmap("../images/TrackerOff.jpg"))
        self.annunciator_tracker.setObjectName("annunciator_tracker")
        self.annunciator_blank1 = QtWidgets.QLabel(self.centralwidget)
        self.annunciator_blank1.setGeometry(QtCore.QRect(58, 272, 84, 40))
        self.annunciator_blank1.setText("")
        self.annunciator_blank1.setPixmap(QtGui.QPixmap("../images/BlankOff.jpg"))
        self.annunciator_blank1.setObjectName("annunciator_blank1")
        self.annunciator_blank2 = QtWidgets.QLabel(self.centralwidget)
        self.annunciator_blank2.setGeometry(QtCore.QRect(150, 272, 84, 40))
        self.annunciator_blank2.setText("")
        self.annunciator_blank2.setPixmap(QtGui.QPixmap("../images/BlankOff.jpg"))
        self.annunciator_blank2.setObjectName("annunciator_blank2")
        self.annunciator_blank3 = QtWidgets.QLabel(self.centralwidget)
        self.annunciator_blank3.setGeometry(QtCore.QRect(58, 321, 84, 40))
        self.annunciator_blank3.setText("")
        self.annunciator_blank3.setPixmap(QtGui.QPixmap("../images/BlankOff.jpg"))
        self.annunciator_blank3.setObjectName("annunciator_blank3")
        self.annunciator_blank4 = QtWidgets.QLabel(self.centralwidget)
        self.annunciator_blank4.setGeometry(QtCore.QRect(150, 321, 84, 40))
        self.annunciator_blank4.setText("")
        self.annunciator_blank4.setPixmap(QtGui.QPixmap("../images/BlankOff.jpg"))
        self.annunciator_blank4.setObjectName("annunciator_blank4")
        self.annunciator_comp_acty.setGeometry(QtCore.QRect(324, 22, 64, 64))
        self.annunciator_comp_acty.setText("")
        self.annunciator_comp_acty.setPixmap(QtGui.QPixmap("../images/CompActyOff.jpg"))
        self.annunciator_comp_acty.setObjectName("annunciator_comp_acty")
        self.button_verb = QtWidgets.QPushButton(self.centralwidget)
        self.button_verb.setGeometry(QtCore.QRect(6, 430, 75, 75))
        self.button_verb.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("../images/VerbUp.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_verb.setIcon(icon1)
        self.button_verb.setIconSize(QtCore.QSize(65, 65))
        self.button_verb.setObjectName("button_verb")
        self.button_noun = QtWidgets.QPushButton(self.centralwidget)
        self.button_noun.setGeometry(QtCore.QRect(6, 510, 75, 75))
        self.button_noun.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("../images/NounUp.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_noun.setIcon(icon2)
        self.button_noun.setIconSize(QtCore.QSize(65, 65))
        self.button_noun.setObjectName("button_noun")
        self.button_plus = QtWidgets.QPushButton(self.centralwidget)
        self.button_plus.setGeometry(QtCore.QRect(88, 390, 75, 75))
        self.button_plus.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("../images/PlusUp.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_plus.setIcon(icon3)
        self.button_plus.setIconSize(QtCore.QSize(65, 65))
        self.button_plus.setObjectName("button_plus")
        self.button_minus = QtWidgets.QPushButton(self.centralwidget)
        self.button_minus.setGeometry(QtCore.QRect(88, 470, 75, 75))
        self.button_minus.setText("")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("../images/MinusUp.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_minus.setIcon(icon4)
        self.button_minus.setIconSize(QtCore.QSize(65, 65))
        self.button_minus.setObjectName("button_minus")
        self.button_0 = QtWidgets.QPushButton(self.centralwidget)
        self.button_0.setGeometry(QtCore.QRect(88, 550, 75, 75))
        self.button_0.setText("")
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap("../images/0Up.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_0.setIcon(icon5)
        self.button_0.setIconSize(QtCore.QSize(65, 65))
        self.button_0.setObjectName("button_0")
        self.button_4 = QtWidgets.QPushButton(self.centralwidget)
        self.button_4.setGeometry(QtCore.QRect(170, 470, 75, 75))
        self.button_4.setText("")
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap("../images/4Up.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_4.setIcon(icon6)
        self.button_4.setIconSize(QtCore.QSize(65, 65))
        self.button_4.setObjectName("button_4")
        self.button_7 = QtWidgets.QPushButton(self.centralwidget)
        self.button_7.setGeometry(QtCore.QRect(170, 390, 75, 75))
        self.button_7.setText("")
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap("../images/7Up.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_7.setIcon(icon7)
        self.button_7.setIconSize(QtCore.QSize(65, 65))
        self.button_7.setObjectName("button_7")
        self.button_1 = QtWidgets.QPushButton(self.centralwidget)
        self.button_1.setGeometry(QtCore.QRect(170, 550, 75, 75))
        self.button_1.setText("")
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap("../images/1Up.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_1.setIcon(icon8)
        self.button_1.setIconSize(QtCore.QSize(65, 65))
        self.button_1.setObjectName("button_1")
        self.button_9 = QtWidgets.QPushButton(self.centralwidget)
        self.button_9.setGeometry(QtCore.QRect(252, 470, 75, 75))
        self.button_9.setText("")
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap("../images/5Up.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_9.setIcon(icon9)
        self.button_9.setIconSize(QtCore.QSize(65, 65))
        self.button_9.setObjectName("button_9")
        self.button_8 = QtWidgets.QPushButton(self.centralwidget)
        self.button_8.setGeometry(QtCore.QRect(252, 390, 75, 75))
        self.button_8.setText("")
        icon10 = QtGui.QIcon()
        icon10.addPixmap(QtGui.QPixmap("../images/8Up.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_8.setIcon(icon10)
        self.button_8.setIconSize(QtCore.QSize(65, 65))
        self.button_8.setObjectName("button_8")
        self.button_2 = QtWidgets.QPushButton(self.centralwidget)
        self.button_2.setGeometry(QtCore.QRect(252, 550, 75, 75))
        self.button_2.setText("")
        icon11 = QtGui.QIcon()
        icon11.addPixmap(QtGui.QPixmap("../images/2Up.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_2.setIcon(icon11)
        self.button_2.setIconSize(QtCore.QSize(65, 65))
        self.button_2.setObjectName("button_2")
        self.button_6 = QtWidgets.QPushButton(self.centralwidget)
        self.button_6.setGeometry(QtCore.QRect(335, 470, 75, 75))
        self.button_6.setText("")
        icon12 = QtGui.QIcon()
        icon12.addPixmap(QtGui.QPixmap("../images/6Up.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_6.setIcon(icon12)
        self.button_6.setIconSize(QtCore.QSize(65, 65))
        self.button_6.setObjectName("button_6")
        self.button_10 = QtWidgets.QPushButton(self.centralwidget)
        self.button_10.setGeometry(QtCore.QRect(335, 390, 75, 75))
        self.button_10.setText("")
        icon13 = QtGui.QIcon()
        icon13.addPixmap(QtGui.QPixmap("../images/9Up.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_10.setIcon(icon13)
        self.button_10.setIconSize(QtCore.QSize(65, 65))
        self.button_10.setObjectName("button_10")
        self.button_3 = QtWidgets.QPushButton(self.centralwidget)
        self.button_3.setGeometry(QtCore.QRect(335, 550, 75, 75))
        self.button_3.setText("")
        icon14 = QtGui.QIcon()
        icon14.addPixmap(QtGui.QPixmap("../images/3Up.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_3.setIcon(icon14)
        self.button_3.setIconSize(QtCore.QSize(65, 65))
        self.button_3.setObjectName("button_3")
        self.button_pro = QtWidgets.QPushButton(self.centralwidget)
        self.button_pro.setGeometry(QtCore.QRect(418, 470, 75, 75))
        self.button_pro.setText("")
        icon15 = QtGui.QIcon()
        icon15.addPixmap(QtGui.QPixmap("../images/ProUp.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_pro.setIcon(icon15)
        self.button_pro.setIconSize(QtCore.QSize(65, 65))
        self.button_pro.setObjectName("button_pro")
        self.button_clr = QtWidgets.QPushButton(self.centralwidget)
        self.button_clr.setGeometry(QtCore.QRect(418, 390, 75, 75))
        self.button_clr.setText("")
        icon16 = QtGui.QIcon()
        icon16.addPixmap(QtGui.QPixmap("../images/ClrUp.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_clr.setIcon(icon16)
        self.button_clr.setIconSize(QtCore.QSize(65, 65))
        self.button_clr.setObjectName("button_clr")
        self.button_key_rel = QtWidgets.QPushButton(self.centralwidget)
        self.button_key_rel.setGeometry(QtCore.QRect(418, 550, 75, 75))
        self.button_key_rel.setText("")
        icon17 = QtGui.QIcon()
        icon17.addPixmap(QtGui.QPixmap("../images/KeyRelUp.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_key_rel.setIcon(icon17)
        self.button_key_rel.setIconSize(QtCore.QSize(65, 65))
        self.button_key_rel.setObjectName("button_key_rel")
        self.button_entr = QtWidgets.QPushButton(self.centralwidget)
        self.button_entr.setGeometry(QtCore.QRect(496, 411, 75, 75))
        self.button_entr.setText("")
        icon18 = QtGui.QIcon()
        icon18.addPixmap(QtGui.QPixmap("../images/EntrUp.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_entr.setIcon(icon18)
        self.button_entr.setIconSize(QtCore.QSize(65, 65))
        self.button_entr.setObjectName("button_entr")
        self.button_rset = QtWidgets.QPushButton(self.centralwidget)
        self.button_rset.setGeometry(QtCore.QRect(496, 491, 75, 75))
        self.button_rset.setText("")
        icon19 = QtGui.QIcon()
        icon19.addPixmap(QtGui.QPixmap("../images/RsetUp.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_rset.setIcon(icon19)
        self.button_rset.setIconSize(QtCore.QSize(65, 65))
        self.button_rset.setObjectName("button_rset")
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
        self.annunciator_comp_acty.raise_()
        self.ctrl_reg_prog_d1.raise_()
        self.ctrl_reg_prog_d2.raise_()
        self.lighting_verb.raise_()
        self.lighting_noun.raise_()
        self.ctrl_reg_verb_d1.raise_()
        self.ctrl_reg_verb_d2.raise_()
        self.ctrl_reg_noun_d1.raise_()
        self.ctrl_reg_noun_d2.raise_()
        self.lighting_sep_bar_1.raise_()
        self.data_reg_1_plus_minus.raise_()
        self.lighting_sep_bar_2.raise_()
        self.data_reg_2_plus_minus.raise_()
        self.lighting_sep_bar_3.raise_()
        self.data_reg_3_plus_minus.raise_()
        self.data_reg_1_d1.raise_()
        self.data_reg_1_d2.raise_()
        self.data_reg_1_d3.raise_()
        self.data_reg_1_d4.raise_()
        self.data_reg_1_d5.raise_()
        self.data_reg_2_d3.raise_()
        self.data_reg_2_d1.raise_()
        self.data_reg_2_d4.raise_()
        self.data_reg_2_d2.raise_()
        self.data_reg_2_d5.raise_()
        self.data_reg_3_d3.raise_()
        self.data_reg_3_d1.raise_()
        self.data_reg_3_d4.raise_()
        self.data_reg_3_d2.raise_()
        self.data_reg_3_d5.raise_()
        self.static_display_1.raise_()
        self.annunciator_uplink_acty.raise_()
        self.annunciator_temp.raise_()
        self.annunciator_no_att.raise_()
        self.annunciator_gimbal_lock.raise_()
        self.annunciator_stby.raise_()
        self.annunciator_prog.raise_()
        self.annunciator_key_rel.raise_()
        self.annunciator_restart.raise_()
        self.annunciator_opr_err.raise_()
        self.annunciator_tracker.raise_()
        self.annunciator_blank1.raise_()
        self.annunciator_blank2.raise_()
        self.annunciator_blank3.raise_()
        self.annunciator_blank4.raise_()
        self.button_verb.raise_()
        self.button_noun.raise_()
        self.button_plus.raise_()
        self.button_minus.raise_()
        self.button_0.raise_()
        self.button_4.raise_()
        self.button_7.raise_()
        self.button_1.raise_()
        self.button_9.raise_()
        self.button_8.raise_()
        self.button_2.raise_()
        self.button_6.raise_()
        self.button_10.raise_()
        self.button_3.raise_()
        self.button_pro.raise_()
        self.button_clr.raise_()
        self.button_key_rel.raise_()
        self.button_entr.raise_()
        self.button_rset.raise_()
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 572, 21))
        self.menubar.setObjectName("menubar")
        self.menu_file = QtWidgets.QMenu(self.menubar)
        self.menu_file.setObjectName("menu_file")
        self.menu_help = QtWidgets.QMenu(self.menubar)
        self.menu_help.setObjectName("menu_help")
        MainWindow.setMenuBar(self.menubar)
        self.action_settings = QtWidgets.QAction(MainWindow)
        self.action_settings.setEnabled(True)
        self.action_settings.setObjectName("action_settings")
        self.action_show_log = QtWidgets.QAction(MainWindow)
        self.action_show_log.setObjectName("action_show_log")
        self.action_quit = QtWidgets.QAction(MainWindow)
        self.action_quit.setObjectName("action_quit")
        self.action_verbs = QtWidgets.QAction(MainWindow)
        self.action_verbs.setObjectName("action_verbs")
        self.action_nouns = QtWidgets.QAction(MainWindow)
        self.action_nouns.setObjectName("action_nouns")
        self.action_programs = QtWidgets.QAction(MainWindow)
        self.action_programs.setObjectName("action_programs")
        self.action_alarm_codes = QtWidgets.QAction(MainWindow)
        self.action_alarm_codes.setObjectName("action_alarm_codes")
        self.action_about = QtWidgets.QAction(MainWindow)
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

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "basaGC"))
        self.menu_file.setTitle(_translate("MainWindow", "&File"))
        self.menu_help.setTitle(_translate("MainWindow", "&Help"))
        self.action_settings.setText(_translate("MainWindow", "&Settings..."))
        self.action_show_log.setText(_translate("MainWindow", "Show &Log..."))
        self.action_quit.setText(_translate("MainWindow", "&Quit"))
        self.action_verbs.setText(_translate("MainWindow", "&Verbs..."))
        self.action_nouns.setText(_translate("MainWindow", "&Nouns..."))
        self.action_programs.setText(_translate("MainWindow", "&Programs"))
        self.action_alarm_codes.setText(_translate("MainWindow", "&Alarm Codes..."))
        self.action_about.setText(_translate("MainWindow", "Abou&t..."))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

