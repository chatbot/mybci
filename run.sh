#!/bin/bash
n_channels=3
n_points=1024
n_fft_points=50

mcast_port=17001
tcpN_port=17002
showfft_port=17003


xterm -T udp2tcpN.py -e /bin/bash -l -c "python pyeeg/tests/udp2tcpN.py $n_points $mcast_port $tcpN_port & bash" &
xterm -T showfft.py -e /bin/bash -l -c "python myfft/showfft.py $n_channels $n_fft_points $showfft_port & bash"  &
sleep 3
xterm -T myfft -e /bin/bash -l -c "myfft/fft/a.out 127.0.0.1 $showfft_port $tcpN_port $n_channels $n_points $n_fft_points & bash" &
xterm -T eeg-player -e /bin/bash -l -c "python pyeeg/eeg-player/main.py & bash" &
#xterm -T showsignal -e /bin/bash -l -c "python pyeeg/tests/showsignal.py $mcast_port & bash" &
