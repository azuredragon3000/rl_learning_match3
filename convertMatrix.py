huycuong@huycuong-HP-245-G8-Notebook-PC:~$ sudo docker start myapp
[sudo] password for huycuong: 
myapp
huycuong@huycuong-HP-245-G8-Notebook-PC:~$ docker exec -it myapp 
docker: 'docker exec' requires at least 2 arguments

Usage:  docker exec [OPTIONS] CONTAINER COMMAND [ARG...]

See 'docker exec --help' for more information
huycuong@huycuong-HP-245-G8-Notebook-PC:~$ docker exec -it myapp /bin/bash
permission denied while trying to connect to the Docker daemon socket at unix:///var/run/docker.sock: Get "http://%2Fvar%2Frun%2Fdocker.sock/v1.48/containers/myapp/json": dial unix /var/run/docker.sock: connect: permission denied
huycuong@huycuong-HP-245-G8-Notebook-PC:~$ sudo docker exec -it myapp /bin/bash
root@10e1159573a5:/# cd ~/workspace
root@10e1159573a5:~/workspace# cd fdbus/build
root@10e1159573a5:~/workspace/fdbus/build# ls
CMakeCache.txt	cmake_install.cmake    fdbxserver   install_manifest.txt  logsvc     lsevt   name_server
CMakeFiles	cmake_uninstall.cmake  host_server  libcommon_base.so	  logviewer  lshost  ntfcenter
Makefile	fdbxclient	       install	    libfdbus-clib.so	  lsclt      lssvc
root@10e1159573a5:~/workspace/fdbus/build# ./logsvc
^C
root@10e1159573a5:~/workspace/fdbus/build# cmake \
      -DCMAKE_INSTALL_PREFIX=install \
      -Dfdbus_ENABLE_LOG=ON \
      -Dfdbus_LOG_TO_STDOUT=ON \
      ../cmake
