topbind_dbg_server = localStorage.getItem('topbind_dbg_server');
if (!topbind_dbg_server) {
    topbind_dbg_server = 'http://10.21.15.91:8000';
    localStorage.setItem('topbind_dbg_server', topbind_dbg_server);
}
if (!map.topbind_dbg_roomid) {
    roomid = localStorage.getItem('topbind_dbg_roomid');
    if(!roomid) { // random roomid if not globally set
        roomid = ([1e7]+-1e3+-4e3+-8e3+-1e11).replace(/[018]/g, c => (c ^ (crypto.getRandomValues(new Uint8Array(1))[0] & (15 >> c / 4))).toString(16));
    }
    map.topbind_dbg_roomid = roomid;
}
async function takeScreenshot(map) {
  return new Promise(function(resolve, reject) {
    map.once("render", function() {
        resolve(map.getCanvas().toDataURL());
    })
    map.setBearing(map.getBearing()); // triger render!
  })
}
var btnImg1 = document.createElement("div");
var btnImg2 = document.createElement("div");
btnImg1.appendChild(document.createElement("img"));
btnImg2.appendChild(document.createElement("img"));
[btnImg2, btnImg1].forEach((b, i) => {
    b.style.position = 'fixed';
    b.style.width = '100px';
    b.style.height = '100px';
    b.style.bottom = '0px';
    b.style.right = `${i * 150 + 100}px`;
    b.style.border = '1px solid gray';
    b.style.zIndex = 1000;
    b.style.overflow = 'hidden';
    var img = b.firstChild;
    img.style.top = '0';
    img.style.left = '0';
    img.style.width = '100%';
    img.style.height = '100%';
});
btnImg1.title = '单击截图(1)，双击查看';
btnImg1.onclick = async () => {
    map.img1 = await takeScreenshot(map);
    btnImg1.firstChild.src = map.img1;
    fetch(`${topbind_dbg_server}/upload`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({'roomid': map.topbind_dbg_roomid, 'image': map.img1, 'label': 'img1'}),
    })
    .then((response) => response.json())
    .then((data) => {console.log("Success:", data); })
    .catch((error) => { console.error("Error:", error); });
};
btnImg2.title = '单击截图(2)，双击查看';
btnImg2.onclick = async () => {
    map.img2 = await takeScreenshot(map);
    btnImg2.firstChild.src = map.img2;
    fetch(`${topbind_dbg_server}/upload`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({'roomid': map.topbind_dbg_roomid, 'image': map.img2, 'label': 'img2'}),
    })
    .then((response) => response.json())
    .then((data) => {console.log("Success:", data); })
    .catch((error) => { console.error("Error:", error); });
};
function open_pixelmatch() {
    window.open(`${topbind_dbg_server}/pixelmatch?roomid=${map.topbind_dbg_roomid}`, '_blank');
};
btnImg1.ondblclick = open_pixelmatch;
btnImg2.ondblclick = open_pixelmatch;
document.body.appendChild(btnImg1);
document.body.appendChild(btnImg2);