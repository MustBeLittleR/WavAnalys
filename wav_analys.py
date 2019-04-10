import wave
import numpy as np
import matplotlib.pyplot as plt
import wave

import numpy
import pylab


def wavread(path):
    wavfile = wave.open(path, "rb")
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


def main():
    # path = sys.argv[1]
    # path = input("The Path is:")
    # print(path)
    wavdata, wavtime, nchannels, framerate = wavread("20190308_095639car.wav")

    N = len(wavdata)

    start = 0  # 开始采样位置
    df = framerate / (N - 1)  # 分辨率
    freq = [df * n for n in range(0, N)]  # N个元素

    print(len(wavdata))
    print(len(wavtime))

    c = np.fft.fft(wavdata) * 2 / N

    d = int(len(c) / 2)
    c_scale = abs(c[:d - 1])
    c_scale = c_scale*50
    print(len(c))

    fig, ax = plt.subplots(2, 1)

    ax[0].plot(wavtime, wavdata, color='green')
    ax[0].set_xlabel('Time')
    ax[0].set_ylabel('Amplitude')

    # ax[1].plot(freq, abs(c), color='red')
    # ax[1].set_xlabel('Freq(HZ)')
    # ax[1].set_ylabel('Y(freq)')
    ax[1].plot(freq[10000:d - 1], c_scale[10000:d - 1], color='red')
    ax[1].set_xlabel('Freq(HZ)')
    ax[1].set_ylabel('Freq(Y)')
    plt.show()


def analys_freq():
    wf = wave.open("20190308_095545car.wav", "rb")
    # 创建PyAudio对象

    nframes = wf.getnframes()
    framerate = wf.getframerate()
    # 读取完整的帧数据到str_data中，这是一个string类型的数据
    str_data = wf.readframes(nframes)
    wf.close()
    # 将波形数据转换为数组
    # A new 1-D array initialized from raw binary or text data in a string.
    wave_data = numpy.fromstring(str_data, dtype=numpy.short)
    # 将wave_data数组改为2列，行数自动匹配。在修改shape的属性时，需使得数组的总长度不变。
    wave_data.shape = -1, 2
    # 将数组转置
    wave_data = wave_data.T
    # time 也是一个数组，与wave_data[0]或wave_data[1]配对形成系列点坐标
    # time = numpy.arange(0,nframes)*(1.0/framerate)
    # 绘制波形图
    # pylab.plot(time, wave_data[0])
    # pylab.subplot(212)
    # pylab.plot(time, wave_data[1], c="g")
    # pylab.xlabel("time (seconds)")
    # pylab.show()
    #
    # 采样点数，修改采样点数和起始位置进行不同位置和长度的音频波形分析
    N = 44100
    start = 0  # 开始采样位置
    df = framerate / (N - 1)  # 分辨率
    freq = [df * n for n in range(0, N)]  # N个元素
    wave_data2 = wave_data[0][start:start + N]
    c = numpy.fft.fft(wave_data2) * 2 / N
    # 常规显示采样频率一半的频谱
    d = int(len(c) / 2)
    # 仅显示频率在4000以下的频谱
    # while freq[d] > 4000:
    #     d -= 10
    pylab.plot(freq[:d - 1], abs(c[:d - 1]), 'r')
    pylab.show()


main()
#analys_freq()