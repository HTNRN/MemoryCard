from memo_card_layout import (
   app, layout_card,
   lb_Question, lb_Correct, lb_Result,
   rbtn_1, rbtn_2, rbtn_3, rbtn_4,
   btn_OK, show_question, show_result
)
from PyQt5.QtWidgets import QWidget, QApplication
from random import shuffle # будем перемешивать ответы в карточке вопроса
from PyQt5.QtCore import QTimer

card_width, card_height = 600, 500 # начальные размеры окна "карточка"
text_wrong = 'Невірно'
text_correct = 'Вірно'


# в этой версии напишем в коде один вопрос и ответы к нему
# соответствующие переменные как бы поля будущего объекта "form" (т.е. анкета)
frm_question = 'Яблуко'
frm_right = 'apple'
frm_wrong1 = 'application'
frm_wrong2 = 'building'
frm_wrong3 = 'caterpillar'


# Теперь нам нужно показать эти данные,
# причём ответы распределить случайно между радиокнопками, и помнить кнопку с правильным ответом.
# Для этого создадим набор ссылок на радиокнопки и перемешаем его
radio_list = [rbtn_1, rbtn_2, rbtn_3, rbtn_4]
shuffle(radio_list)
answer = radio_list[0] # мы не знаем, какой это из радиобаттонов, но можем положить сюда правильный ответ и запомнить это
wrong_answer1, wrong_answer2, wrong_answer3 = radio_list[1], radio_list[2], radio_list[3]


def show_data():
   ''' показує на екрані потрібну інформфцію '''
   # объединим в функцию похожие действия
   lb_Question.setText(frm_question)
   lb_Correct.setText(frm_right)
   answer.setText(frm_right)
   wrong_answer1.setText(frm_wrong1)
   wrong_answer2.setText(frm_wrong2)
   wrong_answer3.setText(frm_wrong3)


def check_result():
   ''' перевірка, правильный ли ответ выбран
   если ответ был выбран, то надпись "верно/неверно" приобретает нужное значение
   и показывается панель ответов '''
   correct = answer.isChecked() # в этом радиобаттоне лежит наш ответ!
   if correct:
       # ответ верный, запишем
      lb_Result.setText(text_correct) # надпись "верно" или "неверно"
      show_result()
   else:
      incorrect = wrong_answer1.isChecked() or wrong_answer2.isChecked() or wrong_answer3.isChecked()
      if incorrect:
           # ответ неверный, запишем и отразим в статистике
         lb_Result.setText(text_wrong) # надпись "верно" или "неверно"
         show_result()


def click_OK(self):
   # пока что проверяем вопрос, если мы в режиме вопроса, иначе ничего
    if btn_OK.text() != 'Наступне питання':
        check_result()


win_card = QWidget()
win_card.resize(card_width, card_height)
win_card.move(300, 300)
win_card.setWindowTitle('Memory Card')


win_card.setLayout(layout_card)
show_data()
show_question()
btn_OK.clicked.connect(click_OK)


win_card.show()
app.exec_()

from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QWidget

from memo_app import app
from memo_data import *
from memo_main_layout import *
from memo_card_layout import *
from memo_edit_layout import txt_Question, txt_Answer, txt_Wrong1, txt_Wrong2, txt_Wrong3

main_width, main_height = 1000, 450 # начальные размеры главного окна
card_width, card_height = 600, 500 # начальные размеры окна "карточка"
time_unit = 1000    # столько длится одна единица времени из тех, на которые нужно засыпать 
                    # (в рабочей версии программы увеличить в 60 раз!)

questions_listmodel = QuestionListModel() # список вопросов
radio_list = [rbtn_1, rbtn_2, rbtn_3, rbtn_4] # список виджетов, который надо перемешивать (для случайного размещения ответов)
frm_card = 0 # здесь будет связываться вопрос с формой теста
win_card = QWidget() # окно карточки
win_main = QWidget() # окно редактирования вопросов, основное в программе

def testlist():
    
    frm = Question('Яблоко', 'apple', 'application', 'pinapple', 'apply')
    questions_listmodel.form_list.append(frm)
    frm = Question('Дом', 'house', 'horse', 'hurry', 'hour')
    questions_listmodel.form_list.append(frm)
    frm = Question('Мышь', 'mouse', 'mouth', 'muse', 'museum')
    questions_listmodel.form_list.append(frm)
    frm = Question('Число', 'number', 'digit', 'amount', 'summary')
    questions_listmodel.form_list.append(frm)

def set_card():
    ''' задаёт, как выглядит окно карточки'''
    win_card.resize(card_width, card_height)
    win_card.move(300, 300)
    win_card.setWindowTitle('Memory Card')
    win_card.setLayout(layout_card)

def set_main():
    ''' задаёт, как выглядит основное окно'''
    win_main.resize(main_width, main_height)
    win_main.move(100, 100)
    win_main.setWindowTitle('Список вопросов')
    win_main.setLayout(layout_main)

def show_random():
    ''' показать случайный вопрос '''
    global frm_card # как бы свойство окна - текущая форма с данными карточки
    # получаем случайные данные, и случайно же распределяем варианты ответов по радиокнопкам:
    frm_card = random_AnswerCheck(questions_listmodel, lb_Question, radio_list, lb_Correct, lb_Result)
    # мы будем запускать функцию, когда окно уже есть. Так что показываем:
    frm_card.show() # загрузить нужные данные в соответствующие виджеты 
    show_question() # показать на форме панель вопросовq

def click_OK():
    ''' проверяет вопрос или загружает новый вопрос '''
    if btn_OK.text() != 'Следующий вопрос':
        frm_card.check()
        show_result()
    else:
        show_random()

def back_to_menu():
    ''' возврат из теста в окно редактора '''
    win_card.hide()
    win_main.showNormal()

def start_test():
    ''' при начале теста форма связывается со случайным вопросом и показывается'''
    show_random()
    win_card.show()
    win_main.showMinimized()

def connects():
    list_questions.setModel(questions_listmodel) # связать список на экране со списком вопросов
    btn_start.clicked.connect(start_test) # нажатие кнопки "начать тест" 
    btn_OK.clicked.connect(click_OK) # нажатие кнопки "OK" на форме теста
    btn_Menu.clicked.connect(back_to_menu) # нажатие кнопки "Меню" для возврата из формы теста в редактор вопросов

time_unit = 60000

def sleep_card():
testlist()
set_card()
set_main()
connects()
win_main.show()
app.exec_()

timer.timeout.connect(show_card)
btn_Sleep.clicked.connect(sleep_)
