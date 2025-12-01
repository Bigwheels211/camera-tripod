This is code to run on a Raspberry Pi(although it could be adapted to run on any machine). It is currently a WIP, and I will continue to improve it and add more functionality. 
The Raspberry Pi should be connected to 2 motors, one for the rotation axis and one for the tilt axis.
A camera on the end is fed into the Raspberry Pi, and the Pi runs a computer vision algorithm to track different things. 
Currently, the vision algorithm is only set up to track faces, but more functionality will be added later. 
The Pi hosts a web server on port 5000, which can be used to view what the camera is seeing and start and stop the facial tracking. 
Functionality will also be added to take pictures(and hopefully videos) from the camera, which can be downloaded from the web server. 
