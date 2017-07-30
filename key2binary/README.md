# Script
Have you ever wanted an easy way to show the binary ASCII for a typical keyboard input? Well that is exactly what this little script does. When run, it takes in a key from your keyboard (using USB or SSH to access the console) and displayes that key as a binary code using the Digital IO output. port D0 (or PE4) is considered the low end of the sequence (D0=1, D1=2, D2=4...)
# Usage
`sudo python key2binary.py`