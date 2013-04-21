
DIR_NAVI_SCHEDULE_MEETING=engine/rules/yafriend/schedule_meeting

schedule_meeting: ${DIR_BIN}/yafriend.schedule_meeting.remorph.bin

${DIR_BIN}/yafriend.schedule_meeting.remorph.bin: ${DIR_BIN}/yafriend.gzt.bin \
         ${DIR_NAVI_SCHEDULE_MEETING}/main.remorph
	${REMORPH_COMPILER} -g ${DIR_BIN}/yafriend.gzt.bin -t remorph ${DIR_NAVI_SCHEDULE_MEETING}/main.remorph -o ${DIR_BIN}/yafriend.schedule_meeting.remorph.bin

clean_schedule_meeting: 
	rm -f ${DIR_BIN}/yafriend.schedule_meeting.remorph.bin


