SewKinect
=========

Final Hackbright Project

SewKinect was inspired by an absense of basic pattern generation software for sewers. Pattern drafting is key to custom-fit garments and costumes and relies on a geometric understanding three-dimensional body curves. Traditionally, patterns are drafted for individuals on paper at full scale, a huge inconvenience of time and space. SewKinect aims to streamline bespoke pattern development by creating a digital pipeline from measurements to printable pdf slopers.

###Video Demo
<div align="center">
<iframe width="420" height="315" src="//www.youtube.com/embed/Qnv36XxjC98?rel=0&amp;controls=0&amp;showinfo=0" frameborder="0" allowfullscreen></iframe>
</div>

SewKinect consists of a Kinect/PyGame app and a Flask application. The Kinect app posts scan data to the Flask server. SewKinect was developed on OSX and the technology required is as follows: 

- libusb
- libfreenect
- OpenNI
- SensorKinect
- NITE
- PyOpenNI
- Flask
- Jinja2
- PyCairo
- Numpy
- Scipy

Also relies on default Python libraries listed below: 

- httplib
- urllib
- json
- math
- pickle
- base64
- datetime


Kinect Install Instructions
==================
1. libusb 
```sh
  homebrew libusb
```
2. libfreenect 
```sh
  homebrew libfreenect
```
3. OpenNI - Available at https://mega.co.nz/#!Hc5kwAiZ!uJiLY4180QGXjKp7sze8S3eDVU71NHiMrXRq0TA7QpU

4. SensorKinect - git clone https://github.com/avin2/SensorKinect.git
    Uncompress Bin/SensorKinect093-Bin-MacOSX-v*tar.bz2.
```sh
 $ sudo ./install.sh.
```
5. NITE - Available at https://mega.co.nz/#!nZYwgJiQ!m091FXc4U6GwjRfpHK-puPvBjkHdWc6KmQH-_RzXfOw.

 ```sh
 $ sudo ./install.sh.
 $ cd ~/Kinect/nite-bin-macosx-v1.5.0.2/Data.
 $ cp *.xml ../../SensorKinect/Data.
```
6. PyOpenNI - 
 
 ```sh
$ git clone https://github.com/jmendeth/PyOpenNI.git
$  mkdir PyOpenNI-build
$  cd PyOpenNI-build
$ cmake ../PyOpenNI
$ cp openni.so .../python2.7/site-packages/
```
  
###For Install Reference: 
http://justinfx.com/2012/06/21/getting-started-with-xbox-360-kinect-on-osx/
http://developkinect.com/resource/mac-os-x/install-openni-nite-and-sensorkinect-mac-os-x
http://blog.nelga.com/setup-microsoft-kinect-on-mac-os-x-10-9-mavericks/

###Important Directory Contents: 
- /app.py - main Flask applicaiton
- /calculations.py - Kinect point cloud processing 
- /drafting.py - Cairo pattern drafting instructions 
- /kinect/kinect_obj.py - Kinect application
- /kinect/ - also contains pickled Kinect data for proofing if a Kinect is not available
- /static/JSON/ - standard US pattern sizes in JSON format
- /static/patterns/ - PDF pattens are stored here 

In order to get accurate measurements from the Kinect, users should stand ~5ft away from the camera with a clear foreground. Wearing tight clothing that constrasts the background also helps. 

Have fun! Send questions or comments to @giantspatula on Twitter. 