-- PACKAGE_SOURCE_ROOT=/root/workspace/fdbus
-- fdbus_ENABLE_LOG=ON
-- fdbus_LOG_TO_STDOUT=ON
-- fdbus_SOCKET_ENABLE_PEERCRED=ON
-- fdbus_ALLOC_PORT_BY_SYSTEM=OFF
-- fdbus_SECURITY=OFF
-- fdbus_ANDROID=OFF
-- fdbus_PIPE_AS_EVENTFD=OFF
-- fdbus_BUILD_JNI=OFF
-- fdbus_LINK_SOCKET_LIB=OFF
-- fdbus_LINK_PTHREAD_LIB=ON
-- fdbus_BUILD_CLIB=ON
-- Configuring done
-- Generating done
-- Build files have been written to: /root/workspace/fdbus/build
root@10e1159573a5:~/workspace/fdbus/build# make    
[  1%] Building CXX object CMakeFiles/common_base.dir/root/workspace/fdbus/fdbus/CBaseClient.cpp.o
[  2%] Building CXX object CMakeFiles/common_base.dir/root/workspace/fdbus/fdbus/CBaseEndpoint.cpp.o
[  3%] Building CXX object CMakeFiles/common_base.dir/root/workspace/fdbus/fdbus/CBaseServer.cpp.o
[  4%] Building CXX object CMakeFiles/common_base.dir/root/workspace/fdbus/fdbus/CEventSubscribeHandle.cpp.o
[  6%] Building CXX object CMakeFiles/common_base.dir/root/workspace/fdbus/fdbus/CFdbAFComponent.cpp.o
[  7%] Building CXX object CMakeFiles/common_base.dir/root/workspace/fdbus/fdbus/CFdbBaseContext.cpp.o
[  8%] Building CXX object CMakeFiles/common_base.dir/root/workspace/fdbus/fdbus/CFdbBaseObject.cpp.o
[  9%] Building CXX object CMakeFiles/common_base.dir/root/workspace/fdbus/fdbus/CFdbCJsonMsgBuilder.cpp.o
[ 11%] Building CXX object CMakeFiles/common_base.dir/root/workspace/fdbus/fdbus/CFdbContext.cpp.o
[ 12%] Building CXX object CMakeFiles/common_base.dir/root/workspace/fdbus/fdbus/CFdbEventRouter.cpp.o
[ 13%] Building CXX object CMakeFiles/common_base.dir/root/workspace/fdbus/fdbus/CFdbMessage.cpp.o
[ 14%] Building CXX object CMakeFiles/common_base.dir/root/workspace/fdbus/fdbus/CFdbMsgDispatcher.cpp.o
[ 16%] Building CXX object CMakeFiles/common_base.dir/root/workspace/fdbus/fdbus/CFdbSession.cpp.o
[ 17%] Building CXX object CMakeFiles/common_base.dir/root/workspace/fdbus/fdbus/CFdbSessionContainer.cpp.o
[ 18%] Building CXX object CMakeFiles/common_base.dir/root/workspace/fdbus/fdbus/CFdbSimpleSerializer.cpp.o
[ 19%] Building CXX object CMakeFiles/common_base.dir/root/workspace/fdbus/fdbus/CFdbUDPSession.cpp.o
[ 20%] Building CXX object CMakeFiles/common_base.dir/root/workspace/fdbus/fdbus/CFdbWatchdog.cpp.o
[ 22%] Building CXX object CMakeFiles/common_base.dir/root/workspace/fdbus/fdbus/CIntraNameProxy.cpp.o
[ 23%] Building CXX object CMakeFiles/common_base.dir/root/workspace/fdbus/platform/linux/CBaseMutexLock.cpp.o
[ 24%] Building CXX object CMakeFiles/common_base.dir/root/workspace/fdbus/platform/linux/CBasePipe.cpp.o
[ 25%] Building CXX object CMakeFiles/common_base.dir/root/workspace/fdbus/platform/linux/CBaseSemaphore.cpp.o
[ 27%] Building CXX object CMakeFiles/common_base.dir/root/workspace/fdbus/platform/linux/CBaseSysDep.cpp.o
[ 28%] Building CXX object CMakeFiles/common_base.dir/root/workspace/fdbus/platform/linux/CBaseThread.cpp.o
[ 29%] Building CXX object CMakeFiles/common_base.dir/root/workspace/fdbus/platform/CEventFd_eventfd.cpp.o
[ 30%] Building CXX object CMakeFiles/common_base.dir/root/workspace/fdbus/platform/socket/CBaseSocketFactory.cpp.o
[ 32%] Building CXX object CMakeFiles/common_base.dir/root/workspace/fdbus/platform/socket/linux/CLinuxSocket.cpp.o
[ 33%] Building CXX object CMakeFiles/common_base.dir/root/workspace/fdbus/platform/socket/sckt-0.5/sckt.cpp.o
[ 34%] Building CXX object CMakeFiles/common_base.dir/root/workspace/fdbus/utils/CBaseNameProxy.cpp.o
[ 35%] Building CXX object CMakeFiles/common_base.dir/root/workspace/fdbus/utils/fdb_option_parser.cpp.o
[ 37%] Building CXX object CMakeFiles/common_base.dir/root/workspace/fdbus/worker/CBaseEventLoop.cpp.o
[ 38%] Building CXX object CMakeFiles/common_base.dir/root/workspace/fdbus/worker/CBaseWorker.cpp.o
[ 39%] Building CXX object CMakeFiles/common_base.dir/root/workspace/fdbus/worker/CFdEventLoop.cpp.o
[ 40%] Building CXX object CMakeFiles/common_base.dir/root/workspace/fdbus/worker/CSysFdWatch.cpp.o
[ 41%] Building CXX object CMakeFiles/common_base.dir/root/workspace/fdbus/worker/CThreadEventLoop.cpp.o
[ 43%] Building C object CMakeFiles/common_base.dir/root/workspace/fdbus/utils/cJSON/cJSON.c.o
[ 44%] Building CXX object CMakeFiles/common_base.dir/root/workspace/fdbus/log/CLogProducer.cpp.o
[ 45%] Building CXX object CMakeFiles/common_base.dir/root/workspace/fdbus/log/CLogPrinter.cpp.o
[ 46%] Building CXX object CMakeFiles/common_base.dir/root/workspace/fdbus/log/CFdbLogCache.cpp.o
[ 48%] Building CXX object CMakeFiles/common_base.dir/root/workspace/fdbus/security/CApiSecurityConfig.cpp.o
[ 49%] Building CXX object CMakeFiles/common_base.dir/root/workspace/fdbus/security/CFdbToken.cpp.o
[ 50%] Building CXX object CMakeFiles/common_base.dir/root/workspace/fdbus/security/CFdbusSecurityConfig.cpp.o
[ 51%] Linking CXX shared library libcommon_base.so
[ 51%] Built target common_base
[ 53%] Building CXX object CMakeFiles/name_server.dir/root/workspace/fdbus/server/main_ns.cpp.o
[ 54%] Building CXX object CMakeFiles/name_server.dir/root/workspace/fdbus/server/CNameServer.cpp.o
[ 55%] Building CXX object CMakeFiles/name_server.dir/root/workspace/fdbus/server/CInterNameProxy.cpp.o
[ 56%] Building CXX object CMakeFiles/name_server.dir/root/workspace/fdbus/server/CHostProxy.cpp.o
[ 58%] Building CXX object CMakeFiles/name_server.dir/root/workspace/fdbus/server/CAddressAllocator.cpp.o
[ 59%] Building CXX object CMakeFiles/name_server.dir/root/workspace/fdbus/security/CServerSecurityConfig.cpp.o
[ 60%] Linking CXX executable name_server
[ 60%] Built target name_server
[ 61%] Building CXX object CMakeFiles/host_server.dir/root/workspace/fdbus/server/main_hs.cpp.o
[ 62%] Building CXX object CMakeFiles/host_server.dir/root/workspace/fdbus/server/CHostServer.cpp.o
[ 64%] Building CXX object CMakeFiles/host_server.dir/root/workspace/fdbus/security/CHostSecurityConfig.cpp.o
[ 65%] Linking CXX executable host_server
[ 65%] Built target host_server
[ 66%] Building CXX object CMakeFiles/lssvc.dir/root/workspace/fdbus/server/main_ls.cpp.o
[ 67%] Linking CXX executable lssvc
[ 67%] Built target lssvc
[ 69%] Building CXX object CMakeFiles/lshost.dir/root/workspace/fdbus/server/main_lh.cpp.o
[ 70%] Linking CXX executable lshost
[ 70%] Built target lshost
[ 71%] Building CXX object CMakeFiles/lsclt.dir/root/workspace/fdbus/server/main_lc.cpp.o
[ 72%] Linking CXX executable lsclt
[ 72%] Built target lsclt
[ 74%] Building CXX object CMakeFiles/logsvc.dir/root/workspace/fdbus/log/main_log_server.cpp.o
[ 75%] Building CXX object CMakeFiles/logsvc.dir/root/workspace/fdbus/log/CLogFileManager.cpp.o
[ 76%] Building CXX object CMakeFiles/logsvc.dir/root/workspace/fdbus/log/fdb_log_config.cpp.o
[ 77%] Linking CXX executable logsvc
[ 77%] Built target logsvc
[ 79%] Building CXX object CMakeFiles/logviewer.dir/root/workspace/fdbus/log/main_log_client.cpp.o
[ 80%] Building CXX object CMakeFiles/logviewer.dir/root/workspace/fdbus/log/fdb_log_config.cpp.o
[ 81%] Linking CXX executable logviewer
[ 81%] Built target logviewer
[ 82%] Building CXX object CMakeFiles/fdbxclient.dir/root/workspace/fdbus/server/main_xclient.cpp.o
In file included from /root/workspace/fdbus/server/main_xclient.cpp:26:
/root/workspace/fdbus/server/../public/common_base/CFdbProtoMsgBuilder.h: In member function 'virtual int32_t CFdbProtoMsgBuilder::build()':
/root/workspace/fdbus/server/../public/common_base/CFdbProtoMsgBuilder.h:38:33: warning: 'int google::protobuf::MessageLite::ByteSize() const' is deprecated: Please use ByteSizeLong() instead [-Wdeprecated-declarations]
   38 |         return mMessage.ByteSize();
      |                ~~~~~~~~~~~~~~~~~^~
