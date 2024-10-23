import streamlit as st
from streamlit_option_menu import option_menu
from streamlit_lottie import st_lottie
import requests
import cv2
import numpy as np
import HandTrackingModule as htm
import time
import pyautogui
import math
import os

# Pycaw initialization
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


# Set Streamlit to wide mode
st.set_page_config(layout="wide")

# hide streamlit's default style
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# with st.sidebar:
st.title("GestureAI")
# st.image("image.png", use_column_width=True)

# Initialize session state for navigation
if "selected" not in st.session_state:
    st.session_state.selected = "Home"


selected = option_menu(
    menu_title=None,
    options=["Home", "Virtual Mouse", "Virtual Paint", "Contact"],
    icons=["house-fill", "mouse2-fill", "brush-fill", "telephone-fill"],
    default_index=0,
    orientation="horizontal",
)

# Update session state based on selected option
if selected:
    st.session_state.selected = selected


def load_lottie(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()


if selected == "Home":
    col1, col2, col3 = st.columns([1, 2, 1])

    with col1:
        st.image("virtual_mouse.png", use_column_width=True)

        st.markdown(
            """
        <div style="text-align: center; font-size: 1.2em; color: #444;">
            🖱️ Ready to ditch your physical mouse? <br>
            <strong>Head over to the <span style="color: #4A90E2;">Virtual Mouse</span> tab</strong> and control your computer with just hand gestures! ✋💻
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            """
            <div style="text-align: center; font-family: Arial, sans-serif;">
                <h1 style="color: #4A90E2; font-size: 48px;">Welcome to GestureAI</h1>
                <p style="color: #7D7D7D; font-size: 18px; line-height: 1.6;">
                    Experience the future of human-computer interaction where simple hand gestures empower 
                    you to control your screen and unleash your creativity in a whole new way. 
                    <strong>Navigate. Paint. Create.</strong> All in the air.
                </p>
            </div>
        """,
            unsafe_allow_html=True,
        )

        lottie = load_lottie(
            "https://lottie.host/2553d0e4-45db-427f-9dc8-8bb48d58dc38/BtIBCPoyta.json"
        )
        st_lottie(lottie, height=300)

    with col3:
        st.image("virtual_paint.png", use_column_width=True)

        st.markdown(
            """
        <div style="text-align: center; font-size: 1.2em; color: #444;">
            🎨 Feeling creative? <br>
            <strong>Go to the <span style="color: #4A90E2;">Virtual Paint</span> tab</strong> and start painting your imagination into reality! 🖌️✨
        </div>
        """,
            unsafe_allow_html=True,
        )

    # New section for contact information
    st.markdown(
        """
        <div style="text-align: center; font-family: Arial, sans-serif; margin-top: 50px;">
        <h2 style="color: #4A90E2; font-size: 32px;">Let's Connect! 🤝</h2>
        <p style="color: #7D7D7D; font-size: 18px; line-height: 1.6;">
            Got questions, feedback, or ideas for collaboration? <br> 
            You can <strong>reach me</strong> directly by going to the <strong>Contact</strong> tab above, or connect with me on my professional platforms:
        </p>
        
        <!-- GitHub and LinkedIn links -->
        <p style="font-size: 20px;">
            <a href="https://github.com/yourusername" target="_blank" style="text-decoration: none;">
                <img src="https://img.icons8.com/ios-glyphs/30/000000/github.png" style="vertical-align: middle;"/> <span style="color: #4A90E2;">GitHub</span>
            </a>
            &nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;
            <a href="https://linkedin.com/in/yourusername" target="_blank" style="text-decoration: none;">
                <img src="https://img.icons8.com/color/48/000000/linkedin.png" style="vertical-align: middle;"/> <span style="color: #4A90E2;">LinkedIn</span>
            </a>
        </p>

        <!-- Resume link -->
        <p style="color: #7D7D7D; font-size: 18px;">
            Or, you can take a look at my <a href="https://your-resume-link.com" target="_blank" style="color: #4A90E2;">Resume 📄</a> to see my skills and experience.
        </p>

        <p style="color: #4A90E2; font-size: 22px; font-weight: bold;">
            Looking forward to hearing from you! 😊
        </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


elif selected == "Virtual Mouse":

    # Title of the Streamlit app
    st.title("Virtual Mouse with Hand Gesture Control")

    # Introduction to the app
    st.markdown(
        """
    Welcome to the **Virtual Mouse** application! This tool uses cutting-edge computer vision techniques to allow you to control your mouse with simple hand gestures. No more need for a physical mouse—your hand movements are all you need!
    """
    )

    # Important warning message
    st.warning(
        "⚠️ **Note:** Navigating away from this page or reloading it will automatically close the webcam. Feel free to explore our **Virtual Paint** tool in the other tab, also powered by our computer vision algorithms!"
    )

    # Gesture control instructions
    st.subheader("Gesture Control Guide:")
    st.markdown(
        """
    - **Move the Mouse:** Use your **index finger** to guide the cursor around the screen.
    - **Left Click:** Tap your **index and middle fingers** together to simulate a left click.
    - **Right Click:** Raise all **five fingers** for a right-click action.
    - **Scroll Down:** Hold up **three fingers** to scroll down.
    - **Scroll Up:** Hold up **four fingers** to scroll up.
    - **Adjust Volume:** Use your **index finger and thumb** in a pinch motion—pinch **inward** to lower the volume and **outward** to raise it.
    """
    )

    # Call to action
    st.markdown(
        """
    Put your hand in front of the webcam and give it a try! The system is designed to be intuitive and responsive, making it easy for you to navigate your computer effortlessly.
    """
    )

    # Create placeholders for the webcam stream and buttons
    frame_placeholder = st.empty()
    start_button = st.empty()
    stop_button_placeholder = st.empty()

    # Webcam settings
    cap = None  # Initialize it as None for the webcam
    stop_requested = False  # Variable to manage the state of the stop button

    def start_virtual_mouse():
        global cap, stop_requested
        # Disable PyAutoGUI fail-safe
        pyautogui.FAILSAFE = False

        ##########################################################################################
        # Hand detector
        detector = htm.handDetector(maxHands=1)

        # Smoothing and location variables
        smoothening = 3
        plocX, plocy = 0, 0
        curlocX, curlocy = 0, 0
        frame_reduction = 10

        # Getting screen width and height
        width_screen, height_screen = pyautogui.size()
        cap = cv2.VideoCapture(1)
        WIDTH_CAM = 640
        HEIGHT_CAM = 480
        cap.set(3, WIDTH_CAM)
        cap.set(4, HEIGHT_CAM)

        previous_time = 0

        # Volume control setup
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = interface.QueryInterface(IAudioEndpointVolume)

        minvol, maxvol, _ = volume.GetVolumeRange()  # unpacking
        vol = 0
        volume_bar = 400  # setting initial value of the bar, 400 is the coordinate when its lowest
        vol_percentage = 0
        ##########################################################################################

        # Create the "Stop" button once outside the loop
        if stop_button_placeholder.button("Stop Virtual Mouse", key="stop_button"):
            stop_requested = True
            return  # Exit the function when the "Stop" button is clicked

        # Continuously capture video frames
        while cap.isOpened():
            success, frame = cap.read()
            if not success:
                break

            # Convert frame to RGB for Streamlit
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Detect hands and get landmark positions
            frame = detector.findHands(frame)
            lmlist, bbox = detector.findPosition(frame)

            # If landmarks are detected, process gestures
            if len(lmlist) != 0:
                x0, y0 = lmlist[4][1:]  # 4 for Thumb tip
                x1, y1 = lmlist[8][1:]  # 8 for Index finger tip
                x2, y2 = lmlist[12][1:]  # 12 Middle finger tip

                # Check which fingers are up
                fingers = detector.fingersUp()

                # Draw a rectangle where the hand movement is confined
                cv2.rectangle(
                    frame,
                    (frame_reduction, frame_reduction),
                    (WIDTH_CAM - frame_reduction, HEIGHT_CAM - frame_reduction),
                    (255, 0, 255),
                    2,
                )

                # Moving mode: If only the index finger is up
                if fingers[1] == 1 and fingers[2] == 0:
                    # Convert coordinates
                    x3 = np.interp(
                        x1,
                        (frame_reduction, WIDTH_CAM - frame_reduction),
                        (0, width_screen),
                    )
                    y3 = np.interp(
                        y1,
                        (frame_reduction, HEIGHT_CAM - frame_reduction),
                        (0, height_screen),
                    )

                    # Smooth the values
                    curlocX = plocX + (x3 - plocX) / smoothening
                    curlocy = plocy + (y3 - plocy) / smoothening

                    # Move the mouse
                    pyautogui.moveTo(curlocX, curlocy)
                    plocX, plocy = curlocX, curlocy

                # Clicking mode: If both index and middle fingers are up
                if fingers[1] == 1 and fingers[2] == 1:
                    length, frame, lineInfo = detector.findDistance(8, 12, frame)

                    # Perform click if fingers are close enough
                    if length < 45:
                        # change mid circle color when clicked
                        cv2.circle(
                            frame,
                            (lineInfo[4], lineInfo[5]),
                            15,
                            (0, 255, 255),
                            cv2.FILLED,
                        )
                        pyautogui.click()

                # Scrolling down: If three fingers are up, A positive value scrolls up, and a negative value scrolls down.
                if (
                    fingers[0] == 0
                    and fingers[1] == 1
                    and fingers[2] == 1
                    and fingers[3] == 1
                    and fingers[4] == 0
                ):
                    pyautogui.scroll(-30)  # Scroll down

                # Scrolling up: If four fingers are up, A positive value scrolls up, and a negative value scrolls down.
                if (
                    fingers[0] == 0
                    and fingers[1] == 1
                    and fingers[2] == 1
                    and fingers[3] == 1
                    and fingers[4] == 1
                ):
                    pyautogui.scroll(30)  # Scroll up

                # Right-click: All five fingers up
                if fingers == [1, 1, 1, 1, 1]:  # All fingers up
                    pyautogui.click(button="right")  # Perform right-click

                # Volume control mode: Thumb and Index finger pinch together
                if fingers[1] == 1 and fingers[0] == 1 and fingers[2:] == [0, 0, 0]:

                    # draw circle on tip of the thumb and index finger
                    cv2.circle(frame, (x0, y0), 15, (255, 0, 255), cv2.FILLED)
                    cv2.circle(frame, (x1, y1), 15, (255, 0, 255), cv2.FILLED)

                    # draw line between the two circles
                    cv2.line(frame, (x0, y0), (x1, y1), (255, 0, 255), 3)

                    # get the center of the line
                    centerx, centery = (x0 + x1) // 2, (y0 + y1) // 2

                    # draw circle for the center of the line as well
                    cv2.circle(frame, (centerx, centery), 15, (255, 0, 255), cv2.FILLED)

                    # Calculate the distance between thumb and index finger
                    length = math.hypot(x1 - x0, y1 - y0)

                    # Adjust the volume based on the finger distance
                    vol = np.interp(length, [50, 250], [minvol, maxvol])
                    volume.SetMasterVolumeLevel(vol, None)

                    # Visual feedback for the volume
                    volume_bar = np.interp(length, [50, 250], [400, 150])
                    vol_percentage = np.interp(length, [50, 250], [0, 100])

                    # Change color if fingers are too close
                    if length < 50:
                        cv2.circle(
                            frame,
                            (centerx, centery),
                            15,
                            (255, 0, 0),
                            cv2.FILLED,
                        )
                    if length >= 250:
                        cv2.circle(
                            frame, (centerx, centery), 15, (255, 0, 0), cv2.FILLED
                        )

                    # Draw volume bar
                    cv2.rectangle(frame, (50, 150), (85, 400), (0, 255, 0), 3)
                    cv2.rectangle(
                        frame, (50, int(volume_bar)), (85, 400), (0, 255, 0), cv2.FILLED
                    )
                    cv2.putText(
                        frame,
                        f"{int(vol_percentage)}%",
                        (40, 450),
                        cv2.FONT_HERSHEY_PLAIN,
                        3,
                        (0, 255, 0),
                        3,
                    )

            # Calculate the FPS
            current_time = time.time()
            fps = 1 / (current_time - previous_time)
            previous_time = current_time

            # Display FPS on the frame
            cv2.putText(
                frame,
                str(int(fps)),
                (20, 50),
                cv2.FONT_HERSHEY_PLAIN,
                3,
                (255, 0, 0),
                3,
            )

            # Display the frame in Streamlit
            frame_placeholder.image(frame, channels="RGB")

        cap.release()
        cv2.destroyAllWindows()

    # Display the "Start Virtual Mouse" button only if the webcam is not already running
    if not stop_requested:
        if start_button.button("Enable Gesture Control", key="start_button"):
            start_button.empty()  # Remove the start button
            stop_button_placeholder.empty()  # Clear the stop button placeholder
            start_virtual_mouse()  # Start the virtual mouse detection


elif selected == "Virtual Paint":
    # Title of the Virtual Paint app
    st.title("🎨 Virtual Paint: Paint Freely in the Air! 🖌️")

    # Introduction to the app
    st.markdown(
        """
    **Unleash your creativity** with **Virtual Paint**, a cutting-edge tool that lets you paint in mid-air using nothing but hand gestures! ✋ No brushes, no mess—just pure artistic freedom powered by advanced computer vision technology. 
    """
    )

    # Features overview
    st.subheader("Features:")
    st.markdown(
        """
    - **7 vibrant colors** to choose from, allowing you to create colorful masterpieces. 🌈
    - **Simple hand gestures** let you control the virtual brush effortlessly.
    - **No canvas needed**—paint directly into the air and see your creations on screen! 🖼️
    """
    )

    # Gesture control instructions
    st.subheader("How to Use:")
    st.markdown(
        """
    - **Paint**: Hold only your **index finger** up to start painting with your virtual brush.
    - **Selection Mode**: Raise both your **index and middle fingers** to enter selection mode, where you can choose a new color or the eraser tool. 
    """
    )

    # Call to action
    st.markdown(
        """
    Ready to become the next virtual Picasso? 🎨 Put your creativity to the test—start painting now and have fun expressing yourself in an entirely new way! 🖌️💡
    """
    )

    # Create placeholders for the webcam stream and buttons
    frame_placeholder = st.empty()
    start_button = st.empty()
    stop_button_placeholder = st.empty()

    # Webcam settings
    cap2 = None  # Initialize it as None for the webcam
    stop_requested2 = False  # Variable to manage the state of the stop button

    def start_virtual_paint():
        global cap2, stop_requested2
        # Constants
        brushThickness = 25
        eraserThickness = 100

        # Define Headers folder path
        folderPath = "virtualPaint_Headers"

        # going through each image path and appending them
        myList = os.listdir(folderPath)
        print(myList)
        overlayList = []
        for imPath in myList:
            image = cv2.imread(f"{folderPath}/{imPath}")
            overlayList.append(image)
        print(len(overlayList))

        # display the first image as default
        header = overlayList[0]

        # store color (whenever a brush is selected the color will change)
        drawColor = (255, 255, 255)

        cap2 = cv2.VideoCapture(1)
        cap2.set(3, 1280)
        cap2.set(4, 720)

        # instantiating our detector
        detector = htm.handDetector(detectionCon=0.65, maxHands=1)

        # these is x previous and y previous (prev coordinates of both axis)
        xp, yp = 0, 0

        # this will be the canvas on which we will draw
        imgCanvas = np.zeros((720, 1280, 3), np.uint8)

        # Create the "Stop" button once outside the loop
        if stop_button_placeholder.button("Stop Virtual Paint", key="stop_button"):
            stop_requested2 = True
            return  # Exit the function when the "Stop" button is clicked

        # Continuously capture video frames
        while cap2.isOpened():
            success, img = cap2.read()
            if not success:
                break

            # Convert frame to RGB for Streamlit
            # img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            img = detector.findHands(img)
            lmList, bbox = detector.findPosition(img, draw=False)

            if len(lmList) != 0:
                # tip of index and middle fingers
                x1, y1 = lmList[8][1:]  # 8 is tip of index finger
                x2, y2 = lmList[12][1:]  # 12 is tip of middle finger

                # Check which fingers are up
                fingers = detector.fingersUp()

                # If Selection Mode - Two finger are up
                if fingers[1] and fingers[2]:
                    xp, yp = 0, 0
                    print("Selection Mode")

                    # Checking for clicks
                    if y1 < 120:
                        if 223 < x1 < 309:
                            header = overlayList[0]
                            drawColor = (255, 255, 255)
                        elif 348 < x1 < 434:
                            header = overlayList[1]
                            drawColor = (49, 49, 255)
                        elif 473 < x1 < 559:
                            header = overlayList[2]
                            drawColor = (255, 182, 56)
                        elif 598 < x1 < 684:
                            header = overlayList[3]
                            drawColor = (99, 191, 0)
                        elif 723 < x1 < 809:
                            header = overlayList[4]
                            drawColor = (196, 102, 255)
                        elif 848 < x1 < 934:
                            header = overlayList[5]
                            drawColor = (89, 222, 255)
                        elif 973 < x1 < 1059:
                            header = overlayList[6]
                            drawColor = (235, 23, 94)
                        elif 1098 < x1 < 1280:
                            header = overlayList[7]
                            drawColor = (0, 0, 0)
                    # draw rectangle if selection mode
                    cv2.rectangle(
                        img, (x1, y1 - 25), (x2, y2 + 25), drawColor, cv2.FILLED
                    )

                # If Drawing Mode - Index finger is up
                if fingers[1] and fingers[2] == False:

                    # draw circle if drawing mode
                    cv2.circle(img, (x1, y1), 15, drawColor, cv2.FILLED)

                    print("Drawing Mode")

                    if xp == 0 and yp == 0:
                        xp, yp = x1, y1  # draw point at the start

                    # if color is black (meaning if its eraser)
                    if drawColor == (0, 0, 0):
                        cv2.line(img, (xp, yp), (x1, y1), drawColor, eraserThickness)
                        cv2.line(
                            imgCanvas, (xp, yp), (x1, y1), drawColor, eraserThickness
                        )
                    # else if its not the eraser
                    else:
                        cv2.line(img, (xp, yp), (x1, y1), drawColor, brushThickness)
                        cv2.line(
                            imgCanvas, (xp, yp), (x1, y1), drawColor, brushThickness
                        )

                    xp, yp = x1, y1

                # first creating a gray image (basically converting `imgCanvas` to gray image)
            imgGray = cv2.cvtColor(imgCanvas, cv2.COLOR_BGR2GRAY)

            # converting it to binary image and inverse it
            _, imgInv = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)

            # convert back to BGR
            imgInv = cv2.cvtColor(imgInv, cv2.COLOR_GRAY2BGR)

            # adding our original image with the inverse image
            img = cv2.bitwise_and(img, imgInv)  # using AND operation
            img = cv2.bitwise_or(img, imgCanvas)  # using OR operation

            # Setting the header image
            img[0:120, 0:1280] = (
                header  # height is from 0 to 120 and width 0 to 1280 (thats our headers size)
            )

            # Display the frame in Streamlit
            frame_placeholder.image(img, channels="BGR")

        cap2.release()
        cv2.destroyAllWindows()

    # Display the "Start Virtual Paint" button only if the webcam is not already running
    if not stop_requested2:
        if start_button.button("Enable Gesture Control", key="start_button"):
            start_button.empty()  # Remove the start button
            stop_button_placeholder.empty()  # Clear the stop button placeholder
            start_virtual_paint()  # Start the virtual mouse detection

elif selected == "Contact":
    # Title of the Contact Page
    st.title("Get in Touch with Me! 💬")

    # Introductory text
    st.markdown(
        """
    I'd love to hear from you! Whether you have questions, feedback, or collaboration ideas, feel free to reach out. Please fill in the form below and I'll get back to you as soon as possible! 🚀
    """
    )

    contact_form = """
        <div class="background">
        <div class="container">
          <div class="screen">
            <div class="screen-header">
              <div class="screen-header-left">
                <div class="screen-header-button close"></div>
                <div class="screen-header-button maximize"></div>
                <div class="screen-header-button minimize"></div>
              </div>
              <div class="screen-header-right">
                <div class="screen-header-ellipsis"></div>
                <div class="screen-header-ellipsis"></div>
                <div class="screen-header-ellipsis"></div>
              </div>
            </div>
            <form action="https://formspree.io/f/mpwzwrnv" method="POST">
              <div class="screen-body">
                <div class="screen-body-item left">
                  <div class="app-title">
                    <span>CONTACT</span>
                    <span>US</span>
                  </div>
                  <div class="app-contact">CONTACT INFO : +91 750 698 4906</div>
                </div>
                <div class="screen-body-item">
                  <div class="app-form">
                    <div class="app-form-group">
                      <input name="name" class="app-form-control" placeholder="NAME" value="Mohd Faiz Khan">
                    </div>
                    <div class="app-form-group">
                      <input name="email" class="app-form-control" placeholder="EMAIL">
                    </div>
                    <div class="app-form-group">
                      <input name="number" class="app-form-control" placeholder="CONTACT NO">
                    </div>
                    <div class="app-form-group message">
                      <input name="message" class="app-form-control" placeholder="MESSAGE">
                    </div>
                    <div class="app-form-group buttons">
                      <button type="submit" class="app-form-button">SEND</button>
                    </div>
                  </div>
                </div>
              </div>
            </form>

          </div>
        </div>
        </div>
    """

    st.markdown(contact_form, unsafe_allow_html=True)

    # use local css file
    def local_css(filename):
        with open(filename) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    local_css("form_style.css")

    # Additional text
    st.markdown(
        """
    Or, if you'd prefer, you can connect with me on my professional networks: 

    - [![LinkedIn](https://img.icons8.com/color/48/000000/linkedin.png) **LinkedIn**](https://www.linkedin.com/in/yourprofile) — Let's network and grow together! 🤝
    - [![GitHub](https://img.icons8.com/ios-glyphs/30/000000/github.png) **GitHub**](https://github.com/yourusername) — Check out my projects and code! 💻
    """
    )

    # Closing message
    st.markdown(
        """
    Looking forward to connecting with you! 😊
    """
    )
