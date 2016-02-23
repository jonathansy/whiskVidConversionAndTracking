%% Used to do whisker tracking on raw video data
%Attempts to process in parallel
%In theory, sections 3 (CLASSIFY) and 3.5 (CLASSIFY-SINGLE-WHISKER) should
%not be in use at the same time, since they do the same thing
% Created by SAH and JS, 2014-08-04
% Edited by JS 2014-11-10, for Linux support

%% (1) TRACE: Uses Janelia Farm's whisker tracking software to track all whiskers in a directory 
traces = dir('*.mp4'); %Searches only for .mp4 files, change if using other type (e.g. SEQ)

parfor n=1:length(traces)
    [~, outputFileName] = fileparts(traces(n).name);
    system(['/home/hireslab/Code/whisk-1.1.0d-Linux/bin/whisk/trace ' traces(n).name ' ' outputFileName])
    display([traces(n).name ' has been traced'])
end

%% (2) MEASURE: Generates measurements of traced shapes for later evaluation
measures = dir('*.whiskers');

parfor n=1:length(measures)
    [~, outputFileName] = fileparts(measures(n).name);
    system(['/home/hireslab/Code/whisk-1.1.0d-Linux/bin/whisk/measure ' '--face ' 'top ' measures(n).name ' ' outputFileName '.measurements']);
    display([measures(n).name ' has been measured'])
end

%% (3) CLASSIFY: Helps refine tracing to more accurately determine which shapes are whiskers
%Use for multiple whiskers
classes = dir('*.measurements');

parfor n=1:length(classes)
    [~, outputFileName] = fileparts(classes(n).name);
    system(['/home/hireslab/Code/whisk-1.1.0d-Linux/bin/whisk/classify ' classes(n).name ' ' outputFileName '.measurements ' 'top ' '--px2mm ' pixDen ' -n ' trackingInfo{4}]) ; 
    display([classes(n).name ' has been classified'])
end

%% (3.5) CLASSIFY-SINGLE-WHISKER: A variation of the above code designed for one whisker
% %Comment out if not in use, use for single whiskers 
% classes = dir('*.measurements');
% 
% parfor n=1:length(classes)
%     [~, outputFileName] = fileparts(classes(n).name);
%     system(['classify-single-whisker ' classes(n).name ' ' outputFileName '.measurements']);
%     display([classes(n).name ' has been classified'])
% end

%% (4) RECLASSIFY: Refines previous step
classes = dir('*.measurements');

parfor n=1:length(classes)
    [~, outputFileName] = fileparts(classes(n).name);
    system(['/home/hireslab/Code/whisk-1.1.0d-Linux/bin/whisk/reclassify ' classes(n).name ' ' outputFileName '.measurements' ' ' '-n ' trackingInfo{4}]);
    display([classes(n).name ' has been reclassified'])
    display([classes(n).name ' completed'])
end
%%
%Please visit http://whiskertracking.janelia.org/wiki/display/MyersLab/Whisker+Tracking+Tutorial
%for more information
%   Clack NG, O'Connor DH, Huber D, Petreanu L, Hires A., Peron, S., Svoboda, K., and Myers, E.W. (2012) 
%   Automated Tracking of Whiskers in Videos of Head Fixed Rodents.
%   PLoS Comput Biol 8(7):e1002591. doi:10.1371/journal.pcbi.1002591