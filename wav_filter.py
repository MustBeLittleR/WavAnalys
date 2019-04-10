import wave as we
import numpy as np
import matplotlib.pyplot as plt

def read_wav(wavfile, plots=True, normal=False):
    f = wavfile
    params = f.getparams()
    nchannels, sampwidth, framerate, nframes = params[:4]
    strData = f.readframes(nframes) # 读取音频，字符串格式
    waveData = np.frombuffer(strData, dtype=np.int16) # 将字符串转化为int # wave幅值归一化
    if normal == True:
        waveData = waveData*1.0/(max(abs(waveData)))
    # 绘图
    if plots == True:
        time = np.arange(0, nframes)*(1.0 / framerate)
        plt.figure(dpi=100)
        plt.plot(time, waveData)
        plt.xlabel("Time")
        plt.ylabel("Amplitude")
        plt.title("Single channel wavedata")
        plt.show()
    return (waveData, time)

def wavread(path):
    wavfile = we.open(path, "rb")
    params = wavfile.getparams()
    framesra, frameswav = params[2], params[3]
    nchannels, sampwidth, framesra, frameswav = params[:4]
    print("nchannels:%d" % nchannels)
    print("sampwidth:%d" % sampwidth)
    datawav = wavfile.readframes(frameswav)
    wavfile.close()
    datause = np.fromstring(datawav, dtype=np.short)
    print(len(datause))
    if nchannels == 2:
        datause.shape = -1, 2
    datause = datause.T
    time = np.arange(0, frameswav) * (1.0 / framesra)
    return datause, time, nchannels, wavfile.getframerate()

def fft_wav(waveData, plots=True):
    f_array = np.fft.fft(waveData) # 傅里叶变换，结果为复数数组
    f_abs = f_array
    axis_f = np.linspace(0, 250, np.int(len(f_array)/2))# 映射到250
    #axis_f = np.linspace(0, 250, np.int(len(f_array)))  # 映射到250
    if plots == True:
        plt.figure(dpi=100)
        plt.plot(axis_f, np.abs(f_abs[0:len(axis_f)]))
        plt.xlabel("Frequency")
        plt.ylabel("Amplitude spectrum")
        plt.title("Tile map")
        plt.show()
    return f_abs

def cut_wav(waveData, wavefft):
    #1200-2200
    #6400-7800
    savewav = []
    N = len(waveData)
    df = framerate / (N - 1)  # 分辨率
    #freq = [df * n for n in range(0, N)]  # N个元素

    cutFreq = []
    # cutFreq.append((300,600))
    # cutFreq.append((1000,1100))
    # cutFreq.append((1400, 1600))
    # cutFreq.append((1900, 2200))
    cutFreq.append((100, 1100))
    cutFreq.append((5900, 7900))

    for n in range(0,N):
        curFreq = df*n
        bInCutFreq = False
        for i, freq in enumerate(cutFreq):
            lowFreq = freq[0]
            highFreq = freq[1]
            if curFreq > lowFreq and curFreq < highFreq:
                bInCutFreq = True

        if bInCutFreq:
            savewav.append(wavefft[n])
        else:
            savewav.append(0)


    axis_f = np.linspace(0, 250, np.int(len(wavefft)/2)) # 映射到250
    plt.figure(dpi=100)
    plt.plot(axis_f, np.abs(savewav[0:len(axis_f)])) # plt.plot(axis_f, np.abs(savewav))
    plt.xlabel("Frequency")
    plt.ylabel("Amplitude spectrum")
    plt.title("Tile map after wave filtering")
    plt.show()
    return savewav

def save_wave(i_array):
    # 保存
    save_wav = i_array.real.reshape((len(i_array), 1)).T.astype(np.short) # print(save_wav.shape) # i_array.real.tofile(dir+r'\test.bin')
    f = we.open('car20181114_114351_filter.wav', "wb") # 配置声道数、量化位数和取样频率
    f.setnchannels(1)
    f.setsampwidth(2)
    f.setframerate(44100) # 将wav_data转换为二进制数据写入文件
    f.writeframes(save_wav.tostring())
    f.close()


wavdata, wavtime, nchannels, framerate = wavread("car20181114_114351.wav")
wavefft = fft_wav(wavdata)
savewav = cut_wav(wavdata, wavefft)
i_array = np.fft.ifft(savewav)
save_wave(i_array)


