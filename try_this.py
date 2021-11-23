def GuitarString(frequency, duration=1., sample_rate=44800, p=0.9, beta=0.1, S=0.5, C=0.1, L=0.2, toType=False):
    N = int(sample_rate / frequency)  # Длина шума в сэмплах

    noise = np.random.uniform(-1, 1, N)  # Создаем шум

    # Pick-direction lowpass filter (Фильтр низких частот).
    # H(z) = (1-p)/(1-p*z^(-1)). p ∈ [0, 1)
    # y(n) = (1-p)*x(n)+p*y(n-1)
    buffer = np.zeros_like(noise)
    buffer[0] = (1 - p) * noise[0]
    for i in range(1, N):
        buffer[i] = (1 - p) * noise[i] + p * buffer[i - 1]
    noise = buffer

    # Pick-position comb filter (Гребенчатый фильтр).
    # H(z) = 1-z^(-int(beta*N+1/2)). beta ∈ (0, 1)
    # y(n) = x(n)-x(n-int(beta*N+1/2))
    pick = int(beta * N + 1 / 2)
    if pick == 0:
        pick = N  # То есть фильтр не будет действовать
    buffer = np.zeros_like(noise)
    for i in range(N):
        if i - pick < 0:
            buffer[i] = noise[i]
        else:
            buffer[i] = noise[i] - noise[i - pick]
    noise = buffer

    # Добавляем шум в начале.
    samples = np.zeros(int(sample_rate * duration))
    for i in range(N):
        samples[i] = noise[i]

    # Неявно использутся тот факт, что на конце массива samples значение 0.
    # То есть при n-N<0 значение будет 0, как и должно быть.
    def DelayLine(n):
        return samples[n - N]

    # String-dampling filter.
    # H(z) = 0.996*((1-S)+S*z^(-1)). В оригинальном алгоритме S = 0.5. S ∈ [0, 1]
    # y(n)=0.996*((1-S)*x(n)+S*x(n-1))
    def StringDampling_filter(n):
        return 0.996 * ((1 - S) * DelayLine(n) + S * DelayLine(n - 1))

    # First-order string-tuning allpass filter
    # H(z) = (C+z^(-1))/(1+C*z^(-1)). C ∈ (-1, 1)
    # y(n) = C*x(n)+x(n-1)-C*y(n-1)
    def FirstOrder_stringTuning_allpass_filter(n):
        # Тут следовало использовать буфер и хранить прошлые значение, но это не нужно, так как
        # неявно используется тот факт, что прошлое значение уже сохранено и записано в массив samples.
        return C * (StringDampling_filter(n) - samples[n - 1]) + StringDampling_filter(n - 1)

    def Modeling(n):
        return FirstOrder_stringTuning_allpass_filter(n)

    for i in range(N, len(samples)):
        samples[i] = Modeling(i)

    # Dynamic-level lowpass filter. L ∈ (0, 1/3)
    w_tilde = np.pi * frequency / sample_rate
    buffer = np.zeros_like(samples)
    buffer[0] = w_tilde / (1 + w_tilde) * samples[0]
    for i in range(1, len(samples)):
        buffer[i] = w_tilde / (1 + w_tilde) * (samples[i] + samples[i - 1]) + (1 - w_tilde) / (1 + w_tilde) * buffer[
            i - 1]
    samples = (L ** (4 / 3) * samples) + (1.0 - L) * buffer

    if toType:
        samples = samples / np.max(np.abs(samples))  # Нормируем от -1 до 1
        return np.int16(samples * 32767)  # Переводим в тип данных int16
    else:
        return samples