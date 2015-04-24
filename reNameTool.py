
import os
import glob
import re



dictProduct = {"3289648":"022", "3355184":"023", "3158321":"110", "3682609":"118", "3485745":"105",
               "3289393":"112", "4534320":"00E", "3486001":"115", "3420465":"114", "3354929":"113",
               "3682353":"108", "3223601":"101", "3617073":"117", "3551537":"116", "3747889":"109",
               "3354673":"103", "3551281":"106", "3616817":"107", "3420209":"104", "3159344":"050",
               "3289137":"102", "3223857":"111", "3748145":"119", "3158577":"120"}


if __name__=='__main__':

    rootdir = os.getcwd()
    for folderdir in glob.glob(rootdir + os.sep + 'KLine*'):
        print folderdir
        if os.path.isdir(folderdir):
            for fileKline in os.listdir(folderdir): 
                matched = re.search('([0-9]{7})', fileKline)
                if matched is None:
                    print fileKline , "  no matching"
                    continue
                subss = matched.group()
                try :
                    newName = fileKline.replace(subss, dictProduct[subss])
                    print fileKline, "---->", newName
                    os.rename (os.path.join(folderdir,fileKline) ,os.path.join(folderdir, newName) )
                except KeyError :
                    print "KeyError",fileKline
                    
    raw_input("Done, please input Enter to close ...")