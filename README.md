# Chaoxing-dl
超星学术视频Downloader
==========

用法：
----
*    -h , --help                      获取帮助信息
*    -v , --version                   获取版本信息
*    -s , --serie                     超星课程列表地址,多个用逗号分隔,如："http://video.chaoxing.com/serie_400000001.shtml"
*    -g , --get                       选择课程列表的某项或某几项(逗号分隔)下载,如："1,5-10,11"
*    -o , --output                    选择输出路径,如："D:\Download\\"
*    -r , --raw                       支持wget源命令，如："--limit-rate=1024k"
*    -i , --id                        指定video_id，某些情况下，无法仅由列表获取下载链接;获取方法:使用idm下载其中任意一个视频，对照如下链接格式，使用-i参数指定video_id即可;http://video.superlib.com/shipin0(server_id)/cx/(video_id)/0/(teacher_id)/(video_number).flv
