/*
 * Copyright (C) 2015   Jeremy Chen jeremy_cz@yahoo.com
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

#include <string.h>
#include <stdlib.h>
#include <iostream>
#include <common_base/fdbus.h>
#include "sample.pb.h"
#include "../public/common_base/CFdbProtoMsgBuilder.h"

#define XCLT_TEST_SINGLE_DIRECTION 0
#define XCLT_TEST_SINGLE_DIRECTION1 3
#define XCLT_TEST_SINGLE_DIRECTION2 4
#define XCLT_TEST_BI_DIRECTION     1

class CXServer;
static CBaseWorker *fdb_worker;

class CXServer : public CBaseServer
{
public:
    CXServer(const char *name, CBaseWorker *worker = 0)
        : CBaseServer(name, worker)
    {
        enableUDP(true);
        enableAysncRead(true);
        enableAysncWrite(true);
    }
    
protected:
    void onOnline(FdbSessionId_t sid, bool is_first)
    {
        std::cout << "server Online: ready to received any request!" << std::endl;
        FDB_TLOG_I("Client", "Server received valid reply from client.");
    }
    void onOffline(FdbSessionId_t sid, bool is_last)
    {
        std::cout << "server offline" << std::endl;
    }
    void onInvoke(CBaseJob::Ptr &msg_ref)
    {
        auto msg = castToMessage<CBaseMessage *>(msg_ref); // todo: doan nay lam gi
        auto buffer = msg->getPayloadBuffer(); // in cai nay ra
        auto size = msg->getPayloadSize();

        // Chuyển payload buffer thành string (giả sử payload là dữ liệu text)
        //std::string received_msg(static_cast<const char *>(buffer), size);
        std::string received_msg(reinterpret_cast<const char *>(buffer), size); //-> cach nay ko an toan
        // data co the bi sai

        // In ra màn hình
        std::cout << "check received msg: " << received_msg << std::endl;
        
        // tao 1 protobuf
        ClientOnlineMsg client_msg;
        if (!client_msg.ParseFromArray(buffer, size)) { // assign buffer toi protobuf
        std::cerr << "Failed to parse ClientOnlineMsg protobuf message" << std::endl;
        return;
        }

        // lay data tu protobuf
        std::string received_msg1 = client_msg.extra_info();

        // So sánh nội dung nhận được với "your id:"
        if (received_msg1 == "yourId")
        {
            const char* reply_msg = "pch1hc";
            std::cout << "Server accept request from client - my id is: " << reply_msg << std::endl;
            msg->reply(msg_ref, reply_msg, strlen(reply_msg));
        }
        else if(received_msg1 == "yourName")
        {
            const char* reply_msg = "Cuong";
            std::cout << "Server accept request from client - my name is: " << reply_msg << std::endl;
            msg->reply(msg_ref, reply_msg, strlen(reply_msg));
        }
        else
        {
            std::cout << "Server NOT accept request from client - my name is: " << received_msg << std::endl;
            // Nếu không phải, phản hồi lại như cũ
            auto to_be_release = msg->ownBuffer();
            msg->reply(msg_ref, buffer, size);
            msg->releaseBuffer(to_be_release);
        }

        // khu vuc broascast
        const char *payload1 = "hello world 1";
        // neu ai dk XCLT_TEST_SINGLE_DIRECTION1 -> tra data cho client do
        // cau hoi la cau truc msg ?
        broadcast(XCLT_TEST_SINGLE_DIRECTION1,  payload1, strlen(payload1),
                          "", FDB_QOS_BEST_EFFORTS);
        const char *payload2 = "hello world 2";
        broadcast(XCLT_TEST_SINGLE_DIRECTION2,  payload2, strlen(payload2),
                          "", FDB_QOS_BEST_EFFORTS);

    }
private:

   
};


int main(int argc, char **argv)
{
    std::cout << "Hello Fdbus from server" << std::endl;
    
    FDB_CONTEXT->enableLogger(false);
    /* start fdbus context thread */
    FDB_CONTEXT->start();

    //fdb_worker = new CBaseWorker();
    //fdb_worker->start();
    for (int i = 1; i < argc; ++i)
    {
        std::string server_name = argv[i];
        std::string url(FDB_URL_SVC);
        url += server_name;
        server_name += "_server";
        
        auto server = new CXServer(server_name.c_str());
        server->bind(url.c_str());
    }
    /* convert main thread into worker */
    CBaseWorker background_worker;
    background_worker.start(FDB_WORKER_EXE_IN_PLACE);
}

