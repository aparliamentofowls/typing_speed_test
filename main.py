import json
from tkinter import *
import tkinter.scrolledtext as scrolledtest
from datetime import datetime
from random import randint


# Global Variables
BLUE = "#607EAA"
DARK_BEIGE = "#EAE3D2"
LIGHT_BEIGE = "#F9F5EB"
DARK_BLUE = "#1C3879"
timer = NONE
sample_text = "It was the best of times, it was the worst of times, it was the age of wisdom, it was the age of " \
              "foolishness, it was the epoch of belief, it was the epoch of incredulity, it was the season of Light, " \
              "it was the season of Darkness, it was the spring of hope, it was the winter of despair, we had " \
              "everything before us, we had nothing before us, we were all going direct to Heaven, we were all going " \
              "direct the other way—in short, the period was so far like the present period, that some of its " \
              "noisiest authorities insisted on its being received, for good or for evil, in the superlative degree " \
              "of comparison only"
count = 120
wpm = 0
accuracy = 0


# functions
def typing_test():
    global count
    if count == 120:
        count_down()
        start_button.configure(text="stop")
    else:
        start_button.config(text="stop")
        stop()


# if count hasn't reached zero, update everything, wait half a second, then call itself again.
# Else, stop
def count_down():
    global timer, count
    if count > 0:
        update()
        count -= 1
        timer = window.after(500, count_down)
    else:
        stop()


def update():
    global count
    timer_label.config(text=f"current time remaining: {int(count / 2)}")
    user_input = text_field.get("1.0", END)
    update_wpm(user_input)
    update_accuracy(user_input)
    correct_text_text_area.see(f"1.10 + {len(list(user_input.strip()))} char")


def update_wpm(user_input):
    global count, wpm
    user_list_of_word = user_input.split()
    correct_list_of_word = sample_text.split()
    num_correct_word = 0
    for x in range(0, len(user_list_of_word)):
        if x <= len(correct_list_of_word) and user_list_of_word[x] == correct_list_of_word[x]:
            num_correct_word += 1

    if count != 120:
        wpm = round(num_correct_word / ((120 - count) / 120), 2)
        wpm_label.config(text=f"wpm: {wpm}")


def update_accuracy(user_input):
    global count, accuracy
    user_list_of_char = list(user_input.strip())
    correct_list_of_char = list(sample_text.strip())

    number_of_correct_char = 0
    for x in range(0, len(user_list_of_char)):
        if x <= len(correct_list_of_char) and user_list_of_char[x] == correct_list_of_char[x]:
            number_of_correct_char += 1
            correct_text_text_area.tag_add("correct", f"1.0 + {x} char")
        else:
            correct_text_text_area.tag_add("incorrect", f"1.0 + {x} char")

    if len(user_list_of_char) > 0:
        accuracy = round(number_of_correct_char / len(user_list_of_char), 2)
        accuracy_label.config(text=f"accuracy: {accuracy}")


def stop():
    global count, timer
    timer_label.config(text=f"current time remaining: {int(count / 2)}")
    open_end_result_popup_window()
    window.after_cancel(timer)
    count = 120
    start_button.config(text="start")
    timer_label.config(text=f"current time remaining: {int(count/2)}")
    wpm_label.config(text=f"wpm: 0")
    accuracy_label.config(text=f"accuracy: 0")
    correct_text_text_area.tag_remove("correct", "1.0", END)
    correct_text_text_area.tag_remove("incorrect", "1.0", END)
    text_field.replace("1.0", END, "")


def open_end_result_popup_window():
    popup_win = Toplevel(window)
    popup_win.title("Result")
    popup_win.config(background=LIGHT_BEIGE)

    # label
    result_label = Label(popup_win, text="Test Completed!",
                         bg=LIGHT_BEIGE, fg=DARK_BLUE, font=("Helvetica", 30, "bold"))
    wpm_label = Label(popup_win, text=f"Your wpm is {wpm}!", bg=LIGHT_BEIGE,
                      fg=DARK_BLUE, font=("Helvetica", 30, "bold"))
    accuracy_label = Label(popup_win, text=f"Your accuracy is {accuracy}!", bg=LIGHT_BEIGE,
                           fg=DARK_BLUE, font=("Helvetica", 30, "bold"))
    result_label.config(padx=100, pady=30)
    wpm_label.config(padx=100, pady=30)
    accuracy_label.config(padx=100, pady=30)
    result_label.grid(column=0, row=0)
    wpm_label.grid(column=0, row=1)
    accuracy_label.grid(column=0, row=2)

    # function
    def close_popup_window():
        popup_win.destroy()
        save()
        load_past_result()

    # button
    close_button = Button(popup_win, text="close", command=close_popup_window)
    close_button.config(padx=10, pady=10, highlightbackground=LIGHT_BEIGE,
                     fg=DARK_BLUE, font=("Helvetica", 15, "bold"))
    close_button.grid(column=0, row=3)


