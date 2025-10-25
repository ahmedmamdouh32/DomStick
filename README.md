<h1 class="demoTitle">&nbsp; &nbsp; DomStick</h1>
<p data-start="857" data-end="1110"><strong data-start="857" data-end="869">DomStick</strong> is a compact wireless console built for <strong data-start="910" data-end="944">robotics and embedded projects</strong>.</p>
<p data-start="857" data-end="1110">It connects via <strong data-start="964" data-end="977">Bluetooth</strong>, offering smooth, cable-free control through a <strong data-start="1025" data-end="1073">PCB crafted to fit comfortably in your hands</strong> for better precision and handling.</p>
<p data-start="857" data-end="1110">You can power DomStick either from the <strong data-start="1151" data-end="1172">Arduino Nano jack</strong> or a <strong data-start="1178" data-end="1191">DC socket</strong> with <strong data-start="1197" data-end="1212">7&ndash;35V input</strong>, and it&rsquo;s equipped with a <strong data-start="1239" data-end="1258">voltage divider</strong> to safely shift the Bluetooth <strong data-start="1289" data-end="1299">Rx pin</strong> from <strong data-start="1305" data-end="1325">5V to 3.3V logic</strong>, protecting the module while maintaining stable communication.</p>
<p align="right"><img src="https://github.com/ahmedmamdouh32/DomStick/blob/master/Images/DomStick.png?raw=true" alt="DomStick Logo" width="300" height="228" /></p>
<h2>Board content:</h2>
<ul>
<li>Arduino Nano</li>
<li>Joystick</li>
<li>Four Push Buttons</li>
<li>Bluetotoh Module <strong>HC-05</strong></li>
<li>DC Power Socket</li>
</ul>
<p>&nbsp;</p>
<p>&nbsp;</p>
<h2>Pins Connections:</h2>
<table style="width: 200px;">
<tbody>
<tr style="height: 32px;">
<td style="width: 258px; height: 32px;" colspan="2" align="center">
<p align="center"><strong>Joystick</strong></p>
</td>
</tr>
<tr style="height: 13px;">
<td style="width: 120.525px; height: 13px;" align="center">&nbsp;X-Axis&nbsp;&nbsp;&rarr;</td>
<td style="width: 137.475px; height: 13px;" align="center">A1&nbsp;</td>
</tr>
<tr style="height: 13px;">
<td style="width: 120.525px; height: 13px;" align="center">&nbsp;Y-Axis&nbsp;</td>
<td style="width: 137.475px; height: 13px;" align="center">A2&nbsp;</td>
</tr>
<tr style="height: 13px;">
<td style="width: 120.525px; height: 13px;" align="center">&nbsp;Push Button</td>
<td style="width: 137.475px; height: 13px;" align="center">D8&nbsp;</td>
</tr>
<tr style="height: 32px;">
<td style="width: 258px; height: 32px;" colspan="2" align="center">
<p align="center"><strong>Push Buttons</strong></p>
</td>
</tr>
<tr style="height: 13px;">
<td style="width: 120.525px; height: 13px;" align="center">&nbsp;Top Button</td>
<td style="width: 137.475px; height: 13px;" align="center">&nbsp;D5</td>
</tr>
<tr style="height: 13px;">
<td style="width: 120.525px; height: 13px;" align="center">Bottom Button&nbsp;</td>
<td style="width: 137.475px; height: 13px;" align="center">D3&nbsp;</td>
</tr>
<tr style="height: 13px;">
<td style="width: 120.525px; height: 13px;" align="center">Left Button&nbsp;</td>
<td style="width: 137.475px; height: 13px;" align="center">D2&nbsp;</td>
</tr>
<tr style="height: 13px;">
<td style="width: 120.525px; height: 13px;" align="center">Right Button&nbsp;</td>
<td style="width: 137.475px; height: 13px;" align="center">D4&nbsp;</td>
</tr>
<tr style="height: 32px;">
<td style="width: 258px; height: 32px;" colspan="2" align="center">
<p align="center"><strong>Bluetooth</strong></p>
</td>
</tr>
<tr style="height: 13px;">
<td style="width: 120.525px; height: 13px;" align="center">&nbsp;Tx</td>
<td style="width: 137.475px; height: 13px;" align="center">&nbsp;D10</td>
</tr>
<tr style="height: 13px;">
<td style="width: 120.525px; height: 13px;" align="center">Rx&nbsp;</td>
<td style="width: 137.475px; height: 13px;" align="center">D9&nbsp;</td>
</tr>
<tr style="height: 13px;">
<td style="width: 120.525px; height: 13px;" align="center">State&nbsp;</td>
<td style="width: 137.475px; height: 13px;" align="center">D7&nbsp;</td>
</tr>
<tr style="height: 13px;">
<td style="width: 120.525px; height: 13px;" align="center">Enable&nbsp;</td>
<td style="width: 137.475px; height: 13px;" align="center">D6&nbsp;</td>
</tr>
</tbody>
</table>
<p>&nbsp;</p>
<h2 data-start="188" data-end="238">Turning DomStick into a Keyboard Controller</h2>
<p data-start="240" data-end="450">To make <strong data-start="248" data-end="260">DomStick</strong> act like a <strong data-start="272" data-end="284">keyboard</strong> and control any PC game or application, we designed a system that translates the data sent via <strong data-start="380" data-end="393">Bluetooth</strong> into standard <strong data-start="408" data-end="440">HID (Human Interface Device)</strong> commands.</p>
<p data-start="452" data-end="777">Since the <strong data-start="462" data-end="488">HC-05 Bluetooth module</strong> used on DomStick doesn&rsquo;t natively support HID mode, we created a <strong data-start="554" data-end="574">Python interface</strong> that bridges this gap. The Python script listens to the serial data coming from the DomStick through the selected <strong data-start="689" data-end="701">COM port</strong> and converts each received signal into a corresponding <strong data-start="757" data-end="776">keyboard action</strong>.</p>
<p data-start="779" data-end="869">A simple <strong data-start="788" data-end="822">Graphical User Interface (GUI)</strong> is included to make the process user-friendly:</p>
<ul data-start="870" data-end="1043">
<li data-start="870" data-end="923">
<p data-start="872" data-end="923">Scan and select available Bluetooth COM ports.</p>
</li>
<li data-start="924" data-end="967">
<p data-start="926" data-end="967">Connect to your DomStick wirelessly.</p>
</li>
<li data-start="968" data-end="1043">
<p data-start="970" data-end="1043">Automatically map incoming joystick or button data to keyboard keys.</p>
</li>
</ul>

&nbsp;
<p align="center">
        <img
          src="https://github.com/ahmedmamdouh32/DomStick/blob/master/Images/AppGUI.PNG?raw=true"
          alt="DomStick App GUI"
          width="400"
          height="464"
        />
</p>





<p data-start="779" data-end="869"></p>
<p data-start="1045" data-end="1330">Once connected, every command from DomStick &mdash; joystick movements or button presses &mdash; is instantly translated into keyboard inputs on your computer, allowing you to <strong data-start="1209" data-end="1223">play games</strong>, <strong data-start="1225" data-end="1248">control simulations</strong>, or even <strong data-start="1258" data-end="1283">navigate applications</strong> as if DomStick were a real <strong data-start="1311" data-end="1329">HID controller</strong>.</p>
