import cv2
from nudenet import NudeDetector
import numpy as np
import tempfile
import base64
from io import BytesIO
from PIL import Image
import io
import os
# Initialize the detector
nude_detector = NudeDetector()

def nudeNetImages(payload):
    input_img = payload['image']

    file_contents = input_img.file.read()

    image = np.fromstring(file_contents, np.uint8)
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)

    imageOriginal = np.fromstring(file_contents, np.uint8)
    imageOriginal = cv2.imdecode(imageOriginal, cv2.IMREAD_COLOR)

    # Save the image to a temporary file
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.jpg')
    cv2.imwrite(temp_file.name, image)

    # Detect nudity in the image
    detections = nude_detector.detect(temp_file.name)

    # Define the explicit nudity labels
    explicit_labels = ["FEMALE_GENITALIA_COVERED", "BUTTOCKS_EXPOSED", 
                    "FEMALE_BREAST_EXPOSED", "FEMALE_GENITALIA_EXPOSED", "MALE_BREAST_EXPOSED",
                    "ANUS_EXPOSED", "FEET_EXPOSED", "BELLY_COVERED", "FEET_COVERED", "ARMPITS_COVERED", 
                    "ARMPITS_EXPOSED", "BELLY_EXPOSED", "MALE_GENITALIA_EXPOSED", 
                    "ANUS_COVERED", "FEMALE_BREAST_COVERED", "BUTTOCKS_COVERED"
                    ]
    nudanalyze = {}
    for detection in detections:
        # Get the class and check if it is explicit nudity
        detection_class = detection['class']
        score = detection['score']
        if detection_class in explicit_labels and score > 0.5:
            nudanalyze[detection_class] = score
            # Get the bounding box
            box = detection['box']
            x1, y1, width, height = box

            # Blur the exposed body part
            roi = image[y1:y1+height, x1:x1+width]
            blurred_roi = cv2.GaussianBlur(roi, (75, 75), 0)
            image[y1:y1+height, x1:x1+width] = blurred_roi

            # # Draw the bounding box on the image
            # cv2.rectangle(image, (x1, y1), (x1 + width, y1 + height), (0, 0, 255), 2)

            # # Put the class and score on the image
            # text = f"{detection_class}: {detection['score']:.2f}"
            # cv2.putText(image, text, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
        else:
            # Handle non-explicit detections (e.g., faces)
            pass

    # Save the image
    # Convert the processed image to base64
    originalImageBase64=imageToByte(imageOriginal)
    imageBase64=imageToByte(image)
    # base64_string = base64.b64encode(image).decode("utf-8")
    cv2.imwrite('output.jpg', image)
    response = {
        "blurredImage": imageBase64,
        "originalImage": originalImageBase64,
        "nudanalyze": nudanalyze
    }
    return response

def imageToByte(img):
    # Swap color channels from BGR to RGB
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Convert numpy array to PIL Image
    img_pil = Image.fromarray(img_rgb)

    buffer = io.BytesIO()
    img_pil.save(buffer, format="png")
    image_data = buffer.getvalue()
    base64_string = base64.b64encode(image_data).decode("utf-8")
    return base64_string


# def nudeNetVideo(payload):
#     input_video = payload['video']

#     # Save the video file to a temporary location
#     with tempfile.NamedTemporaryFile(delete=False) as temp_file:
#         temp_file.write(input_video.file.read())
#         temp_file_path = temp_file.name

#     # Open the video file
#     video = cv2.VideoCapture(temp_file_path)

#     if not video.isOpened():
#         raise Exception("Failed to open the video file.")

#     # Get video properties
#     fps = video.get(cv2.CAP_PROP_FPS)
#     frame_width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
#     frame_height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))

#     # Create a VideoWriter object to save the processed video
#     output_filename = 'output.mp4'
#     fourcc = cv2.VideoWriter_fourcc(*'mp4v')
#     output_video = cv2.VideoWriter(output_filename, fourcc, fps, (frame_width, frame_height))
#     # Define the explicit nudity labels
#     explicit_labels = ["FEMALE_GENITALIA_COVERED", "BUTTOCKS_EXPOSED", 
#                     "FEMALE_BREAST_EXPOSED", "FEMALE_GENITALIA_EXPOSED", "MALE_BREAST_EXPOSED",
#                     "ANUS_EXPOSED", "FEET_EXPOSED", "BELLY_COVERED", "FEET_COVERED", "ARMPITS_COVERED", 
#                     "ARMPITS_EXPOSED", "BELLY_EXPOSED", "MALE_GENITALIA_EXPOSED", 
#                     "ANUS_COVERED", "FEMALE_BREAST_COVERED", "BUTTOCKS_COVERED"
#                     ]
#     nudanalyze = {}

#     # Process each frame in the video
#     while video.isOpened():
#         ret, frame = video.read()

#         if not ret:
#             break

#         frame_original = frame.copy()
#         image = np.fromstring(frame, np.uint8)
#         image = cv2.imdecode(image, cv2.IMREAD_COLOR)
#         # Detect nudity in the frame
#         detections = nude_detector.detect(image)

#         for detection in detections:
#             detection_class = detection['class']
#             score = detection['score']

