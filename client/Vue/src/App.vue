<template>
  <div id="app">
    <div class="left" align="center">
      <div style="padding-bottom: 10px">Draw your number</div>
      <div><canvas id="canvas" @mousedown="handleMouseDown" @mouseup="handleMouseUp" @mousemove="handleMouseMove" @mouseleave="handleMouseUp" width="200px" height="200px"></canvas></div>
      <div style="padding: 10px 0px 10px 0px">
        <button class="btn" @click="send">Predict</button>
        <button class="btn" @click="clear">Clear</button>
      </div>
      <div class="leftleft">
        <div align="left" style="font-size: 25px">Your number:</div>
        <div align="left">Second guess:</div>
      </div>
      <div style="padding-right: 25px">
        <div align="right" style="font-size: 25px">{{firstGuess}}</div>
        <div align="right">{{secondGuess}}</div>
      </div>
      <div align="center" style="font-size: 12px; color: #fff; padding-top: 20px">
        <span v-if="!connected">Connecting</span>
        <span v-if="connected">Connected</span>
      </div>
    </div>
    <div style="color: #fff; text-align: center; position: absolute; bottom: 10px;">Ahmet Say</div>
  </div>
</template>

<script>
export default {
  name: 'app',
  beforeCreate() {
    this.$http.get('https://safe-tor-75945.herokuapp.com/')
    .then(function(data){
      this.connected = true;
    });
  },
  data() {
    return {
      time: false,
      connected: false,
      firstGuess: '-',
      secondGuess: '-',
      mouse: {
        current: {
          x: 0,
          y: 0
        },
        previous: {
          x: 0,
          y: 0
        },
        down: false
      }
    }
  },
  computed: {
    currentMouse: function() {
      var c = document.getElementById("canvas");
      var rect = c.getBoundingClientRect();
      return {
        x: this.mouse.current.x - rect.left,
        y: this.mouse.current.y - rect.top
      }
    }
  },
  methods: {
    draw: function(event) {
      if (this.mouse.down) {
        var c = document.getElementById("canvas");
        var ctx = c.getContext("2d");
        ctx.strokeStyle ="#FFFFFF";
        ctx.lineCap="round";
        ctx.lineJoin = "round"
        ctx.lineWidth = 20;
        ctx.lineTo(this.currentMouse.x, this.currentMouse.y);
        ctx.stroke();
      }
    },
    handleMouseDown: function(event) {
      this.mouse.down = true;
      this.mouse.current = {
        x: event.pageX,
        y: event.pageY
      }
      var c = document.getElementById("canvas");
      var ctx = c.getContext("2d");
      ctx.beginPath();
      ctx.moveTo(this.currentMouse.x, this.currentMouse.y)
    },
    handleMouseUp: function() {
      this.mouse.down = false;
      var c = document.getElementById("canvas");
      var ctx = c.getContext("2d");
      ctx.closePath();
    },
    handleMouseMove: function(event) {
      this.mouse.current = {
        x: event.pageX,
        y: event.pageY
      }
      this.draw(event);
    },
    send: function() {
      if (this.connected) {
        var c = document.getElementById("canvas");
        var dataURL = canvas.toDataURL();
        this.$http.post('https://safe-tor-75945.herokuapp.com/', {'data': dataURL})
        .then(function(data){
          return data.json();
        }).then(function(data){
          this.display(data['pred']);
        });
      } else {
        alert("The server is not ready yet. It will be ready in a few seconds.");
      }
    },
    clear: function() {
      var c = document.getElementById("canvas");
      var ctx = c.getContext('2d');
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      this.firstGuess = '-';
      this.secondGuess = '-';
    },
    display: function(arr) {
      var pred = arr;
      var predSorted = pred.slice();
      predSorted.sort(function(a,b){return a - b});
      this.firstGuess = pred.indexOf(predSorted[9]);
      this.secondGuess = pred.indexOf(predSorted[8]);
    }
  },
  ready: function() {
    var c = document.getElementById("canvas");
    var ctx = c.getContext("2d");
    ctx.translate(0.5, 0.5);
    ctx.imageSmoothingEnabled = false;
  }
}
</script>

<style>
  body {
    margin: 2rem;
    background: #35495e;
  }
  canvas {
    background: black;
  }
  #app {
    height: 100%;
    width: 100%;
    font-family: Calibri;
  }
  .left, .middle, .right {
    display: inline-block;
    *display: inline;
    zoom: 1;
    vertical-align: top;
    font-size: 20px;
    color: #fff;
  }
  .left {
    width: 250px;
    background: #48627c;
    padding: 10px;
    transition-duration: 0.4s;
  }
  .left:hover {
    background: #5a7591;
  }
  .leftleft {
    padding-left: 25px;
    display: inline-block;
    *display: inline;
    float: left;
  }
  .btn {
    background-color: #35495e;
    border: none;
    width: 98px;
    padding: 8px;
    color: #fff;
    cursor: pointer;
    outline: 0;
  }
</style>