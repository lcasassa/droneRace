import numpy as np
import cv2


def main():
    #cap = cv2.VideoCapture(0)
    cap = cv2.VideoCapture('/home/lcasassa/Drone/YDXJ0225.avi')

    cap.set(0, 25000)
    cv2.namedWindow('image')

    def nothing(x):
        pass

    # create trackbars for color change
    cv2.createTrackbar('pasto_hm', 'image', 0, 255, nothing)
    cv2.createTrackbar('pasto_hM', 'image', 0, 255, nothing)

    cv2.createTrackbar('pasto_sm', 'image', 0, 255, nothing)
    cv2.createTrackbar('pasto_sM', 'image', 0, 255, nothing)

    cv2.createTrackbar('pasto_vm', 'image', 0, 255, nothing)
    cv2.createTrackbar('pasto_vM', 'image', 0, 255, nothing)

    cv2.createTrackbar('pasto_am', 'image', 0, 60000, nothing)

    cv2.createTrackbar('hm', 'image', 0, 255, nothing)
    cv2.createTrackbar('hM', 'image', 0, 255, nothing)

    cv2.createTrackbar('sm', 'image', 0, 255, nothing)
    cv2.createTrackbar('sM', 'image', 0, 255, nothing)

    cv2.createTrackbar('vm', 'image', 0, 255, nothing)
    cv2.createTrackbar('vM', 'image', 0, 255, nothing)

    cv2.createTrackbar('am', 'image', 0, 12000, nothing)
    cv2.createTrackbar('aM', 'image', 0, 12000, nothing)


    # Pasto
    cv2.setTrackbarPos('pasto_hm','image', 27)
    cv2.setTrackbarPos('pasto_hM','image', 120)

    cv2.setTrackbarPos('pasto_sm','image', 97)
    cv2.setTrackbarPos('pasto_sM','image', 239)

    cv2.setTrackbarPos('pasto_vm','image', 68)
    cv2.setTrackbarPos('pasto_vM','image', 208)

    cv2.setTrackbarPos('pasto_am','image', 70000)

    # Cono
    cv2.setTrackbarPos('hm','image', 131)
    cv2.setTrackbarPos('hM','image', 255)

    cv2.setTrackbarPos('sm','image', 228)
    cv2.setTrackbarPos('sM','image', 255)

    cv2.setTrackbarPos('vm','image', 171)
    cv2.setTrackbarPos('vM','image', 255)

    cv2.setTrackbarPos('am','image', 5)
    cv2.setTrackbarPos('aM','image', 10000)

    count_to_reset = 0
    #while(True):
    while(cap.isOpened()):
        if count_to_reset <= 0:
            cap.set(0, 55000)
            count_to_reset = 50*40
        count_to_reset -= 1


        # Capture frame-by-frame

        ret, frame = cap.read()

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Our operations on the frame come here
        #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Display the resulting frame
        #cv2.imshow('frame', hsv)
        #if cv2.waitKey(1) & 0xFF == ord('q'):
        #    break

        pasto_hm = cv2.getTrackbarPos('pasto_hm','image')
        pasto_hM = cv2.getTrackbarPos('pasto_hM','image')

        pasto_sm = cv2.getTrackbarPos('pasto_sm','image')
        pasto_sM = cv2.getTrackbarPos('pasto_sM','image')

        pasto_vm = cv2.getTrackbarPos('pasto_vm','image')
        pasto_vM = cv2.getTrackbarPos('pasto_vM','image')

        # define range of blue color in HSV
        lower_pasto = np.array([pasto_hm,pasto_sm,pasto_vm])
        upper_pasto = np.array([pasto_hM,pasto_sM,pasto_vM])

        # Threshold the HSV image to get only blue colors
        mask_pasto = cv2.inRange(hsv, lower_pasto, upper_pasto)

        # Bitwise-AND mask and original image
        res_pasto = cv2.bitwise_and(frame,frame, mask= mask_pasto)


        contours, hier = cv2.findContours(mask_pasto.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

        pasto_am = cv2.getTrackbarPos('pasto_am','image')

        #bigest_area = amg
        for cnt in contours:
            if pasto_am <= cv2.contourArea(cnt):
                biggest_area = cnt
                cv2.drawContours(frame, [cnt], 0, (0,255,0), 2)
                #cv2.drawContours(res_pasto, [cnt], 0, 255, -1)
                break

        mask_pasto = np.zeros(frame.shape[:-1],np.uint8)
        cv2.drawContours(mask_pasto,[biggest_area],0,255,-1)
        pasto = cv2.bitwise_and(frame,frame, mask= mask_pasto)



        hm = cv2.getTrackbarPos('hm','image')
        hM = cv2.getTrackbarPos('hM','image')

        sm = cv2.getTrackbarPos('sm','image')
        sM = cv2.getTrackbarPos('sM','image')

        vm = cv2.getTrackbarPos('vm','image')
        vM = cv2.getTrackbarPos('vM','image')

        lower_cono = np.array([hm,sm,vm])
        upper_cono = np.array([hM,sM,vM])
        mask = cv2.inRange(pasto, lower_cono, upper_cono)

        res = cv2.bitwise_and(pasto,pasto, mask= mask)

        contours0, hier1 = cv2.findContours(mask.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        contours = [cv2.approxPolyDP(cnt3, 2, True) for cnt3 in contours0]

        #contours = []
        #for cnt in contours1:
        #    if 4 <= cnt.size <= 18:
        #        contours.append(cnt)

        moments = []
        for cnt in contours:
            m = cv2.moments(cnt)
            if m['m00'] > 0:
                cx = int(m['m10']/m['m00'])
                cy = int(m['m01']/m['m00'])
                moments.append([cx, cy])

        if len(moments) <= 0:
            continue

        # drawing fist one
        moments.sort(key = lambda p: -p[1])
        cv2.circle(frame, (moments[0][0], moments[0][1]), 10, (0,255,0), -1)

        moments_copy = moments[:]
        moments_order = []
        moments_order.append(moments_copy.pop(0))
        while len(moments_copy) > 0:
            from math import sqrt

            moments.sort(key = lambda p: sqrt((p[0] - moments_copy[-1][0])**2 + (p[1] - moments_copy[-1][1])**2))
            moments_order.append(moments_copy.pop(0))

        size = 10
        for m in moments_order:
            cv2.circle(frame, (m[0], m[1]), size, (255,0,0), -1)
            #size += 1

        """
        size = 1
        for m in moments:
            cv2.circle(frame, (m[0], m[1]), size, (0,0,255), -1)
            size += 1
        """



        #contours.append(np.array(moments, dtype=np.int32))

        """
        moments = np.array(moments)


        model = LinearLeastSquaresModel([0],[1],debug=True)
        ransac_fit, ransac_data = ransac(moments, model,
                                         5, 1000, 7e3, 6, # misc. parameters
                                         debug=True,return_all=True)

        points = moments[ransac_data['inliers'],:]

        for i in xrange(len(points)-1):
            cv2.line(frame,(points[i][0], points[i][1]), (points[i+1][0], points[i+1][1]),(255,0,0),5)
        """


        am = cv2.getTrackbarPos('am','image')
        aM = cv2.getTrackbarPos('aM','image')


        for cnt in contours:
            #x,y,w,h = cv2.boundingRect(cnt)

            if am <= cv2.contourArea(cnt) <= aM:
            #if am <= w*h and w*h <= aM:
                cv2.drawContours(frame, [cnt], 0, (0,255,0), 2)
                cv2.drawContours(res, [cnt], 0, (0,255,0), -1)
            else:
                cv2.drawContours(res, [cnt], 0, (0,0,255), -1)


        res_pasto_small = cv2.resize(res_pasto, (0,0), fx=0.3, fy=0.3)
        mask_pasto_small_grey = cv2.resize(mask_pasto, (0,0), fx=0.3, fy=0.3)
        mask_pasto_small = cv2.cvtColor(mask_pasto_small_grey, cv2.COLOR_GRAY2RGB)
        pasto_small = cv2.resize(pasto, (0,0), fx=0.3, fy=0.3)

        res_small = cv2.resize(res, (0,0), fx=0.3, fy=0.3)
        mask_small_grey = cv2.resize(mask, (0,0), fx=0.3, fy=0.3)
        mask_small = cv2.cvtColor(mask_small_grey, cv2.COLOR_GRAY2RGB)
        frame_small = cv2.resize(frame, (0,0), fx=0.3, fy=0.3)

        frame2 = np.concatenate((res_pasto_small,mask_pasto_small, pasto_small), axis=1)
        frame3 = np.concatenate((res_small,mask_small, frame_small), axis=1)
        frame4 = np.concatenate((frame2, frame3), axis=0)


        #cv2.imshow('res_pasto', res_pasto)
        #cv2.imshow('pasto', pasto)
        #cv2.imshow('res',res)
        cv2.imshow('frame',frame4)
        #cv2.imshow('mask',mask)
        out.write(frame)

        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
