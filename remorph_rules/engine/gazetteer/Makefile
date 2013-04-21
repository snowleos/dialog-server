
DIR_GZT=engine/gazetteer

gazetteer: ${DIR_BIN}/yafriend.gzt.bin
	
${DIR_BIN}/yafriend.gzt.bin: ${DIR_GZT}/yafriend.gzt ${DIR_GZT}/yafriend.proto ${DIR_GZT}/cascade.proto
	${GZT_COMPILER} -f ${DIR_GZT}/yafriend.gzt ${DIR_BIN}/yafriend.gzt.bin

clean_gazetteer: 
	rm -f ${DIR_BIN}/yafriend.gzt.bin

.PHONY: gazetteer clean_gazetter

