import os, time
import numpy as np
from PIL import Image


ascii_chars = [' ','.', '-','•', ':', '=', '+','*',"░", '%',"#",'@',"▒", "▓","█","x"]

ascii_chars2 = [" ", ':',"░","▒","▓","█"]
ascii_chars1 = [" ","▓","█"]


# Define the size of the ASCII art
ascii_width = 40
ascii_height = 28




for root, dirs, files in os.walk('number_dataset'):
    for filename in files:
        print(filename)
                
        # Load image
        try:
            old_path = os.path.join(root, filename)
            img = Image.open(old_path)

            # Preprocess image
            img = img.resize((40, 28))  # Resize to the required input size
            img = np.array(img.convert('L')) / 255.0  # Convert to grayscale and normalize pixel values

            
            #frame = cv2.resize(img, (ascii_width, ascii_height))
            #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)


            ascii_image = ""
            for y in range(ascii_height):
                for x in range(ascii_width):
                    pixel = img[y][x]
                    char_index = int((pixel) * (len(ascii_chars1)-1))
                    ascii_image += ascii_chars1[char_index]
                ascii_image += "\n"
            print(ascii_image)
            time.sleep(0.1)



                
        except Exception as error:
           # handle the exception
           print("An exception occurred:", error)



