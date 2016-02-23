#!/usr/bin/env python

####################################################################################
#
# S Peron 2014 Mar -- Script that will convert .SEQ to .MP4
#
# J Sy 2014 Nov -- v1.3, due to size constraints, this version of the script will # # convert files directly on the external hard drive specified, rather than the
# computer's local hard drive. 
#
#   1) determine which sub directories were added to the parent
#   2) cluster-based compression & deletion of original
#
# Does all this by generating a python script per file, then having qsub run
#  it.  The python script invokes the necessary os calls etc.
#
# Linux edit started by J. Sy on 30 October 2014 
# v.1.0.2 started 7 November 2014
# >>Edited for hireslab computer
####################################################################################
import sys, struct, os, re, string, subprocess, glob, time;
import xml.dom.minidom;

print "Something worked"
# definitely (?) fixed -- where you go huntin for dem files
# "SvobodaBackup/AH0030/141112" should be changed to specify the directory of your
# choice -J. Sy 2014 Nov 14 

root_search_path = os.getcwd();

# settings that may change per-user?
if (1 == 1):  # production
    ffmpeg_path = "/home/hireslab/Code/ffmpeg-2.4.3/ffmpeg";
    raw2tiff_path = "/usr/local/bin/raw2tiff";
# qsub_path = "/sge/current/bin/lx-amd64/qsub";


#
# This will take a single file - specified in FULL path in mypath, and
#  mypath = mydir+myfile where mydir is the dir name and myfile is file name
def process_mp4_file(mypath, myfile, mydir):
    print "Starting process"
    remove_unprocessed = 1;  # set to 0 and NOTHING will be deleted ;
    # set to 1, and xml and session log gone
    # set to 2, and ORIGINAL seq also gone *** THIS IS ASSIGNED BY TRANSMOG; see below

    runit = 1;  # set to 0 to enter a debug mode where commands are printed and executed sans qsub

    # some sanity checks
    fs = os.path.getsize(mypath);
    if (fs < 10000):
        print mypath + " has size < 10000 ; not processing.";
        return;

    # script init
    script = "#!/usr/bin/env python\n";
    script += "import os, os.path, sys, struct, re, string, xml.dom.minidom, shutil;\n"
    script += "os.system(\'hostname\');\n";

    # 777 permission ; this will have to occur a few times more
    script += "os.system(\'chmod -R 777 " + mydir + "\');\n";


    ####################################################################################
    #
    # compression section
    #
    ####################################################################################

    # read width, height, num bits, real size, num frame
    fil = open(mypath, 'rb');
    fil.seek(548, 0);
    width_ = fil.read(4);
    height_ = fil.read(4);
    depth_ = fil.read(4);
    fil.seek(548 + 24, 0);
    nframes_ = fil.read(4);
    fil.seek(580, 0);
    truesize_ = fil.read(4);
    fil.close();

    # header params to real
    nframes = struct.unpack("<l", nframes_);
    truesize = struct.unpack("<l", truesize_);
    width = struct.unpack("<l", width_);
    height = struct.unpack("<l", height_);

    print width
    print height
    print "Made it past part 1"  # Just testing for how far the program will make it
    # make a temp dir based of seq file name

    tmp_dir = "/home/hireslab/WhiskerVideos/Scratch/" + myfile.replace(".seq", "_tmp");
    script += "try:\n";
    script += "  os.mkdir(\'" + tmp_dir + "\');\n";
    script += "except:\n";
    script += "  print(\'" + tmp_dir + " already exists; nuking.\');\n";
    script += "  shutil.rmtree(\'" + tmp_dir + "\');\n";
    script += "  os.mkdir(\'" + tmp_dir + "\');\n";
    print tmp_dir;
    if (runit == 1):
        os.mkdir(tmp_dir);
        print "made dir"
    print "Made it past temp dir"
    # --- go thru the file and raw2tiff via the command below but increasing header size appropriately ...
    # raw2tiff -H 1024 -w 332 -l 400 foo_0140.seq test.tif
    for f in range(0, nframes[0]):
        offs = 8192 + (
        f * truesize[0]);  # Changed header size from 1024 due to chagne in streampix -JS 2014-11-07 17:52:38
        # r2tcmd = "%s -H %d -w %d -l %d %s %s/tmp/%05d.tif" % (raw2tiff_path, offs, width[0], height[0], mypath, mydir, f+1);
        r2tcmd = "%s -H %d -c none -M -w %d -l %d %s %s/%05d.tif" % (
        raw2tiff_path, offs, width[0], height[0], mypath, tmp_dir, f + 1);
        script += "os.system(\'" + r2tcmd + "\');\n";
        if (runit == 1):
            os.system(r2tcmd);

    # --- call ffmpeg
    # ffmcmd = "%s -i mov_path '/seq_tmp/%' num2str(n_digs) 'd.tif ' mov_path '/' out_fname
    # output to processed
    ffmpeg_outpath = mypath.replace("seq", "mp4");
    ffmpeg_outpath = ffmpeg_outpath.replace("/unprocessed/", "/processed/");
    ffmpeg_leftpath = ffmpeg_outpath.replace(".mp4", "_leftCrop.mp4");  # Inputed by J. Sy on Oct 14 2015 to crop video into two pieces
    ffmpeg_rightpath = ffmpeg_outpath.replace(".mp4", "_rightCrop.mp4");
    ffmcmd = "%s -y -i %s/%%5d.tif -b:v 800k %s" % (ffmpeg_path, tmp_dir, ffmpeg_outpath);
    ffmcmd_leftcrop = "%s -i %s/%%5d.mp4 -filter:v 'crop=600:394:0:0' %s " % (ffmpeg_outpath, tmp_dir, ffmpeg_leftpath);
    ffmcmd_rightcrop = "%s -i %s/%%5d.mp4 -filter:v 'crop=600:394:600:0' %s " % (ffmpeg_outpath, tmp_dir, ffmpeg_rightpath);
    script += "os.system(\'" + ffmcmd + "\');\n";
    print ffmcmd;
    if (runit == 1):
        os.system(ffmcmd);
        os.system(ffmcmd_leftcrop);
        os.system(ffmcmd_rightcrop);
    print "Made it past ffmpeg, end"
    clearTiffs = "rm -rf ~/WhiskerVideos/Scratch/*"
    if (runit == 1):
        os.system(clearTiffs);  # Added section to clear tiff files automatically after looping.
    ####################################################################################
    #
    # rerun, cue & cleanup section
    #
    ####################################################################################


