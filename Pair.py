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
#include <stdio.h>
#include <iostream>
#include <common_base/fdbus.h>
#include <common_base/fdb_log_trace.h>
#include <mutex>
#include <list>
#include "sample.pb.h"
#include "../public/common_base/CFdbProtoMsgBuilder.h"

#define XCLT_TEST_SINGLE_DIRECTION 0
#define XCLT_TEST_BI_DIRECTION     1
#define XCLT_INIT_SKIP_COUNT       16
#define XCLT_TEST_SINGLE_DIRECTION1 3
#define XCLT_TEST_SINGLE_DIRECTION2 4

class CXClient;
static CBaseWorker *fdb_worker_A;

class CXTestJob : public CBaseJob {
public:
    explicit CXTestJob(const ClientOnlineMsg &msg, CXClient* client)
    : mMsg(msg)
    , mClient(client){}

protected:
    void run(CBaseWorker* worker, Ptr& ref) override;

private:
    ClientOnlineMsg mMsg;
    CXClient* mClient;
};



class CXClient : public CBaseClient
{
public:
    const char* mExtraName; 
    CXClient(const char *name, const char *extraName = nullptr, CBaseWorker *worker = 0, int8_t mBcast=0)
        : CBaseClient(name, worker)
        , mExtraName(extraName)
        , mBcast(mBcast)
    {
        enableUDP(true);
        enableTimeStamp(true);
        enableAysncWrite(true);
        enableAysncRead(true);
    }
    
    void invokeMethod(const char *data, const char* message)
    {
        //const char* message = "your id";
        //invoke(XCLT_TEST_BI_DIRECTION, (void*)message, strlen(message));
        invoke(XCLT_TEST_BI_DIRECTION, (void *)data, strlen(data));
        
        // only for in ra data
        if(mExtraName == "yourId"){
            std::cout << "hello server can you here me client : please send me your id" <<std::endl;
        }else if (mExtraName == "yourName"){
            std::cout << "hello server can you here me client : please send me your Name" <<std::endl;
        }
    }
protected:
    /* called when connected to the server */
    void onOnline(FdbSessionId_t sid, bool is_first)
    {
        // set value cho file sample.proto 
        ClientOnlineMsg msg;
        msg.set_sid(sid);
        msg.set_is_first(is_first);
        msg.set_extra_info(mExtraName);

        // sau do truyen msg worker de invoke -> or co the invoke truc tiep -> truyen qua server
        std::cout << "client " << sid << " Online" <<std::endl;
        //msg dc dua vao constructor cua cxtestjob -> gui cho worker
        fdb_worker_A->sendAsync(new CXTestJob(msg,this)); // send xtestjob, worker A do his job
        // khi worker A run thi no mới seriable 
        FDB_TLOG_I("Client", "Client received valid reply from server.");

        if(mBcast != 0){
            // --- Đăng ký nhận thông báo từ server ---
            CFdbMsgSubscribeList sub_list;
            addNotifyItem(sub_list, mBcast);  // đăng ký nhận broadcast với msg code
            subscribe(sub_list); // gọi hàm subscribe
        }
        
    }
    
    void onOffline(FdbSessionId_t sid, bool is_last)
    {
        std::cout << "offline from client " << sid << " goodbye " << std::endl;   
    }
    
    void onBroadcast(CBaseJob::Ptr &msg_ref)
    {
        //std::cout << "on broachcast " << std::endl;
        auto msg = castToMessage<CBaseMessage *>(msg_ref); // Ép kiểu từ job thành message
        const void *buffer = msg->getPayloadBuffer();      // Lấy buffer payload
        int32_t size = msg->getPayloadSize();              // Lấy kích thước payload

        // Chuyển payload thành std::string
        std::string received_msg(reinterpret_cast<const char *>(buffer), size);

        // In ra thông tin nhận được
        std::cout << "Received broadcast message: " << received_msg << std::endl;

    }

    void onReply(CBaseJob::Ptr &msg_ref)
    {
        auto msg = castToMessage<CBaseMessage *>(msg_ref);
        if (msg->isStatus())
        {
            /* Unable to get intended reply from server... Check what happen. */
            if (msg->isError())
            {
                int32_t error_code;
                std::string reason;
                if (!msg->decodeStatus(error_code, reason))
                {
                    std::cout << "onReply: fail to decode status!\n" << std::endl;
                    return;
                }
                std::cout << "onReply(): status is received: msg code: " << msg->code()
                            << ", error_code: " << error_code
                            << ", reason: " << reason
                            << std::endl;
                //mFailureCount++;
            }
            return;
        }
        // Giải mã nội dung phản hồi từ server
        auto buffer = msg->getPayloadBuffer();
        auto size = msg->getPayloadSize();
        std::string reply_msg(reinterpret_cast<const char *>(buffer), size);

        // In ra kết quả
        std::cout << "Client nhận được ID từ server: " << reply_msg << std::endl;
}

    // Getter
    uint8_t getBcast() const {
        return mBcast;
    }

    // Setter
    void setBcast(uint8_t bcast) {
        mBcast = bcast;
    }

private:
    uint8_t mBcast;
};


void CXTestJob::run(CBaseWorker *worker, Ptr &ref)
{
    //fdb_xtest_client->invokeMethod(mSid,"yourId");
    //mClient->invokeMethod(mSid,mClient->mExtraName);
    //FDB_CONTEXT->flush();
    // serial xong bien thanh string
    std::string data = mMsg.SerializeAsString();
    mClient->invokeMethod(data.c_str(), mClient->mExtraName);

    FDB_CONTEXT->flush();
}

std::vector<CXClient*> clients;
CXClient* fdb_xtest_client1 = nullptr;
CXClient* fdb_xtest_client2 = nullptr;

int main(int argc, char **argv)
{

    std::cout << "Hello Fdbus from Client" << std::endl;
    
    FDB_CONTEXT->enableLogger(false);
    /* start fdbus context thread */
    FDB_CONTEXT->start();

    fdb_worker_A = new CBaseWorker();
    fdb_worker_A->start();
    
    
    //for (int i = 1; i < argc; ++i)
    //{
        ////if (argc < 3)
        //{
        //    std::cout << "Please provide two client names\n";
        //    return -1;
        //}

        std::string url1(FDB_URL_SVC);
        url1 += argv[1];
        std::string client_name1 = std::string(argv[1]) + "_client";
        fdb_xtest_client1 = new CXClient(client_name1.c_str(),"yourId",nullptr,XCLT_TEST_SINGLE_DIRECTION1);
        fdb_xtest_client1->connect(url1.c_str());

        std::string url2(FDB_URL_SVC);
        url2 += argv[2];
        std::string client_name2 = std::string(argv[2]) + "_client";
        fdb_xtest_client2 = new CXClient(client_name2.c_str(),"yourName",nullptr,XCLT_TEST_SINGLE_DIRECTION2);
        fdb_xtest_client2->connect(url2.c_str());
        
        /* std::string server_name = argv[i];
        std::string url(FDB_URL_SVC);
        url += server_name;
        server_name += "_client";
        //auto fdb_xtest_client = new CXClient(server_name.c_str());
        //fdb_xtest_client->connect(url.c_str());

        CXClient* client = new CXClient(server_name.c_str(),"yourId");
        client->connect(url.c_str());
        clients.push_back(client); */
   // }

    //FDB_TLOG_D("Client", "onReply: received error");
    //FDB_TLOG_I("Client", "Client received valid reply from server.");

    /* convert main thread into worker */
    CBaseWorker background_worker;
    background_worker.start(FDB_WORKER_EXE_IN_PLACE);
}

