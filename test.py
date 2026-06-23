import cv2       
from deepface import DeepFace
                                   #helps to open web cam 
cap = cv2.VideoCapture(0)
print("Starting the WEBCAM.... PRESS Q to quit :) ")
while True:
    ret,frame = cap.read() #here ret mean return value -> true or false
    if not ret:
        break
    try:
        result  = DeepFace.analyze(frame, actions=["emotion"], enforce_detection = False)
        emotion = result[0]["dominant_emotion"]
        cv2.putText(frame,emotion, (50,50), cv2.FONT_HERSHEY_SIMPLEX,3,(0,255,0), 5)
    except:
        pass
    cv2.imshow("Emotion Detector", frame)
    cv2.imshow("My Webcam", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'): # wait key means here to waits b/w 1ms every frame 
        break
cap.release()              #terminates web ca politely
cv2.destroyAllWindows()    #closes all windows from cv 