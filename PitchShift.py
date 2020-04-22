import wave
import numpy as np

SHIFT_HZ = 300
INPUT_FILE_NAME = 'input.wav'
OUTPUT_FILE_NAME = 'output.wav'

inputWave = wave.open(INPUT_FILE_NAME, 'r')
inputParams = list(inputWave.getparams())
inputParams[3] = 0
# par = tuple(par)
outputWave = wave.open(OUTPUT_FILE_NAME, 'w')
outputWave.setparams(inputParams)
fr = 20
sz = inputWave.getframerate()//fr
c = int(inputWave.getnframes()/sz)
shift = SHIFT_HZ//fr
for num in range(c):
    inputData = np.frombuffer(inputWave.readframes(sz), dtype=np.int16)
    leftChannel = inputData[0::2]
    rightChannel = inputData[1::2]
    leftChannelSpectrum = np.fft.rfft(leftChannel)
    rightChannelSpectrum = np.fft.rfft(rightChannel)
    leftChannelSpectrum = np.roll(leftChannelSpectrum, shift)
    rightChannelSpectrum = np.roll(rightChannelSpectrum, shift)
    leftChannelSpectrum[0:shift] = 0
    rightChannelSpectrum[0:shift] = 0
    outputLeftChannel = np.fft.irfft(leftChannelSpectrum)
    outputRightChannel = np.fft.irfft(rightChannelSpectrum)
    outputData = np.column_stack((outputLeftChannel, outputRightChannel)).ravel().astype(np.int16)
    outputWave.writeframes(outputData.tostring())
inputWave.close()
outputWave.close()
