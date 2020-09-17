from tkinter import *
from PIL import ImageTk, Image
from os import listdir, path
from os.path import isfile, join
import re

# update img_list to img_path_list
# only store the paths of the images in that list
# in update_image take the path from the list and turn it into a photo object, then call resize_image and display it
# change all instances of img_list
# change initial definiton of image_label to be taken care of by update_image
# add resizing buttons

path = path.dirname(path.realpath(__file__))
icon = "/cat-grumpy-icon.png"

# set up the root
root = Tk()
root.title("Cat Viewer")
root.iconphoto(False, PhotoImage(file= path + "/" + icon))
root.geometry("+500+200")

# set image scale
image_size = 600

accepted_image_formats = [
"png",
"jpg",
"jpeg",
"gif",
]

# set up the list of images and add all accepted image files contained in the image folder
img_path_list = []
image_folder_path = "/Users/michael/Desktop/Documents/misc/cats"
# list will contain only files found in the image folder
image_folder_files = [f for f in listdir(image_folder_path) if isfile(join(image_folder_path, f))]
# regex to match file extension names
p = re.compile("\.\w*$")
# add image to img_path_list if its file extension is in accepted_image_formats
for f in image_folder_files:
	result = p.search(f)
	if result.group(0)[1:] in accepted_image_formats:
		img_path_list.append(join(image_folder_path, f))

# global variable containing the current image index
image_index = 0


# define the buttons functions
def update_status():
	global status_label
	global image_index

	try:
		status_label.grid_forget()
	except NameError:
		pass

	status_label = Label(text="Cat {} of {}  ".format(image_index + 1, len(image_folder_files) - 1), pady=5, bd=1, relief=SUNKEN, anchor=E)
	status_label.grid(row=2, column = 0, columnspan=5, sticky=W+E)


def update_image():
	global image_label
	global img_path_list
	global image_size
	global image_index

	try:
		image_label.grid_forget()
	except NameError:
		pass

	image = Image.open(img_path_list[image_index])
	image = image.resize((image_size, image_size), Image.ANTIALIAS)
	image = ImageTk.PhotoImage(image)

	image_label = Label(root, image=image)
	image_label.photo = image
	image_label.grid(row=0, column=0, columnspan=5)


def back():
	global image_index

	button_forward.config(state=ACTIVE)

	image_index -= 1
	if image_index == 0:
		button_back.config(state=DISABLED)
	
	update_image()
	update_status()


def forward():
	global image_index

	button_back.config(state=ACTIVE)

	image_index += 1
	if image_index == len(img_path_list) - 1:
		button_forward.config(state=DISABLED)
	
	update_image()
	update_status()


def bigger():
	global image_size

	button_smaller.config(state=ACTIVE)

	if image_size >= 800:
		button_bigger.config(state=DISABLED)
	image_size += 100

	update_image()


def smaller():
	global image_size

	button_bigger.config(state=ACTIVE)

	if image_size <= 300:
		button_smaller.config(state=DISABLED)
	image_size -= 100

	update_image()


# define the buttons
button_back    = Button(root, padx=30, pady=10, text="<< Last Cat", command=back, state=DISABLED)
button_forward = Button(root, padx=30, pady=10, text="Next Cat >>", command=forward)
button_quit    = Button(root, padx=10, pady=10, text="Goodbye Cats", command=root.quit)
button_bigger  = Button(root, padx=10, pady=10, text="Bigger Cats", command=bigger)
button_smaller = Button(root, padx=10, pady=10, text="Smaller Cats", command=smaller)

# place the buttons on the grid
button_back.grid(row=1, column=0)
button_forward.grid(row=1, column=4)
button_quit.grid(row=1, column=2)
button_bigger.grid(row=1, column=3)
button_smaller.grid(row=1, column=1)

# place the first image on the screen initially
update_image()
# place the status bar on the screen intially
update_status()


root.mainloop()
