%% This command manages the overall pipeline of the whisker tracking process, from untracked .seq to tracked .mp4
%
% Created by J. Sy, 19 November 2014
%
% Dependencies: mp4_converterJS3.py, whiskerTrackerParforLinux.m, Janelia Farm Whisker Tracking package 
%
%% Section 1: Directories
% We've got to set a few directories straight here. For usability, input
% commands will be used

options.Resize ='on';
options.WindowStyle='normal';
options.Interpreter='none';
trackingInfo = inputdlg({'Enter directory where your .seq files are found',...
    'Enter directory where you would like to place your tracked .mp4s (Should be on NAS mounted under /mnt)',...
    'Pixel density:', 'Number of Whiskers'},'Please input information', [1 100; 1 100; 1 8; 1 8], {'','','0.016',''},options); %Displays input prompt for directory info
% trackingInfo{1} = Directory files are found (input
% trackingInfo{2} = output directory
% trackingInfo{3} = mm per pixel. Defaults to 0.016
% trackingInfo{4} = Number of whiskers on mice, used to determine which
% version of the whisker tracker to use 

% seqDir = input('Please give the directory of the seq files to be converted: ','s');
% trackingDir = input('Please give the directory where you would like to move the .mp4 vidoes to be tracked \nNote: This should be on the NAS: ','s');
disp('Thank you, no further inputs required') 
startTimeStat = datestr(now); 
tic;

%% Section 2: Convert .seq files to .mp4 files
% Uses python script mp4_converterJS3.py, originally written by
% S. Peron, to convert files

disp('CONVERTING TO .MP4')
cd(trackingInfo{1});
system(['python /home/hireslab/Code/mp4_converter/mp4_converterJS4.py']);
system(['ls'])
disp('Finished converting')


%% Section 3: Upload data to NAS and track the .mp4 files
% Uses 'whiskerTrackerParforLinux.m' which in turn utilizes scripts
% written by Janelia Farm and included in the Whisker Tracking package

system (['cp ' trackingInfo{1} '/*.mp4 /home/hireslab/WhiskerVideos/Transit']) %Move to temporary directory so we can change permissions below
system (['chmod ugo+rwx /home/hireslab/WhiskerVideos/Transit/*.mp4']) %Change permissions to avoid write errors later in code

system(['cp /home/hireslab/WhiskerVideos/Transit/*.mp4 ' trackingInfo{2}]); % Move to specified directory, presumably on NAS
disp('STARTING WHISKER TRACKING')
disp('Note: This will take some time') 
cd(trackingInfo{2}); 
whiskerNumber = str2num(trackingInfo{4}); 

checkSettings = exist('default.parameters');
if checkSettings == 2
    disp('Resetting parameters') 
    delete default.parameters %Typically, having a default.parameters file around from previous tracking sessions causes an error with the whikser tracker 
end 
    
if whiskerNumber == 1; % Uses 'classify-single-whisker' for better tracking of a single whisker
    disp('Type = Single')
    %whiskerTrackerParforLinuxSW 
    whiskerTrackerParforLinux
else
    disp('Type = Multiple')
    whiskerTrackerParforLinux % Uses 'classify' for multiple whisker tracking. 
end
disp('Finished tracking')

%% Section 4: Finish program and display time statistics
% Indicates end of program and displays start time, end time, and elapsed
% time 
disp('FINISHED PROGRAM') 
endTimeStat = datestr(now);

disp(['Program started: ' startTimeStat])
disp(['Program ended: ' endTimeStat]) 
toc