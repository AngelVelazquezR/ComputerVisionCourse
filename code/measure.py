import cv2
import math


clickL_ix, clickL_iy = -1,-1 #left coords
clickR_ix, clickR_iy = -1,-1 #right coords
clickA_ix, clickA_iy = -1,-1 #cursor coords

#Coords of the reference object
clickRef_Ax, clickRef_Ay = -1,-1
clickRef_Dx, clickRef_Dy = -1,-1

pixDistance = 0
distanciapix = 0

cmValue=20
cx=640
cy=480


#Mouselistener
def clickListener(event, x, y, flags, param):
   
    #Global variables
    global clickL_ix,clickL_iy
    global clickR_ix,clickR_iy
    global clickA_ix,clickA_iy

    #LeftClick
    if event == cv2.EVENT_LBUTTONDOWN:
        clickL_ix = x
        clickL_iy = y
        
 
    #Right Click
    elif event == cv2.EVENT_RBUTTONDOWN:
        clickR_ix = x
        clickR_iy = y
        

    #Cursor position
    elif event == cv2.EVENT_MOUSEMOVE:
        clickA_ix = x
        clickA_iy = y


while(True):
    #get frame
    frame = cv2.imread("../img/cosas2.jpeg")

    #add the listener to the frame
    cv2.setMouseCallback("Frame", clickListener, frame)
    #Frame,position,color,type,size,thickness
    cv2.drawMarker(frame, (cx,cy), (255,255,255), 0, 25, 1) #marcador de cruz

    #Show coords
    cv2.putText(frame,'X:', (0,20), cv2.FONT_HERSHEY_DUPLEX, 1,(255,255,255), 2)
    cv2.putText(frame,'Y:', (0,50), cv2.FONT_HERSHEY_DUPLEX, 1,(255,255,255), 2)
    cv2.putText(frame,str((clickA_ix-cx)), (30,20), cv2.FONT_HERSHEY_DUPLEX, 1,(255,255,255), 1)
    cv2.putText(frame,str((clickA_iy-cy)*-1), (30,50), cv2.FONT_HERSHEY_DUPLEX, 1,(255,255,255), 1)
    

    #Reference Object
    if clickRef_Ax >= 0 and clickRef_Dx >= 0:
        cv2.line(frame, (clickRef_Ax, clickRef_Ay), (clickRef_Dx, clickRef_Dy), (255,0,0), 5)
        
        ###################
        ## TO-DO CALCULATE PIXVALE PIX/CM

        #get x and y difference
        xsdif=clickRef_Ax-clickRef_Dx
        ysdif=clickRef_Ay-clickRef_Dy

        #get distance
        xp=math.pow(xsdif,2)
        yp=math.pow(ysdif,2)
        distanciapix=math.sqrt(xp+yp)
        #cm value per pixel
        pixValue=cmValue/distanciapix

        ###################

    #Measure Object
    if clickL_ix >= 0 and clickR_ix >= 0 and distanciapix > 0:
        cv2.line(frame, (clickL_ix, clickL_iy), (clickR_ix, clickR_iy), (255,255,0), 5)

        ###################
        ## TO-DO CALCULATE CM PIX*CM

        #get x and y difference
        xdif=clickL_ix-clickR_ix
        ydif=clickL_iy-clickR_iy

        #get pixel Distance
        xp=math.pow(xdif,2)
        yp=math.pow(ydif,2)
        distanciapix=math.sqrt(xp+yp)
        #get cm distance using pixel value
        distanciaCm=distanciapix*pixValue

        ###################
        
        #show results
        cv2.putText(frame,str(round(distanciaCm,2))+'cm', (round((clickR_ix+clickL_ix)/2),round((clickR_iy+clickL_iy)/2)),
                    cv2.FONT_HERSHEY_DUPLEX, .80,(0,255,255), 1)

    

    #Show a zoom of 40 pixels
    if clickA_ix > 40 and clickA_iy > 40:
        #[y1:y2,x1:x2]
        #Make a roi
        roi = frame[clickA_iy-40:clickA_iy+40,clickA_ix-40:clickA_ix+40]
        #resize zoom
        roi = cv2.resize(roi,(int(480),int(480)))
        cv2.drawMarker(roi, (240,240), (255,255,255), 0, 25, 1) #draw marker
        #show zoom frame
        cv2.imshow('Zoom',roi)


    #Show frame
    cv2.imshow('Frame',frame)
    #Get Keyboard key
    key = cv2.waitKey(1) & 0xFF

    if key == ord('a'):
        clickRef_Ax, clickRef_Ay = clickA_ix, clickA_iy

    if key == ord('d'):
        clickRef_Dx, clickRef_Dy = clickA_ix, clickA_iy

    if key == ord('q'):
        break

#Close frames
cap.release()
cv2.destroyAllWindows()
