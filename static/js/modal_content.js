const socket = Initials.socket
const activeUserName = Initials.activeUserName
const workSpaceName = Initials.workSpaceName
    
function activeUsers() {
    let activeUsersObj = {};
    activeUsersObj.task = "activeUsers";
    activeUsersObj.requestingUser = activeUserName;
    activeUsersObj.workSpaceName = workSpaceName;
    let activeUsersJson = JSON.stringify(activeUsersObj);
    socket.send(activeUsersJson)
}
setInterval(function () { activeUsers(); }, 30000);


function switchTab(to) {
    activetab = $('.tab-content .active').attr('id')
    $("#"+activetab).removeClass("active")
    $(to).addClass("active")
    sessionStorage.setItem("activeWindow",to);
}

function initialSwitchTab(){
    if(!sessionStorage.getItem("activeWindow")) {
    }
    else {
        switchTab(sessionStorage.getItem("activeWindow"))
    }
}
initialSwitchTab()


function AddFriendsModal() {
    let obj = {};
    obj.task = "addUserToWorkSpace";
    obj.requestingUser = activeUserName;
    obj.workSpaceName = workSpaceName;
    obj.addUserMail = document.getElementById("AddFriendsModalInput").value;

    if (document.getElementById("AddFriendsModalInput").value !== "") {
        let jsonStringObj = JSON.stringify(obj);
        socket.send(jsonStringObj)
        document.getElementById('AddFriendsModalInput').value = '';
        location.reload();
    }
    else {
        return false;
    }


}

function avoidSpace(){
    $('#groupName').on('keypress', function(e) {
        if (e.which == 32)
            return false;
    });
}


function createGroup() {
    let obj = {};
    obj.groupName = document.getElementById("groupName").value;
    obj.Description = document.getElementById("groupDescription").value;
    obj.task = "createGroup";
    obj.workSpaceName = workSpaceName;
    // obj.Admin = sessionStorage.getItem("userName");
    obj.Admin = activeUserName;
    var x = document.getElementById("groupName").value;
    var y = document.getElementById("groupDescription").value;

    if (x !== "") {
        let jsonStringObj = JSON.stringify(obj);
        document.getElementById("groupName").value = '';
        document.getElementById("groupDescription").value = '';
        socket.send(jsonStringObj)
        location.reload();
    }
    else {
        document.getElementById("groupName").value = '';
        document.getElementById("groupDescription").value = '';
        alert("please fill the empty area")
    }
}

function sendfile() {
    time = formatAMPM(new Date)
    let obj = {};
    var filename = document.getElementById("file1").value.split("\\").pop()
    obj.fileurl = "/messenger/static/files/"+filename;
    obj.message = filename;
    obj.From = activeUserName;
    obj.task = "onMessage";
    obj.workSpaceName = workSpaceName;
    obj.type_ = "file";
    obj.To = $('.tab-content .active').attr('id').replace("-","");
    // {fileurl: "http://192.168.1.18:10000/static/files/Testing_Database.py", message: "Testing_Database.py", From: "beast", task: "onMessage", workSpaceName: "python", …}
    var us = $('.tab-content .active').attr('id').replace("-","");
    let jsonStringObj = JSON.stringify(obj);
    socket.send(jsonStringObj);
    checkFileType_(filename,us,activeUserName,obj.fileurl,time)
    document.getElementById('file1').value = '';
    $('#FileModal').modal('toggle');
}

