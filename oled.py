# import time
# import subprocess
# from luma.core.interface.serial import i2c
# from luma.oled.device import sh1106
# from PIL import Image, ImageDraw, ImageFont

# # Create the I2C interface and initialize the SH1106 OLED display
# serial = i2c(port=1, address=0x3C)  # Adjust address if necessary
# device = sh1106(serial)

# # Clear display
# device.clear()

# # Create blank image for drawing
# width = device.width
# height = device.height
# image = Image.new("1", (width, height))

# # Get drawing object to draw on image
# draw = ImageDraw.Draw(image)

# # Define constants for line spacing
# padding = -2
# line_spacing = 10  # Space between lines of text

# top = padding
# bottom = height - padding

# # Load default font
# font = ImageFont.load_default()

# def get_printer_status():
#     try:
#         # Check the status of the printer
#         cmd = "lpstat -p"
#         result = subprocess.check_output(cmd, shell=True).decode("utf-8").strip()

#         # Process the result to determine printer status
#         if "disabled" in result.lower() or "unplugged" in result.lower():
#             return "Printer Disabled/Unplugged"
#         if "idle" in result.lower():
#             return "Printer Connected"
#         if "Rendering completed" in result.lower():
#             return "Rendering completed"
#         return "Printer Status Unknown"
#     except subprocess.CalledProcessError:
#         return "Error Checking Printer"

# while True:
#     # Draw a black filled box to clear the image
#     draw.rectangle((0, 0, width, height), outline=0, fill=0)

#     # Shell scripts for system monitoring
#     cmd = "hostname -I | cut -d' ' -f1"
#     IP = subprocess.check_output(cmd, shell=True).decode("utf-8").strip()
#     cmd = "top -bn1 | grep load | awk '{printf \"CPU Load: %.2f\", $(NF-2)}'"
#     CPU = subprocess.check_output(cmd, shell=True).decode("utf-8").strip()
#     cmd = "free -m | awk 'NR==2{printf \"Mem: %s/%sMB %.2f%%\", $3,$2,$3*100/$2 }'"
#     MemUsage = subprocess.check_output(cmd, shell=True).decode("utf-8").strip()
#     cmd = "df -h | awk '$NF==\"/\"{printf \"Disk: %d/%dGB %s\", $3,$2,$5}'"
#     Disk = subprocess.check_output(cmd, shell=True).decode("utf-8").strip()
#     cmd = "vcgencmd measure_temp | cut -f 2 -d '='"
#     temp = subprocess.check_output(cmd, shell=True).decode("utf-8").strip()

#     # Get printer status
#     printer_status = get_printer_status()

#     # Write lines of text with increased spacing
#     draw.text((0, top), "IP: " + IP, font=font, fill=255)
#     draw.text((0, top + line_spacing), str(CPU) + " " + str(temp), font=font, fill=255)
#     draw.text((0, top + 2 * line_spacing), str(MemUsage), font=font, fill=255)
#     draw.text((0, top + 3 * line_spacing), str(Disk), font=font, fill=255)
#     draw.text((0, top + 4 * line_spacing), "Printer Status:", font=font, fill=255)
#     draw.text((0, top + 5 * line_spacing), printer_status, font=font, fill=255)

#     # Display image
#     device.display(image)
#     time.sleep(2)  # Update every 10 seconds
import time
import subprocess
from luma.core.interface.serial import i2c
from luma.oled.device import sh1106
from PIL import Image, ImageDraw, ImageFont

# Create the I2C interface and initialize the SH1106 OLED display
serial = i2c(port=1, address=0x3C)  # Adjust address if necessary
device = sh1106(serial)

# Clear display
device.clear()

# Create blank image for drawing
width = device.width
height = device.height
image = Image.new("1", (width, height))

# Get drawing object to draw on image
draw = ImageDraw.Draw(image)

# Define constants for line spacing
padding = -2
line_spacing = 10  # Space between lines of text

top = padding
bottom = height - padding

# Load default fonts
font_large = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 24)
font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 10)

