<template>
  <div id="app">
    <div class="left" align="center">
      <div style="padding-bottom: 10px">Draw your number</div>
      <div>
        <canvas id="canvas" @mousedown="handleMouseDown" @mouseup="handleMouseUp" @mousemove="handleMouseMove" @mouseleave="handleMouseUp" width="200px" height="200px"/>
      </div>
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
  </div>
</template>

<script>
export default {
  name: 'app',
  beforeCreate() {
    this.$http.get(this.url)
    .then(() => {
      this.connected = true
    })
  },
  mounted: function() {
    this.canvas = document.getElementById("canvas")
    this.context = this.canvas.getContext("2d")
    this.canvas.addEventListener("touchstart", function (event) {
      this.handleTouchStart(event)
    }.bind(this), false)
    this.canvas.addEventListener("touchend", function () {
      this.handleTouched()
    }.bind(this), false)
    this.canvas.addEventListener("touchmove", function (event) {
      this.handleTouchMove(event)
    }.bind(this), false)
  },
  data() {
    return {
      url: 'https://safe-tor-75945.herokuapp.com/',
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
      },
      canvas: null,
      context: null
    }
  },
  computed: {
    currentMouse: function() {
      var rect = this.canvas.getBoundingClientRect()
      return {
        x: this.mouse.current.x - rect.left,
        y: this.mouse.current.y - rect.top
      }
    }
  },
  methods: {
    draw: function() {
      if (this.mouse.down) {
        this.context.strokeStyle ="#FFFFFF"
        this.context.lineCap="round"
        this.context.lineJoin = "round"
        this.context.lineWidth = 20
        this.context.lineTo(this.currentMouse.x, this.currentMouse.y)
        this.context.stroke()
      }
    },
    handleMouseDown: function(event) {
      this.mouse.down = true
      this.mouse.current = {
        x: event.pageX,
        y: event.pageY
      }
      this.context.beginPath()
      this.context.moveTo(this.currentMouse.x, this.currentMouse.y)
    },
    handleMouseUp: function() {
      this.mouse.down = false
      this.context.closePath()
    },
    handleMouseMove: function(event) {
      this.mouse.current = {
        x: event.pageX,
        y: event.pageY
      }
      this.draw()
    },
    handleTouchStart: function(event) {
      this.mouse.down = true
      this.mouse.current = {
        x: event.touches[0].clientX,
        y: event.touches[0].clientY
      }
      this.context.beginPath()
      this.context.moveTo(this.currentMouse.x, this.currentMouse.y)
    },
    handleTouched: function() {
      this.mouse.down = false
      this.context.closePath()
    },
    handleTouchMove: function(event) {
      this.mouse.current = {
        x: event.touches[0].clientX,
        y: event.touches[0].clientY
      }
      this.draw()
    },
    send: function() {
      if (this.connected) {
        var dataURL = this.canvas.toDataURL();
        this.$http.post(this.url, { 'data': dataURL })
        .then(function(data){
          this.display(data.body.pred)
        })
      } else {
        alert("The server is not ready yet. It will be ready in a few seconds.")
      }
    },
    clear: function() {
      this.context.clearRect(0, 0, this.canvas.width, this.canvas.height)
      this.firstGuess = '-'
      this.secondGuess = '-'
    },
    display: function(arr) {
      var pred = arr
      var predSorted = pred.slice();
      predSorted.sort(function(a,b){return a - b})
      this.firstGuess = pred.indexOf(predSorted[9])
      this.secondGuess = pred.indexOf(predSorted[8])
    }
  },
  ready: function() {
    this.context.translate(0.5, 0.5)
    this.context.imageSmoothingEnabled = false
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