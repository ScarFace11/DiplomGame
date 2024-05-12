from PIL import Image


def convert_image_to_binary(image_path, wall_thickness, scale_factor):
    image = Image.open(image_path)
    image = image.convert("L")  # Преобразование в оттенки серого
    pixels = image.load()
    width, height = image.size

    scaled_width = width // scale_factor
    scaled_height = height // scale_factor

    binary_data = []

    for y in range(0, scaled_height):
        row_data = []
        for x in range(0, scaled_width):
            pixel = pixels[x * scale_factor, y * scale_factor]
            if pixel == 0 or (
                    x < wall_thickness or x >= scaled_width - wall_thickness or y < wall_thickness or y >= scaled_height - wall_thickness):
                row_data.append(1)  # Черный цвет или граница стенки
            else:
                row_data.append(0)  # Белый цвет
        binary_data.append(row_data)

    return binary_data


def GetMazeFromImage():
    maze_name = 'm8'
    image_path = f"Sprite/{maze_name}.png"
    wall_thickness = 1
    scale_factor = 2
    binary_data = convert_image_to_binary(image_path, wall_thickness, scale_factor)
    maze = binary_data

    print(f"{maze_name} = [")
    for row in maze:
        print(f"{row},")
    print(']')


GetMazeFromImage()
