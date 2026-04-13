go to file home/VBX:

After put the Wav file to mydata - example.wav (need to be 16k) need to make example.lab file from make_lab.py (terminal python make_lab.py example.wav example.lab)

after that:

cd ~/VBx 
source vbx-env/bin/activate
rm -rf myexp myxvec
mkdir -p myexp myxvec
./run_my_one_file.sh

output: myexp file there will be new output (AHC+VB) with the rttm file


after that 
Cut wav file after getting rttm file to seperate speakers audio:

/home/auto-tech/VBx/mydata/cut file after rttm:
run Cut_file_afrer_rttm.py with the wav file  and the rttm file (each time go into the code and put the speaker id.




