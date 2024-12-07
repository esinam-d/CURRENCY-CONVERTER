import tkinter
from tkinter import ttk
from tkinter import *
import requests
from PIL import Image, ImageTk

#Using Tkinter to define the structure and body of the application window
converterapp = tkinter.Tk()

converterapp.title("CURRENCY CONVERTER") #This is for the title
converterapp.geometry("500x500")

#This is to load and set the background image. I made sure to save the image in the same file as my code so I can access it here.
background_image = Image.open("17454.jpg")
background_image = background_image.resize((500,500)) #This would make sure the image fits the window size
bg_photo = ImageTk.PhotoImage(background_image)

#Using canvas for the background 
canvas = Canvas(converterapp, width=500, height=500)
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, image=bg_photo, anchor="nw")

main_frame= Frame(canvas, bg="", bd=0) #This would produce a frame that is "transparent"
main_frame.place(relx=0.5, rely=0.5, anchor="center") 

def convert_the_currency():
    ''' 
    Converts amount from one currency to the other using real time exchange rates
    Displays the results of the conversion
    Returns an error message when any of the fields are left empty

    '''
    currency_to_convert_from= entry_currency_to_convert_from.get().upper()
    currency_to_convert_to= entry_currency_to_conver_to.get().upper()

    #using exception handling for a more robust code.
    try:
        amount= float(amount_input_from_entry.get())
    except ValueError: #if there is an unexpected error such as: input not being a number, error message will be displayed and code stops executing.
        display_result.config(text="Input a valid amount", foreground="red")
        return
    if not currency_to_convert_from or not currency_to_convert_to:
        display_result.config(text="The fields for currency cannot be empty", foreground="red")
        return
    if len(currency_to_convert_from) != 3 or len(currency_to_convert_to) != 3: #This is to check if the user has entered 3 letter code for the currency as an input
        display_result.config(text= "Currency must be a 3 letters code, for instance: USD, GBP")
        return
    

    # Construct API link using the currency_to_convert from
    apilink= f"https://open.er-api.com/v6/latest/{currency_to_convert_from}"
    
    try:
        # Make a get rquest to fetch data from the API
        response=requests.get(apilink)

        # Parse the JSON response from the API
        data=response.json()
        print(data)
        if currency_to_convert_to in data['rates']: #checks to see if the currency exists in the API data
            rate=data['rates'][currency_to_convert_to] # Retrieves conversion rate for the target currency
            amount_converted= amount * rate # Calculate the converted amount

            # Display results in a specified and appropriate format.
            display_result.config(
                text=f"{amount} {currency_to_convert_from} = {amount_converted:.3f}{currency_to_convert_to}"
            )
        else:
            display_result.config(text= "Invalid Currency/ Invalid currency code", foreground="red") #This would report a message any of the entry boxes are empty
    except requests.exceptions.RequestException:
        display_result.config(text= "There was an error connecting to server to fetch the rates", foreground="red") 



#Label and entry currency to convert from
label_currency_to_convert_from= ttk.Label(main_frame, text= "From what Currency: ") 
label_currency_to_convert_from.pack(pady=5) #Adding vertical padding for spacing
entry_currency_to_convert_from= ttk.Entry(main_frame) # Input field for the the current from
entry_currency_to_convert_from.pack(pady=5) #Adding vertical padding for spacing

# Label and entry currency to convert to
label_currency_to_conver_to=ttk.Label(main_frame, text="To what Currency: ") 
label_currency_to_conver_to.pack(pady=5) #Adding vertical padding for spacing
entry_currency_to_conver_to= ttk.Entry(main_frame) # Input field for the the currency to
entry_currency_to_conver_to.pack(pady=5)

#Label and entry amount to convert
label_for_amount= ttk.Label(main_frame, text= "Amount to convert: ") 
label_for_amount.pack(pady=5)#Adding vertical padding for spacing
amount_input_from_entry=ttk.Entry(main_frame) # Input field for amount to be converted
amount_input_from_entry.pack() #Adding vertical padding for spacing

#This is for the conversion button which will process the convert_the_currency function once it is clicked on
conversion_button= ttk.Button(main_frame, text= "CONVERT", command= convert_the_currency)
conversion_button.pack(pady=10)

#This label will display the results after the function has been processed
display_result= ttk.Label(main_frame, text=" ")
display_result.pack(pady=10)
 
# Start the tkinter main event loop
converterapp.mainloop() 