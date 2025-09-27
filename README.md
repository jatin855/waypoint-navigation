# waypoint-navigation
this project includes waypoint navigation using rpi4.0

drone is set on guided moded and rpi give commands that make the drone to fly.

first we have to run the script on ardupilot SITL which is simulation,

here,required packages in virtual environment:-
1. python 3.8.10( max)
2. dronekit 
3. mavproxy
4. dronekit-sitl
5. pymavlink - 2.4.43
### follow strps given below first to prevent any error--
Step: 01: Install the required packages: 
pip install dronekit dronekit-sitl mavproxy 

Step: 02: Fix the bug with Pymavlink:
a. Go to your site packages and open pymavlink folder
b. Open pymavutil.py file
c. Find the fucntion set_mode_apm and Comment out the following section: 

        self.mav.command_long_send(self.target_system,
        self.target_component,
        mavlink.MAV_CMD_DO_SET_MODE,
        0,
        mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED,
        mode,
        0,
        0,
        0,
        0,
        0)

d. Replace it by the following section and save the file: 

    self.mav.set_mode_send(self.target_system, 
                                       mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED,
                                       mode,
                                       )
                                   
### Now execute the following commands in different windows of terminal--

1.     dronekit-sitl copter--home = _<desired latitude>_,_<desired longitude>_,_<sea level>_,_<desired yaw>_

### to start a copter simulation
### Open a TCP/UDP port so that tools like Mission Planner, MAVProxy, or your DroneKit Python script can connect to this simulated drone. generaly that port is 5760
### TCP and UDP ### --
TCP and UDP are two important types of communication protocols used to send data between computers or devices over a network — like your PC talking to the drone simulator.
🌐 1. TCP (Transmission Control Protocol)

📦 Connection-based → It first establishes a reliable connection (like a phone call) before sending data.

✅ Reliable → It checks for errors, ensures all data packets arrive in order, and resends any lost packets.

🐢 Slightly slower because of all the checking and handshaking.

👉 Example: When you browse a website or send a file, TCP is used so that nothing gets lost.

In drone simulation:

TCP is often used between SITL and your DroneKit script because you want commands and telemetry to be accurate and reliable.

🌊 2. UDP (User Datagram Protocol)

📡 Connectionless → No formal connection; it just sends packets (like throwing letters in the mail).

🚀 Faster → No error checking or packet order guarantee.

⚠️ Less reliable → Some packets may get lost or arrive out of order, but usually this is fine for real-time data.

👉 Example: Online gaming, live video streaming, or live telemetry — where speed matters more than 100% reliability.

In drone simulation:

UDP is often used to broadcast telemetry to multiple ground control stations or apps at once, because it’s fast and light.

2.     python -m MAVProxy.mavproxy --master tcp:127.0.0.1:5760 --sitl 127.0.0.1:5501 --out 127.0.0.1:14550 --out 127.0.0.1:14551 --out 127.0.0.1:14552
### This is used to start MAVProxy and connect it to the SITL simulator, while also forwarding the telemetry data to multiple outputs (like Mission Planner, QGroundControl, or other programs).
let's break it down:--
  > python -m MAVProxy.mavproxy ==> used to start mavproxy.

    a. mavproxy ==> it is tool(middleware) that converts dronekit commands (high level commands) to raw mavlink commands( low level commands).
    b. mavlink commands ==> commands that are given to drone.

  > --master tcp:127.0.0.1:5760 ==> tells MAVProxy where to connect to the vehicle.

    ## Here, it connects to the SITL drone running on your local computer (127.0.0.1 is localhost) on TCP port 5760.

  > --sitl 127.0.0.1:5501 ==> This tells MAVProxy that the SITL instance is running on port 5501.

        ## This lets MAVProxy communicate directly with SITL for some simulation-specific features (like changing location, environment, etc.) if needed.

  > --out 127.0.0.1:14551

      --out is used to forward the MAVLink telemetry data to other programs.Here, MAVProxy sends data via UDP to 127.0.0.1:14550
      
 when connection has setup correctly then run the script to give commands at port where vehicle is simulated( by default it is 5760).

3.       python --<script name>-- --connect udp 127.0.0.1: _<desired port of GCS>_ 

