<h1>DomStick</h1>

<p><strong>DomStick</strong> is a compact wireless console built for <strong>robotics and embedded projects</strong>.</p>
<p>
  It connects via <strong>Bluetooth</strong>, offering smooth, cable-free control through a
  <strong>PCB crafted to fit comfortably in your hands</strong> for better precision and handling.
</p>
<p>
  You can power DomStick either from the <strong>Arduino Nano jack</strong> or a <strong>DC socket</strong> with
  <strong>7–12V input</strong>. It’s equipped with a <strong>voltage divider</strong> to safely shift the Bluetooth
  <strong>Rx pin</strong> from <strong>5V to 3.3V logic</strong>, protecting the module while maintaining stable communication.
</p>

<p align="right">
  <img src="https://github.com/ahmedmamdouh32/DomStick/blob/master/Images/DomStick.png?raw=true"
       alt="DomStick Logo"
       width="300"
       height="228" />
</p>

<h2>Board Content</h2>
<ul>
  <li>Arduino Nano</li>
  <li>Joystick</li>
  <li>Four Push Buttons</li>
  <li>Bluetooth Module <strong>HC-05</strong></li>
  <li>DC Power Socket</li>
</ul>

<h2>Pins Connections</h2>
<table style="width: 200px; text-align: center;">
  <tbody>
    <tr><td colspan="2" align="center"><strong>Joystick</strong></td></tr>
    <tr><td>X-Axis →</td><td>A1</td></tr>
    <tr><td>Y-Axis ↑</td><td>A2</td></tr>
    <tr><td>Push Button</td><td>D8</td></tr>
    <tr><td colspan="2" align="center"><strong>Push Buttons</strong></td></tr>
    <tr><td>Top Button</td><td>D5</td></tr>
    <tr><td>Bottom Button</td><td>D3</td></tr>
    <tr><td>Left Button</td><td>D2</td></tr>
    <tr><td>Right Button</td><td>D4</td></tr>
    <tr><td colspan="2" align="center"><strong>Bluetooth</strong></td></tr>
    <tr><td>Tx</td><td>D10</td></tr>
    <tr><td>Rx</td><td>D9</td></tr>
    <tr><td>State</td><td>D7</td></tr>
    <tr><td>Enable</td><td>D6</td></tr>
  </tbody>
</table>

<h2>Turning DomStick into a Keyboard Controller</h2>
<p>
  To make <strong>DomStick</strong> act like a <strong>keyboard</strong> and control any PC game or application, we designed
  a system that translates the data sent via <strong>Bluetooth</strong> into standard
  <strong>HID (Human Interface Device)</strong> commands.
</p>
<p>
  Since the <strong>HC-05 Bluetooth module</strong> used on DomStick doesn’t natively support HID mode,
  we created a <strong>Python interface</strong> that bridges this gap. The Python script listens to the serial data
  coming from the DomStick through the selected <strong>COM port</strong> and converts each received signal into a
  corresponding <strong>keyboard action</strong>.
</p>

<p align="center">
  <img src="https://github.com/ahmedmamdouh32/DomStick/blob/master/Images/AppGUI.PNG?raw=true"
       alt="DomStick App GUI"
       width="400"
       height="464"
       style="border: 3px solid #0078D7; border-radius: 8px;" />
</p>

<p>
  A simple <strong>Graphical User Interface (GUI)</strong> is included to make the process user-friendly:
</p>
<ul>
  <li>Scan and select available Bluetooth COM ports.</li>
  <li>Connect to your DomStick wirelessly.</li>
  <li>Automatically map incoming joystick or button data to keyboard keys.</li>
</ul>

<p>
  Once connected, every command from DomStick — joystick movements or button presses —
  is instantly translated into keyboard inputs on your computer, allowing you to
  <strong>play games</strong>, <strong>control simulations</strong>, or even
  <strong>navigate applications</strong> as if DomStick were a real
  <strong>HID controller</strong>.
</p>

<h2>How the GUI Works</h2>
<p>
  The <strong>DomStick App GUI</strong> provides an easy way to connect your
  <strong>DomStick controller</strong> to your PC via Bluetooth.
</p>

<ol>
  <li>
    <strong>Enable Bluetooth</strong> on your computer before starting the app.
    <ul>
      <li>
        If the <strong>COM port list (ComboBox)</strong> appears empty, the app will prompt you to check
        your Bluetooth state — make sure it’s turned <strong>on</strong> and your
        <strong>DomStick</strong> is already paired.
      </li>
    </ul>
  </li>
  <li>
    Once the COM ports appear, you can <strong>select any available port</strong> from the list.
    <ul>
      <li>However, <strong>only one port</strong> corresponds to the actual DomStick Bluetooth connection.</li>
      <li>Even if a port connects successfully, it doesn’t necessarily mean it’s the correct one.</li>
    </ul>
  </li>
  <li>
    To confirm a <strong>successful connection</strong>, check the <strong>HC-05 Bluetooth module</strong> on your DomStick.
    <ul>
      <li>The <strong>LED indicator will stop blinking</strong> once a stable connection is established.</li>
    </ul>
  </li>
</ol>

<p align="center">
  <img src="https://github.com/ahmedmamdouh32/DomStick/blob/master/Images/GUIPorts.PNG?raw=true"
       alt="DomStick COM Ports"
       width="400"
       style="border: 3px solid #0078D7; border-radius: 8px;" />
</p>
