# Drop impact force measured with Piezo element and distance sensor
Measuring high speed cocoa butter crystal- melt suspension droplet deposition onto chocolate surfaces. 

- Bachelors Thesis
- Python data analyis

## Summary
- Distance Sensor(DS)-Piezo Set-up callibration through Texture Analyser 


#DS - Piezo Set-up Callibration 
##0. Callibration Piezo element Fleximibity constant

Stain-Stress curve: Counter force (F) recorded by TA during calibration as a function of the live deflection (W) of the piezo element in mm. A refers to the area of the TA application in m^2. h is the thickness of the piezo element in mm.
![Flex Constant](https://user-images.githubusercontent.com/88829879/131498651-096cc177-3f5e-4bea-ad69-3145b205d367.png |width=400)

##1. Turning distance sensor (DS) voltage output to Piezo maximum deflection
- Requires deformation rate to be determined

The minimum DS voltage as a function of velocity, at distances 0.001, 0.005, 0.010, 0.015, 0.020 and 0.025 mm. 
Used to calculate he distance traveled at a theoretical deformation rate of 0.0 mm/s
![Figure_1](https://user-images.githubusercontent.com/88829879/131498713-66c6c896-b55c-4676-984a-d4f7689712c7.png)

The minimum voltage as a function of distance, at velocities 0.0,0.1, 0.3, 0.5, 0.7, 0.9, 1.5 and 2.0 mm/s. Original data points and the y-intercepts of the linear regressions are also included. * refers to theoretical values.
![Figure_2](https://user-images.githubusercontent.com/88829879/131498712-431dec83-94bd-4de5-bcc7-a15814ff2c3e.png)
d = (V - y_{d=0}) / -9.82

The y-intercept voltage as a function of velocity
![Figure_3](https://user-images.githubusercontent.com/88829879/131498709-7409149f-febd-4ce1-952a-acab071fe6f8.png)
Gives calllibration line:
y_{d = 0} = v * -0.96821 -0.60860

2. Turing DS signal slope into Piezo deofmation rate
The DS calibration signal slope as a function of distance, at velocities ,0.1, 0.3, 0.5, 0.7, 0.9, 1.5 and 2.0 mm/s.
![Figure_4](https://user-images.githubusercontent.com/88829879/131498706-ad6893e4-5204-4ecd-8990-f9f1e7692b47.png)

The DS calibration signal slope as a function of velocity, at distances 0.0* ,0.001, 0.005, 0.010, 0.015, 0.020 and 0.025 mm. Original data points and the y-intercepts calculated through of the linear regressions of graph above are also included. * refers to theoretical values.
![Figure_5](https://user-images.githubusercontent.com/88829879/131498695-6298ed0d-2c8e-470e-a389-f761f789049f.png)




