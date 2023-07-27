const Socket = Initials.socket
const local_user = Initials.activeUserName
const userWorkSpaceNAme = Initials.workSpaceName


Socket.onmessage = function (event) {
    var element = document.createElement('div');
    var chtmsg = event.data
    var parsedData = JSON.parse(chtmsg)
    var Type = parsedData.Type
    var text = document.createTextNode(message);
    var task = parsedData.task
    element.appendChild(text);
    element.setAttribute('style', 'color:black;');
    if (task === "onMessage") 
    {   
        var from = parsedData.from
        var to = parsedData.to
        var message = parsedData.Message
        var type_ = parsedData.type_
        var date = parsedData.date
        var time = parsedData.time
        if (Type === "Private") 
        {
            if (from === local_user) 
            {
                if (type_ == "message") 
                {
                    var container = document.getElementById(from+"-Message");
                    const mes = `<div id="Message" class="d-flex bd-highlight m-2">
                            <div class="p-2 flex-shrink-1 bd-highlight">
                                <div class="rounded message-profile-pic"><p class="message-profile-pic-text">`+from+`<p></div>
                            </div>
                            <div class="p-2 w-100 bd-highlight">
                                <p class="font-weight-bold d-inline">`+from+`</p><span class="text-muted float-right">`+time+`</span>
                                <p class="text-break">`+message+`</p>
                            </div>
                        </div>`;
                    $(container).append(mes);
                    scrollBottom("#"+from+"-Main") 
                }
                else 
                {
                    var container = document.getElementById(from);
                    checkFileType(message,from,to,parsedData.fileurl,date,time)            
                }
            }
            else 
            {
                if(type_ == "message")
                {   
                    var container = document.getElementById(from+"-Message");
                    const mes = `<div id="Message" class="d-flex bd-highlight m-2">
                            <div class="p-2 flex-shrink-1 bd-highlight">
                                <div class="rounded message-profile-pic"><p class="message-profile-pic-text">`+from+`</p></div>
                            </div>
                            <div class="p-2 w-100 bd-highlight">
                                <p class="font-weight-bold d-inline">`+from+`</p><span class="text-muted float-right">`+time+`</span>
                                <p class="text-break">`+message+`</p>
                            </div>
                        </div>`;
                    $(container).append(mes);
                    scrollBottom("#"+from+"-Main")
                }
                else
                {
                    var container = document.getElementById(from);
                    checkFileType(message,from,to,parsedData.fileurl,date,time)            
                }
            }
        }
        else 
        {   
            if(type_ == "message")
            {   
                const mes = `<div id="Message" class="d-flex bd-highlight m-2">
                        <div class="p-2 flex-shrink-1 bd-highlight">
                            <div class="rounded message-profile-pic"><p class="message-profile-pic-text">`+from+`</p></div>
                        </div>
                        <div class="p-2 w-100 bd-highlight">
                            <p class="font-weight-bold d-inline">`+from+`</p><span class="text-muted float-right">`+time+`</span>
                            <p class="text-break">`+message+`</p>
                        </div>
                    </div>`;
                $("#"+parsedData.to+"-Message").append(mes);
                scrollBottom("#"+to+"-Main")
            }
            else {
                checkFileTypeGroup(message,from,parsedData.to,"msg1",parsedData.fileurl,time,date)
                
            }
        }
    }
    else if (task === "retriveOlderMessage") {
        var retriveMessage = parsedData.data
        messageAppend(retriveMessage)
    }
    else if (task === "flash") {
        notify("ChatApp",parsedData['alertMessage']);
    }
    else if (task === "activeUsers") {
        onlineStatus(parsedData)
    }
}

Socket.onclose = function (event) {
    alert("Session Closed! Please Reload!")
    location.reload();
}

Socket.onerror = function (error) {
    alert(error);
}
// --------------------------------------------------------------Functions------------------------------------------------------------------------------------

