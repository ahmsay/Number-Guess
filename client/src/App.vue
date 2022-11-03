<template>
  <div>
    <canvas id="canvas" style="background: black" @mouseleave="handleInputEnd" :width="canvasSize" :height="canvasSize"/>
  </div>
  <div>
    Your number: {{firstGuess}}
  </div>
  <div>
    Second guess: {{secondGuess}}
  </div>
  <button @click="send" :loading="loading">Predict</button>
  <button @click="clear">Clear</button>
</template>

<script>
  export default {
    data() {
      return {
        url: 'https://w2jmrv6qirtajgutl7gqeo3c440npwlp.lambda-url.eu-central-1.on.aws',
        firstGuess: '-',
        secondGuess: '-',
        mouse: {
          current: {
            x: 0,
            y: 0
          },
          down: false
        },
        canvas: null,
        context: null,
        loading: false,
        canvasSize: '300'
      }
    },
    mounted: function() {
      this.canvas = document.getElementById("canvas")
      this.context = this.canvas.getContext("2d")
      this.context.strokeStyle = "#FFFFFF"
      this.context.lineCap = "round"
      this.context.lineJoin = "round"
      this.context.lineWidth = this.canvasSize / 10

      this.canvas.addEventListener("mousedown", function (event) {
        this.handleInputStart(event.pageX, event.pageY)
      }.bind(this), false)
      this.canvas.addEventListener("mouseup", function () {
        this.handleInputEnd()
      }.bind(this), false)
      this.canvas.addEventListener("mousemove", function (event) {
        this.handleInputMove(event.pageX, event.pageY)
      }.bind(this), false)
      
      this.canvas.addEventListener("touchstart", function (event) {
        event.preventDefault()
        this.handleInputStart(event.touches[0].clientX, event.touches[0].clientY)
      }.bind(this), false)
      this.canvas.addEventListener("touchend", function () {
        event.preventDefault()
        this.handleInputEnd()
      }.bind(this), false)
      this.canvas.addEventListener("touchmove", function (event) {
        event.preventDefault()
        this.handleInputMove(event.touches[0].clientX, event.touches[0].clientY)
      }.bind(this), false)
    },
    computed: {
      currentMouse: function() {
        let rect = this.canvas.getBoundingClientRect()
        return {
          x: this.mouse.current.x - rect.left,
          y: this.mouse.current.y - rect.top
        }
      }
    },
    methods: {
      handleInputStart: function(x, y) {
        this.mouse.down = true
        this.mouse.current = { x, y }
        this.context.beginPath()
        this.context.moveTo(this.currentMouse.x, this.currentMouse.y)
      },
      handleInputEnd: function() {
        this.mouse.down = false
        this.context.closePath()
      },
      handleInputMove: function(x, y) {
        this.mouse.current = { x, y }
        this.draw()
      },
      draw: function() {
        if (this.mouse.down) {
          this.context.lineTo(this.currentMouse.x, this.currentMouse.y)
          this.context.stroke()
        }
      },
      clear: function() {
        this.context.clearRect(0, 0, this.canvas.width, this.canvas.height)
        this.firstGuess = '-'
        this.secondGuess = '-'
      },
      send: function() {
        this.loading = true
        const dataURL = this.canvas.toDataURL();
        fetch(this.url, {
          method:  'POST',
          headers: {'Content-Type': 'application/json'},
          body: dataURL
        })
        .then(response => response.json())
        .then(data => {
          this.firstGuess = data.first_guess
          this.secondGuess = data.second_guess
        })
      },
      display: function(predictions) {
        console.log(predictions)
      },
      goToSource: function() {
        window.open("https://github.com/ahmsay/Number-Guess", "_blank");
      }
    }
  }
</script>
