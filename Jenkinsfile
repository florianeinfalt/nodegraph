pipeline {
  agent {
    dockerfile true
  }
  stages {
    stage('Python 2.7') {
      steps {
        sh 'tox -e py27 --recreate'
        junit '**/junit-py27.xml'
        cobertura(coberturaReportFile: '**/coverage.xml')
      }
    }
    stage('Python 3.5') {
      steps {
        sh 'tox -e py35 --recreate'
        junit '**/junit-py35.xml'
        cobertura(coberturaReportFile: '**/coverage.xml')
      }
    }
    stage('Python 3.6') {
      steps {
        sh 'tox -e py36 --recreate'
        junit '**/junit-py36.xml'
        cobertura(coberturaReportFile: '**/coverage.xml')
      }
    }
  }
}