// Show image if images are sent on the Privatechat 
function checkFileType(Messages,_User,from,url,date,time) {
    var extensions = ["PNG","png","jpg","jpeg","JPEG","gif","webp"]
    var fileExt = Messages.split('.').pop();
    var checkExtension = extensions.includes(fileExt)
    if (checkExtension == true){
        const mes = `<div id="Message" class="d-flex bd-highlight m-2">
                        <div class="p-2 flex-shrink-1 bd-highlight">
                            <div class="rounded message-profile-pic"><p class="message-profile-pic-text">`+_User+`</p></div>
                        </div>
                        <div class="p-2 w-100 bd-highlight">
                            <p class="font-weight-bold d-inline">`+_User+`</p><span class="text-muted float-right">`+time+`</span>
                            <a class="" href="`+url+`" download><img class="d-flex img-fluid" style="max-width:256px;max-height:256px;" src="`+url+`" alt="`+url+`"></a>
                        </div>
                    </div>`;
        $("#"+_User+"-Message").append(mes);
        scrollBottom("#"+_User+"-Main")
        // $(".chatBody").animate({ scrollTop: 20000000 }, "fast");
    }
    else {
        const mes = `<div id="Message" class="d-flex bd-highlight m-2">
                        <div class="p-2 flex-shrink-1 bd-highlight">
                            <div class="rounded message-profile-pic"><p class="message-profile-pic-text">`+_User+`</p></div>
                        </div>
                        <div class="p-2 w-100 bd-highlight">
                            <p class="font-weight-bold d-inline">`+_User+`</p><span class="text-muted float-right">`+time+`</span>
                            <div class="d-flex bd-highlight p-4 rounded text-center border" style="height:100px;width:300px;background-color: rgb(223, 217, 217);">
                                <div class="p-2 w-100 bd-highlight">`+Messages+`</div>
                                <div class="p-2 flex-shrink-1 bd-highlight">
                                    <a href="`+url+`" download><span class="fa fa-download	 mr-1 text-black" style="font-size: 40px;"></span></a>
                                </div>
                            </div>
                        </div>
                    </div>`;
        $("#"+_User+"-Message").append(mes);
        scrollBottom("#"+_User+"-Main")
    }
    
}


// Show image if images are sent on the Groupchat 
function checkFileTypeGroup(Message,from,_User,side,url,time,date) {
    var extensions = ["PNG","png","jpg","jpeg","JPEG","gif","webp"]
    var fileExt = Message.split('.').pop();
    var checkExtension = extensions.includes(fileExt)
    if (checkExtension == true){
        const mes = `<div id="Message" class="d-flex bd-highlight m-2">
                        <div class="p-2 flex-shrink-1 bd-highlight">
                            <div class="rounded message-profile-pic"><p class="message-profile-pic-text">`+from+`</p></div>
                        </div>
                        <div class="p-2 w-100 bd-highlight">
                            <p class="font-weight-bold d-inline">`+from+`</p><span class="text-muted float-right">`+time+`</span>
                            <a href="`+url+`" download><img class="d-flex img-fluid" style="max-width:256px;max-height:256px;" src="`+url+`" alt="`+url+`"></a>
                        </div>
                    </div>`;
        $("#"+_User+"-Message").append(mes);
        scrollBottom("#"+_User+"-Main")
    }
    else {
        const mes = `<div id="Message" class="d-flex bd-highlight m-2">
                        <div class="p-2 flex-shrink-1 bd-highlight">
                            <div class="rounded message-profile-pic"><p class="message-profile-pic-text">`+from+`</p></div>
                        </div>
                        <div class="p-2 w-100 bd-highlight">
                            <p class="font-weight-bold d-inline">`+from+`</p><span class="text-muted float-right">`+time+`</span>
                            <div class="d-flex bd-highlight p-4 rounded text-center border" style="height:100px;width:300px;background-color: rgb(223, 217, 217);">
                                <div class="p-2 w-100 bd-highlight text-break">`+Message+`</div>
                                <div class="p-2 flex-shrink-1 bd-highlight">
                                    <a href="`+url+`" download><span class="fa fa-download	 mr-1 text-black" style="font-size: 40px;"></span></a>
                                </div>
                            </div>
                        </div>
                    </div>`;
        $("#"+_User+"-Message").append(mes);
        scrollBottom("#"+_User+"-Main")
    }
    
}


