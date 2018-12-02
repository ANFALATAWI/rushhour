let bored;
let carX;
let carB;
let carC;
let carA;
let trackQ;
let trackP;
let trackR;
let trackO;
this.i = 0;
var sol = "CL,AR,PU,BU,OD,OD,CL,CL,QD,OD,RL,RL,QD,XR,XR,XR";
sol += ",XR";
var res = sol.split(",");

//************* for Car x *************
this.Xx = 113;
this.Xy = 210;
this.Xw = 150;
this.Xh = 78;
//************* for Car B *************
this.Bx = 44;
this.By = 355;
this.Bw = 78;
this.Bh = 144;

//************* for Car C ************* 
this.Cx = 333;
this.Cy = 349;
this.Cw = 150;
this.Ch = 78;
//************* for Car A *************
this.Ax = 45;
this.Ay = 69;
this.Aw = 150;
this.Ah = 78;

//************* for track O *************
this.Ox = 395;
this.Oy = 70;
this.Ow = 85;
this.Oh = 222;

//************* for track Q *************
this.Qx = 255;
this.Qy = 140;
this.Qw = 85;
this.Qh = 215;

//************* for track P *************
this.Px = 37;
this.Py = 143;
this.Pw = 85;
this.Ph = 222;

//************* for track R *************
this.Rx = 180;
this.Ry = 420;
this.Rw = 230;
this.Rh = 78;

// --------------------------------------

function setup() {
  createCanvas(550, 600);
}

function draw() {
  background(220);

  image(bored, 0, 0);
  this.O = image(trackO, this.Ox, this.Oy, this.Ow, this.Oh);
  this.Q = image(trackQ, this.Qx, this.Qy, this.Qw, this.Qh);
  this.P = image(trackP, this.Px, this.Py, this.Pw, this.Ph);
  this.R = image(trackR, this.Rx, this.Ry, this.Rw, this.Rh);
  this.X = image(carX, this.Xx, this.Xy, this.Xw, this.Xh);
  this.A = image(carA, this.Ax, this.Ay, this.Aw, this.Ah);
  this.C = image(carC, this.Cx, this.Cy, this.Cw, this.Ch);
  this.B = image(carB, this.Bx, this.By, this.Bw, this.Bh);

  for (var j = 0; j < 900000000; j++) {}
  if (res[i].charAt(0) === "X") {
    if (res[i].charAt(1) === "L") {
      this.Xx -= 72;
    } else {
      this.Xx += 70;
    }
  }
  if (res[i].charAt(0) === "A") {
    if (res[i].charAt(1) === "L") {
      this.Ax -= 72;
    } else {
      this.Ax += 70;
    }
  }
  if (res[i].charAt(0) === "B") {
    if (res[i].charAt(1) === "U") {
      this.By -= 72;
    } else {
      this.By += 70;
    }
  }
  if (res[i].charAt(0) === "C") {
    if (res[i].charAt(1) === "L") {
      this.Cx -= 72;
    } else {
      this.Cx += 70;
    }
  }
  if (res[i].charAt(0) === "O") {
    if (res[i].charAt(1) === "U") {
      this.Oy -= 72;
    } else {
      this.Oy += 70;
    }
  }
  if (res[i].charAt(0) === "P") {
    if (res[i].charAt(1) === "U") {
      this.Py -= 72;
    } else {
      this.Py += 70;
    }
  }
  if (res[i].charAt(0) === "Q") {
    if (res[i].charAt(1) === "U") {
      this.Qy -= 72;
    } else {
      this.Qy += 70;
    }
  }
  if (res[i].charAt(0) === "R") {
    if (res[i].charAt(1) === "D") {
      this.Rx += 72;
    } else {
      this.Rx -= 70;
    }
  }
  i++;


}

function preload() {

  bored = loadImage('r.png');

  trackO = loadImage('trackO.png');
  trackQ = loadImage('trackQ.png');
  trackP = loadImage('trackP.png');
  trackR = loadImage('trackR.png');

  carX = loadImage('carX.png');
  carA = loadImage('carA.png');
  carB = loadImage('carB.png');
  carC = loadImage('carC.png');


}