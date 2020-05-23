import sys
import cv2
import os
import time
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5 import QtWidgets, uic
import numpy as np

import matplotlib

from sys import platform as sys_pf
if sys_pf == 'darwin':
    import matplotlib
    matplotlib.use("TkAgg")

from matplotlib import pyplot as plt
from numpy.linalg import inv

import time
import threading


path = os.getcwd()
qtCreatorFile = path + os.sep + "mainwindow.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile) 

imgpath = path + os.sep + "CameraCalibration"
imglist = os.listdir(imgpath)
imglistd = [i[:-4] for i in imglist]
imglistd = np.sort(np.array(imglistd).astype('int'))
imgSortedList = [format(i)+".bmp" for i in imglistd]

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.onBindingUI()

        self.imgSortedList = imgSortedList
        self.selected_img = self.imgSortedList[0]
        print(self.selected_img)

        self.objpoints = []
        self.imgpoints = []

        self.gray_imgs = []
        self.color_imgs = []

        # Camera parameter
        self.RMS = None
        self.camera_matrix = []
        self.distortion_coefficients = []
        self.rotation_matrix = []

        # pyramid
        self.pyramid_img = []

        # pre-read imgs in memory as array
        self.read_img()
        

    def read_img(self):
        for i in range(len(self.imgSortedList)):
            print(imgpath + os.sep + self.imgSortedList[i])
            img = cv2.imread(imgpath + os.sep + self.imgSortedList[i])
            gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
            self.color_imgs.append(img)
            self.gray_imgs.append(gray)

    def onBindingUI(self):
        self.bt_find_corners.clicked.connect(self.on_bt_find_corners_click)
        #self.bt_intrinsic.clicked.connect(self.on_bt_find_intrinsic_click)
        self.comboBox.addItems(imgSortedList)
        self.comboBox.activated[str].connect(self.comboBox_onChanged) 
        self.bt_cancel.clicked.connect(self.on_bt_cancel_click)

        self.bt_intrinsic.clicked.connect(self.on_bt_intrinsic_click)
        self.bt_distortion.clicked.connect(self.on_bt_distortion_click)
        self.bt_extrinsic.clicked.connect(self.on_bt_extrinsic_click)
        self.bt_augmented_reality.clicked.connect(self.on_bt_augmented_reality_click)

        self.bt_rot_scale_translate.clicked.connect(self.on_bt_rot_scale_translate_click)

    def on_bt_find_corners_click(self):
        find_corner_img = self.find_imgs_corner()
        #plt.figure(figsize=(10,10))
        for i in range(len(find_corner_img)):
            # plt.subplot(4,4,i)
            # plt.imshow(find_corner_img[i])
            t = threading.Thread(target = self.diaplay_imgs(find_corner_img[i],i))
            t.start()
        # plt.savefig(path + "/result.jpg")
        # self.diaplay_imgs(path + "/result.jpg")
        



    def on_bt_cancel_click(self):
        sys.exit(app.exec_())

    def on_bt_intrinsic_click(self):
        if len(self.camera_matrix) == 0:
            self.camera_calibration()
        print ("Intrinsic matrix:\n", self.camera_matrix)

    def on_bt_distortion_click(self):
        #print(self.distortion_coefficients)
        if len(self.distortion_coefficients) == 0 :
            self.camera_calibration()
        print ("Distortion matrix:\n", self.distortion_coefficients)

    def on_bt_extrinsic_click(self):
        if len(self.distortion_coefficients) == 0 :
            self.camera_calibration()
        #print(self.selected_img[:-4])
        idx = self.selected_img[:-4]
        print ("Extrinsic matrix of img "+idx+" :\n", self.rotation_matrix[int(idx)-1])

    def on_bt_rot_scale_translate_click(self):
        try:
            angel = int(self.lineEdit_angle.text())
        except:
            angel = 0

        try:
            scale = int(self.lineEdit_scale.text())
        except:
            scale = 1.0

        try:
            tx = int(self.lineEdit_tx.text())
        except:
            tx = 0
        
        try:
            ty = int(self.lineEdit_ty.text())
        except:
            ty = 0

        imgE = cv2.imread(path + os.sep + "OriginalTransform.png")

        R = cv2.getRotationMatrix2D((130,125),angel,scale)

        rows,cols = imgE.shape[:2]
        H = np.float32([[1,0,tx],[0,1,ty]])
        res = cv2.warpAffine(imgE,R,(cols,rows))
        res = cv2.warpAffine(res,H,(cols,rows))

        t = threading.Thread(target = self.diaplay_imgs(res,0))
        t.start()
        #print(angel)

    def comboBox_onChanged(self,text):
        self.selected_img = text

    def diaplay_imgs(self, imgs, idx):
        leng = len(imgs)
        #plt.figure(figsize=(10,10))
        #for i in range(leng):
        cv2.imshow('img'+format(idx+1),imgs)
        cv2.waitKey(0)
        # time.sleep(5)
        cv2.destroyAllWindows()
        #plt.subplot(2,int(leng/2),i)
        #plt.imshow(imgs)

    def camera_calibration(self):
        if len(self.objpoints) == 0 :
            self.find_imgs_corner()
        ret, mtx, dist, rvecs, tvecs  = cv2.calibrateCamera(self.objpoints, self.imgpoints, self.gray_imgs[0].shape[::-1],None,None)
        self.RMS = ret
        self.camera_matrix = mtx
        self.distortion_coefficients = dist.ravel()
        """
        # rvecs is rotation vector, not the rotation matrix
        # tvecs is translation vector
        Vr = np.array(rvecs)
        Tr = np.array(tvecs)
        extrinsics = np.concatenate((Vr, Tr), axis=1).reshape(-1,6)
        """
        
        #print(np.array(rvecs).shape)
        # rt,_ = cv2.Rodrigues(np.array(rvecs)[0])

        

        # Tr = np.array(tvecs)
        # #rtt = np.append(rt.T, Tr[0])

        # ex = np.concatenate((rt, Tr[0]),axis = 1)

        # print("RT : \n",rt.T)
        # print("R : \n",rt)
        # #print("RTT : \n",rtt)
        # print("TR : \n",Tr[0].T[0])
        # print("ex : \n",ex)
        #print(dist)
        #print(np.array(rt).shape)
        Vr = np.array(rvecs)
        Tr = np.array(tvecs)
        for i in range(len(Tr)):
            rt,_ = cv2.Rodrigues(Vr[i])

            ex = np.concatenate((rt, Tr[i]),axis = 1)
            self.rotation_matrix.append(ex)
        
        # extrinsics = np.concatenate((Vr, Tr), axis=1).reshape(-1,6)
        # print(extrinsics)

    def find_imgs_corner(self):

        find_corner_img = []

        for i in range(len(self.imgSortedList)):
            criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 500, 0.001)

            objp = np.zeros((8*11,3), np.float32)
            objp[:,:2] = np.mgrid[0:11,0:8].T.reshape(-1,2)

            img = self.color_imgs[i]
            #print(img.shape)
            gray = self.gray_imgs[i]
            #print(gray.shape)

            ret, corners = cv2.findChessboardCorners(gray, (11,8),None)
            #print(ret)

            if ret == True:
                self.objpoints.append(objp)
                #print(np.array(corners).shape)
                corners2 = cv2.cornerSubPix(gray,corners,(11,8),(-1,-1),criteria)
                self.imgpoints.append(corners2)

                # Draw and display the corners
                img = cv2.drawChessboardCorners(img, (11,8), corners2,ret)
                img = cv2.resize(img, (600, 600)) 
                find_corner_img.append(img)
            else:
                img = cv2.resize(img, (600, 600)) 
                find_corner_img.append(img)
        return find_corner_img


    def on_bt_augmented_reality_click(self):
        pyramid_imgs = self.caculate_pyramid()

        print(len(pyramid_imgs))

        for i in range(len(pyramid_imgs)):
            # plt.subplot(4,4,i)
            # plt.imshow(find_corner_img[i])
            t = threading.Thread(target = self.diaplay_imgs(pyramid_imgs[i],i))
            t.start()

    def caculate_pyramid(self):
        pyramid_imgs = []
        if len(self.distortion_coefficients) == 0 :
            self.camera_calibration()

        for i in range(10):
            img = self.color_imgs[i].copy()
            _, corners = cv2.findChessboardCorners(self.gray_imgs[i], (11,8),None)
            #print(tuple(corners[0][0]))
            ################################################################################################
            p1 = corners[-1][0].reshape(len(corners[-1][0]),1)
            p1 = np.concatenate((p1, np.array([[1],[1]])),axis = 0)

            p2 = corners[-2][0].reshape(len(corners[-2][0]),1)
            p2 = np.concatenate((p2, np.array([[1],[1]])),axis = 0)

            p3 = corners[-12][0].reshape(len(corners[-12][0]),1)
            p3 = np.concatenate((p3, np.array([[1],[1]])),axis = 0)

            p4 = corners[-13][0].reshape(len(corners[-13][0]),1)
            p4 = np.concatenate((p4, np.array([[1],[1]])),axis = 0)

            p_h = corners[-11][0].reshape(len(corners[-11][0]),1)
            p_h = np.concatenate((p_h, np.array([[1],[1]])),axis = 0)

            p_v = corners[-82][0].reshape(len(corners[-82][0]),1)
            p_v = np.concatenate((p_v, np.array([[1],[1]])),axis = 0)
            ################################################################################################
            rt = np.concatenate((self.camera_matrix@self.rotation_matrix[i], np.array([[0.,0.,0.,1.]])),axis = 0)

            x1 = np.linalg.inv(rt) @ p1
            x2 = np.linalg.inv(rt) @ p2
            x3 = np.linalg.inv(rt) @ p3
            #x4 = np.linalg.inv(rt) @ p4
            x4 = x1 + (x3-x1) + (x2-x1)

            ################################################################################################
            x5 = x1 + (x1-x4) 
            x6 = x2 + (x2-x4) 
            x7 = x3 + (x3-x4) 

            #print(x3)
            #print(x2)
            vec = np.cross((p_v-x5).T[0][:3], (p_h-x5).T[0][:3])

            vec = vec /(vec**2).sum()**0.5

            #print("ves+\n",vec)
            #print("ves\n",500*(x2-x1).T[0][:3])
            vec = np.concatenate((vec.reshape(len(vec),1), np.array([[1.]])),axis = 0)
            #print(((x3-x1).T[0][:3]**2).sum()**0.5)
            center = (x4+x5+x6+x7)/4
            x8 = center + vec*((x3-x1).T[0]**2).sum()**0.5 + 0.4*(x2-x1)
            x8[3][0] = 1
            #print(x8)
            ################################################################################################
            p1 = rt@x1
            p1 = p1.reshape(1,len(p1))[0][:2]
            
            p2 = rt@x2
            p2 = p2.reshape(1,len(p2))[0][:2]

            p3 = rt@x3
            p3 = p3.reshape(1,len(p3))[0][:2]

            p3 = rt@x3
            p3 = p3.reshape(1,len(p3))[0][:2]

            p4 = rt@x4
            p4 = p4.reshape(1,len(p4))[0][:2]

            p5 = rt@x5
            p5 = p5.reshape(1,len(p5))[0][:2]

            p6 = rt@x6
            p6 = p6.reshape(1,len(p6))[0][:2]

            p7 = rt@x7
            p7 = p7.reshape(1,len(p7))[0][:2]

            p8 = rt@x8
            #print("p8\n",p8)
            p8 = p8.reshape(1,len(p8))[0][:2]
            ################################################################################################

            #print("P1\n",p1)

            #img = cv2.circle(img,tuple(p1.astype('int')), 30, (0, 255, 255), 3)
            #img = cv2.circle(img,tuple(p2.astype('int')), 30, (0, 255, 255), 3)
            #img = cv2.circle(img,tuple(p3.astype('int')), 30, (0, 255, 255), 3)
            # img = cv2.circle(img,tuple(p4.astype('int')), 30, (0, 255, 255), 3)
            # img = cv2.circle(img,tuple(p5.astype('int')), 30, (0, 255, 255), 3)
            # img = cv2.circle(img,tuple(p6.astype('int')), 30, (0, 255, 255), 3)
            # img = cv2.circle(img,tuple(p7.astype('int')), 30, (0, 255, 255), 3)
            # img = cv2.circle(img,tuple(p8.astype('int')), 30, (0, 255, 255), 3)

            img = cv2.line(img, tuple(p4.astype('int')), tuple(p6.astype('int')), (0, 0, 255), 10)
            img = cv2.line(img, tuple(p6.astype('int')), tuple(p5.astype('int')), (0, 0, 255), 10)
            img = cv2.line(img, tuple(p5.astype('int')), tuple(p7.astype('int')), (0, 0, 255), 10)
            img = cv2.line(img, tuple(p7.astype('int')), tuple(p4.astype('int')), (0, 0, 255), 10)

            img = cv2.line(img, tuple(p8.astype('int')), tuple(p4.astype('int')), (0, 0, 255), 10)
            img = cv2.line(img, tuple(p8.astype('int')), tuple(p5.astype('int')), (0, 0, 255), 10)
            img = cv2.line(img, tuple(p8.astype('int')), tuple(p6.astype('int')), (0, 0, 255), 10)
            img = cv2.line(img, tuple(p8.astype('int')), tuple(p7.astype('int')), (0, 0, 255), 10)

            #img = cv2.line(img, tuple(p1.astype('int')), tuple(p8.astype('int')), (0, 0, 255), 10)
            
            
            img = cv2.resize(img, (600, 600)) 
            pyramid_imgs.append(img)
        return pyramid_imgs
        # t = threading.Thread(target = self.diaplay_imgs(img,0))
        # t.start()
        # point = []
        # self.pyramid_img
        # self.color_imgs
        
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