def save():
    new_test_result = {
        f"{datetime.now().strftime('%Y-%m-%d %H:%M')}": {
            "wpm": wpm,
            "accuracy": accuracy,
        }
    }

    with open("data/past_result.json", "r") as file:
        old_data = json.load(file)

    with open("data/past_result.json", "w") as file:
        old_data.update(new_test_result)
        json.dump(old_data, file, indent=4)


def load_past_result():
    with open("data/past_result.json") as file:
        past_result_dict = json.load(file)
        historical_results = ""
        num = 0
        for past_result in past_result_dict.items():
            date = past_result[0]
            info = past_result[1]
            wpm = info["wpm"]
            accuracy = info["accuracy"]
            historical_results += f"{num}. {date} \n wpm: {wpm}, accuracy: {accuracy} \n"
            num += 1

        past_results['state'] = "normal"
        past_results.delete("1.0", END)
        past_results.insert(
            "1.0",
            historical_results
        )
        past_results['state'] = "disabled"


def change_text():
    global sample_text
    with open("data/text.json") as file:
        text_dictionary = json.load(file)
        text = text_dictionary[f"{randint(1, 5)}"]
        sample_text = text
        correct_text_text_area["state"] = "normal"
        correct_text_text_area.delete("1.0", END)
        correct_text_text_area.insert(
            INSERT,
            text,
        )
        correct_text_text_area["state"] = "disabled"


# window
window = Tk()
window.title("Typing Speed Test")
window.config(bg=LIGHT_BEIGE, padx=10, pady=10)


# buttons
start_button = Button(text="start", command=typing_test, highlightbackground=LIGHT_BEIGE,
                      fg=DARK_BLUE, font=("Helvetica", 15, "bold"), padx=5, pady=5)
change_text_button = Button(text="change text", command=change_text, highlightbackground=LIGHT_BEIGE,
                            fg=DARK_BLUE, font=("Helvetica", 15, "bold"), padx=5, pady=5)
load_button = Button(text="load past scores", command=load_past_result, highlightbackground=LIGHT_BEIGE,
                     fg=DARK_BLUE, font=("Helvetica", 15, "bold"), padx=5, pady=5)
load_button.grid(column=0, row=6)
change_text_button.grid(column=1, row=6)
start_button.grid(column=2, row=6)

# labels
main_label = Label(text="Typing Speed", bg=LIGHT_BEIGE,
                   fg=DARK_BLUE, font=("Helvetica", 30, "bold"), pady=20)
timer_label = Label(text=f"Time Remaining: {int(count / 2)} s", bg=LIGHT_BEIGE,
                    fg=DARK_BLUE, font=("Helvetica", 15, "bold"))
wpm_label = Label(text="WPM: 0", bg=LIGHT_BEIGE,
                  fg=DARK_BLUE, font=("Helvetica", 15, "bold"))
accuracy_label = Label(text="Accuracy: 0", bg=LIGHT_BEIGE,
                       fg=DARK_BLUE, font=("Helvetica", 15, "bold"))
scoreboard_label = Label(text="Past Scores", bg=LIGHT_BEIGE,
                         fg=DARK_BLUE, font=("Helvetica", 15, "bold"), pady=10)
main_label.grid(column=1, row=0, sticky="N")
timer_label.grid(column=0, row=1, sticky="N", padx=10)
wpm_label.grid(column=0, row=2, sticky="N")
accuracy_label.grid(column=0, row=3, sticky="N")
scoreboard_label.grid(column=0, row=4, sticky="N")

# Text
past_results = Text(width=13, wrap=WORD, height=16, padx=15, fg=BLUE, font=("Helvetica", 15))
past_results.grid(column=0, row=5)
past_results.insert(
    INSERT,
    "Press the load button!"
)
past_results['state'] = "disabled"

# scrolledText
correct_text_text_area = scrolledtest.ScrolledText(
    foreground=BLUE,
    width=25,
    height=8,
    font=("Helvetica", 25)
)
correct_text_text_area.insert(
    INSERT,
    sample_text,
)
correct_text_text_area.config(state="disabled", wrap=WORD, padx=20, pady=20)
correct_text_text_area.tag_configure("correct", background="#D3EBCD", foreground=BLUE)
correct_text_text_area.tag_configure("incorrect", background="#F55050", foreground=BLUE)
correct_text_text_area.grid(column=1, row=1, columnspan=2, rowspan=3, sticky="N")

# text field
text_field = Text(height=9, width=28, pady=10, wrap=WORD, foreground=BLUE, font=("Helvetica", 25))
text_field.grid(column=1, row=5, columnspan=2)

window.mainloop()
