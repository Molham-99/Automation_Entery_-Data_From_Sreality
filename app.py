from tkinter import *
from tkhtmlview import HTMLLabel
from tkinter import messagebox
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from tkinter import filedialog as fd

class App:
    def __init__(self):
        self.window = Tk()
        self.window.title("Created By Molham")
        self.window.config(padx=20, pady=20)
        self.window.maxsize(width=800, height=500)
        self.google_form_label = Label(text="Enter the link for your Questionare", font=("Arial", 10, "bold"))
        self.google_form_label.grid(column=0, row=0)

        self.link = HTMLLabel(self.window, html="<a href = https://docs.google.com/forms/> Google form </a>", font=("Arial", 10, "bold"))
        self.link.config(padx=30, pady=80)
        self.link.grid(column=0, row=8, columnspan=2)

        self.price_label = Label(text="Enter your budget (Up to):", font=("Arial", 10, "bold"))
        self.price_label.grid(column=0, row=2, padx=15, pady=15)

        self.location_label = Label(text="Enter the location \n(in Czech language):", font=("Arial", 10, "bold"))
        self.location_label.grid(column=0, row=3, padx=15, pady=15)

        self.google_doc_label = Label(text="Enter the link for your form", font=("Arial", 10, "bold"))
        self.google_doc_label.grid(column=0, row=4, padx=15, pady=15)

        self.google_form_text = Entry(width=20, font=('Arial', 16))
        self.google_form_text.grid(column=1, row=0, rowspan=2)
        self.google_form_text.focus()

        self.price_text = Entry(width=20, font=('Arial', 16))
        self.price_text.grid(column=1, row=2)

        self.location_text = Entry(width=20, font=('Arial', 16))
        self.location_text.grid(column=1, row=3)

        self.google_doc_text = Entry(width=20, font=('Arial', 16))
        self.google_doc_text.grid(column=1, row=4)

        self.start_button = Button(text="Start", width=40, command=self.start)
        self.start_button.grid(column=0, row=5, columnspan=2)

        self.files_location_button = Button(text="Downloads Location", width=40, command=self.opendownloads)
        self.files_location_button.grid(column=0, row=6, columnspan=2)

        self.hint_button = Button(text="Hints & Support", width=40, command=self.hints)
        self.hint_button.grid(column=0, row=7, columnspan=2)
        self.window.mainloop()

    def hints(self):
        ok = messagebox.askokcancel(title="Hints", message="This application created for automate entering data from"
                                                           " Sreality website\nClick Ok to continue")
        if ok:
            ok = messagebox.askokcancel(title="Hints", message="You need to create a new form in Google"
                                                   " Forms, Go to https://docs.google.com/forms/ and create your own "
                                                   "form and add 3 questions to the form, make all questions "
                                                   "(short-answer)\nThe adress \nThe price\nThe link\nThen Click send "
                                                   "and copy the link address of the form\nPaste the link in the "
                                                   "first box\nClick Ok to continue")
            if ok :
                ok = messagebox.askokcancel(title="Hints", message="In the second box enter your MAXIMUM budget"
                                                                   "\nClick Ok to continue")
                if ok:
                    ok = messagebox.askokcancel(title="Hints", message="In the third box enter your target location"
                                                                       "(in Czech language)"
                                                                       "\nClick Ok to continue")
                    if ok:
                        ok = messagebox.askokcancel(title="Hints", message="In the forth box enter Google Sheet URL"
                                                                           "\nClick Ok to continue")
                        if ok:
                            ok = messagebox.askokcancel(title="Hints",
                                                        message="NOTICE: You need to change your setting in the form "
                                                                "\nGo to setting --> ADD COLLABORATORS --> General Access"
                                                                " --> Anyone with the link"
                                                                "\nClick Ok to continue")
                            if ok:
                                messagebox.askokcancel(title="Hints",
                                                            message="FINALLY!\nYou should click manually on "
                                                                    "Souhlasim button")

    def start(self):
        google_form_url_content = self.google_form_text.get()
        price_text_content = self.price_text.get()
        location_text_content = self.location_text.get()
        google_doc_content = self.google_doc_text.get()
        if google_form_url_content == "" or price_text_content == "" \
                or location_text_content == "" or google_doc_content == "":
            messagebox.showinfo(title="Oops!!!!", message="Please don't leave any fields empty! ")
        else:
            is_ok = messagebox.askokcancel(title="Details message!",
                                           message=f"Those are the details entered :\n"
                                                   f" Google form URL: {google_form_url_content}\n"
                                                   f" The price: {price_text_content}\n"
                                                   f" The location: {location_text_content}"
                                                   f" The location: {google_doc_content}")
            if is_ok:
                self.price_text.delete(0, END)
                self.location_text.delete(0, END)
                Search(google_form_url_content ,location_text_content, price_text_content, google_doc_content)

    def opendownloads(self):
        fd.askopenfilename(initialdir=r"C:\Users\Dado\Downloads", title= "All files")


