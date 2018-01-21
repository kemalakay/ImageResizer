# Image Resizer
A tool to do batch resizing with your images

### Why?

Often times working with images, I sometimes find myself having resizing multiple images, both at work and at home. Normally, I use Photoshop to do this task as I couldn't find any free alternative to resize images, specifically. However, after a more thorough research, I found [PIL](http://www.pythonware.com/products/pil/). A free Python library to resize images in batches. Regardless, this is still not a very user friendly solution as there are no interfaces to load images or specify directory. 

After talking to a couple of colleagues and friends, we agreed that there is a lack of such free solution on the internet. Certainly, there are many professional tools to handle this process but there is also a necessity to have this kind of application that can only serve this single purpose. That's where **Image Resizer** comes in.

![](https://github.com/kemalakay/imageresizer/blob/master/README/ImageResizing.gif)

Image Resizer allows you to easily load your images, set a resolution size, choose a directory to output your images and start rendering process to resize them. Besides resizing your photos, it can also be used to resize textures, e.g. of your game project. Currently, most of the functionality is completed but there are still remaining bits. For instance, you can load `JPG` and `PNG` files but you can only output to `JPG`. But I still thought that it can be helpful to some people in its current status therefore I decided to share it here. You can find the remaining tasks below, you're more than welcome to help if you want.

![](https://github.com/kemalakay/imageresizer/blob/master/README/SetResolution.jpg)

#### TO-DO:
* Port it to Windows
* Provide compiled executables for Windows and Mac
* Add functionality to multi-load images from a user specified directory instead of a pre-determined path
* Add functionality to choose output image format (currently, it only outputs to jpg format)

#### Setup:
You need to install some Python libraries if you want to compile the code. Python 2.7 is used for this project.
Used external libraries are:

* [PIL](http://www.pythonware.com/products/pil/)
* [PyQT 4](https://pypi.python.org/pypi/PyQt4)

#### Updates: 
* 21/01/2018 - Initial commit




