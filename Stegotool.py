import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from PIL import Image


def encode_message():
    file_path = filedialog.askopenfilename(title="Select Image", filetypes=[("PNG files", "*.png")])
    if not file_path:
        return

    def save_encoded_image():
        message = entry_message.get()
        if not message:
            messagebox.showerror("Error", "Message cannot be empty!")
            return

        img = Image.open(file_path)
        encoded_img = img.copy()
        pixels = encoded_img.load()

        binary_message = ''.join(format(ord(char), '08b') for char in message) + '1111111111111110'  # End marker
        width, height = img.size
        idx = 0

        for y in range(height):
            for x in range(width):
                if idx < len(binary_message):
                    r, g, b = pixels[x, y]
                    r = (r & ~1) | int(binary_message[idx])  # Modify LSB of red channel
                    pixels[x, y] = (r, g, b)
                    idx += 1

        save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
        if save_path:
            encoded_img.save(save_path)
            messagebox.showinfo("Success", "Message encoded and image saved!")

    encode_window = tk.Toplevel(root)
    encode_window.title("Encode Message")
    encode_window.geometry("400x150")
    encode_window.resizable(False, False)

    tk.Label(encode_window, text="Enter Message to Encode:", font=("Arial", 12)).pack(pady=10)
    entry_message = ttk.Entry(encode_window, width=50)
    entry_message.pack(pady=5)
    ttk.Button(encode_window, text="Save Encoded Image", command=save_encoded_image).pack(pady=10)


def decode_message():
    file_path = filedialog.askopenfilename(title="Select Image", filetypes=[("PNG files", "*.png")])
    if not file_path:
        return

    img = Image.open(file_path)
    pixels = img.load()

    binary_message = ""
    width, height = img.size

    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]
            binary_message += str(r & 1)  # Get LSB of red channel

            if binary_message[-16:] == '1111111111111110':  # End marker
                break
        else:
            continue
        break

    decoded_message = ''.join(chr(int(binary_message[i:i+8], 2)) for i in range(0, len(binary_message) - 16, 8))
    messagebox.showinfo("Decoded Message", f"Message: {decoded_message}")


# Main Tkinter window
root = tk.Tk()
root.title("Steganography Tool")
root.geometry("400x250")
root.resizable(False, False)

# Styling
style = ttk.Style()
style.configure("TButton", font=("Arial", 12), padding=5)
style.configure("TLabel", font=("Arial", 14))

# Main Frame
frame = ttk.Frame(root, padding=20)
frame.pack(fill="both", expand=True)

# UI Components
ttk.Label(frame, text="Steganography Tool", font=("Arial Bold", 16)).pack(pady=10)

ttk.Button(frame, text="Encode Message", width=25, command=encode_message).pack(pady=10)
ttk.Button(frame, text="Decode Message", width=25, command=decode_message).pack(pady=10)

ttk.Label(frame, text="Created with ❤️ by RushiMalve", font=("Arial", 10)).pack(side="bottom", pady=10)

root.mainloop()