// Message Append
function messageAppend(retriveMessage){
    var i;
        var j;
        for (i in retriveMessage) {
            var User = retriveMessage[i][0]
            var _User = document.getElementById(User);
            var Messages = retriveMessage[i][1]
            
            for (j in Messages) {
                // if condition is for group Messages
                if (Messages[j]["from"]) {
                    if (Messages[j]['type_'] === "file"){
                        checkFileTypeGroup(Messages[j]['Message'],Messages[j]["from"],User,"msg1",Messages[j]['fileurl'],Messages[j]['time'],Messages[j]['date'])
                    }
                    else {
                        const mes = `<div id="Message" class="d-flex bd-highlight m-2">
                            <div class="p-2 flex-shrink-1 bd-highlight">
                                <div class="rounded message-profile-pic"><p class="message-profile-pic-text">`+Messages[j]["from"]+`</p></div>
                            </div>
                            <div class="p-2 w-100 bd-highlight">
                                <p class="font-weight-bold d-inline">`+Messages[j]["from"]+`</p><span class="text-muted float-right">`+Messages[j]["time"]+`</span>
                                <p>`+Messages[j]['Message']+`</p>
                            </div>
                        </div>`;
                        var us = User;
                        $("#" + us + "-Message").append(mes);
                        scrollBottom("#"+us+"-Main")
                    }
                }

                // Else-If condition is for the Private Messages Sender side    
                else if (Messages[j]['msgType'] === "S") {
                    if (Messages[j]['type_'] === "file"){
                        checkFileType(Messages[j]['Message'],User,"msg2", Messages[j]['fileurl'],Messages[j]['date'],Messages[j]['time'])
                        }
                    else{
                        var container = document.getElementById(User+"-Message");
                        const mes = `<div id="Message" class="d-flex bd-highlight m-2">
                                        <div class="p-2 flex-shrink-1 bd-highlight">
                                            <div class="rounded message-profile-pic"><p class="message-profile-pic-text">`+local_user+`</p></div>
                                        </div>
                                        <div class="p-2 w-100 bd-highlight">
                                            <p class="font-weight-bold d-inline">`+local_user+`</p><span class="text-muted float-right">`+Messages[j]['time']+`</span>
                                            <p>`+Messages[j]['Message']+`</p>
                                        </div>
                                    </div>`;
                        $(container).append(mes);
                        scrollBottom("#"+User+"-Main")
                    }
                }
                else {
                    if (Messages[j]['type_'] === "file"){
                        checkFileType(Messages[j]['Message'],User,"msg1",Messages[j]['fileurl'])
                    }
                    else{
                        var container = document.getElementById(User+"-Message");
                        const mes = `<div id="Message" class="d-flex bd-highlight m-2">
                                        <div class="p-2 flex-shrink-1 bd-highlight">
                                            <div class="rounded message-profile-pic"><p class="message-profile-pic-text">`+User+`</p></div>
                                        </div>
                                        <div class="p-2 w-100 bd-highlight">
                                            <p class="font-weight-bold d-inline">`+User+`</p><span class="text-muted float-right">`+Messages[j]['time']+`</span>
                                            <p>`+Messages[j]['Message']+`</p>
                                        </div>
                                    </div>`;
                        $(container).append(mes);
                        scrollBottom("#"+User+"-Main")
            }
        }
}
        }
    }



function onlineStatus(_Data_){
    statusData = _Data_
    // {'task': 'activeUsers', 'online': ['beast'], 'offline': ['akshaya']}
    for (x of statusData.online) {
        // $("#"+x+"-status").toggleClass("text-success");
        $("#"+x+"-status").addClass("text-success");
    }
    for ( y of statusData.offline) {
        // $("#"+x+"-status").removeClass("text-success");
        $("#"+y+"-status").addClass("text-danger");        
    }        
}
