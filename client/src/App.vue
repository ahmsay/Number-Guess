<template>
  <v-app :style="{background: $vuetify.theme.themes['dark'].background}">
    <v-container fluid>
      <v-row>
        <v-col cols="12">
          <v-row justify="center">
            <v-card :style="{background: $vuetify.theme.themes['dark'].card}">
              <v-card-text>
                <p class="white--text text-center title">Draw a Number</p>
                <canvas id="canvas" style="background: black" @mouseleave="handleInputEnd" :width="canvasSize" :height="canvasSize"/>
                <div class="title white--text mt-3">
                  Your number: {{firstGuess}}
                </div>
                <div class="white--text">
                  Second guess: {{secondGuess}}
                </div>
              </v-card-text>
              <v-card-text class="pt-0 pb-2">
                <v-layout row wrap>
                  <v-flex xs6 sm6 md6>
                    <v-btn class="white--text" block text @click="send" :loading="loading">Predict</v-btn>
                  </v-flex>
                  <v-flex xs6 sm6 md6>
                    <v-btn class="white--text" block text @click="clear">Clear</v-btn>
                  </v-flex>
                </v-layout>
              </v-card-text>
            </v-card>
          </v-row>
        </v-col>
      </v-row>
    </v-container>
    <div align="center" class="overline white--text">
      <span v-if="!connected">Connecting</span>
      <span v-if="connected">Connected</span>
      <div class="mt-5">
        <v-btn @click="goToSource" icon color="white">
          <v-icon large>mdi-github</v-icon>  
        </v-btn>
      </div>
    </div>
  </v-app>
</template>

<script>
  export default {
    name: 'app',
    beforeCreate() {
      if (this.$vuetify.breakpoint.name == 'xs')
        this.canvasSize = window.innerWidth - 50 + ''
    },
    mounted: function() {
      this.$http.get(this.url).then(() => {
        this.connected = true
      })

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
          down: false
        },
        canvas: null,
        context: null,
        loading: false,
        canvasSize: '300'
      }
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
        if (this.connected) {
          this.loading = true
          const dataURL = this.canvas.toDataURL();
          this.$http.post(this.url, { 'data': dataURL })
          .then(function(data){
            this.display(data.body.pred)
            this.loading = false
          })
        } else {
          alert("The server is not ready yet. It will be ready in a few seconds.")
        }
      },
      display: function(predictions) {
        const predSorted = new Array(...predictions).sort((a, b) => { return a - b });
        this.firstGuess = predictions.indexOf(predSorted[9]);
        this.secondGuess = predictions.indexOf(predSorted[8]);
      },
      goToSource: function() {
        window.open("https://github.com/ahmsay/Number-Guess", "_blank");
      }
    }
  }
</script>

<style>
  #canvas {
    border-radius: 6px;
  }
</style>
