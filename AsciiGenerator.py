import os
import json
import threading
import tkinter as tk
from PIL import Image

class ASCIIGENERATOR:
    def __init__(self) -> None:
        self.image_path = None
        self.img = None
        self.output = ""

    def generate(self, image_path, char_set="large", background_color="black"):
        self.image_path = image_path
        self.background_color = background_color

        try:
            self.img = Image.open(image_path).convert('L')
        except Exception as e:
            OutputLog.log(f"Failed to open image: {e}")
            return
        
        pixels = self.img.load()
        width, height = self.img.size

        OutputLog.log(f"Using AsciiGenerator by AlexDM")
        OutputLog.log(f"Starting conversion of {self.image_path}, using charset {char_set}")
        OutputLog.log(f"Image size: {width}x{height}")
        
        all_pixels = []
        for x in range(width):
            for y in range(height):
                cpixel = pixels[x, y]
                all_pixels.append(cpixel)

                # OutputLog.log(f"Retrieved pixel's brightness value at {x}, {y}")
        
        self.output = ""
        for y in range(height):
            for x in range(width):
                with open(f'assets/charsets/{char_set}.json', "r") as f:
                    chars = json.load(f)["chars"]
                    # if self.background_color == "white":
                    #     chars = chars[::-1]
                
                cpixel = pixels[x, y]
                clamp = round(300 / len(chars))
                
                char = round(cpixel / clamp) * clamp
                char = chars[int(char / clamp)]
                
                self.output = f'{self.output}{char * 2}'

                # OutputLog.log(f"Selected char: {char} at {x}, {y}")
                
            self.output = f'{self.output}\n'

        self.export()

    def export(self, path=None):
        if path is None:
            output_dir = output_path.entry.get()
            filename = os.path.basename(self.image_path) + "-ascii.asciiart"
            path = os.path.join(output_dir, filename)
            
        with open(path, 'w') as f:
            f.write(self.output)

        OutputLog.log(f"Successfully converted the image! {path}")

ascii_generator = ASCIIGENERATOR()


root = tk.Tk()
root.geometry("300x350")
root.title("Ascii Generator")

icon = tk.PhotoImage(file="assets/icon.png")
root.iconphoto(False, icon)

class TextEntry:
    def __init__(self, text, row=0):
        self.text = text

        self.label = tk.Label(root, text=self.text)
        self.label.grid(row=row, padx=10, pady=10)

        self.entry = tk.Entry(root)
        self.entry.grid(row=row, column=1, padx=10, pady=10)

class List:
    def __init__(self, text, texts, row=0):
        self.text = text

        self.label = tk.Label(root, text=self.text)
        self.label.grid(row=row, padx=10, pady=10)
        
        self.list = tk.Listbox(root)
        for text in texts:
            self.list.insert(tk.END, text)
        self.list.grid(row=row, column=1, padx=10, pady=10)
        

class OUTPUTLOG:
    def __init__(self, row=0):
        self.text = tk.Text(root)
        self.text.config(width=35, height=7)
        self.text.grid(row=row, column=0, columnspan=2, padx=10, pady=10)
    
    def log(self, text):
        self.text.insert(tk.END, text)
        self.text.insert(tk.END, '\n')
OutputLog = OUTPUTLOG(4)


path = TextEntry("Image path")

output_path = TextEntry("Output path", row=1)
output_path.entry.insert(0, os.path.join(os.path.expanduser("~"), "Downloads"))


char_sets = os.listdir("assets/charsets")
char_sets = [os.path.splitext(file)[0] for file in os.listdir("assets/charsets")]
char_select = List("Charset", char_sets, row=2)
char_select.list.config(height=3)


generate = tk.Button(root, text="Generate", command=lambda: generate())
generate.grid(row=3, padx=10, pady=10)


def generate():
    OutputLog.text.delete(1.0, tk.END)
    
    image_path = path.entry.get()
    
    selected_index = char_select.list.curselection()
    if not selected_index:
        OutputLog.log("No charset selected.")
        return
    
    char_set = char_select.list.get(char_select.list.curselection())

    OutputLog.log(f"Generating ascii art from path: {image_path}")
    OutputLog.log(f"Using charset: {char_set}")

    thread = threading.Thread(target=ascii_generator.generate, args=(image_path, char_set))
    thread.daemon = True
    thread.start()

root.mainloop()