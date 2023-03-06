from tkinter import *

BLUE = "#C2DED1"
BEIGE = "#ECE5C7"
DARK_BEIGE = "#CDC2AE"
DARK_BLUE = "#354259"
sample_text = "It was the best of times, it was the worst of times, it was the age of wisdom, it was the age of foolishness, it was the epoch of belief, it was the epoch of incredulity, it was the season of Light, it was the season of Darkness, it was the spring of hope, it was the winter of despair, we had everything before us, we had nothing before us, we were all going direct to Heaven, we were all going direct the other way—in short, the period was so far like the present period, that some of its noisiest authorities insisted on its being received, for good or for evil, in the superlative degree of comparison only"
sample_text_split = sample_text.split()
timer = None
count = 60

window = Tk()
window.title("Typing Speed Test")
window.config(bg=DARK_BEIGE)


# functions
def update():
    timer_label.config(text=f"current time remaining: {count}")

    # wpm
    user_input = text_field.get("1.0", END)
    list_of_words = user_input.split()
    number_of_correct_words = 0
    for x in range(0, len(list_of_words)):
        if list_of_words[x] == sample_text_split[x]:
            number_of_correct_words += 1

    print(number_of_correct_words)
    if count != 60:
        wpm = round(number_of_correct_words / ((60 - count) / 60), 2)
        wpm_label.config(text=f"wpm: {wpm}")

    # accuracy
    if len(list_of_words) > 0:
        accuracy = round(number_of_correct_words / len(list_of_words), 2)
        accuracy_label.config(text=f"accuracy: {accuracy}")


def count_down():
    global timer, count
    if count > 0:
        update()
        count -= 1
        timer = window.after(1000, count_down)
    else:
        timer_label.config(text=f"current time remaining: {count}")
        stop()


def typing_test():
    global count
    if count == 60:
        start_button.config(text="stop")
        count_down()
    else:
        stop()


def stop():
    global count, timer
    window.after_cancel(timer)
    count = 60
    start_button.config(text="start")
    timer_label.config(text=f"current time remaining: {count}")
    wpm_label.config(text=f"wpm: __")
    accuracy_label.config(text=f"accuracy: __")
    text_field.replace("1.0", END, "")



def change_text():
    pass


# buttons
start_button = Button(text="start", command=typing_test, highlightbackground=DARK_BEIGE)
start_button.grid(column=0, row=0)
change_text_button = Button(text="change text", command=change_text, highlightbackground=DARK_BEIGE)
change_text_button.grid(column=1, row=0)

# labels
timer_label = Label(text=f"current time remaining: {count}", bg=DARK_BEIGE)
timer_label.grid(column=0, row=1)
wpm_label = Label(text="wpm: 0", bg=DARK_BEIGE)
wpm_label.grid(column=0, row=2)
accuracy_label = Label(text="accuracy: ", bg=DARK_BEIGE)
accuracy_label.grid(column=0, row=3)

# canvas
canvas = Canvas(width=400, height=240)
display_text = canvas.create_text(
    200,
    120,
    text=sample_text,
    width=280,
    font=("Arial", 14),
    fill=DARK_BLUE,
)

canvas.grid(column=1, row=1, rowspan=3, padx=20, pady=20)
text_field = Text(height=20, width=58, pady=10, wrap=WORD)
text_field.grid(column=1, row=4)

window.mainloop()