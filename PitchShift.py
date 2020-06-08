import wave
import numpy as np

SHIFT_HZ = 300
INPUT_FILE_NAME = 'input.wav'
OUTPUT_FILE_NAME = 'output.wav'

# Получение списка параметров
inputWave = wave.open(INPUT_FILE_NAME, 'r')
inputParams = list(inputWave.getparams())
# Параметр nFrames обнуляется, он задастся автоматически
inputParams[3] = 0
# Задание параметров выходного файла
outputWave = wave.open(OUTPUT_FILE_NAME, 'w')
outputWave.setparams(inputParams)
# Задание параметров
# fr - не помню, что, но похоже на "количество фреймов, обрабатываемых за одну итерацию основного цикла"
# c - количество итераций цикла для данного файла
fr = 20
sz = inputWave.getframerate()//fr
c = int(inputWave.getnframes()/sz)
shift = SHIFT_HZ//fr
for num in range(c):
    # Считывание данных
    inputData = np.frombuffer(inputWave.readframes(sz), dtype=np.int16)
    # Разделение на каналы
    leftChannel = inputData[0::2]
    rightChannel = inputData[1::2]
    # ДПФ к обоим каналам
    leftChannelSpectrum = np.fft.rfft(leftChannel)
    rightChannelSpectrum = np.fft.rfft(rightChannel)
    # Сдвиг на нужную частоту
    leftChannelSpectrum = np.roll(leftChannelSpectrum, shift)
    rightChannelSpectrum = np.roll(rightChannelSpectrum, shift)
    # Обнуление всего лишнего, появившегося после roll
    leftChannelSpectrum[0:shift] = 0
    rightChannelSpectrum[0:shift] = 0
    # Обратное ДПФ у обоим каналам
    outputLeftChannel = np.fft.irfft(leftChannelSpectrum)
    outputRightChannel = np.fft.irfft(rightChannelSpectrum)
    # Слияние двух каналов в один поток данных
    outputData = np.column_stack((outputLeftChannel, outputRightChannel)).ravel().astype(np.int16)
    # Запись изменённых в выходной файл
    outputWave.writeframes(outputData.tostring())
# Закрытие данных
inputWave.close()
outputWave.close()
