import tkinter as tk
import tkinter.messagebox
import customtkinter
import os
from tkinter import filedialog
from tkinter import simpledialog, messagebox
from pickle import TRUE
import cv2
from PIL import Image, ImageTk
import numpy as np
import matplotlib as plt

#initialize the default color mode
customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("Image processing tool")
        self.geometry(f"{910}x{730}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # create left sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        #title
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="IPT", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        #open button
        self.sidebar_button_open = customtkinter.CTkButton(self.sidebar_frame, text="Open", 
                                                           command=self.sidebar_button_open_event)
        self.sidebar_button_open.grid(row=1, column=0, padx=20, pady=10)

        #save button
        #self.sidebar_button_save = customtkinter.CTkButton(self.sidebar_frame, text="Save", 
                                                           #command=self.sidebar_button_save_event)
        #self.sidebar_button_save.grid(row=2, column=0, padx=20, pady=10)


        #theme dropdown

        #theme title
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Theme:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))

        #theme menu
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"], 
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 20))



        #original image preview code should be here

        # create middle top widget to preview original image
        self.middle_frame = customtkinter.CTkFrame(self, width= 200, height = 210, corner_radius=8)
        self.middle_frame.grid(row=0, column=1, sticky="w", padx=(10, 5), pady=(5, 5))
        self.middle_frame.grid_rowconfigure(1, weight=1)

        #original image display

        self.image_preview = tk.Label(self.middle_frame, bg="#f0f0f0")
        self.image_preview.grid(row=0, column=0, padx=20, pady=10)


        #showing the original image title
        self.title_image_preview = customtkinter.CTkLabel(self.middle_frame, text="Original Image")
        self.title_image_preview.grid(row=0, column=1, padx=20, pady=10)


        #output image code

        # create middle bottom widget to preview output image
        self.middle_frame = customtkinter.CTkFrame(self, width=100, height = 100, corner_radius=8)
        self.middle_frame.grid(row=1, column=1, sticky="w",padx=(10, 10), pady=(5, 5))
        #self.middle_frame.grid_rowconfigure(4, weight=1)

        #output image title
        self.title_image_output = customtkinter.CTkLabel(self.middle_frame, text="Output Image")
        self.title_image_output.grid(row=0, column=0, padx=20, pady=10)


        #output image display

        self.image_output = tk.Label(self.middle_frame, bg="#f0f0f0")
        self.image_output.grid(row=1, column=0, padx=20, pady=10)





    #tab widget

        #tabview
        self.tabview = customtkinter.CTkTabview(self, width=250)
        self.tabview.grid(row=0, column=2, rowspan=3, padx=(0, 20), pady=(20, 20), sticky="nsew")

        #define tabs
        self.tabview.add("Basic")
        self.tabview.add("Advanced")
        self.tabview.add("AI")
        
        # configure grid of individual tabs
        self.tabview.tab("Basic").grid_columnconfigure(0, weight=1)  
        self.tabview.tab("Advanced").grid_columnconfigure(0, weight=1)
        self.tabview.tab("AI").grid_columnconfigure(0, weight=1)



        #configure basic tab

        #colour title
        self.title_basic_color = customtkinter.CTkLabel(self.tabview.tab("Basic"), anchor="w", 
                                                        text="Color Mode:")
        self.title_basic_color.grid(row=0, column=0, padx=20, pady=(10, 0))

        #color list
        self.optionmenu_basic_color = customtkinter.CTkOptionMenu(self.tabview.tab("Basic"), dynamic_resizing=False, values=["RGB", "Grayscale", "B&W"], 
                                                            command=self.basic_color_option) #color menu function
        self.optionmenu_basic_color.grid(row=1, column=0, padx=20, pady=(5,10))

        #transformations title
        self.title_basic_transformations = customtkinter.CTkLabel(self.tabview.tab("Basic"), text="Transformations", anchor="w")
        self.title_basic_transformations.grid(row=2, column=0, padx=20, pady=(10, 0))

        #rotate title
        self.title_basic_rotation = customtkinter.CTkLabel(self.tabview.tab("Basic"), text="Rotation:", anchor="w")
        self.title_basic_rotation.grid(row=3, column=0, padx=20, pady=(0, 0))

        #rotate input box
        self.inputBox_basic_rotation = customtkinter.CTkEntry(self.tabview.tab("Basic"), placeholder_text="Enter Value")
        self.inputBox_basic_rotation.grid(row=4, column=0, padx=(20, 20), pady=(0, 0), sticky="nsew")

        #rotate submit button
        self.main_button_basic_rotation = customtkinter.CTkButton(master=self.tabview.tab("Basic"), fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), 
                                                                  text="Rotate",
                                                                  command=self.button_basic_rotate_event)
        self.main_button_basic_rotation.grid(row=5, column=0, padx=(40, 40), pady=(10, 0), sticky="nsew")

        #checkbox cropping
        self.check_var_basic_crop = customtkinter.StringVar(value="off")
        self.checkbox_basic_crop = customtkinter.CTkCheckBox(self.tabview.tab("Basic"), text="   Cropping", command=self.checkbox_basic_crop_event, variable=self.check_var_basic_crop, onvalue="on", offvalue="off")
        self.checkbox_basic_crop.grid(row=6, column=0, padx=5, pady=(20, 5))


        #cropping input box
        self.inputBox_basic_cropping = customtkinter.CTkEntry(self.tabview.tab("Basic"), 
                                                              placeholder_text="Enter Value (X Y)")
        self.inputBox_basic_cropping.grid(row=7, column=0, padx=(20, 20), pady=(0, 0), sticky="nsew")

        #cropping submit button
        self.main_button_basic_cropping_submit = customtkinter.CTkButton(master=self.tabview.tab("Basic"), fg_color="transparent", text="Submit Values", border_width=2, text_color=("gray10", "#DCE4EE"), 
                                                                  command=self.button_basic_cropping_submit_event)
        self.main_button_basic_cropping_submit.grid(row=8, column=0, padx=(40, 40), pady=(10, 0), sticky="nsew")

        #cropping button
        self.main_button_basic_cropping = customtkinter.CTkButton(master=self.tabview.tab("Basic"), fg_color="transparent", text="Crop", border_width=2, text_color=("gray10", "#DCE4EE"), 
                                                                  command=self.button_basic_cropping_event)
        self.main_button_basic_cropping.grid(row=9, column=0, padx=(40, 40), pady=(10, 0), sticky="nsew")

        #flipping title
        self.title_basic_flipping = customtkinter.CTkLabel(self.tabview.tab("Basic"), text="Flipping:", anchor="w")
        self.title_basic_flipping.grid(row=10, column=0, padx=20, pady=(10, 0))

        #flip X button
        self.main_button_basic_flip_x = customtkinter.CTkButton(master=self.tabview.tab("Basic"), fg_color="transparent", text="Flip X", border_width=2, text_color=("gray10", "#DCE4EE"),
                                                                command=self.button_basic_flip_x_event)
        self.main_button_basic_flip_x.grid(row=11, column=0, padx=(50, 50), pady=(0, 10), sticky="nsew")

        #flip Y button
        self.main_button_basic_flip_y = customtkinter.CTkButton(master=self.tabview.tab("Basic"), fg_color="transparent", text="Flip Y", border_width=2, text_color=("gray10", "#DCE4EE"), 
                                                                command=self.button_basic_flip_y_event)
        self.main_button_basic_flip_y.grid(row=12, column=0, padx=(50, 50), pady=(0, 0), sticky="nsew")

        #reset button
        self.main_button_basic_reset = customtkinter.CTkButton(master=self.tabview.tab("Basic"), fg_color="transparent", text="Reset Values", border_width=2, text_color=("gray10", "#DCE4EE"),
                                                               command=self.button_basic_reset_event)
        self.main_button_basic_reset.grid(row=13, column=0, padx=(80, 10), pady=(50, 0), sticky="nsew")



        #configure advanced tab

        #sharpening

        #checkbox sharpening
        self.check_var_advanced_sharp = customtkinter.StringVar(value="off")
        self.checkbox_advanced_sharp = customtkinter.CTkCheckBox(self.tabview.tab("Advanced"), text="   Sharpening", command=self.checkbox_advanced_sharp_event, variable=self.check_var_advanced_sharp, onvalue="on", offvalue="off")
        self.checkbox_advanced_sharp.grid(row=0, column=0, padx=5, pady=(20, 0))


        # Embossing Filter

        #checkbox Embossing Filter
        self.check_var_advanced_emboss = customtkinter.StringVar(value="off")
        self.checkbox_advanced_emboss = customtkinter.CTkCheckBox(self.tabview.tab("Advanced"), text="   Embossing Filter",
                                                                  command=self.checkbox_advanced_emboss_event, 
                                                                  variable=self.check_var_advanced_emboss, onvalue="on", offvalue="off")
        self.checkbox_advanced_emboss.grid(row=1, column=0, padx=5, pady=(20, 0))


        # Point Detection Filter

        #checkbox point detect Filter
        self.check_var_advanced_point = customtkinter.StringVar(value="off")
        self.checkbox_advanced_point = customtkinter.CTkCheckBox(self.tabview.tab("Advanced"), text="  Point Detect Filter", 
                                                                  command=self.checkbox_advanced_point_event, 
                                                                  variable=self.check_var_advanced_point, onvalue="on", offvalue="off")
        self.checkbox_advanced_point.grid(row=2, column=0, padx=5, pady=(20, 0))

        #self.check_var_advanced_pointDetect = customtkinter.StringVar(value="off")
        #self.checkbox_advanced_pointDetect = customtkinter.CTkCheckBox(self.tabview.tab("Advanced"), text="   Point Detect Filter",
                                                                  #command=self.checkbox_advanced_point_event, 
                                                                  #variable=self.check_var_advanced_pointDetect, onvalue="on", offvalue="off")
        #self.checkbox_advanced_emboss.grid(row=2, column=0, padx=5, pady=(20, 0))


        #smoothing

        #checkbox smoothing
        self.check_var_advanced_smooth = customtkinter.StringVar(value="off")
        self.checkbox_advanced_smooth = customtkinter.CTkCheckBox(self.tabview.tab("Advanced"), text="   Smoothing", 
                                                                  command=self.checkbox_advanced_smooth_event, 
                                                                  variable=self.check_var_advanced_smooth, onvalue="on", offvalue="off")
        self.checkbox_advanced_smooth.grid(row=3, column=0, padx=5, pady=(20, 0))

        #slider smoothing 
        self.slider_advanced_smooth = customtkinter.CTkSlider(self.tabview.tab("Advanced"), from_=1, to=101, command=self.slider_advanced_smooth_event)
        self.slider_advanced_smooth.configure(number_of_steps=50)
        self.slider_advanced_smooth.grid(row=4, column=0, padx=5, pady=(20, 0))


        #edge detection

        #checkbox edge detection
        self.check_var_advanced_edges = customtkinter.StringVar(value="off")
        self.checkbox_advanced_edges = customtkinter.CTkCheckBox(self.tabview.tab("Advanced"), text="   Edge Detection", command=self.checkbox_advanced_edges_event, variable=self.check_var_advanced_edges, onvalue="on", offvalue="off")
        self.checkbox_advanced_edges.grid(row=6, column=0, padx=5, pady=(20, 0))

        #slider edge detection
        self.slider_advanced_edges = customtkinter.CTkSlider(self.tabview.tab("Advanced"), from_=0, to=500, command=self.slider_advanced_edges_event)
        self.slider_advanced_edges.configure(number_of_steps=100)
        self.slider_advanced_edges.grid(row=7, column=0, padx=5, pady=(20, 0))

        #checkbox tones
        self.check_var_advanced_tones = customtkinter.StringVar(value="off")
        self.checkbox_advanced_tones = customtkinter.CTkCheckBox(self.tabview.tab("Advanced"), text="   Tones", 
                                                                 command=self.checkbox_advanced_tones_event, 
                                                                 variable=self.check_var_advanced_tones, onvalue="on", offvalue="off")
        self.checkbox_advanced_tones.grid(row=8, column=0, padx=5, pady=(20, 0))

        #slider alpha
        self.slider_advanced_alpha = customtkinter.CTkSlider(self.tabview.tab("Advanced"), from_=1, to=3, command=self.slider_advanced_alpha_event)
        self.slider_advanced_alpha.configure(number_of_steps=2)
        self.slider_advanced_alpha.grid(row=9, column=0, padx=5, pady=(5, 0))

        #slider beta
        self.slider_advanced_beta = customtkinter.CTkSlider(self.tabview.tab("Advanced"), from_=0, to=100, command=self.slider_advanced_beta_event)
        self.slider_advanced_beta.configure(number_of_steps=100)
        self.slider_advanced_beta.grid(row=10, column=0, padx=5, pady=(5, 0))


        #color balancing

        #checkbox HSV
        #self.check_var_advanced_hsv = customtkinter.StringVar(value="off")
        #self.checkbox_advanced_hsv = customtkinter.CTkCheckBox(self.tabview.tab("Advanced"), text="   Color Balancing", 
                                                                 #command=self.checkbox_advanced_hsv_event, 
                                                                 #variable=self.check_var_advanced_hsv, onvalue="on", offvalue="off")
        #self.checkbox_advanced_hsv.grid(row=11, column=0, padx=5, pady=(20, 0))

        #title hue
        #self.title_advanced_hue = customtkinter.CTkLabel(self.tabview.tab("Advanced"), text="Hue:", anchor="w")
        #self.title_advanced_hue.grid(row=12, column=0, padx=(10, 0), pady=(0, 0))

        #slider hue
        #self.slider_advanced_hue = customtkinter.CTkSlider(self.tabview.tab("Advanced"), from_=0, to=100, command=self.slider_advanced_hue_event)
        #self.slider_advanced_hue.configure(number_of_steps=100)
        #self.slider_advanced_hue.grid(row=13, column=0, padx=(5, 0), pady=(0, 5))

        #title saturation
        #self.title_advanced_saturation = customtkinter.CTkLabel(self.tabview.tab("Advanced"), text="Saturation:", anchor="w")
        #self.title_advanced_saturation.grid(row=14, column=0, padx=(10, 0), pady=(0, 0))

        #slider saturation
        #self.slider_advanced_saturation = customtkinter.CTkSlider(self.tabview.tab("Advanced"), from_=0, to=100, command=self.slider_advanced_saturation_event)
        #self.slider_advanced_saturation.configure(number_of_steps=100)
        #self.slider_advanced_saturation.grid(row=15, column=0, padx=(5, 0), pady=(0, 5))

        #title value
        #self.title_advanced_value = customtkinter.CTkLabel(self.tabview.tab("Advanced"), text="Value:", anchor="w")
        #self.title_advanced_value.grid(row=16, column=0, padx=(10, 0), pady=(0, 0))

        #slider value
        #self.slider_advanced_value = customtkinter.CTkSlider(self.tabview.tab("Advanced"), from_=0, to=100, command=self.slider_advanced_value_event)
        #self.slider_advanced_value.configure(number_of_steps=100)
        #self.slider_advanced_value.grid(row=17, column=0, padx=(5, 0), pady=(0, 0))






        #reset button
        self.main_button_basic_reset = customtkinter.CTkButton(master=self.tabview.tab("Advanced"), fg_color="transparent", text="Reset Values", border_width=2, text_color=("gray10", "#DCE4EE"),
                                                               command=self.button_basic_reset_event)
        self.main_button_basic_reset.grid(row=18, column=0, padx=(80, 10), pady=(50, 0), sticky="nsew")












        #configure AI tab

        
        self.label_tab_3 = customtkinter.CTkLabel(self.tabview.tab("AI"), text="This is the AI tab")
        self.label_tab_3.grid(row=0, column=0, padx=20, pady=20)










        # set default values
        
        self.appearance_mode_optionemenu.set("System")


