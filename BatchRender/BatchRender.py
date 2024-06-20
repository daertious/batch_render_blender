import os
import subprocess
import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image
import sys


ctk.set_appearance_mode("Dark")  # Modes: system (default), light, dark
ctk.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

if getattr(sys, 'frozen', False):
    import pyi_splash


class BlenderRenderApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("BATCH RENDER - BLENDER")
        self.geometry("600x800")
        self.resizable(False, True)
        icon_path = os.path.join(os.path.dirname(__file__), "data", "img", "logo.ico")
        if os.path.exists(icon_path):
            self.iconbitmap(icon_path)

        self.blender_path = ctk.StringVar()
        self.scenes = []
        self.scene_widgets = []

        self.create_widgets()

    def create_widgets(self):
        image_path = os.path.join(os.path.dirname(__file__), "data", "img", "logo.png")
        if os.path.exists(image_path):
            self.planetarium_image = ctk.CTkImage(Image.open(image_path), size=(230, 150))

        image_render_path = os.path.join(os.path.dirname(__file__), "data", "img", "render_image.png")
        if os.path.exists(image_path):
            self.render_image = ctk.CTkImage(Image.open(image_render_path), size=(32, 32))

        label_image = ctk.CTkLabel(self, image=self.planetarium_image, text="")
        label_image.pack(side="top", pady=(0, 0))

        main_frame = ctk.CTkFrame(self)
        main_frame.pack(padx=20, pady=20, fill='both', expand=True)

        sidebar_frame = ctk.CTkFrame(main_frame, width=200)
        sidebar_frame.pack(side="left", fill='y', padx=20, pady=20)
        

        self.content_frame = ctk.CTkFrame(main_frame)
        self.content_frame.pack(side="right", fill='both', expand=True)

        self.render_button = ctk.CTkButton(sidebar_frame, text="Render", command=lambda: self.show_frame(self.render_frame), image=self.render_image, anchor="w")
        self.render_button.pack(pady=10, padx=10)

        self.render_frame = ctk.CTkFrame(self.content_frame)

        self.create_render_frame()

        self.render_frame.pack(fill='both', expand=True)

    def create_render_frame(self):
        render_notebook = ctk.CTkTabview(self.render_frame)
        render_notebook.pack(fill='both', expand=True)

        rendering_frame = render_notebook.add("Render")

        rendering_label = ctk.CTkLabel(rendering_frame, text="Render", font=ctk.CTkFont("Montserrat", 15))
        rendering_label.pack(padx=20, pady=20)

        ctk.CTkLabel(rendering_frame, text="The path to Blender: ", font=ctk.CTkFont("Montserrat")).pack(pady=5, padx=5, anchor="w")
        ctk.CTkButton(rendering_frame, text="Browse", command=self.select_blender_path, font=ctk.CTkFont("Montserrat")).pack(pady=5, padx=5, anchor="w")

        self.blender_path_label = ctk.CTkLabel(rendering_frame, text="")
        self.blender_path_label.pack(pady=5, padx=5, anchor="w")

        ctk.CTkButton(rendering_frame, text="Add a scene", command=self.add_scene, width=15, font=ctk.CTkFont("Montserrat")).pack(pady=5, padx=5, anchor="w")

        self.scene_frame = ctk.CTkFrame(rendering_frame)
        self.scene_frame.pack(fill='both', expand=True)

        ctk.CTkButton(rendering_frame, text="Render", command=self.render, fg_color="light green", text_color="black", width=1000, font=ctk.CTkFont("Montserrat", 15)).pack(pady=10, padx=10, anchor="w")

        tutorial_frame = render_notebook.add("Guide")

        tutorial_label = ctk.CTkLabel(tutorial_frame, text="Guide", font=ctk.CTkFont("Montserrat", 15))
        tutorial_label.pack(padx=10, pady=10)
        tutorial_label2 = ctk.CTkLabel(tutorial_frame, text="1) Select the path to blender.exe\n by clicking the Browse button", font=ctk.CTkFont("Montserrat", 12))
        tutorial_label2.pack(padx=5, pady=5)
        tutorial_label3 = ctk.CTkLabel(tutorial_frame, text="2) Select the scene's .blend files\n to add it to the render queue", font=ctk.CTkFont("Montserrat", 12))
        tutorial_label3.pack(padx=5, pady=5)
        tutorial_label4 = ctk.CTkLabel(tutorial_frame, text="3) Click the Render button", font=ctk.CTkFont("Montserrat", 12))
        tutorial_label4.pack(padx=5, pady=5)
        tutorial_label5 = ctk.CTkLabel(tutorial_frame, text="If the render is error-free,\n the scene name will be green.", font=ctk.CTkFont("Montserrat", 12))
        tutorial_label5.pack(padx=5, pady=5)
        tutorial_label6 = ctk.CTkLabel(tutorial_frame, text="If the render failed,\n the scene name will be in red.", font=ctk.CTkFont("Montserrat", 12))
        tutorial_label6.pack(padx=5, pady=5, fill="both")

    def show_frame(self, frame):
        for child in self.content_frame.winfo_children():
            child.pack_forget()
        frame.pack(fill='both', expand=True)

    def select_blender_path(self):
        self.blender_path.set(filedialog.askdirectory())
        self.blender_path_label.configure(text=self.blender_path.get())

    def add_scene(self):
        scene_file = filedialog.askopenfilename(filetypes=[("Blender files", "*.blend")])
        if scene_file:
            self.scenes.append(scene_file)
            scene_label = ctk.CTkLabel(self.scene_frame, text=os.path.basename(scene_file), font=ctk.CTkFont("Montserrat"))
            scene_label.pack(padx=10,anchor="n")
            remove_button = ctk.CTkButton(self.scene_frame, text="Remove", command=lambda: self.remove_scene(scene_label), fg_color="red", text_color="white", font=ctk.CTkFont("Montserrat"))
            remove_button.pack(padx=10,anchor="n")
            self.scene_widgets.append((scene_label, remove_button))

    def remove_scene(self, scene_label):
        index = None
        for i, (label, _) in enumerate(self.scene_widgets):
            if label == scene_label:
                index = i
                break
        if index is not None:
            del self.scenes[index]
            scene_label.pack_forget()
            scene_label.destroy()
            self.scene_widgets[index][1].pack_forget()
            self.scene_widgets[index][1].destroy()
            del self.scene_widgets[index]

    def render(self):
        blender_path = self.blender_path.get()
        if not os.path.isdir(blender_path):
            print("The path to Blender is not valid.")
            return

        blender_executable = os.path.join(blender_path, "blender.exe")
        if not os.path.isfile(blender_executable):
            print("Blender .exe was not found.")
            return

        for i, scene_file in enumerate(self.scenes, start=1):
            if not os.path.isfile(scene_file):
                print(f"Scene file {i} not found: {scene_file}")
                continue

            try:
                subprocess.run([blender_executable, "-b", scene_file, "-a"], check=True, creationflags=subprocess.CREATE_NEW_CONSOLE)
                self.scene_widgets[i - 1][0].configure(text_color="green")
            except subprocess.CalledProcessError:
                self.scene_widgets[i - 1][0].configure(text_color="red")

    #SPLASH
    if getattr(sys, 'frozen', False):
        pyi_splash.close()
    #SPLASH

if __name__ == "__main__":
    app = BlenderRenderApp()

    #SPLASH
    if getattr(sys, 'frozen', False):
        pyi_splash.close()
    #SPLASH

    app.mainloop()
