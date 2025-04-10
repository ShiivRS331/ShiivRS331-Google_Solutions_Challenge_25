
% ---- Helper Function: frequencyToNote -----
function noteName = frequencyToNote(inputFrequency, A4, A4_INDEX, notes)
% Converts a frequency to the nearest note name, similar to the JavaScript code.
% inputFrequency: Frequency in Hz.
% inputFrequency: Frequency in Hz.
% A4: Frequency of A4 (440 Hz).
% A4_INDEX: Index of A4 in the 'notes' cell array.
% notes: Cell array of note names.

    MINUS = 0;
    PLUS = 1;

    frequency = A4;
    r = 2^(1/12);  % Semitone ratio
    cent = 2^(1/1200); % Cent ratio

    r_index = 0;
    cent_index = 0;
    side = 0;

    if inputFrequency >= frequency
        while inputFrequency >= r * frequency
            frequency = r * frequency;
            r_index = r_index + 1;
        end
        while inputFrequency > cent * frequency
            frequency = cent * frequency;
            cent_index = cent_index + 1;
        end

        if (cent * frequency - inputFrequency) < (inputFrequency - frequency)
            cent_index = cent_index + 1;
        end

        if cent_index > 50
            r_index = r_index + 1;
            cent_index = 100 - cent_index;
            if cent_index ~= 0
                side = MINUS;
            else
                side = PLUS;
            end
        else
            side = PLUS;
        end
    else
        while inputFrequency <= frequency / r
            frequency = frequency / r;
            r_index = r_index - 1;
        end
        while inputFrequency < frequency / cent
            frequency = frequency / cent;
            cent_index = cent_index + 1;
        end

        if (inputFrequency - frequency/cent) < (frequency - inputFrequency)
            cent_index = cent_index + 1;
        end

        if cent_index >= 50
            r_index = r_index - 1;
            cent_index = 100 - cent_index;
            side = PLUS;
        else
            if cent_index ~= 0
                side = MINUS;
            else
                side = PLUS;
            end
        end
    end

    % Get the note
    noteIndex = A4_INDEX + r_index;

    % Check index bounds (IMPORTANT: Prevent errors)
    if noteIndex < 1
        noteIndex = 1;
    elseif noteIndex > length(notes)
        noteIndex = length(notes);
    end

    result = notes{noteIndex}; % Use curly braces for cell array indexing

    % Append cents value
    if side == PLUS
        result = result + " + " + cent_index + " cents";
    else
        result = result + " - " + cent_index + " cents";
    end
    noteName = result;

end


function noteIndex = frequencyToNoteIndex(inputFrequency, A4, A4_INDEX, numNotes)
% Converts a frequency to the nearest note index.

    frequency = A4;
    r = 2^(1/12);  % Semitone ratio

    r_index = 0;

    if inputFrequency >= frequency
        while inputFrequency >= r * frequency
            frequency = r * frequency;
            r_index = r_index + 1;
        end
    else
        while inputFrequency <= frequency / r
            frequency = frequency / r;
            r_index = r_index - 1;
        end
    end

    noteIndex = A4_INDEX + r_index;

    % Check index bounds (IMPORTANT: Prevent errors)
    if noteIndex < 1
        noteIndex = 1;
    elseif noteIndex > numNotes
        noteIndex = numNotes;
    end
end

function [peaks, peakLocations] = findpeaks_gpu(data, minPeakDistance)
%Finds peaks in GPU array data. Returns peaks and their locations.

    data_size = size(data);
    data_length = data_size(2);

    peakLocations = gpuArray(zeros(1,0,'int32'));
    peaks = gpuArray(zeros(1,0));

    if data_length < 3
        return; % Not enough data to find peaks
    end

    for i = 2:(data_length - 1)
        if data(i) > data(i-1) && data(i) > data(i+1)
            % Potential peak
            is_valid_peak = true;

            % Check minimum peak distance
            if ~isempty(peakLocations)
                last_peak_location = peakLocations(end);
                if i - last_peak_location < minPeakDistance
                    is_valid_peak = false;
                end
            end

            if is_valid_peak
                peakLocations = [peakLocations, i];
                peaks = [peaks, data(i)];
            end
        end
    end
end

