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
        self.sidebar_button_save = customtkinter.CTkButton(self.sidebar_frame, text="Save", 
                                                           command=self.sidebar_button_save_event)
        self.sidebar_button_save.grid(row=2, column=0, padx=20, pady=10)


        #theme dropdown

        #theme title
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Theme:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))

        #theme menu
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"], 
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))


        #default button architecture
        #def button_event():
        # print("button pressed")
        #button = customtkinter.CTkButton(app,  command=button_event)

        #button 3
        #self.sidebar_button_3 = customtkinter.CTkButton(self.sidebar_frame, command=self.sidebar_button_event)
        #self.sidebar_button_3.grid(row=3, column=0, padx=20, pady=10)

        #scale dropdown list
        #self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        #self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        #self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],
                                                               #command=self.change_scaling_event)
        #self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))

        # create main entry and button
        #self.entry = customtkinter.CTkEntry(self, placeholder_text="CTkEntry")
        #self.entry.grid(row=3, column=1, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew")

        #self.main_button_1 = customtkinter.CTkButton(master=self, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"))
        #self.main_button_1.grid(row=3, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew")







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

        #cropping title
        self.title_basic_cropping = customtkinter.CTkLabel(self.tabview.tab("Basic"), text="Cropping:", anchor="w")
        self.title_basic_cropping.grid(row=6, column=0, padx=20, pady=(10, 0))

        #cropping input box
        self.inputBox_basic_cropping = customtkinter.CTkEntry(self.tabview.tab("Basic"), 
                                                              placeholder_text="Enter Value (X Y)")
        self.inputBox_basic_cropping.grid(row=7, column=0, padx=(20, 20), pady=(0, 0), sticky="nsew")

        #cropping submit button
        self.main_button_basic_cropping = customtkinter.CTkButton(master=self.tabview.tab("Basic"), fg_color="transparent", text="Crop", border_width=2, text_color=("gray10", "#DCE4EE"), 
                                                                  command=self.button_basic_cropping_event)
        self.main_button_basic_cropping.grid(row=8, column=0, padx=(40, 40), pady=(10, 0), sticky="nsew")

        #flipping title
        self.title_basic_flipping = customtkinter.CTkLabel(self.tabview.tab("Basic"), text="Flipping:", anchor="w")
        self.title_basic_flipping.grid(row=9, column=0, padx=20, pady=(10, 0))

        #flip X button
        self.main_button_basic_flip_x = customtkinter.CTkButton(master=self.tabview.tab("Basic"), fg_color="transparent", text="Flip X", border_width=2, text_color=("gray10", "#DCE4EE"),
                                                                command=self.button_basic_flip_x_event)
        self.main_button_basic_flip_x.grid(row=10, column=0, padx=(50, 50), pady=(0, 10), sticky="nsew")

        #flip Y button
        self.main_button_basic_flip_y = customtkinter.CTkButton(master=self.tabview.tab("Basic"), fg_color="transparent", text="Flip Y", border_width=2, text_color=("gray10", "#DCE4EE"), 
                                                                command=self.button_basic_flip_y_event)
        self.main_button_basic_flip_y.grid(row=11, column=0, padx=(50, 50), pady=(0, 0), sticky="nsew")

        #reset button
        self.main_button_basic_reset = customtkinter.CTkButton(master=self.tabview.tab("Basic"), fg_color="transparent", text="Reset Values", border_width=2, text_color=("gray10", "#DCE4EE"),
                                                               command=self.button_basic_reset_event)
        self.main_button_basic_reset.grid(row=12, column=0, padx=(80, 10), pady=(50, 0), sticky="nsew")



        #configure advanced tab


                #configure advanced tab


        #sharpening

        #checkbox sharpening
        self.check_var_advanced_sharp = customtkinter.StringVar(value="off")
        self.checkbox_advanced_sharp = customtkinter.CTkCheckBox(self.tabview.tab("Advanced"), text="   Sharpening", command=self.checkbox_advanced_sharp_event, variable=self.check_var_advanced_sharp, onvalue="on", offvalue="off")
        self.checkbox_advanced_sharp.grid(row=0, column=0, padx=5, pady=(20, 0))

        #slider sharpening
        self.slider_advanced_sharp = customtkinter.CTkSlider(self.tabview.tab("Advanced"), from_=0, to=100, command=self.slider_advanced_sharp_event)
        self.slider_advanced_sharp.configure(number_of_steps=100)
        self.slider_advanced_sharp.grid(row=1, column=0, padx=5, pady=(20, 0))


        #smoothing

        #checkbox smoothing
        self.check_var_advanced_smooth = customtkinter.StringVar(value="off")
        self.checkbox_advanced_smooth = customtkinter.CTkCheckBox(self.tabview.tab("Advanced"), text="   Smoothing", command=self.checkbox_advanced_smooth_event, variable=self.check_var_advanced_smooth, onvalue="on", offvalue="off")
        self.checkbox_advanced_smooth.grid(row=3, column=0, padx=5, pady=(20, 0))

        #slider smoothing 
        self.slider_advanced_smooth = customtkinter.CTkSlider(self.tabview.tab("Advanced"), from_=0, to=100, command=self.slider_advanced_smooth_event)
        self.slider_advanced_smooth.configure(number_of_steps=100)
        self.slider_advanced_smooth.grid(row=4, column=0, padx=5, pady=(20, 0))


        #filter 3

        #checkbox filter 3
        self.check_var_advanced_filter3 = customtkinter.StringVar(value="off")
        self.checkbox_advanced_filter3 = customtkinter.CTkCheckBox(self.tabview.tab("Advanced"), text="   Filter 3", command=self.checkbox_advanced_filter3_event, variable=self.check_var_advanced_filter3, onvalue="on", offvalue="off")
        self.checkbox_advanced_filter3.grid(row=5, column=0, padx=5, pady=(20, 0))

        #slider filter 3
        self.slider_advanced_filter3 = customtkinter.CTkSlider(self.tabview.tab("Advanced"), from_=0, to=100, command=self.slider_advanced_filter3_event)
        self.slider_advanced_filter3.configure(number_of_steps=100)
        self.slider_advanced_filter3.grid(row=6, column=0, padx=5, pady=(20, 0))


        #filter 4

        #checkbox filter 4
        self.check_var_advanced_filter4 = customtkinter.StringVar(value="off")
        self.checkbox_advanced_filter4 = customtkinter.CTkCheckBox(self.tabview.tab("Advanced"), text="   Filter 4", command=self.checkbox_advanced_filter4_event, variable=self.check_var_advanced_filter4, onvalue="on", offvalue="off")
        self.checkbox_advanced_filter4.grid(row=7, column=0, padx=5, pady=(20, 0))

        #slider filter 4
        self.slider_advanced_filter4 = customtkinter.CTkSlider(self.tabview.tab("Advanced"), from_=0, to=100, command=self.slider_advanced_filter4_event)
        self.slider_advanced_filter4.configure(number_of_steps=100)
        self.slider_advanced_filter4.grid(row=8, column=0, padx=5, pady=(20, 0))

        #threshold
        self.button_thresh = customtkinter.CTkButton(master=self.tabview.tab("Advanced"), fg_color="transparent", text="thresh", border_width=2, text_color=("gray10", "#DCE4EE"),
                                                               command=self.button_thresh_event)
        self.button_thresh.grid(row=13, column=0, padx=(80, 10), pady=(50, 0), sticky="nsew")

        #edge detect
        self.button_edge_detect = customtkinter.CTkButton(master=self.tabview.tab("Advanced"), fg_color="transparent", text="edge detect", border_width=2, text_color=("gray10", "#DCE4EE"),
                                                               command=self.button_edge_detect_event)
        self.button_edge_detect.grid(row=14, column=0, padx=(80, 10), pady=(50, 0), sticky="nsew")

         #tonal transform
        self.button_tonal_transform = customtkinter.CTkButton(master=self.tabview.tab("Advanced"), fg_color="transparent", text="tonal transform", border_width=2, text_color=("gray10", "#DCE4EE"),
                                                               command=self.button_tonal_transform_event)
        self.button_tonal_transform.grid(row=14, column=0, padx=(80, 10), pady=(50, 0), sticky="nsew")

        #old code

        #Sharpening title
        #self.title_advanced_filterType = customtkinter.CTkLabel(self.tabview.tab("Advanced"), text="Sharpening", anchor="w")
        #self.title_advanced_filterType.grid(row=0, column=0, padx=20, pady=(10, 0))

        #filter list
        #self.optionmenu_advanced_filterType = customtkinter.CTkOptionMenu(self.tabview.tab("Advanced"), dynamic_resizing=False, values=["Type 1", "Type 2", "Type 3", "Type 4"],
                                                                          #command=self.advanced_filterType_option) #filter type menu function)
        #self.optionmenu_advanced_filterType.grid(row=1, column=0, padx=20, pady=(5,10))

        #filter value input box
        #self.inputBox_advanced_filterValue = customtkinter.CTkEntry(self.tabview.tab("Advanced"), placeholder_text="Enter Filter Value")
        #self.inputBox_advanced_filterValue.grid(row=2, column=0, padx=(30, 30), pady=(0, 10), sticky="nsew")

        #filter apply button
        #self.main_button_advanced_filterApply = customtkinter.CTkButton(master=self.tabview.tab("Advanced"), fg_color="transparent", text="Apply Now", border_width=2, text_color=("gray10", "#DCE4EE"),
                                                                        #command=self.button_advanced_filterApply_event)
        #self.main_button_advanced_filterApply.grid(row=3, column=0, padx=(40, 40), pady=(0, 0), sticky="nsew")

        #intensity manipulation title
        #self.title_advanced_intensityManipulation = customtkinter.CTkLabel(self.tabview.tab("Advanced"), text="Intensity Manipulation", anchor="w")
        #self.title_advanced_intensityManipulation.grid(row=4, column=0, padx=20, pady=(20, 0))





        #reset button
        self.main_button_basic_reset = customtkinter.CTkButton(master=self.tabview.tab("Advanced"), fg_color="transparent", text="Reset Values", border_width=2, text_color=("gray10", "#DCE4EE"),
                                                               command=self.button_basic_reset_event)
        self.main_button_basic_reset.grid(row=12, column=0, padx=(80, 10), pady=(50, 0), sticky="nsew")












        #configure AI tab

        
        self.label_tab_3 = customtkinter.CTkLabel(self.tabview.tab("AI"), text="This is the AI tab")
        self.label_tab_3.grid(row=0, column=0, padx=20, pady=20)










        # set default values
        
        self.appearance_mode_optionemenu.set("System")
        #self.sidebar_button_3.configure(state="disabled", text="Disabled CTkButton")
        #self.checkbox_3.configure(state="disabled")
        #self.checkbox_1.select()
        #self.scrollable_frame_switches[0].select()
        #self.scrollable_frame_switches[4].select()
        #self.radio_button_3.configure(state="disabled")
        #self.scaling_optionemenu.set("100%")
        #self.optionmenu_1.set("CTk Option menu")
        #self.combobox_1.set("CTkComboBox")
        #self.slider_1.configure(command=self.progressbar_2.set)
        #self.slider_2.configure(command=self.progressbar_3.set)
        #self.progressbar_1.configure(mode="indeterminnate")
        #self.progressbar_1.start()
        #self.textbox.insert("0.0", "CTkTextbox\n\n" + "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua.\n\n" * 20)
        #self.seg_button_1.configure(values=["CTkSegmentedButton", "Value 2", "Value 3"])
        #self.seg_button_1.set("Value 2")


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


    #cropping submit button function
    def button_basic_cropping_event(self):
            crop_value = self.inputBox_basic_cropping.get()
            if crop_value:
                try:
                    width, height = map(int, crop_value.split())
                    print("cropping values are, X:", width, " Y:", height)
                    #self.image = cv2.resize(self.image, (width, height))
                    #self.display_image()
                except ValueError:
                    tk.messagebox.showerror("Error", "Invalid input. Please enter valid width and height.")

    #flip x button function
    def button_basic_flip_x_event(self):
        self.flipHorizontal = cv2.flip(self.image_out, 1)
        self.image_out = cv2.resize(self.flipHorizontal, (400, 400))
        img_pil_out = Image.fromarray(self.image_out)
        self.tk_image_out = ImageTk.PhotoImage(image=img_pil_out)
        self.image_output.configure(image=self.tk_image_out)
        print("flipping x")

    #flip y button function
    def button_basic_flip_y_event(self):
        self.flipVertical = cv2.flip(self.image_out, 0)
        self.image_out = cv2.resize(self.flipVertical, (400, 400))
        img_pil_out = Image.fromarray(self.image_out)
        self.tk_image_out = ImageTk.PhotoImage(image=img_pil_out)
        self.image_output.configure(image=self.tk_image_out)
        print("flipping y")

    #reset button function
    def button_basic_reset_event(self):
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
        print("sharpeness checkbox toggled, current value:", self.check_var_advanced_sharp.get())

    #sharpening slider event
    def slider_advanced_sharp_event(self, value):
        print("sharpness is: ", value)


    #smoothness

    #smoothness checkbox event
    def checkbox_advanced_smooth_event(self):
        print("smoothness checkbox toggled, current value:", self.check_var_advanced_smooth.get())

    #smoothness slider event
    def slider_advanced_smooth_event(self, value):
        print("smoothness is: ", value)


    #filter 3

    #filter 3 checkbox event
    def checkbox_advanced_filter3_event(self):
        print("filter 3 checkbox toggled, current value:", self.check_var_advanced_filter3.get())

    #filter 3 slider event
    def slider_advanced_filter3_event(self, value):
        print("filter 3 is: ", value)


    #filter 4

    #filter 4 checkbox event
    def checkbox_advanced_filter4_event(self):
        print("filter 4 checkbox toggled, current value:", self.check_var_advanced_filter4.get())

    #filter 4 slider event
    def slider_advanced_filter4_event(self, value):
        print("filter 4 is: ", value)





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

 #threshold button
    def button_thresh_event(self):
        if hasattr(self, 'image'):
            og_image = cv2.cvtColor(self.image, cv2.COLOR_RGB2GRAY)
            _, thresh1 = cv2.threshold(og_image, 127, 255, cv2.THRESH_BINARY)
            self.image_out = thresh1
        self.display_image_out()  # Update the output image display

    #edge detect button
    def button_edge_detect_event(self):
        if hasattr(self, 'image'):
            og_image = cv2.cvtColor(self.image, cv2.COLOR_RGB2GRAY)
            edge_image = cv2.Canny(self.image, 100, 200)
            self.image_out = edge_image
        self.display_image_out()  #Update the output image display

    #tonal transform button
    def button_tonal_transform_event(self):
        if hasattr(self, 'image'):
         alpha = simpledialog.askfloat("Tonal Transform", "Enter alpha value:")
         beta = simpledialog.askinteger("Tonal Transform", "Enter beta value:")
        
        if alpha is not None and beta is not None:
            og_image = cv2.convertScaleAbs(self.image, alpha=alpha, beta=beta)
            self.image_out=og_image
            self.display_image_out()

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