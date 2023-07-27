// Show image if images are sent on the Privatechat 
function checkFileType_(Messages,to,from,url,time) {
    var extensions = ["PNG","png","jpg","jpeg","JPEG","gif","webp"]
    var fileExt = Messages.split('.').pop();
    var checkExtension = extensions.includes(fileExt)
    if (checkExtension == true){
        const mes = `<div id="Message" class="d-flex bd-highlight m-2">
                        <div class="p-2 flex-shrink-1 bd-highlight">
                            <div class="rounded message-profile-pic"><p class="message-profile-pic-text">`+from+`</p></div>
                        </div>
                        <div class="p-2 w-100 bd-highlight">
                            <p class="font-weight-bold d-inline">`+from+`</p><span class="text-muted float-right text-uppercase">`+time+`</span>
                            <a href="`+url+`" download><img class="d-flex img-fluid" style="max-width:256px;max-height:256px;" src="`+url+`" alt="`+url+`"></a>
                        </div>
                    </div>`;
        if (from === to) {    
        }
        else {
            $("#"+to+"-Message").append(mes);
        }
        
        scrollBottom("#"+to+"-Main")
    }
    else {
        const mes = `<div id="Message" class="d-flex bd-highlight m-2">
                        <div class="p-2 flex-shrink-1 bd-highlight">
                            <div class="rounded message-profile-pic"><p class="message-profile-pic-text">`+from+`</p></div>
                        </div>
                        <div class="p-2 w-100 bd-highlight">
                            <p class="font-weight-bold d-inline">`+from+`</p><span class="text-muted float-right text-uppercase">`+time+`</span>
                            <div class="d-flex bd-highlight p-4 rounded text-center border" style="height:100px;width:300px;background-color: rgb(223, 217, 217);">
                                <div class="p-2 w-100 bd-highlight">`+Messages+`</div>
                                <div class="p-2 flex-shrink-1 bd-highlight">
                                    <a href="`+url+`" download><span class="fa fa-download	 mr-1 text-black" style="font-size: 40px;"></span></a>
                                </div>
                            </div>
                        </div>
                    </div>`;
        if (from === to) {    
        }
        else {
            $("#"+to+"-Message").append(mes);
        }
        scrollBottom("#"+to+"-Main")
    }
    
}


//older msg retrive function
function retrieveOlderMessage() {
    let obj = {};
    // obj.From = sessionStorage.getItem("userName");
    obj.From = activeUserName;
    obj.task = "retrieveOlderMessage";
    obj.workSpaceName = workSpaceName;
    let jsonStringObj = JSON.stringify(obj);
    socket.send(jsonStringObj);
}


function addUserFromModal(activeUserName, addingUser) {
    let obj = {};
    obj.requestingUser = activeUserName;
    obj.addUserName = addingUser;
    obj.groupName = $('.tab-content .active').attr('id').replace("-","");
    obj.task = "addUserToGroup";
    let jsonStringObj = JSON.stringify(obj);
    if (addingUser !== "") {
        let jsonStringObj = JSON.stringify(obj);
        socket.send(jsonStringObj)
        location.reload();
    }
    else {
        return false;
    }
}

// Message Sending on enter key press
$("#MessageBox").on('keypress',function(e) {
    if(e.which == 13) {
        do_post()
        e.preventDefault();
    }
});


// Get Current Time
function formatAMPM(date) {
    var hours = date.getHours();
    var minutes = date.getMinutes();
    var ampm = hours >= 12 ? 'pm' : 'am';
    hours = hours % 12;
    hours = hours ? hours : 12; // the hour '0' should be '12'
    minutes = minutes < 10 ? '0'+minutes : minutes;
    var strTime = hours + ':' + minutes + ' ' + ampm;
    return strTime;
  }




  