#  # --- setup rerun script -- since it is just the qsub command call, make this as well, and initialize stuff

#  # init code that must be here
#	pyscript = mypath.replace(".seq", ".py"); # this must be here so that dispatch_cmd can be assigned
#	pyscript_log = mypath.replace(".seq", ".log");
#	print "1";

#  # qsub job stuff
#	jobname = "mp4_compress_" + myfile;
#	dispatch_cmd = qsub_path + " -N " + jobname + " -j y -o /dev/null -b y -cwd -V \"python " + pyscript + " > " + pyscript_log + "\"";
## 3/5/13 removed:	dispatch_cmd = qsub_path + " -N " + jobname + " -l short=true -j y -o /dev/null -b y -cwd -V \"python " + pyscript + " > " + pyscript_log + "\"";

#	# --- cleanup -- DELETE the original .seq file, script file (.py), tmp dir

##	script += "os.remove(\'" + pyscript + "\');\n";
#	script += "shutil.rmtree(\'" + tmp_dir + "\');\n";

#  # This removes seq file -- if remove_unprocessed <= 1, it will copy it to processed; otherwise, it is gone forever
#	script += "os.remove(\'" + mypath + "\');\n";

#  # 777 permission for everything in processed so that user calling daemon is not blocking access
#	script += "os.system(\'chmod -R 777 " + mydir.replace("/unprocessed/", "/processed/") + "\');\n";
#	script += "os.system(\'chmod -R 777 " + mydir + "\');\n";

#	# final step is to kill log and py file
#	script += "os.remove(\'" + pyscript + "\');\n";
#	script += "os.remove(\'" + pyscript_log + "\');\n";

#	text_file = open(pyscript, 'w');
#	text_file.write(script);
#	text_file.close();

#  # --- cue this script via qsub ; put the rerun command in position
#	print(dispatch_cmd);
#	os.system(dispatch_cmd);





####################################################################################
#
# "crawls" a single directory going thru its files
#
####################################################################################
def parse_directory(arg, dirname, names):
    print "parsing directory"
    try:
        # --- are there seq files?  are they older than 1 h?
        #		cmd = "ls " + dirname + " | grep seq | wc -l";
        #		print "DOING: " + cmd;
        #		seq_count = int(bash_run(cmd));

        #		cmd = "find " + dirname + " -mmin -30 | grep seq | wc -l";
        #		print "DOING: " + cmd;
        #		new_count = int(bash_run(cmd));

        # --- execute!
        seq_count = 1;
        new_count = 0;
        if (seq_count > 0 & new_count == 0):
            for fname in names:
                # ---   if yes, make the processed version of the directory, then
                #       go thru the files and call process_mp4_file, for each .seq file
                #       that has an accompanying xml

                # check that its a .seq file
                if (string.find(fname, ".seq") != -1):
                    print "dn: " + dirname + " fn: " + fname;
                    process_mp4_file(dirname + "/" + fname, fname, dirname);
                    time.sleep(.5);  # wait 30 seconds before kickoff of next ... for cluster's sake!
    except:
        e = sys.exc_info()[0];
        print "failed to process directory " + dirname + " message: ", e;


####################################################################################
#
# Wrapper to get output of a system call
#
####################################################################################
def bash_run(cmd):
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE);
    out = p.stdout.read().strip();
    return out;


####################################################################################
# Some testing here - JS
# dirname = root_search_path;
# names = os.listdir(dirname)

####################################################################################
#
# The actual directory crawler
#
####################################################################################

# --- go thru each directory at top
os.path.walk(root_search_path, parse_directory, "");
print "End of code"
