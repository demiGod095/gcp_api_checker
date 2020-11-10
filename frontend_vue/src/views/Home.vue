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
        <table class="table is-fullwidth is-striped">
          <tr>
            <th>URL</th>
            <th>Tries</th>
            <th>Status</th>
          </tr>

          <tr v-bind:key="job.id" v-for="job in jobs"
          :class="job.tries==0? 'is-primary' : ''">
            <td>{{ job.url }}</td>
            <td>{{ job.tries }}</td>
            <td>{{ job.status || "None" }}</td>
          </tr>
        </table>


<!--        <div class="card" v-bind:key="job.id" v-for="job in jobs">-->
<!--          <div class="card-content">{{ job.url }}</div>-->

<!--          <footer class="card-footer">-->
<!--            <a @click="setStatus(job.id, 'done')" class="card-footer-item">Done</a>-->
<!--          </footer>-->
<!--        </div>-->

      </div>
    </div>
  </div>
</template>

<script>
const API_URL = 'http://127.0.0.1:8000/api/'
import axios from 'axios'

const validUrl = require('valid-url');

export default {
  name: 'Home',
  data() {
    return {
      jobs: [],
      url: '',
      tries: 0
    }
  },
  mounted() {
    this.getTasks()
  },
  methods: {
    getTasks() {
      axios({
        method: 'get',
        url: API_URL + 'jobs/'
      }).then((response) => {
        this.jobs = response.data
        // console.log(response)
      })
    },
    addJob() {

      if (this.url) {
        if (validUrl.isHttpUri(this.url)) {
          console.log('Looks like an URI ' + this.url);
        } else {
          alert('Not a valid URL!');
          return;
        }

        axios({
          method: 'post',
          url: API_URL + 'jobs/',
          data: {
            url: this.url,
            status: this.status
          }
        }).then((response) => {
          let newTask = {
            'id': response.data.id,
            'url': this.url,
          }
          this.jobs.push(newTask)
          this.url = ''
        }).catch((error) => {
          console.log(error)
        })
      }
    },
    setStatus(job_id, status) {
      const job = this.jobs.filter(job => job.id === job_id)[0]
      const url = job.url
      axios({
        method: 'put',
        url: API_URL + 'jobs/' + job_id + '/',
        headers: {
          'Content-Type': 'application/json',
        },
        data: {
          status: status,
          url: url
        }
      }).then(() => {
        job.status = status
      })
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