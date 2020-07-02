# blender-2d-projector
Add-on for projecting 3D animation to 2D image sheets using Blender

### To-do's:

- render normal maps

- dynamic outlines (most likely won't happen soon)

### How to install the addon

- Clone this repository

- Open Blender

- Go to **Edit -> Preferences -> Add-ons -> Install**

- Go to the folder of this repository

- Click on **main.py**

- You'll be able to see a panel under the **Tool** section, under the **Properties** window.

- You'll also have to set up your camera and lights before rendering.

- Tune the parameters in the panel and click on **Render** to generate your image(s) in the output path you specified.

### Please notice that:

- This is **work in progress**. If you're not happy about something here, feel free to improve this program by making your own pull request, or if you can't/don't want to program, please open an issue and let me know about it. While you're at it, a motivational star will surely make me want to improve this.

- This only supports the EEVEE render engine for now, and was only tested in Blender version 2.82. I might upgrade and change this soon though.

- Rendering animations will render every frame. This is a process that takes a fair amount of time and produces lots of images. Be sure to make a directory specifically for this output, and be patient.

- This is free software, MIT licensed, therefore it comes with zero warranty.