def get_printer_status():
    try:
        # Check the status of the printer
        cmd = "lpstat -p"
        result = subprocess.check_output(cmd, shell=True).decode("utf-8").strip()

        # Process the result to determine printer status
        if "disabled" in result.lower() or "unplugged" in result.lower():
            return "Printer Disabled/Unplugged"
        if "idle" in result.lower():
            return "Printer Connected"
        if "Rendering completed" in result.lower():
            return "Rendering completed"
        return "Printer Status Unknown"
    except subprocess.CalledProcessError:
        return "Error Checking Printer"

def display_logo():
    # Show "KSP ELECTRONICS" logo text during boot
    draw.rectangle((0, 0, width, height), outline=0, fill=0)

    # Define the text
    ksp_text = "KSP"
    electronics_text = "ELECTRONICS"

    # Calculate text size and position for "KSP"
    ksp_text_bbox = draw.textbbox((0, 0), ksp_text, font=font_large)
    ksp_text_width = ksp_text_bbox[2] - ksp_text_bbox[0]
    ksp_text_height = ksp_text_bbox[3] - ksp_text_bbox[1]
    ksp_text_x = (width - ksp_text_width) / 2
    ksp_text_y = (height - ksp_text_height) / 2 - 10  # Centered with slight adjustment

    # Draw "KSP" in large font
    draw.text((ksp_text_x, ksp_text_y), ksp_text, font=font_large, fill=255)

    # Calculate text size and position for "ELECTRONICS"
    electronics_text_bbox = draw.textbbox((0, 0), electronics_text, font=font_small)
    electronics_text_width = electronics_text_bbox[2] - electronics_text_bbox[0]
    electronics_text_height = electronics_text_bbox[3] - electronics_text_bbox[1]
    electronics_text_x = (width - electronics_text_width) / 2
    electronics_text_y = ksp_text_y + ksp_text_height + 5  # Position below "KSP"

    # Draw "ELECTRONICS" in smaller font
    draw.text((electronics_text_x, electronics_text_y), electronics_text, font=font_small, fill=255)

    # Display image
    device.display(image)
    time.sleep(5)  # Display the logo text for 5 seconds

# Display the logo during boot
display_logo()

while True:
    # Draw a black filled box to clear the image
    draw.rectangle((0, 0, width, height), outline=0, fill=0)

    # Shell scripts for system monitoring
    cmd = "hostname -I | cut -d' ' -f1"
    IP = subprocess.check_output(cmd, shell=True).decode("utf-8").strip()
    cmd = "top -bn1 | grep load | awk '{printf \"CPU Load: %.2f\", $(NF-2)}'"
    CPU = subprocess.check_output(cmd, shell=True).decode("utf-8").strip()
    cmd = "free -m | awk 'NR==2{printf \"Mem: %s/%sMB %.2f%%\", $3,$2,$3*100/$2 }'"
    MemUsage = subprocess.check_output(cmd, shell=True).decode("utf-8").strip()
    cmd = "df -h | awk '$NF==\"/\"{printf \"Disk: %d/%dGB %s\", $3,$2,$5}'"
    Disk = subprocess.check_output(cmd, shell=True).decode("utf-8").strip()
    cmd = "vcgencmd measure_temp | cut -f 2 -d '='"
    temp = subprocess.check_output(cmd, shell=True).decode("utf-8").strip()

    # Get printer status
    printer_status = get_printer_status()

    # Write lines of text with increased spacing
    draw.text((0, top), "IP: " + IP, font=font_small, fill=255)
    draw.text((0, top + line_spacing), str(CPU) + " " + str(temp), font=font_small, fill=255)
    draw.text((0, top + 2 * line_spacing), str(MemUsage), font=font_small, fill=255)
    draw.text((0, top + 3 * line_spacing), str(Disk), font=font_small, fill=255)
    draw.text((0, top + 4 * line_spacing), "Printer Status:", font=font_small, fill=255)
    draw.text((0, top + 5 * line_spacing), printer_status, font=font_small, fill=255)

    # Display image
    device.display(image)
    time.sleep(2)  # Update every 2 seconds