#defining functions

    #open button function
    def sidebar_button_open_event(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.image = cv2.imread(file_path)
            self.image2 = cv2.imread(file_path)
            self.image_out = cv2.imread(file_path)
            self.display_image()
            self.display_image_out()

    def display_image(self):
        if self.image is not None:
            self.image = cv2.resize(self.image, (200, 200))
            self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
            img_pil = Image.fromarray(self.image)
            self.tk_image = ImageTk.PhotoImage(image=img_pil)
            self.image_preview.configure(image=self.tk_image)

    def display_image_out(self):
        if self.image_out is not None:
            self.image_out = cv2.resize(self.image_out, (400, 400))
            self.image_out = cv2.cvtColor(self.image_out, cv2.COLOR_BGR2RGB)
            img_pil_out = Image.fromarray(self.image_out)
            self.tk_image_out = ImageTk.PhotoImage(image=img_pil_out)
            self.image_output.configure(image=self.tk_image_out)


    #save button function
    def sidebar_button_save_event(self, tk_image_out):
        cv2.imwrite('grayscale.jpg',tk_image_out)
        print("Image saved")

    #theme button function
    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

#basic requirements
        
    #color mode menu function
    def basic_color_option(self, basic_color_option): 
        if hasattr(self, 'image'):
            self.grayscale_image = cv2.cvtColor(self.image_out, cv2.COLOR_BGR2GRAY)
            if basic_color_option == "RGB":
                self.rgb_image = cv2.resize(self.image2, (400, 400))
                self.rgb_image= cv2.cvtColor(self.image2, cv2.COLOR_BGR2RGB)
                img_pil_out = Image.fromarray(self.image_out)
                self.tk_image_out = ImageTk.PhotoImage(image=img_pil_out)
                self.image_output.configure(image=self.tk_image_out)
                print("Showing the RGB image")

            elif basic_color_option == "Grayscale":
                img_pil_out = Image.fromarray(self.grayscale_image)
                self.tk_image_out = ImageTk.PhotoImage(image=img_pil_out)
                self.image_output.configure(image=self.tk_image_out)
                print("Showing the Grayscale image")

            elif basic_color_option == "B&W":
                (thresh, BW_image) = cv2.threshold(self.grayscale_image, 127, 255, cv2.THRESH_BINARY)
                img_pil_out = Image.fromarray(BW_image)
                self.tk_image_out = ImageTk.PhotoImage(image=img_pil_out)
                self.image_output.configure(image=self.tk_image_out)
                print("Showing the Black & White image")

        
    #rotate submit button function
    def button_basic_rotate_event(self):
        rotate_value = self.inputBox_basic_rotation.get()
        if rotate_value.isnumeric():
                    rotate_angle = int(rotate_value)
                    rows, cols, _ = self.image_out.shape
                    M = cv2.getRotationMatrix2D((cols / 2, rows / 2), rotate_angle, 1)
                    self.image_out = cv2.warpAffine(self.image_out, M, (cols, rows))
                    img_pil_out = Image.fromarray(self.image_out)
                    self.tk_image_out = ImageTk.PhotoImage(image=img_pil_out)
                    self.image_output.configure(image=self.tk_image_out)
        else:
             tk.messagebox.showerror("Error", "Invalid input. Please enter valid value for rotating angle.")

    #cropping checkbox event
    def checkbox_basic_crop_event(self):
        crop_state = self.check_var_basic_crop.get()
        if hasattr(self, 'image'):
            #x1, x2 = 0, 400
            #y1, y2 = 0, 400
            if crop_state == "on":  
                print("crop checkbox toggled, current value:", self.check_var_basic_crop.get())

            elif crop_state == "off":
                self.rgb_image = cv2.resize(self.image2, (400, 400))
                self.rgb_image= cv2.cvtColor(self.rgb_image, cv2.COLOR_BGR2RGB)
                img_pil_out = Image.fromarray(self.rgb_image)
                self.tk_image_out = ImageTk.PhotoImage(image=img_pil_out)
                self.image_output.configure(image=self.tk_image_out)   

    #cropping submit button function
    def button_basic_cropping_submit_event(self):
        crop_state = self.check_var_basic_crop.get()
        if hasattr(self, 'image'):
            if crop_state == "on":
                crop_value = self.inputBox_basic_cropping.get()
                if crop_value:
                    try:
                        x1 = 0
                        y1 = 0
                        width, height = map(int, crop_value.split())
                        x2, y2 = width, height
                        cv2.rectangle(self.image_out, (x1, y1), (x2, y2), (255, 0, 0), 2)
                        #self.cropped_image = self.image_out[y1:y2, x1:x2]
                        #self.image_out = cv2.resize(self.flipHorizontal, (400, 400))
                        img_pil_out = Image.fromarray(self.image_out)
                        self.tk_image_out = ImageTk.PhotoImage(image=img_pil_out)
                        self.image_output.configure(image=self.tk_image_out)          
                        print("cropping values are, X:", width, " Y:", height)
                    except ValueError:
                        tk.messagebox.showerror("Error", "Invalid input. Please enter valid width and height.")    
            elif crop_state == "off":
                tk.messagebox.showerror("Error", "Turn on cropping.")  


    #cropping button function
    def button_basic_cropping_event(self):
        crop_state = self.check_var_basic_crop.get()
        if hasattr(self, 'image'):
            if crop_state == "on":
                crop_value = self.inputBox_basic_cropping.get()
                if crop_value:
                    try:
                        x1 = 0
                        y1 = 0
                        width, height = map(int, crop_value.split())
                        x2, y2 = width, height
                        cv2.rectangle(self.image_out, (x1, y1), (x2, y2), (255, 0, 0), 2)
                        self.cropped_image = self.image_out[y1:y2, x1:x2]
                        #self.image_out = cv2.resize(self.flipHorizontal, (400, 400))
                        img_pil_out = Image.fromarray(self.cropped_image)
                        self.tk_image_out = ImageTk.PhotoImage(image=img_pil_out)
                        self.image_output.configure(image=self.tk_image_out)          
                        print("cropping values are, X:", width, " Y:", height)
                    except ValueError:
                        tk.messagebox.showerror("Error", "Invalid input. Please enter valid width and height.")    
            elif crop_state == "off":
                tk.messagebox.showerror("Error", "Turn on cropping.")  


    #flip x button function
    def button_basic_flip_x_event(self):
        if hasattr(self, 'image'):
            self.flipHorizontal = cv2.flip(self.image_out, 1)
            self.image_out = cv2.resize(self.flipHorizontal, (400, 400))
            img_pil_out = Image.fromarray(self.image_out)
            self.tk_image_out = ImageTk.PhotoImage(image=img_pil_out)
            self.image_output.configure(image=self.tk_image_out)
            print("flipping x")

    #flip y button function
    def button_basic_flip_y_event(self):
        if hasattr(self, 'image'):
            self.flipVertical = cv2.flip(self.image_out, 0)
            self.image_out = cv2.resize(self.flipVertical, (400, 400))
            img_pil_out = Image.fromarray(self.image_out)
            self.tk_image_out = ImageTk.PhotoImage(image=img_pil_out)
            self.image_output.configure(image=self.tk_image_out)
            print("flipping y")


    #reset button function
    def button_basic_reset_event(self):
        if hasattr(self, 'image'):
            self.image_out = cv2.resize(self.image2, (400, 400))
            self.image_out= cv2.cvtColor(self.image_out, cv2.COLOR_BGR2RGB)
            img_pil_out = Image.fromarray(self.image_out)
            self.tk_image_out = ImageTk.PhotoImage(image=img_pil_out)
            self.image_output.configure(image=self.tk_image_out)

            print("reset image")


#Advanced requirements


    #sharpening

    #sharpening checkbox event
    def checkbox_advanced_sharp_event(self):
        
        sharp_state = self.check_var_advanced_sharp.get()
        if hasattr(self, 'image'):
            if sharp_state == "on":
                kernel = np.array([[0, -1, 0],
                                [-1, 5, -1],
                                [0, -1, 0]])
                self.sharpened_image = cv2.cvtColor(self.image_out, cv2.COLOR_BGR2RGB)
                self.sharpened_image = cv2.filter2D(self.sharpened_image, -1, kernel)
                self.sharp_image = cv2.resize(self.sharpened_image, (400, 400))
                self.sharp_image= cv2.cvtColor(self.sharp_image, cv2.COLOR_BGR2RGB)
                img_pil_out = Image.fromarray(self.sharp_image)
                self.tk_image_out = ImageTk.PhotoImage(image=img_pil_out)
                self.image_output.configure(image=self.tk_image_out) 

            elif sharp_state == "off":
                self.rgb_image = cv2.resize(self.image2, (400, 400))
                self.rgb_image= cv2.cvtColor(self.rgb_image, cv2.COLOR_BGR2RGB)
                img_pil_out = Image.fromarray(self.rgb_image)
                self.tk_image_out = ImageTk.PhotoImage(image=img_pil_out)
                self.image_output.configure(image=self.tk_image_out)     
        
        print("sharpeness checkbox toggled, current value:", self.check_var_advanced_sharp.get())

    #sharpening slider event
    def slider_advanced_sharp_event(self, value):
        
        val = int(value)
        kernel = np.array([[0, -1, 0],
                            [-1, 5, -1],
                            [0, -1, 0]])

        self.sharpened_image = cv2.cvtColor(self.image_out, cv2.COLOR_BGR2RGB)
        self.sharpened_image = cv2.filter2D(self.sharpened_image, -1, kernel)
        self.sharp_image = cv2.resize(self.sharpened_image, (400, 400))
        self.sharp_image= cv2.cvtColor(self.sharp_image, cv2.COLOR_BGR2RGB)
        img_pil_out = Image.fromarray(self.sharp_image)
        self.tk_image_out = ImageTk.PhotoImage(image=img_pil_out)
        self.image_output.configure(image=self.tk_image_out) 

        print("sharpness is: ", value)



    #embossing filter

    #Emboss checkbox event
    def checkbox_advanced_emboss_event(self):
        emboss_state = self.check_var_advanced_emboss.get()
        if hasattr(self, 'image'):
            if emboss_state == "on":
                embossing_kernel = np.array([[-2, -1, 0],
                                            [-1, 1, 1],
                                            [0, 1, 2]])
                self.embossed_image = cv2.cvtColor(self.image_out, cv2.COLOR_BGR2RGB)
                self.embossed_image = cv2.filter2D(self.embossed_image, -1, embossing_kernel)
                self.embossed_image = cv2.resize(self.embossed_image, (400, 400))
                self.embossed_image = cv2.cvtColor(self.embossed_image, cv2.COLOR_BGR2RGB)
                img_pil_out = Image.fromarray(self.embossed_image)
                self.tk_image_out = ImageTk.PhotoImage(image=img_pil_out)
                self.image_output.configure(image=self.tk_image_out) 

            elif emboss_state == "off":
                self.rgb_image = cv2.resize(self.image2, (400, 400))
                self.rgb_image= cv2.cvtColor(self.rgb_image, cv2.COLOR_BGR2RGB)
                img_pil_out = Image.fromarray(self.rgb_image)
                self.tk_image_out = ImageTk.PhotoImage(image=img_pil_out)
                self.image_output.configure(image=self.tk_image_out)     


        print("Emboss checkbox toggled, current value:", self.check_var_advanced_emboss.get())



    #feature detection
    def checkbox_advanced_point_event(self):
        point_state = self.check_var_advanced_point.get()
        if hasattr(self, 'image'):
            if point_state == "on":
                self.rgb_image = cv2.cvtColor(self.image_out, cv2.COLOR_BGR2RGB)
                self.gray_image = cv2.cvtColor(self.image_out, cv2.COLOR_BGR2GRAY)
                sift = cv2.SIFT_create()
                keypoints = sift.detect(self.gray_image, None)
                self.sift_image = cv2.drawKeypoints(self.rgb_image, keypoints, None, flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
                self.point_image = cv2.cvtColor(self.sift_image, cv2.COLOR_BGR2RGB)
                self.point_image = cv2.resize(self.point_image, (400, 400))
                img_pil_out = Image.fromarray(self.point_image)
                self.tk_image_out = ImageTk.PhotoImage(image=img_pil_out)
                self.image_output.configure(image=self.tk_image_out) 

            elif point_state == "off":
                self.rgb_image = cv2.resize(self.image2, (400, 400))
                self.rgb_image= cv2.cvtColor(self.rgb_image, cv2.COLOR_BGR2RGB)
                img_pil_out = Image.fromarray(self.rgb_image)
                self.tk_image_out = ImageTk.PhotoImage(image=img_pil_out)
                self.image_output.configure(image=self.tk_image_out)     


        print("point checkbox toggled, current value:", self.check_var_advanced_point.get())




    #smoothness

    #smoothness checkbox event
    def checkbox_advanced_smooth_event(self):
        smooth_state = self.check_var_advanced_smooth.get()
        if hasattr(self, 'image'):
            if smooth_state == "on":
                self.smoothed_image = cv2.cvtColor(self.image_out, cv2.COLOR_BGR2RGB)
                self.smoothed_image = cv2.GaussianBlur(self.smoothed_image, (5, 5), 0)
                self.smooth_image = cv2.resize(self.smoothed_image, (400, 400))
                self.smooth_image= cv2.cvtColor(self.smooth_image, cv2.COLOR_BGR2RGB)
                img_pil_out = Image.fromarray(self.smooth_image)
                self.tk_image_out = ImageTk.PhotoImage(image=img_pil_out)
                self.image_output.configure(image=self.tk_image_out) 

            elif smooth_state == "off":
                self.rgb_image = cv2.resize(self.image2, (400, 400))
                self.rgb_image= cv2.cvtColor(self.rgb_image, cv2.COLOR_BGR2RGB)
                img_pil_out = Image.fromarray(self.rgb_image)
                self.tk_image_out = ImageTk.PhotoImage(image=img_pil_out)
                self.image_output.configure(image=self.tk_image_out)    

        print("smoothness checkbox toggled, current value:", self.check_var_advanced_smooth.get())


    #smoothness slider event
    def slider_advanced_smooth_event(self, value):
        if hasattr(self, 'image'):
            smooth_state = self.check_var_advanced_smooth.get()
            if smooth_state == "on":
                smooth_val1 = int(value)
                smooth_val2 = int(value)
                self.smoothed_image = cv2.cvtColor(self.image_out, cv2.COLOR_BGR2RGB)
                self.smoothed_image = cv2.GaussianBlur(self.smoothed_image, (smooth_val1, smooth_val2), 0)
                self.smooth_image = cv2.resize(self.smoothed_image, (400, 400))
                self.smooth_image= cv2.cvtColor(self.smooth_image, cv2.COLOR_BGR2RGB)
                img_pil_out = Image.fromarray(self.smooth_image)
                self.tk_image_out = ImageTk.PhotoImage(image=img_pil_out)
                self.image_output.configure(image=self.tk_image_out) 

            elif smooth_state == "off":
                self.rgb_image = cv2.resize(self.image2, (400, 400))
                self.rgb_image= cv2.cvtColor(self.rgb_image, cv2.COLOR_BGR2RGB)
                img_pil_out = Image.fromarray(self.rgb_image)
                self.tk_image_out = ImageTk.PhotoImage(image=img_pil_out)
                self.image_output.configure(image=self.tk_image_out)  
                 
        print("smoothness is: ", value)


    #edge detection

    #edges checkbox event
    def checkbox_advanced_edges_event(self):
        if hasattr(self, 'image'):
            edge_state = self.check_var_advanced_edges.get()
            if edge_state == "on":
                self.edges_image = cv2.cvtColor(self.image_out, cv2.COLOR_BGR2RGB)
                self.edges_image = cv2.Canny(self.edges_image, 100, 500)
                self.edges_image = cv2.resize(self.edges_image, (400, 400))
                self.edges_image= cv2.cvtColor(self.edges_image, cv2.COLOR_BGR2RGB)
                img_pil_out = Image.fromarray(self.edges_image)
                self.tk_image_out = ImageTk.PhotoImage(image=img_pil_out)
                self.image_output.configure(image=self.tk_image_out) 

            elif edge_state == "off":
                self.rgb_image = cv2.resize(self.image2, (400, 400))
                self.rgb_image= cv2.cvtColor(self.rgb_image, cv2.COLOR_BGR2RGB)
                img_pil_out = Image.fromarray(self.rgb_image)
                self.tk_image_out = ImageTk.PhotoImage(image=img_pil_out)
                self.image_output.configure(image=self.tk_image_out)    

        print("edges checkbox toggled, current value:", self.check_var_advanced_edges.get())

    #edges slider event
    def slider_advanced_edges_event(self, value):
        if hasattr(self, 'image'):
            edge_state = self.check_var_advanced_edges.get()
            if edge_state == "on":

                edge_val = int(value)
                self.edges_image = cv2.cvtColor(self.image_out, cv2.COLOR_BGR2RGB)
                self.edges_image = cv2.Canny(self.edges_image, 100, edge_val)
                self.edges_image = cv2.resize(self.edges_image, (400, 400))
                self.edges_image= cv2.cvtColor(self.edges_image, cv2.COLOR_BGR2RGB)
                img_pil_out = Image.fromarray(self.edges_image)
                self.tk_image_out = ImageTk.PhotoImage(image=img_pil_out)
                self.image_output.configure(image=self.tk_image_out) 

            elif edge_state == "off":
                self.rgb_image = cv2.resize(self.image2, (400, 400))
                self.rgb_image= cv2.cvtColor(self.rgb_image, cv2.COLOR_BGR2RGB)
                img_pil_out = Image.fromarray(self.rgb_image)
                self.tk_image_out = ImageTk.PhotoImage(image=img_pil_out)
                self.image_output.configure(image=self.tk_image_out)    


        print("edge value is: ", value)

#tonal transformation

    #tones checkbox event

    def checkbox_advanced_tones_event(self):
        if hasattr(self, 'image'):
            tone_state = self.check_var_advanced_tones.get()
            if tone_state == "on":
                self.alpha_image = cv2.cvtColor(self.image_out, cv2.COLOR_BGR2RGB)
                self.alpha_image = cv2.convertScaleAbs(self.alpha_image, alpha=2, beta=1)
                self.alpha_image = cv2.resize(self.alpha_image, (400, 400))
                self.alpha_image= cv2.cvtColor(self.alpha_image, cv2.COLOR_BGR2RGB)
                img_pil_out = Image.fromarray(self.alpha_image)
                self.tk_image_out = ImageTk.PhotoImage(image=img_pil_out)
                self.image_output.configure(image=self.tk_image_out) 

            elif tone_state == "off":
                self.rgb_image = cv2.resize(self.image2, (400, 400))
                self.rgb_image= cv2.cvtColor(self.rgb_image, cv2.COLOR_BGR2RGB)
                img_pil_out = Image.fromarray(self.rgb_image)
                self.tk_image_out = ImageTk.PhotoImage(image=img_pil_out)
                self.image_output.configure(image=self.tk_image_out) 

            print("tones checkbox toggled, current value:", self.check_var_advanced_tones.get())


    #tones slider event alpha
      
    def slider_advanced_alpha_event(self, value):
        if hasattr(self, 'image'):
            tone_state = self.check_var_advanced_tones.get()
            if tone_state == "on":
                alpha_val = int(value)
                self.alpha_image = cv2.cvtColor(self.image_out, cv2.COLOR_BGR2RGB)
                self.alpha_image = cv2.convertScaleAbs(self.alpha_image, alpha=alpha_val, beta=1)
                self.alpha_image = cv2.resize(self.alpha_image, (400, 400))
                self.alpha_image= cv2.cvtColor(self.alpha_image, cv2.COLOR_BGR2RGB)
                img_pil_out = Image.fromarray(self.alpha_image)
                self.tk_image_out = ImageTk.PhotoImage(image=img_pil_out)
                self.image_output.configure(image=self.tk_image_out) 

            elif tone_state == "off":
                self.rgb_image = cv2.resize(self.image2, (400, 400))
                self.rgb_image= cv2.cvtColor(self.rgb_image, cv2.COLOR_BGR2RGB)
                img_pil_out = Image.fromarray(self.rgb_image)
                self.tk_image_out = ImageTk.PhotoImage(image=img_pil_out)
                self.image_output.configure(image=self.tk_image_out) 

            print("alpha value is: ", value)


    #tones slider event beta
      
    def slider_advanced_beta_event(self, value):
        if hasattr(self, 'image'):
            tone_state = self.check_var_advanced_tones.get()
            if tone_state == "on":

                beta_val = int(value)
                self.beta_image = cv2.cvtColor(self.image_out, cv2.COLOR_BGR2RGB)
                self.beta_image = cv2.convertScaleAbs(self.beta_image, alpha=1 , beta=beta_val)
                self.beta_image = cv2.resize(self.beta_image, (400, 400))
                self.beta_image= cv2.cvtColor(self.beta_image, cv2.COLOR_BGR2RGB)
                img_pil_out = Image.fromarray(self.beta_image)
                self.tk_image_out = ImageTk.PhotoImage(image=img_pil_out)
                self.image_output.configure(image=self.tk_image_out) 

            elif tone_state == "off":
                self.rgb_image = cv2.resize(self.image2, (400, 400))
                self.rgb_image= cv2.cvtColor(self.rgb_image, cv2.COLOR_BGR2RGB)
                img_pil_out = Image.fromarray(self.rgb_image)
                self.tk_image_out = ImageTk.PhotoImage(image=img_pil_out)
                self.image_output.configure(image=self.tk_image_out) 

            print("beta value is: ", value)

#color transformation

    #HSV checkbox event

    def checkbox_advanced_hsv_event(self):
        if hasattr(self, 'image'):
            tone_state = self.check_var_advanced_tones.get()
            if tone_state == "on":
                print("HSV checkbox toggled, current value:", self.check_var_advanced_hsv.get())

            elif tone_state == "off":
                self.rgb_image = cv2.resize(self.image2, (400, 400))
                self.rgb_image= cv2.cvtColor(self.rgb_image, cv2.COLOR_BGR2RGB)
                img_pil_out = Image.fromarray(self.rgb_image)
                self.tk_image_out = ImageTk.PhotoImage(image=img_pil_out)
                self.image_output.configure(image=self.tk_image_out) 

                print("HSV checkbox toggled, current value:", self.check_var_advanced_hsv.get())

    #hue slider event
    def slider_advanced_hue_event(self, value):
        if hasattr(self, 'image'):
            #hsv_state = self.check_var_advanced_hsv.get()

            #if hsv_state == "on":

                #hue_val = int(value)

                #self.hue_image = cv2.cvtColor(self.image_out, cv2.COLOR_BGR2RGB)

                #self.hue_image = self.image_out.convert('HSV')

                #self.hue_image - ImageEnhance.Color(img_hsv).enhance(saturation)

                # Adjust the color based on the values
                #self.hue_image = 


                #img_hsv = ImageEnhance.Brightness(img_hsv).enhance(lightness)
                #img_hsv = ImageEnhance.Contrast(img_hsv).enhance(lightness)

                #self.hue_image = cv2.Canny(self.edges_image, 100, edge_val)

                #self.edges_image = cv2.resize(self.edges_image, (400, 400))
                #self.edges_image= cv2.cvtColor(self.edges_image, cv2.COLOR_BGR2RGB)
                #img_pil_out = Image.fromarray(self.edges_image)
                #self.tk_image_out = ImageTk.PhotoImage(image=img_pil_out)
                #self.image_output.configure(image=self.tk_image_out) 

            #elif hsv_state == "off":

                #self.rgb_image = cv2.resize(self.image2, (400, 400))
                #self.rgb_image= cv2.cvtColor(self.rgb_image, cv2.COLOR_BGR2RGB)
                #img_pil_out = Image.fromarray(self.rgb_image)
                #self.tk_image_out = ImageTk.PhotoImage(image=img_pil_out)
                #self.image_output.configure(image=self.tk_image_out)    


            print("hue value is: ", value)


    #saturation slider event
    def slider_advanced_saturation_event(self, value):
        if hasattr(self, 'image'):
            #hsv_state = self.check_var_advanced_hsv.get()

            #if hsv_state == "on":

                #hue_val = int(value)

                #self.hue_image = cv2.cvtColor(self.image_out, cv2.COLOR_BGR2RGB)

                #self.hue_image = self.image_out.convert('HSV')

                #self.hue_image - ImageEnhance.Color(img_hsv).enhance(saturation)

                # Adjust the color based on the values
                #self.hue_image = 


                #img_hsv = ImageEnhance.Brightness(img_hsv).enhance(lightness)
                #img_hsv = ImageEnhance.Contrast(img_hsv).enhance(lightness)

                #self.hue_image = cv2.Canny(self.edges_image, 100, edge_val)

                #self.edges_image = cv2.resize(self.edges_image, (400, 400))
                #self.edges_image= cv2.cvtColor(self.edges_image, cv2.COLOR_BGR2RGB)
                #img_pil_out = Image.fromarray(self.edges_image)
                #self.tk_image_out = ImageTk.PhotoImage(image=img_pil_out)
                #self.image_output.configure(image=self.tk_image_out) 

            #elif hsv_state == "off":

                #self.rgb_image = cv2.resize(self.image2, (400, 400))
                #self.rgb_image= cv2.cvtColor(self.rgb_image, cv2.COLOR_BGR2RGB)
                #img_pil_out = Image.fromarray(self.rgb_image)
                #self.tk_image_out = ImageTk.PhotoImage(image=img_pil_out)
                #self.image_output.configure(image=self.tk_image_out)    


            print("saturation value is: ", value)

    #hue slider event
    def slider_advanced_value_event(self, value):
        if hasattr(self, 'image'):
            #hsv_state = self.check_var_advanced_hsv.get()

            #if hsv_state == "on":

                #hue_val = int(value)

                #self.hue_image = cv2.cvtColor(self.image_out, cv2.COLOR_BGR2RGB)

                #self.hue_image = self.image_out.convert('HSV')

                #self.hue_image - ImageEnhance.Color(img_hsv).enhance(saturation)

                # Adjust the color based on the values
                #self.hue_image = 


                #img_hsv = ImageEnhance.Brightness(img_hsv).enhance(lightness)
                #img_hsv = ImageEnhance.Contrast(img_hsv).enhance(lightness)

                #self.hue_image = cv2.Canny(self.edges_image, 100, edge_val)

                #self.edges_image = cv2.resize(self.edges_image, (400, 400))
                #self.edges_image= cv2.cvtColor(self.edges_image, cv2.COLOR_BGR2RGB)
                #img_pil_out = Image.fromarray(self.edges_image)
                #self.tk_image_out = ImageTk.PhotoImage(image=img_pil_out)
                #self.image_output.configure(image=self.tk_image_out) 

            #elif hsv_state == "off":

                #self.rgb_image = cv2.resize(self.image2, (400, 400))
                #self.rgb_image= cv2.cvtColor(self.rgb_image, cv2.COLOR_BGR2RGB)
                #img_pil_out = Image.fromarray(self.rgb_image)
                #self.tk_image_out = ImageTk.PhotoImage(image=img_pil_out)
                #self.image_output.configure(image=self.tk_image_out)    


            print("Value value is: ", value)









    #filter type menu function
    def advanced_filterType_option(self, advanced_filterType):
        print("optionmenu dropdown clicked:", advanced_filterType)  

    #filter apply button function
    def button_advanced_filterApply_event(self):
        filter_value = self.inputBox_advanced_filterValue.get()
        if filter_value.isnumeric():
                    filter_val = filter_value
                    print("filter value is", filter_val)
        else:
             tk.messagebox.showerror("Error", "Invalid input. Please enter valid value for the filter value.")

 

    def open_input_dialog_event(self):
        dialog = customtkinter.CTkInputDialog(text="Type in a number:", title="CTkInputDialog")
        print("CTkInputDialog:", dialog.get_input())


    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)



    def sidebar_button_event(self):
        print("sidebar_button click")

#AI requirements







if __name__ == "__main__":
    app = App()
    app.mainloop()