class Search:
    def __init__(self,google_form, location, price, google_doc):
        self.S_REALITY_URL = f"https://www.sreality.cz/hledani/pronajem/byty/{location}?velikost=3%2Bkk&cena-od=0&cena-do={price}"
        self.chrome_options = Options()
        self.chrome_options.add_experimental_option("detach", True)
        self.chrome_driver_path = Service("C:\Development\chromedriver.exe")
        self.driver = webdriver.Chrome(service=self.chrome_driver_path, options=self.chrome_options)
        self.driver.get(f"{self.S_REALITY_URL}")
        time.sleep(5)
        is_ok = messagebox.showwarning(title="NOTICE!!!", message="Click on Souhlasim please")
        if is_ok:
            pass
        time.sleep(5)
        self.prices_list = []
        self.links_list = []
        self.addresses_list = []

        def prices():
            time.sleep(4)
            price = self.driver.find_elements(by="css selector", value='.price')
            for y in price:
                price = y.text
                only_price = price.replace("za měsíc", '')
                self.prices_list.append(only_price)
            if self.prices_list == []:
                messagebox.showinfo(title="NOTICE!!", message="There are no results!\nTry with more budget")
                self.driver.close()
                exit()


        def links():
            time.sleep(4)
            links = self.driver.find_elements(by="css selector", value='.text-wrap span h2 a')
            for x in links:
                link = x.get_attribute("href")
                self.links_list.append(link)

        def address():
            time.sleep(4)
            addresses = self.driver.find_elements(by="css selector", value='.locality')
            for x in addresses:
                address = x.text
                self.addresses_list.append(address)

        n = True
        while True:
            time.sleep(3)
            if n == True:
                prices()
                links()
                address()
                n = False
            try:
                click = self.driver.find_element(by="css selector", value='.paging-next')
                classes = click.get_attribute("class").split()
                if classes[-1] == 'disabled':
                    break
                click.click()
                prices()
                links()
                address()
            except :
                break

        self.driver.get(f"{google_form}")
        length = len(self.addresses_list)
        n = 0
        for h in range(length):
            get_attributes = self.driver.find_elements(by="css selector", value=".Xb9hP input")
            for x in get_attributes:
                y = x.get_attribute("aria-labelledby")
                time.sleep(1)
                if y == 'i1':
                    insert_address = self.driver.find_element(by="css selector", value=".Xb9hP input")
                    insert_address.send_keys(f'{self.addresses_list[n]}')
                if y == 'i5':
                    insert_price = self.driver.find_element(by="xpath",
                                                       value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
                    insert_price.send_keys(f'{self.prices_list[n]}')
                if y == 'i9':
                    insert_link = self.driver.find_element(by="xpath",
                                                      value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
                    insert_link.send_keys(f'{self.links_list[n]}')
                    self.driver.find_element(by="xpath", value='//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div').click()
                    self.driver.find_element(by="css selector", value='.c2gzEf a').click()
                    n += 1
                    time.sleep(2)

        self.driver.get(f"{google_doc}")
        self.driver.find_element(by="xpath", value='//*[@id="tJHJj"]/div[3]/div[1]/div/div[2]').click()
        time.sleep(6)
        create_sheet = self.driver.find_element(by="xpath", value='/html/body/div[3]/div[2]/div[2]/div/div[1]/div[1]/div[2]/div[2]/div/div')
        create_sheet.click()
        time.sleep(1)
        self.driver.find_element(by='xpath', value='/html/body/div[3]/div[5]/div/div/span[4]/div[3]/div').click()
        time.sleep(2)
        self.driver.close()
