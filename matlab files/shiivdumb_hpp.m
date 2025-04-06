function [estimatedFrequencies, confidenceScores, noteIndices] = analyzeHarmonics(estimatedF0, f, P1, A4, A4_INDEX, numNotes, harmonic_indices)
% Analyzes harmonics and returns estimated frequencies, confidence scores, and note indices

numHarmonics = length(harmonic_indices);
estimatedFrequencies = gpuArray(zeros(1, numHarmonics));
confidenceScores = gpuArray(zeros(1, numHarmonics));
noteIndices = gpuArray(zeros(1, numHarmonics));

for harmonic_idx = 1:numHarmonics
    harmonic = harmonic_indices(harmonic_idx);
    harmonicFrequency = estimatedF0 * harmonic;
    [~, harmonicIndex] = min(abs(f - harmonicFrequency)); % Find the nearest frequency bin

    estimatedFrequency = f(harmonicIndex);
    estimatedFrequencies(harmonic_idx) = estimatedFrequency;
    confidenceScores(harmonic_idx) = P1(harmonicIndex); % using spectral magnitude as confidence

    % Map to Note
    noteIndex = frequencyToNoteIndex(estimatedFrequency, A4, A4_INDEX, numNotes);
    noteIndices(harmonic_idx) = noteIndex;
end

end