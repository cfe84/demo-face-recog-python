import face_recognition
from PIL import Image, ImageDraw
import os 
dir_path = os.path.dirname(os.path.realpath(__file__))

# This is an example of running face recognition on a single image
# and drawing a box around each person that was identified.

def get_faces(inputPath, outputPath):
    # Load a sample picture and learn how to recognize it.
    trudeau_image = face_recognition.load_image_file(os.path.join(dir_path, "trudeau.jpg"))
    trudeau_face_encoding = face_recognition.face_encodings(trudeau_image)[0]
    bieber_image = face_recognition.load_image_file(os.path.join(dir_path, "bieber.jpg"))
    bieber_face_encoding = face_recognition.face_encodings(bieber_image)[0]

    # Create arrays of known face encodings and their names
    known_face_encodings = [
        trudeau_face_encoding,
        bieber_face_encoding
    ]
    known_face_names = [
        "J. Trudeau",
        "J. Bieber"
    ]

    # Load an image with an unknown face
    unknown_image = face_recognition.load_image_file(inputPath)

    # Find all the faces and face encodings in the unknown image
    face_locations = face_recognition.face_locations(unknown_image)
    face_encodings = face_recognition.face_encodings(unknown_image, face_locations)

    # Convert the image to a PIL-format image so that we can draw on top of it with the Pillow library
    # See http://pillow.readthedocs.io/ for more about PIL/Pillow
    pil_image = Image.fromarray(unknown_image)
    # Create a Pillow ImageDraw Draw instance to draw with
    draw = ImageDraw.Draw(pil_image)

    # Loop through each face found in the unknown image
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        # See if the face is a match for the known face(s)
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)

        name = "Unknown"

        # If a match was found in known_face_encodings, just use the first one.
        if True in matches:
            first_match_index = matches.index(True)
            name = known_face_names[first_match_index]

        # Draw a box around the face using the Pillow module
        draw.rectangle(((left, top), (right, bottom)), outline=(255, 0, 0))

        # Draw a label with a name below the face
        text_width, text_height = draw.textsize(name)
        if name != "Unknown" :
            draw.rectangle(((left, bottom - text_height - 10), (right, bottom)), fill=(0, 0, 255), outline=(0, 0, 255))
            draw.text((left + 6, bottom - text_height - 5), name, fill=(255, 255, 255, 255))


    # Remove the drawing library from memory as per the Pillow docs
    del draw
    pil_image.save(outputPath)