#for VARIABLE in 1 2 3 4 5 .. 100
#do
#	wget http://dataset.isr.uc.pt/ISRUC_Sleep/subgroupI/$VARIABLE.rar -P ./isruc
#	cd isruc
#	unrar e $VARIABLE.rar
#	rm $VARIABLE.rar
#	cd ..
#done

#!/bin/bash

cd ~/mnt

for VARIABLE in "subgroupI 100" "subgroupII 8" "subgroupIII 10"
do
	set -- $VARIABLE
	mkdir $1
	cd $1

	for ((COUNT=1;COUNT<=$2;COUNT++))
	do
		mkdir $COUNT
		cd $COUNT
		wget http://dataset.isr.uc.pt/ISRUC_Sleep/$1/$COUNT.rar
        unrar e $COUNT.rar
        
        if [ "$1" == "subgroupII" ]
        then
            wget http://dataset.isr.uc.pt/ISRUC_Sleep/ExtractedChannels/$1-Extractedchannels/1/subject$COUNT.mat
            wget http://dataset.isr.uc.pt/ISRUC_Sleep/ExtractedChannels/$1-Extractedchannels/2/subject$COUNT.mat
        else
            wget http://dataset.isr.uc.pt/ISRUC_Sleep/ExtractedChannels/$1-Extractedchannels/subject$COUNT.mat
        fi
        
		rm $COUNT.rar
        rm $COUNT.rec
        
		cd ..
	done

	cd ..
done
