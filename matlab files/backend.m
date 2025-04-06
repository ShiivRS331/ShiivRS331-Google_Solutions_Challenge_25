%% 1. Load Audio File
audioFilePath = "C:\Users\rsshi\Downloads\kal.mp3";  % Update with actual path
[y, sr] = audioread(audioFilePath);   
y = y(:, 1);  % Convert to mono if stereo

%% 2. Parameters
frameLength = 2048;  
hopLength   = 512;   
fmin = 50;  
fmax = 800; 
numHarmonics = 5;  

%% 3. Move Audio Data to GPU
y = gpuArray(y);  

%% 4. Initialize Variables
numFrames = floor((length(y) - frameLength) / hopLength) + 1; 
estimatedFrequencies = zeros(numFrames, numHarmonics, 'gpuArray');  
confidenceScores = zeros(numFrames, numHarmonics, 'gpuArray');  

%% 5. Multi-Pitch Analysis (Parallelized)
parfor i = 1:numFrames
    startIndex = (i - 1) * hopLength + 1;
    endIndex   = startIndex + frameLength - 1;
    
    if endIndex > length(y)
        continue;
    end
    
    frame = y(startIndex:endIndex);
    frame = frame .* hann(frameLength);  % Apply Hanning window
    
    % Compute Spectrum (FFT)
    N = frameLength;
    fft_frame = fft(frame, N);
    P2 = abs(fft_frame / N);
    P1 = P2(1:N/2+1);
    P1(2:end-1) = 2 * P1(2:end-1);
    
    f = sr * (0:(N/2)) / N;  % Frequency axis
    
    % Harmonic Product Spectrum (HPS)
    hps_spectrum = P1;
    for h = 2:numHarmonics
        downsampled_indices = 1:h:length(P1);
        if length(downsampled_indices) > length(hps_spectrum)
            downsampled_indices = downsampled_indices(1:length(hps_spectrum));
        elseif length(downsampled_indices) < length(hps_spectrum)
            hps_spectrum = hps_spectrum(1:length(downsampled_indices));
        end
        hps_spectrum = hps_spectrum .* P1(downsampled_indices);
    end
    
    % Estimate Fundamental Frequency (F0)
    [~, peak_index] = max(hps_spectrum);
    estimatedF0 = f(peak_index);
    
    % Store estimated frequencies and confidence scores
    for harmonic = 1:numHarmonics
        harmonicFrequency = estimatedF0 * harmonic;
        [~, harmonicIndex] = min(abs(f - harmonicFrequency));
        estimatedFrequencies(i, harmonic) = f(harmonicIndex);
        confidenceScores(i, harmonic) = P1(harmonicIndex);
    end
end

%% 6. Tonic Estimation
frequency_weights = mean(confidenceScores ./ sum(confidenceScores, 2), 1);
weighted_frequencies = estimatedFrequencies .* frequency_weights;
[N, edges] = histcounts(weighted_frequencies(:), 50);
[peaks, peakLocations] = findpeaks(N, 'MinPeakDistance', 5);
peakFrequencies = edges(peakLocations);

if isempty(peakFrequencies)
   tonicEstimate = mean(weighted_frequencies(:));
   fprintf('No prominent peaks found. Using mean frequency: %.2f Hz\n', tonicEstimate);
else
   [~, maxPeakIndex] = max(peaks);
   tonicEstimate = peakFrequencies(maxPeakIndex);
   fprintf('Prominent Peak found. Tonic Estimated: %.2f Hz\n', tonicEstimate);
end

%% 7. Visualization
timeAxis = (0:numFrames-1) * hopLength / sr;
figure;

subplot(3, 1, 1);
spectrogram(y, hamming(frameLength), hopLength, frameLength, sr, 'yaxis');
title('Spectrogram of the Audio');
colorbar;

subplot(3, 1, 2);
hold on;
for harmonic = 1:numHarmonics
    plot(timeAxis, estimatedFrequencies(:, harmonic), 'DisplayName', sprintf('Harmonic %d', harmonic));
end
hold off;
xlabel('Time (s)');
ylabel('Frequency (Hz)');
title('Estimated Frequencies over Time');
legend show;
ylim([fmin, fmax*numHarmonics]);

subplot(3, 1, 3);
histogram(weighted_frequencies(:), edges);
hold on;
xline(tonicEstimate, 'r', 'LineWidth', 2, 'DisplayName', sprintf('Tonic Estimate: %.2f Hz', tonicEstimate));
hold off;
xlabel('Frequency (Hz)');
ylabel('Count');
title('Histogram of Estimated Frequencies');
legend show;
sgtitle('Multi-Pitch Analysis and Tonic Estimation');
