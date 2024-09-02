from tkinter import *
import cv2
import mediapipe as mp
from PIL import Image, ImageTk

mp_draw = mp.solutions.drawing_utils
mp_hand = mp.solutions.hands
tipIds = [4, 8, 12, 16, 20]

video = cv2.VideoCapture(0)


def show_values():
    label.config(
        text=f"Values: {text_que.get('1.0', 'end-1c')}, {text_ans.get('1.0', 'end-1c')}",
        fg="blue")


Camcalc = Tk()
Camcalc.title("Camcalc")
Camcalc.geometry('850x570')
Camcalc.configure(bg='lightgrey')
webcam_frame = Frame(Camcalc)
webcam_frame.pack(pady=60, padx=(0, 20), anchor="w")
label = Label(webcam_frame)
label.pack()

text_que = Text(Camcalc, width=25, height=3, background="black", fg="gold", font=("Courgette", 18))
text_que.pack()
text_ans = Text(Camcalc, width=13, height=3, background="black", fg="gold", font=("Courgette", 18))
text_ans.pack()


def add_plus():
    text_que.insert(END, "+")


def add_mines():
    text_que.insert(END, "-")


def add_mull():
    text_que.insert(END,  "*")


def add_div():
    text_que.insert(END, "/")


def calculate():
    input_expression = text_que.get("1.0", "end-1c")
    try:
        result = eval(input_expression)
        text_ans.delete("1.0", END)
        text_ans.insert(END, str(result))
    except Exception as e:
        text_ans.delete("1.0", END)
        text_ans.insert(END, f"Error: {e}")

ok_pressed = False
def set_ok_pressed1():
    global ok_pressed, total_fingers1
    ok_pressed = True
    if ok_pressed:
        current_text = text_que.get("1.0", "end-1c")  # دریافت محتوای قبلی text_que
        new_text = f"{current_text} {total_fingers1}" if current_text else str(total_fingers1)  # اضافه کردن عدد جدید به محتوای قبلی
        text_que.delete(1.0, END)
        text_que.insert(END, new_text)



def clear_finger_count1():
    global total_fingers1, ok_pressed
    total_fingers1 = 0
    ok_pressed = False
    label.config(text="0 Finger(s)")
    current_text = text_que.get("1.0", "end-1c")
    new_text = current_text[:-2]
    text_que.delete(1.0, END)
    text_que.insert(END, new_text)

webcam_active = True
button_ok1 = Button(Camcalc,
                    text="OK",
                    width=18,
                    height=1,
                    bg="black",
                    fg="gold",
                    font=("Courgette", 14),
                    command=set_ok_pressed1)

button_clear1 = Button(Camcalc,
                       text="\u232B",
                       width=18,
                       height=1,
                       background="black",
                       fg="gold",
                       font=("Courgette", 14),
                       command=clear_finger_count1)

button_mull = Button(Camcalc,
                     text="\u00D7",
                     width=15,
                     height=3,
                     background="black",
                     fg="gold",
                     font=("Courgette", 15),
                     command=lambda: add_mull()
                     )
button_div = Button(Camcalc,
                    text="\u00F7",
                    width=15,
                    height=3,
                    background="black",
                    fg="gold",
                    font=("Courgette", 15),
                    command=lambda: add_div()
                    )
button_plus = Button(Camcalc,
                     text="\u002B",
                     width=15,
                     height=3,
                     background="black",
                     fg="gold",
                     font=("Courgette", 15),
                     command=lambda: add_plus()
                     )
button_min = Button(Camcalc,
                    text="\u2212",
                    width=15,
                    height=3,
                    background="black",
                    fg="gold",
                    font=("Courgette", 15),
                    command=lambda: add_mines()
                    )
button_equ = Button(Camcalc,
                    text="=",
                    width=18,
                    height=1,
                    background="black",
                    fg="gold",
                    font=("Courgette", 14),
                    command=calculate
                    )
button1 = Button(Camcalc,
                 text="",
                 width=17,
                 height=1,
                 background="black",
                 fg="gold",
                 font=("Courgette", 14),
                 )
button2 = Button(Camcalc,
                 text="Camcalc",
                 width=15,
                 height=3,
                 background="black",
                 fg="gold",
                 font=("Courgette", 15),
                 )

text_que.place(x=0, y=0)
text_ans.place(x=360, y=0)

button2.place(x=557, y=0)
button_div.place(x=557, y=93)
button_mull.place(x=557, y=183)
button_min.place(x=557, y=273)
button_plus.place(x=557, y=365)

button1.place(x=553, y=459)
button_equ.place(x=370, y=459)
button_clear1.place(x=186, y=459)
button_ok1.place(x=0, y=459)


total_fingers1 = 0
previous_fingers = None
with mp_hand.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:
    while webcam_active:
        ret, image = video.read()
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        results = hands.process(image)
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        lmList = []
        if results.multi_hand_landmarks:
            for hand_landmark in results.multi_hand_landmarks:
                myHands = results.multi_hand_landmarks[0]
                for id, lm in enumerate(myHands.landmark):
                    h, w, c = image.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    lmList.append([id, cx, cy])
                mp_draw.draw_landmarks(image, hand_landmark, mp_hand.HAND_CONNECTIONS)
        fingers = []
        if len(lmList) != 0:
            if lmList[tipIds[0]][1] > lmList[tipIds[0] - 1][1]:
                fingers.append(1)
            else:
                fingers.append(0)
            for id in range(1, 5):
                if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
                    fingers.append(1)
                else:
                    fingers.append(0)
            total = fingers.count(1)
            if total != previous_fingers:
                total_fingers1 = total
                label.config(text=f"{total_fingers1} Finger(s)")

        cv2image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=img)
        label.imgtk = imgtk
        label.configure(image=imgtk)
        label_width = 555
        label_height = 400
        label.config(width=label_width, height=label_height)

        Camcalc.update_idletasks()
        Camcalc.update()

    video.release()
    cv2.destroyAllWindows()

Camcalc.mainloop()