In file included from /usr/include/google/protobuf/any.h:38,
                 from /usr/include/google/protobuf/generated_message_util.h:52,
                 from /root/workspace/fdbus/server/sample.pb.h:26,
                 from /root/workspace/fdbus/server/main_xclient.cpp:25:
/usr/include/google/protobuf/message_lite.h:381:7: note: declared here
  381 |   int ByteSize() const { return internal::ToIntSize(ByteSizeLong()); }
      |       ^~~~~~~~
/root/workspace/fdbus/server/../public/common_base/CFdbProtoMsgBuilder.h: In member function 'virtual int32_t CFdbProtoMsgBuilder::bufferSize()':
/root/workspace/fdbus/server/../public/common_base/CFdbProtoMsgBuilder.h:43:33: warning: 'int google::protobuf::MessageLite::ByteSize() const' is deprecated: Please use ByteSizeLong() instead [-Wdeprecated-declarations]
   43 |         return mMessage.ByteSize();
      |                ~~~~~~~~~~~~~~~~~^~
/usr/include/google/protobuf/message_lite.h:381:7: note: declared here
  381 |   int ByteSize() const { return internal::ToIntSize(ByteSizeLong()); }
      |       ^~~~~~~~
/root/workspace/fdbus/server/main_xclient.cpp: In member function 'void CXClient::invokeMethod(const char*, const char*)':
/root/workspace/fdbus/server/main_xclient.cpp:75:23: warning: comparison with string literal results in unspecified behavior [-Waddress]
   75 |         if(mExtraName == "yourId"){
      |            ~~~~~~~~~~~^~~~~~~~~~~
/root/workspace/fdbus/server/main_xclient.cpp:77:30: warning: comparison with string literal results in unspecified behavior [-Waddress]
   77 |         }else if (mExtraName == "yourName"){
      |                   ~~~~~~~~~~~^~~~~~~~~~~~~
[ 83%] Building CXX object CMakeFiles/fdbxclient.dir/root/workspace/fdbus/server/sample.pb.cc.o
[ 85%] Linking CXX executable fdbxclient
[ 85%] Built target fdbxclient
[ 86%] Building CXX object CMakeFiles/fdbxserver.dir/root/workspace/fdbus/server/main_xserver.cpp.o
In file included from /root/workspace/fdbus/server/main_xserver.cpp:22:
/root/workspace/fdbus/server/../public/common_base/CFdbProtoMsgBuilder.h: In member function 'virtual int32_t CFdbProtoMsgBuilder::build()':
/root/workspace/fdbus/server/../public/common_base/CFdbProtoMsgBuilder.h:38:33: warning: 'int google::protobuf::MessageLite::ByteSize() const' is deprecated: Please use ByteSizeLong() instead [-Wdeprecated-declarations]
   38 |         return mMessage.ByteSize();
      |                ~~~~~~~~~~~~~~~~~^~
In file included from /usr/include/google/protobuf/any.h:38,
                 from /usr/include/google/protobuf/generated_message_util.h:52,
                 from /root/workspace/fdbus/server/sample.pb.h:26,
                 from /root/workspace/fdbus/server/main_xserver.cpp:21:
/usr/include/google/protobuf/message_lite.h:381:7: note: declared here
  381 |   int ByteSize() const { return internal::ToIntSize(ByteSizeLong()); }
      |       ^~~~~~~~
/root/workspace/fdbus/server/../public/common_base/CFdbProtoMsgBuilder.h: In member function 'virtual int32_t CFdbProtoMsgBuilder::bufferSize()':
/root/workspace/fdbus/server/../public/common_base/CFdbProtoMsgBuilder.h:43:33: warning: 'int google::protobuf::MessageLite::ByteSize() const' is deprecated: Please use ByteSizeLong() instead [-Wdeprecated-declarations]
   43 |         return mMessage.ByteSize();
      |                ~~~~~~~~~~~~~~~~~^~
/usr/include/google/protobuf/message_lite.h:381:7: note: declared here
  381 |   int ByteSize() const { return internal::ToIntSize(ByteSizeLong()); }
      |       ^~~~~~~~
/root/workspace/fdbus/server/main_xserver.cpp: At global scope:
/root/workspace/fdbus/server/main_xserver.cpp:30:21: warning: 'fdb_worker' defined but not used [-Wunused-variable]
   30 | static CBaseWorker *fdb_worker;
      |                     ^~~~~~~~~~
[ 87%] Building CXX object CMakeFiles/fdbxserver.dir/root/workspace/fdbus/server/sample.pb.cc.o
[ 88%] Linking CXX executable fdbxserver
[ 88%] Built target fdbxserver
[ 90%] Building CXX object CMakeFiles/ntfcenter.dir/root/workspace/fdbus/server/main_nc.cpp.o
[ 91%] Linking CXX executable ntfcenter
[ 91%] Built target ntfcenter
[ 92%] Building CXX object CMakeFiles/lsevt.dir/root/workspace/fdbus/server/main_le.cpp.o
[ 93%] Linking CXX executable lsevt
[ 93%] Built target lsevt
[ 95%] Building CXX object CMakeFiles/fdbus-clib.dir/root/workspace/fdbus/c/fdbus_afcomponent.cpp.o
[ 96%] Building CXX object CMakeFiles/fdbus-clib.dir/root/workspace/fdbus/c/fdbus_clib.cpp.o
[ 97%] Building CXX object CMakeFiles/fdbus-clib.dir/root/workspace/fdbus/c/fdbus_client.cpp.o
[ 98%] Building CXX object CMakeFiles/fdbus-clib.dir/root/workspace/fdbus/c/fdbus_server.cpp.o
[100%] Linking CXX shared library libfdbus-clib.so
[100%] Built target fdbus-clib
root@10e1159573a5:~/workspace/fdbus/build# ./logsvc
D+I+FDBUS+815@+2025-06-14 03:15:46:309+ CIntraNameProxy: Server: org.fdbus.log-server, address ipc:///tmp/fdb-ipc5 is bound.
D+I+FDBUS+815@10e1159573a5+2025-06-14 03:15:46:309+ CIntraNameProxy: status is received: msg code: 0, id: -22, reason: 