function _(el) {
    return document.getElementById(el);
  }
  
  function uploadFile() {
    var file = _("file1").files[0];
    // alert(file.name+" | "+file.size+" | "+file.type);
    var formdata = new FormData();
    formdata.append("file1", file);
    var ajax = new XMLHttpRequest();
    ajax.upload.addEventListener("progress", progressHandler, false);
    ajax.addEventListener("load", completeHandler, false);
    ajax.addEventListener("error", errorHandler, false);
    ajax.addEventListener("abort", abortHandler, false);
    ajax.open("POST", "/messenger/fileUpload");
    //use file_upload_parser.php from above url
    ajax.send(formdata);
  }
  
  function progressHandler(event) {
    _("loaded_n_total").innerHTML = "Last Uploaded " + event.loaded + " bytes of " + event.total;
    var percent = (event.loaded / event.total) * 100;
    _("progressBar").value = Math.round(percent);
    _("status").innerHTML = Math.round(percent) + "% uploaded... please wait";
  }
  
  function completeHandler(event) {
    _("status").innerHTML = event.target.responseText;
    _("progressBar").value = 0; //wil clear progress bar after successful upload
    sendfile()
  }
  
  function errorHandler(event) {
    _("status").innerHTML = "Upload Failed";
  }
  
  function abortHandler(event) {
    _("status").innerHTML = "Upload Aborted";
  }


function scrollBottom(div) {
    $(div).animate({ scrollTop: 20000000 }, "fast");
}


function do_post() {
    time = formatAMPM(new Date)
    let obj = {};
    obj.message = document.getElementById("MessageBox").value;
    var message_field_elem = document.getElementById("MessageBox").value;
    obj.To = $('.tab-content .active').attr('id').replace("-","");
    var user = $('.tab-content .active').attr('id').replace("-","");
    obj.From = activeUserName;
    obj.task = "onMessage";
    obj.workSpaceName = workSpaceName;
    obj.type_ = "message";
    let jsonStringObj = JSON.stringify(obj);
    if (message_field_elem !== "") {
        const mes = `<div id="Message" class="d-flex bd-highlight m-2">
                            <div class="p-2 flex-shrink-1 bd-highlight">
                                <div class="rounded message-profile-pic"><p class="message-profile-pic-text">`+activeUserName+`</p></div>
                            </div>
                            <div class="p-2 w-100 bd-highlight">
                                <p class="font-weight-bold d-inline">`+activeUserName+`</p><span class="text-muted float-right text-uppercase">`+time+`</span>
                                <p class="text-break">`+message_field_elem+`</p>
                            </div>
                        </div>`;
        var us = user;
        if (obj.From === obj.To) {    
        }
        else {
            $("#" + us + "-Message").append(mes);
        }
        scrollBottom("#"+us+"-Main")
        socket.send(jsonStringObj);
        document.getElementById('MessageBox').value = '';
    }
    else if (message_field_elem.value === "") {
        return false;
    }
}


function Url_Link() {
    link = document.getElementById("modal_link").value;
    mes_elm = "<a href='"+link+"'>"+link+"</a>"
    time = formatAMPM(new Date)
    let obj = {};
    obj.message = mes_elm;
    var message_field_elem = mes_elm;
    obj.To = $('.tab-content .active').attr('id').replace("-","");
    var user = $('.tab-content .active').attr('id').replace("-","");
    obj.From = activeUserName;
    obj.task = "onMessage";
    obj.workSpaceName = workSpaceName;
    obj.type_ = "message";
    let jsonStringObj = JSON.stringify(obj);
    if (message_field_elem !== "") {
        const mes = `<div id="Message" class="d-flex bd-highlight m-2">
                            <div class="p-2 flex-shrink-1 bd-highlight">
                                <div class="rounded message-profile-pic"><p class="message-profile-pic-text">`+activeUserName+`</p></div>
                            </div>
                            <div class="p-2 w-100 bd-highlight">
                                <p class="font-weight-bold d-inline">`+activeUserName+`</p><span class="text-muted float-right">`+time+`</span>
                                <p class="text-break">`+message_field_elem+`</p>
                            </div>
                        </div>`;
        var us = user;
        if (obj.From === obj.To) {    
        }
        else {
            $("#" + us + "-Message").append(mes);
        }
        scrollBottom("#"+us+"-Main")
        socket.send(jsonStringObj);
        document.getElementById('modal_link').value = '';
        $('#TextLinkModal').modal('toggle');
    }
    else if (message_field_elem.value === "") {
        return false;
    }
}
