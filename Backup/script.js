'use strict';

// var ws_url = `ws://${window.location.hostname}:${window.location.port}${window.location.pathname}ws/`;
var ws_url = `ws://${window.location.hostname}:${window.location.port}/messenger/ws/`;
$(".textarea").hide();//hide the text area button in hometab
var activeUserName = userName();
var userWorkSpaceNAme = workSpaceName();
var local_user = activeUserName
var socket = new WebSocket(ws_url);
// init_socket()
socket.onmessage = function (event) {
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
        if (Type === "Private") 
        {
            if (from === local_user) 
            {
                if (type_ == "message") 
                {
                    var container = document.getElementById(from);
                    var rev = '<p class="msg2">' + message + '</p><br>'
                    $(container).append(rev);
                    $(".chatBody").animate({ scrollTop: 20000000 }, "fast");
                }
                else 
                {
                    var container = document.getElementById(from);
                    checkFileType(message,container,"msg2",parsedData.fileurl)            
                }
            }
            else 
            {
                if(type_ == "message")
                {
                    var container = document.getElementById(from);
                    var rev = '<p class="msg1">' + message + '</p><br>'
                    $(container).append(rev);
                    $(".chatBody").animate({ scrollTop: 20000000 }, "fast");
                }
                else
                {
                    var container = document.getElementById(from);
                    checkFileType(message,container,"msg1",parsedData.fileurl)            
                }
            }
        }
        else 
        {
            if(type_ == "message")
            {
                var container = document.getElementById(to);
                var rev = '<p class="msg1"><b style="color:red;">' + from + '</b><br>' + message + '</p><br>'
                $(container).append(rev);
                $(".chatBody").animate({ scrollTop: 20000000 }, "fast");
            }
            else {
                var container = document.getElementById(to);
                checkFileTypeGroup(message,from,container,"msg1",parsedData.fileurl)
            }
        }
    }
    else if (task === "retriveOlderMessage") {
        var retriveMessage = parsedData.data
        messageAppend(retriveMessage)
    }
    else if (task === "flash") {
        alert(parsedData['alertMessage'])
    }


}
socket.onclose = function (event) {
    var element = document.createElement('div');
    var text = document.createTextNode('Websocket closed. Please reload.');
    element.appendChild(text);
    element.setAttribute('style', 'color:red;');
    container.appendChild(element);
}

socket.onerror = function (error) {
    alert(error);
}

// function keypress(){
//     console.log("546546547567846")
// }



function do_post() {
    var t = getEditorValue();
    let obj = {};
    // get value and save to object
    // obj.message = document.getElementById("message-field").value;
    obj.message = t;
    var message_field_elem = t;
    // get value and save to object
    obj.To = $('.tab-content .active').attr('id').replace("-","");
    var user = $('.tab-content .active').attr('id').replace("-","");
    //get the value and save to obj
    // obj.From = sessionStorage.getItem("userName");
    obj.From = activeUserName;
    obj.task = "onMessage";
    obj.workSpaceName = userWorkSpaceNAme;
    obj.type_ = "message";
    let jsonStringObj = JSON.stringify(obj);
    if (message_field_elem !== "") {
        var mes = '<p class="msg2">' + message_field_elem + '</p><br>'
        var us = user;
        $("#" + us).append(mes);
        $("#" + us).animate({ scrollTop: 20000000 }, "fast");
        socket.send(jsonStringObj);
        console.log("success")
        // document.getElementById('message-field').value = '';
    }
    //if msg is equal to null means not send the empty msg
    else if (message_field_elem.value === "") {
        return false;
    }
}

function sendfile() {
    let obj = {};
    var filename = document.getElementById("file").value.split("\\").pop()
    obj.fileurl = "/messenger/static/files/"+filename;
    obj.message = filename;
    obj.From = activeUserName;
    obj.task = "onMessage";
    obj.workSpaceName = userWorkSpaceNAme;
    obj.type_ = "file";
    obj.To = $('.tab-content .active').attr('id').replace("-","");

    console.log(obj)
    $('form#fileUpload').submit();
    // {fileurl: "http://192.168.1.18:10000/static/files/Testing_Database.py", message: "Testing_Database.py", From: "beast", task: "onMessage", workSpaceName: "python", …}
    var mes = '<div class="msg2 h-25"><i class="fas fa-file"></i><a rel="nofollow" href="'+ obj.fileurl + '" download>' + document.getElementById("file").value.split("\\").pop() + '</div><br>'
    var us = $('.tab-content .active').attr('id').replace("-","");
    $("#" + us).append(mes);
    $("#" + us).animate({ scrollTop: 20000000 }, "fast");
    let jsonStringObj = JSON.stringify(obj);
    socket.send(jsonStringObj);
    document.getElementById('file').value = '';
}
//enter key code to send msg
var input = document.getElementById("message-field");
input.addEventListener("keyup", function (event) {
    if (event.keyCode === 13) {
        event.preventDefault();
        document.getElementById("button-addon2").click();
    }
});

