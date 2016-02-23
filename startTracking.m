%% Used for whisker tracking. 
disp('Changing directory to /home/hireslab/WhiskerVideos/TMP') %Change directory to whatever one you wish to use
disp('Please place all relevant video files in this directory') % ""
cd '/home/hireslab/WhiskerVideos/TMP' % ""
disp(' ')

disp('NOTE: Running the entire whisker tracking program')
disp('automatically will take a significant amount of time')
disp('and computing resources. Do not run automatically if')
disp('you only wish to generate .measurements files. Also,')
disp('ensure that the settings in "whiskerTrackerParfor.m"')
disp('match the videos you wish to track')

disp(' ')

y = 1;
Y = 1;
n = 0;
N = 0;

whiskChoice = input('Do you want to run the whisker tracker automacally? [y/n]');

if whiskChoice == 1
    whiskerTrackerParforLinux
elseif whiskChoice == 1
    whiskerTrackerParforLinux
elseif whiskChoice == 0
    disp('Ok')
elseif whiskChoice == 0
    disp('Ok')
else
    disp('Invalid answer')
end