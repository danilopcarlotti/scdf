#!/bin/bash

# sudo updatedb;

ids_investigacao (){
	# echo "$1";
	IFS=' '
	read -a strarr <<< "$1";
	
	# for val in "${strarr[@]}";
	# do
	# python3 print_test.py "$val"
	# done
	
	touch 'investigacoes_processadas_scdf.txt';
	for val in "${strarr[@]}";
	do
	investigacao_processada "$val "
	done

	# if [ "$1" == "3eab531d" ]; then
	# 	echo "Ok!!"
	# 	exit 1;
	# else
	# 	echo 'Not my tempo!'
	# fi
}

investigacao_processada () {
	printf "$1" >> 'investigacoes_processadas_scdf.txt'
}

id_inv=$(locate -e0 'id_investigacao_scdf.txt' | xargs -r0 cat);
ids_investigacao "$id_inv"

# id_inv=$(locate -e0 'investigacoes_processadas_scdf.txt' | xargs -r0 cat);
# echo "$id_inv"