//older msg retrive function
function retrieveOlderMessage() {
    let obj = {};
    // obj.From = sessionStorage.getItem("userName");
    obj.From = activeUserName;
    obj.task = "retrieveOlderMessage";
    obj.workSpaceName = userWorkSpaceNAme;
    let jsonStringObj = JSON.stringify(obj);
    socket.send(jsonStringObj);
    console.log("sucess")
}
//show the text area for user
function show() {
    $(document.getElementById("inputGroup")).show();
}


function editProfile() {
    let obj = {};
    obj.task = "editProfile";
    // obj.requestingUser = sessionStorage.getItem("userName");
    obj.requestingUser = activeUserName;
    obj.userName = document.getElementById("name").value;
    obj.phoneNumber = document.getElementById("phoneNumber").value;
    obj.emailId = document.getElementById("email").value;
    obj.jobDetails = document.getElementById("job").value;
    let jsonStringObj = JSON.stringify(obj);
    socket.send(jsonStringObj)

}

function emailVerification() {
    let obj = {};
    obj.task = "emailVerification";
    // obj.requestingUser = sessionStorage.getItem("userName");
    obj.requestingUser = activeUserName;
    obj.emailId = document.getElementById("email").value;
    let jsonStringObj = JSON.stringify(obj);
    socket.send(jsonStringObj)
}

// Message Append
function messageAppend(retriveMessage){
    console.log(retriveMessage)
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
                        checkFileTypeGroup(Messages[j]['Message'],Messages[j]["from"],_User,"msg1",Messages[j]['fileurl'])
                    }
                    else {
                        var G = '<p class="msg1"><b style="color:red;">' + Messages[j]["from"] + '</b><br>' + Messages[j]['Message'] + '</p><br>'
                        $(_User).append(G);}}

                // Else-If condition is for the Private Messages Sender side    
                else if (Messages[j]['msgType'] === "S") {
                    if (Messages[j]['type_'] === "file"){
                        checkFileType(Messages[j]['Message'],_User,"msg2", Messages[j]['fileurl'])
                        }
                    else{
                        var S = '<p class="msg2">' + Messages[j]['Message'] + '</p><br>'
                        $(_User).append(S);
                        $(".chatBody").animate({ scrollTop: 20000000 }, "fast");
                    }
                }
                else {
                    if (Messages[j]['type_'] === "file"){
                        checkFileType(Messages[j]['Message'],_User,"msg1",Messages[j]['fileurl'])
                    }
                    else{
                        var R = '<p class="msg1">' + Messages[j]['Message'] + '</p><br>'
                        $(_User).append(R);
                        $(".chatBody").animate({ scrollTop: 20000000 }, "fast");}}
            }
        }
}

// Show image if images are sent on the Privatechat 
function checkFileType(Messages,_User,side,url) {
    var extensions = ["PNG","png","jpg","jpeg","JPEG","gif","webp"]
    var fileExt = Messages.split('.').pop();
    var checkExtension = extensions.includes(fileExt)
    if (checkExtension == true){
        var rev = '<div class="'+side+' h-25"><img style="width:100%;height:100%;" src='+ url +'/></div><br>'
        $(_User).append(rev);
        $(".chatBody").animate({ scrollTop: 20000000 }, "fast");
    }
    else {
        var rev = '<div class="'+side+' h-25"><i class="fas fa-file"></i> <a rel="nofollow" href="'+ url + '" download>' + Messages + '</div><br>'
        $(_User).append(rev);
        $(".chatBody").animate({ scrollTop: 20000000 }, "fast");
    }
    
}


// Show image if images are sent on the Groupchat 
function checkFileTypeGroup(Message,from,_User,side,url) {
    var extensions = ["PNG","png","jpg","jpeg","JPEG","gif","webp"]
    var fileExt = Message.split('.').pop();
    var checkExtension = extensions.includes(fileExt)
    if (checkExtension == true){
        var rev = '<div class="'+side+' h-25"><b style="color:red;">'+ from + '</b><br><img style="width:100%;height:80%;" src='+ url +'/></div><br>'
        $(_User).append(rev);
        $(".chatBody").animate({ scrollTop: 20000000 }, "fast");
    }
    else {
        var rev = '<div class="'+side+' h-25"><b style="color:red;">'+ from + '</b><br><i class="fas fa-file"></i> <a rel="nofollow" href="'+ url + '" download>' + Message + '</div><br>'
        $(_User).append(rev);
        $(".chatBody").animate({ scrollTop: 20000000 }, "fast");
    }
    
}



function addUserFromModal(activeUserName, addingUser) {
    alert("adding user to group")
    let obj = {};
    // obj.requestingUser = sessionStorage.getItem("userName");
    obj.requestingUser = activeUserName;
    obj.addUserName = addingUser;
    obj.groupName = $('.tab-content .active').attr('id').replace("-","");
    obj.task = "addUserToGroup";

    if (addUserName !== "") {
        let jsonStringObj = JSON.stringify(obj);
        socket.send(jsonStringObj)
        // document.getElementById('addUserName').value = '';
    }
    else {
        return false;
    }
}



