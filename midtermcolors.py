#I did this on Pyscript first and then put it into Thonny, but I wanted the
#continuous video capture and that wasn't possible on 
import requests
import cv2
import numpy as np
from airtablesecrets import BASE_ID, API_KEY,TABLE_ID,RECORD_ID

colorname = 'None'
cv2.namedWindow('Frame', cv2.WINDOW_NORMAL)
cv2.namedWindow('Mask', cv2.WINDOW_NORMAL)
cap = cv2.VideoCapture(1)
while True:
    try:
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture a frame.")
        else:

            brightframe = cv2.convertScaleAbs(frame, 1, 2)
            cv2.imshow('Frame', brightframe)
            image = cv2.cvtColor(brightframe, cv2.COLOR_BGR2HSV)


            # Define lower and upper bounds for Green and Red
            g_lower = np.array([40, 50, 100])
            g_upper = np.array([80, 255, 255])
            r_lower = np.array([0, 150, 170])
            r_upper = np.array([30, 255, 255])
            r_lower1 = np.array([150, 150, 150])
            r_upper1 = np.array([180, 255, 255])

            # Define masks
            g_mask = cv2.inRange(image, g_lower, g_upper)
            r_mask = cv2.inRange(image, r_lower, r_upper) + cv2.inRange(image, r_lower1, r_upper1)
            greens = g_mask.sum()
            reds = r_mask.sum()

            # Picking Color
            if greens > 100000 and greens > reds:
                print('Green: ', greens)
                cv2.imshow('Mask', g_mask)
                colorname = 'Green'
            elif reds > 100000 and reds > greens:
                print('Red: ', reds)
                cv2.imshow('Mask', r_mask)
                colorname = "Red"
            else:
                print("No Color Detected")
                colorname = "None"


            endpoint = f'https://api.airtable.com/v0/{BASE_ID}/{TABLE_ID}'
            headers = {
                'Authorization': f'Bearer {API_KEY}',
                'Content-Type': 'application/json',
            }

            # Create a dictionary with the fields you want to update
            data = {
                'records': [{
                    'id': RECORD_ID,
                    "fields": {
                        "Color Name": colorname
                    }
                }]
            }

            # Send the PUT request to update the record
            response = requests.patch(endpoint, json=data, headers=headers)
            # Check the response status code
            if response.status_code == 200:
                print("Record updated successfully")
            else:
                print(f"Failed to update record. Status code: {response.status_code}")
                print(response.json())  # Print the error message if available
            cv2.waitKey(1)
    except KeyboardInterrupt:
         # Release the camera and close OpenCV windows
            cap.release()
            cv2.destroyAllWindows()
            break

