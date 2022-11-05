<template>
  <v-app :style="{background: '#35495e'}">
    <v-main>
      <v-container fluid>
        <v-row>
          <v-col cols="12">
            <v-row justify="center">
              <v-card class="mt-5" :style="{background: '#48627c'}">
                <v-card-text>
                  <p class="text-h6 text-center font-weight-bold text-white mb-4">Draw a number below.</p>
                  <canvas id="canvas" :style="{background: 'black', borderRadius: '6px'}" @mouseleave="handleInputEnd" :width="canvasSize" :height="canvasSize"/>
                  <div class="title text-white mt-3 text-h6 font-weight-bold">
                    Your number: {{ firstGuess }}
                  </div>
                  <div class="text-white">
                    Second guess: {{ secondGuess }}
                  </div>
                </v-card-text>
                <v-card-text class="pt-0 pb-2">
                  <div class="d-flex justify-space-around">
                    <v-btn variant="text" class="text-white font-weight-bold" @click="send" :loading="loading">Predict</v-btn>
                    <v-btn variant="text" class="text-white font-weight-bold" @click="clear" :disabled="loading">Clear</v-btn>
                  </div>
                </v-card-text>
              </v-card>
            </v-row>
          </v-col>
        </v-row>
      </v-container>
      <div class="d-flex justify-center mt-5 mb-5">
        <v-btn variant="text" icon @click="goToSource" color="white">
          <v-icon size="x-large">fa-brands fa-github</v-icon>
        </v-btn>
      </div>
    </v-main>
  </v-app>
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
    mounted() {
      this.setUpCanvas()
      this.handleMouseEvents()
      this.handleTouchEvents()
    },
    computed: {
      currentMouse() {
        let rect = this.canvas.getBoundingClientRect()
        return {
          x: this.mouse.current.x - rect.left,
          y: this.mouse.current.y - rect.top
        }
      }
    },
    methods: {
      setUpCanvas() {
        this.canvas = document.getElementById("canvas")
        this.context = this.canvas.getContext("2d")
        this.context.strokeStyle = "#FFFFFF"
        this.context.lineCap = "round"
        this.context.lineJoin = "round"
        this.context.lineWidth = this.canvasSize / 12
      },
      handleMouseEvents() {
        this.canvas.addEventListener("mousedown", function (event) {
          this.handleInputStart(event.pageX, event.pageY)
        }.bind(this), false)
        this.canvas.addEventListener("mouseup", function () {
          this.handleInputEnd()
        }.bind(this), false)
        this.canvas.addEventListener("mousemove", function (event) {
          this.handleInputMove(event.pageX, event.pageY)
        }.bind(this), false)
      },
      handleTouchEvents() {
        this.canvas.addEventListener("touchstart", function (event) {
          event.preventDefault()
          this.handleInputStart(event.touches[0].clientX, event.touches[0].clientY)
        }.bind(this), false)
          this.canvas.addEventListener("touchend", function (event) {
          event.preventDefault()
          this.handleInputEnd()
        }.bind(this), false)
          this.canvas.addEventListener("touchmove", function (event) {
          event.preventDefault()
          this.handleInputMove(event.touches[0].clientX, event.touches[0].clientY)
        }.bind(this), false)
      },
      handleInputStart(x, y) {
        this.mouse.down = true
        this.mouse.current = { x, y }
        this.context.beginPath()
        this.context.moveTo(this.currentMouse.x, this.currentMouse.y)
      },
      handleInputEnd() {
        this.mouse.down = false
        this.context.closePath()
      },
      handleInputMove(x, y) {
        this.mouse.current = { x, y }
        this.draw()
      },
      draw() {
        if (this.mouse.down) {
          this.context.lineTo(this.currentMouse.x, this.currentMouse.y)
          this.context.stroke()
        }
      },
      clear() {
        this.context.clearRect(0, 0, this.canvas.width, this.canvas.height)
        this.firstGuess = '-'
        this.secondGuess = '-'
      },
      send() {
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
          this.loading = false
        })
      },
      goToSource() {
        window.open("https://github.com/ahmsay/Number-Guess", "_blank");
      }
    }
  }
</script>
