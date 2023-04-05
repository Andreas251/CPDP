#for VARIABLE in 1 2 3 4 5 .. 100
#do
#	wget http://dataset.isr.uc.pt/ISRUC_Sleep/subgroupI/$VARIABLE.rar -P ./isruc
#	cd isruc
#	unrar e $VARIABLE.rar
#	rm $VARIABLE.rar
#	cd ..
#done

mkdir isruc
cd isruc

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
		rm $COUNT.rar
		cd ..
	done

	cd ..
done
