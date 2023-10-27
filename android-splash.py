from gimpfu import *
import os

def android_splash_9_png(image, input_layer, bgcolor, output_directory):
    w = image.width
    h = image.height
    
    resolutions = [
    {"name": "ldpi", "orientation": "port", "w": 200, "h": 320},
    {"name": "ldpi", "orientation": "land", "w": 320, "h": 200},
    {"name": "mdpi", "orientation": "port", "w": 320, "h": 480 },
    {"name": "mdpi", "orientation": "land", "w": 480, "h": 320 },
    {"name": "hdpi", "orientation": "port", "w": 480, "h": 720 },
    {"name": "hdpi", "orientation": "land", "w": 720, "h": 480 },
    {"name": "xhdpi", "orientation": "port", "w": 640, "h": 960 },
    {"name": "xhdpi", "orientation": "land", "w": 960, "h": 640 },
    {"name": "xxhdpi", "orientation": "port", "w": 960, "h": 1440 },
    {"name": "xxhdpi", "orientation": "land", "w": 1440, "h": 960 },
    {"name": "xxxhdpi", "orientation": "port", "w": 1280, "h": 1920 },
    {"name": "xxxhdpi", "orientation": "land", "w": 1920, "h": 1280 }
    ]
    
    stretch = 2
    #resolution = resolutions[0]
    pdb.gimp_progress_init("Splashing 9s...", None)
    for resolution in resolutions:

        layer = input_layer.copy()
        image.add_layer(layer, 0)
        
        newWidth = resolution["w"]
        newHeight = resolution["h"]
        
        #offsetX = 0
        #offsetY = 0
        #colorW = 0
        #colorH = 0
        #colorX = 0
        #colorY = 0
        #minSize = 0
        if newWidth < newHeight:
            minSize = newWidth
            offsetX = 0
            offsetY = newHeight / 2 - minSize / 2
            colorW = minSize
            colorH = offsetY
            colorX = 0
            colorY = offsetY + minSize
        else:
            minSize = newHeight
            offsetX = newWidth / 2 - minSize / 2
            offsetY = 0
            colorW = offsetX
            colorH = minSize
            colorX = offsetX + minSize
            colorY = 0

        layer.name = resolution["name"] + "-" + resolution["orientation"]
        layer.scale(minSize, minSize, 1)
        layer.resize(newWidth, newHeight, offsetX, offsetY)
        
        pdb.gimp_image_select_rectangle(image, 2, layer.offsets[0], layer.offsets[1], colorW, colorH)
        pdb.gimp_image_select_rectangle(image, 0, layer.offsets[0] + colorX, layer.offsets[1] + colorY, colorW, colorH)
        pdb.gimp_context_set_foreground(bgcolor)
        pdb.gimp_drawable_edit_fill(layer, 0)
        
        layer.resize(layer.width + 2, layer.height + 2, 1, 1)
        
        pdb.gimp_image_select_rectangle(image, 2, layer.offsets[0] + 1, layer.offsets[1], stretch, 1)
        pdb.gimp_image_select_rectangle(image, 0, layer.offsets[0] + layer.width - stretch - 1, layer.offsets[1], stretch, 1)
        pdb.gimp_image_select_rectangle(image, 0, layer.offsets[0], layer.offsets[1] + 1, 1, stretch)
        pdb.gimp_image_select_rectangle(image, 0, layer.offsets[0], layer.offsets[1] + layer.height - stretch - 1, 1, stretch)
        pdb.gimp_context_set_foreground((0, 0, 0))
        pdb.gimp_drawable_edit_fill(layer, 0)
        
        new_image = pdb.gimp_image_new(layer.width, layer.height, 0)
        new_layer = pdb.gimp_layer_new_from_drawable(layer, new_image)
        pdb.gimp_image_insert_layer(new_image, new_layer, None, 0)
        fileName = 'splash.9.png'
        dirName = os.path.join(output_directory, 'drawable-' + resolution["orientation"] + "-" + resolution["name"])
        pathName = os.path.join(dirName, fileName)
        if not os.path.exists(dirName):
            os.mkdir(dirName)
        pdb.gimp_file_save(new_image, new_layer, pathName, fileName)
        pdb.gimp_image_delete(new_image)
        
        pdb.gimp_image_remove_layer(image, layer)
        

register(
	"android_splash_9_png",
	"Android 9 png",
	"Android splash 9 png",
	"Mattia Baraldi",
	"Mattia Baraldi",
	"2023",
	"<Image>/Filters/AndroidSplash",
	"*",
	[
        (PF_COLOR, "bgcolor", "Background color: ", (0, 0, 0)),
        (PF_DIRNAME, "output_directory", "Output directory", "")
	],
	[],
	android_splash_9_png
)

main()