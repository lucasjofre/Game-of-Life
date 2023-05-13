from PIL import Image, ImageDraw, ImageFont
import settings as s

def text_to_image(text, font_path, font_size, board_size, text_color=s.PINK, bg_color=s.BLACK):
    # Load the font
    font = ImageFont.truetype(font_path, font_size)

    # Measure the size of the text
    text_width, text_height = font.getsize(text)

    # Create a new image with the size of the board
    image = Image.new('RGBA', board_size, bg_color)

    # Calculate the position for the text to be centered
    text_x = (board_size[0] - text_width) // 2
    text_y = (board_size[1] - text_height) // 2

    # Create a draw object
    draw = ImageDraw.Draw(image)

    # Draw the text onto the image
    draw.text((text_x, text_y), text, font=font, fill=text_color)

    # Return the image
    image.save("game_of_life.png")
    return image

# text_to_image("Game of Life", "8bit_arcade.ttf", 64, (1000, 600))
