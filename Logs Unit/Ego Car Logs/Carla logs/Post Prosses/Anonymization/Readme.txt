Part 1: Create a Separate Channel for Each Speaker

### Install

Install VBx from:
`https://github.com/BUTSpeechFIT/VBx`
Recommended: **Linux**

### Go to the VBx folder

```bash
cd ~/VBx
```

### Prepare the `.lab` file

1. Copy the WAV file (**16 kHz**) into:

```bash
path/mydata
```

2. In the terminal, run:

```bash
python make_lab.py example.wav example.lab
```

### Run diarization

```bash
cd ~/VBx
source vbx-env/bin/activate
rm -rf myexp myxvec
mkdir -p myexp myxvec
./run_my_one_file.sh
```

### Output

Inside the `myexp` folder, a new output will be created (`AHC+VB`), including the **RTTM** file.

### Split audio by speaker

Copy the **WAV** file and the **RTTM** file into the script folder for speaker separation, then run:

```bash
Cut_file_afrer_rttm.py
```

For each run of the script, set the required **speaker ID** in the code.

---

Part 2: Voice Conversion

### Install

Install so-vits-svc-fork from:
`https://github.com/voicepaw/so-vits-svc-fork`
Recommended: **Win**

### Additional files

GUI config and model:
`https://drive.google.com/drive/folders/1Ggyz14lo4gTIwUdj5M3G9REj62rHcSOe`

---