#             if detection_class in explicit_labels and score > 0.5:
#                 nudanalyze[detection_class] = nudanalyze.get(detection_class, 0) + 1

#                 # Get the bounding box
#                 box = detection['box']
#                 x1, y1, width, height = box

#                 # Blur the exposed body part
#                 roi = frame[y1:y1+height, x1:x1+width]
#                 blurred_roi = cv2.GaussianBlur(roi, (75, 75), 0)
#                 frame[y1:y1+height, x1:x1+width] = blurred_roi

#         # Write the processed frame to the output video
#         output_video.write(frame)

#     # Release the video and output file
#     video.release()
#     output_video.release()

#     # Convert the processed video to base64
#     with open(output_filename, 'rb') as f:
#         video_bytes = f.read()

#     video_base64 = base64.b64encode(video_bytes).decode("utf-8")

#     response = {
#         "processedVideo": video_base64,
#         "nudanalyze": nudanalyze
#     }

#     return response

# def videoToByte(file_path):
#     with open(file_path, "rb") as file:
#         file_data = file.read()
#         base64_string = base64.b64encode(file_data).decode("utf-8")
#     return base64_string

def nudeNetVideo(payload):
    input_video = payload['video']
    # Save the video file to a temporary location
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(input_video.file.read())
        temp_file_path = temp_file.name
    # Open video capture
    video_path = temp_file_path
    cap = cv2.VideoCapture(video_path)

    # Get video properties
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    # Define output video writer
    output_path = 'output1.mp4'
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    # Define the explicit nudity labels
    explicit_labels = ["FEMALE_GENITALIA_COVERED", "BUTTOCKS_EXPOSED", 
                    "FEMALE_BREAST_EXPOSED", "FEMALE_GENITALIA_EXPOSED", "MALE_BREAST_EXPOSED",
                    "ANUS_EXPOSED", "BELLY_COVERED", "ARMPITS_COVERED", 
                    "ARMPITS_EXPOSED", "BELLY_EXPOSED", "MALE_GENITALIA_EXPOSED", 
                    "ANUS_COVERED", "FEMALE_BREAST_COVERED", "BUTTOCKS_COVERED"
                    ]
    
    # # Define the explicit nudity labels original
    # explicit_labels = ["FEMALE_GENITALIA_COVERED", "BUTTOCKS_EXPOSED", 
    #                 "FEMALE_BREAST_EXPOSED", "FEMALE_GENITALIA_EXPOSED", "MALE_BREAST_EXPOSED",
    #                 "ANUS_EXPOSED", "BELLY_COVERED", "ARMPITS_COVERED", 
    #                 "ARMPITS_EXPOSED", "BELLY_EXPOSED", "MALE_GENITALIA_EXPOSED", 
    #                 "ANUS_COVERED", "FEMALE_BREAST_COVERED", "BUTTOCKS_COVERED"
    #                 ]

    # Create a temporary directory to store image frames
    temp_dir = 'temp_frames'
    os.makedirs(temp_dir, exist_ok=True)

    frame_counter = 0
    nudanalyze = {}
    while cap.isOpened():
        # Read a frame from the video
        ret, frame = cap.read()
        if not ret:
            break

        # Convert frame to the appropriate format
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Save frame as a temporary image file
        temp_file_path = os.path.join(temp_dir, f'frame_{frame_counter}.jpg')
        cv2.imwrite(temp_file_path, frame)

        # Detect nudity in the frame
        detections = nude_detector.detect(temp_file_path)

        for detection in detections:
            # Get the class and check if it is explicit nudity with a score above 0.8
            detection_class = detection['class']
            detection_score = detection['score']
            print(detection)
            if detection_class in explicit_labels and detection_score > 0.3:
                # Get the bounding box
                box = detection['box']
                x1, y1, width, height = box

                # Blur the exposed body part
                roi = frame[y1:y1 + height, x1:x1 + width]
                blurred_roi = cv2.GaussianBlur(roi, (51, 51), 0)
                frame[y1:y1 + height, x1:x1 + width] = blurred_roi

                # # Draw the bounding box on the frame
                # cv2.rectangle(frame, (x1, y1), (x1 + width, y1 + height), (0, 0, 255), 2)

                # # Put the class and score on the frame
                # text = f"{detection_class}: {detection_score:.2f}"
                # cv2.putText(frame, text, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
                # print(text)
                nudanalyze[detection_class] = detection_score
            else:
                # Handle non-explicit detections (e.g., faces)
                pass

        # Convert frame back to BGR format
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        # Write the frame to the output video
        out.write(frame)

        # Increment frame counter
        frame_counter += 1

    # Release video capture and writer
    cap.release()
    out.release()
    base64Video = videoToByte(output_path)
    # Remove temporary image files
    for file_name in os.listdir(temp_dir):
        file_path = os.path.join(temp_dir, file_name)
        os.remove(file_path)
    
    # Remove the temporary directory
    os.rmdir(temp_dir)
    # Delete the output video file
    os.remove(output_path)
    return {
        "nudanalyze": nudanalyze,
        "BLURRED": base64Video
    }

def videoToByte(file_path):
    with open(file_path, "rb") as file:
        file_data = file.read()
        base64_string = base64.b64encode(file_data).decode("utf-8")
    return base64_string