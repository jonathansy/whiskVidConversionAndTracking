%% whiskerQueue- queues up different directories for tracking assignments 
%pause on 

whiskerNumber = '1';
pixDen = '0.033';


startDir = '/media/hireslab/AHHD_009/Data/AH0281/160211/cameraMain';
endDir = '/mnt/Data/Video/AHHD_009/AH0281/160211/';
startItFun(startDir, endDir, pixDen, whiskerNumber)

startDir = '/media/hireslab/AHHD_009/Data/AH0281/160212/cameraMain';
endDir = '/mnt/Data/Video/AHHD_009/AH0281/160212/';
startItFun(startDir, endDir, pixDen, whiskerNumber)
% 
startDir = '/media/hireslab/AHHD_009/Data/AH0281/160214/cameraMain';
endDir = '/mnt/Data/Video/AHHD_009/AH0281/160214/';
startItFun(startDir, endDir, pixDen, whiskerNumber)
% 
% startDir = '/media/hireslab/AHHD_001/Data/AH0287/151117/cameraMain';
% endDir = '/mnt/Data/Video/AHHD_001/AH0287/151117/';
% startItFun(startDir, endDir, pixDen, whiskerNumber)

