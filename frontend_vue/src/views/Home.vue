<template>
  <div class="home">
    <hr>

    <div class="columns">
      <div class="column is-6 is-offset-3">
        <form v-on:submit.prevent="addJob">

          <div class="field">
            <label class="label">Add Job URL</label>
            <div class="control">
              <label>
                <input class="input" type="text" v-model="url">
              </label>
            </div>
          </div>
          <div class="field">
            <div class="control">
              <button class="button is-link">Submit</button>
            </div>
          </div>
        </form>
      </div>
    </div>

    <hr>

    <div class="columns">
      <div class="column is-10 is-offset-1">
        <h2 class="subtitle">Jobs</h2>
        <table class="table is-fullwidth is-bordered">
          <thead>
          <tr>
            <th>URL</th>
            <th>Tries</th>
            <th>Code</th>
          </tr>
          </thead>

          <tr v-bind:key="job.id" v-for="job in jobs"
          :class="job.tries===0? 'has-background-warning-light' :
            job.code<400? 'is-selected' : 'has-background-danger-dark has-text-white-bis'">
            <td>{{ job.url }}</td>
            <td>{{ job.tries }}</td>
            <td>{{ job.code || "None" }} {{ job.response }}</td>
          </tr>
        </table>
      </div>
    </div>

  </div>
</template>

<script>
const API_URL = 'https://shreyas-api-checker.ts.r.appspot.com/api/'
import axios from 'axios'

const validUrl = require('valid-url');

export default {
  name: 'Home',
  data() {
    return {
      jobs: [],
      url: '',
      tries: 0,
      polling: null
    }
  },
  mounted() {
    this.getTasks()
    this.pollData()
  },
  deactivated() {
    clearInterval(this.polling)
  },
  methods: {
    pollData () {
      this.polling = setInterval(() => {
        this.getTasks()
      }, 10000)
    },
    getTasks() {
      axios({
        method: 'get',
        url: API_URL + 'jobs/'
      }).then((response) => {
        this.jobs = response.data.reverse()
      })
    },
    addJob() {
      if (this.url) {
        if (validUrl.isWebUri (this.url)) {
          console.log('Looks like an URI ' + this.url);
        } else {
          // console.log('Not a valid URL! ' + this.url);
          alert('Not a valid URL!');
          return;
        }

        axios({
          method: 'post',
          url: API_URL + 'jobs/',
          data: {
            url: this.url,
            code: this.code
          }
        }).then((response) => {
          let newTask = {
            'id': response.data.id,
            'url': this.url,
            'tries': 0
          }
          this.jobs.unshift(newTask)
          this.url = ''
        }).catch((error) => {
          console.log(error)
        })
      }
    }
  }
}
</script>

<style lang="scss">
.select, select {
  width: 100%;
}

.card {
  margin-bottom: 20px;
}

.done {
  opacity: 0.3;
}
</style>