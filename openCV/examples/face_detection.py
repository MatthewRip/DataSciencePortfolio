import cv2


face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')


img = cv2.imread("images/meh.jpg",cv2.IMREAD_GRAYSCALE)
img = cv2.resize(img,(640,640))

faces = face_cascade.detectMultiScale(img,1.1,4)

for (x,y,w,h) in faces:
    cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
    within_face = img[y:y+h, x:x+w]
    within_face_color = img[y:y+h, x:x+w]
    eyes = eye_cascade.detectMultiScale(within_face)
    for (ex,ey,ew,eh) in eyes:
        cv2.rectangle(within_face_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)



cv2.imshow("Output",img)
cv2.waitKey(0)