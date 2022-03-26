# Virtual-Clothes-Try-on-System-with-sizes
<h3> System Overview </h3>
Web-based virtual clothes try-on system using face detection and alpha blending.
The main purpose of this system is to make users virtually wearing the selected clothes from web interface. 
The system is accessible as long as the devices such as computer or laptop has a web-camera. 
No special devices such as depth sensors cameras, Microsoft Kinect, etc. are required. 
Moreover, it allows for real time dressing up. <br>

<h3>How this system works? </h3>
There is a web user interface for users to be able to choose the desired sizes such as small(S), medium(M), large(L), etc. and the given categories of clothes such as men wears, women blouses , mini dresses, etc. 
The input image of the user getting from the webcam is preprocessed by converting RGB to gray scale image. 
Face detection method is used to know the user’s location. Among various face detection methods, Haar-features based face detection method is applied for real time executing and simplicity. 
Based on the detected face bounding box metrics, the position of the use’s upper body is calculated. 
The clothing image is then resized with the size of the user’s body. 
Finally, one of the image compositing techniques called alpha blending is applied to superimpose the clothing item over the user’s body.
<br>

<h3> Used Technologies </h3>
<li>Haar-features based face detection </li>
<li> Image compositing techniques, alpha blending </li>
<li> Flask framework for web  </li>
