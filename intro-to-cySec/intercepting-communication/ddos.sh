#/run/dojo/bin/bash

for i in {1..10}; do nc  10.0.0.2 31337; done &  for i in {1..10}; do nc 10.0.0.2 31337; done &  
