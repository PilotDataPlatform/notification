pipeline {
    agent { label 'small' }
    environment {
      imagename_dev = "registry-gitlab.indocresearch.org/platform/service_notification"
      imagename_staging = "registry-gitlab.indocresearch.org/platform/service_notification"
      commit = sh(returnStdout: true, script: 'git describe --always').trim()
      registryCredential = 'platform-gitlab-registry'
      dockerImage = ''
    }

    stages {

    stage('Git clone for dev') {
        when {branch "k8s-dev"}
        steps{
          script {
              git branch: "k8s-dev",
                  url: 'https://git.indocresearch.org/platform/service_notification.git',
                  credentialsId: 'lzhao'
              sh 'printenv'
              sh 'git submodule update --recursive --init --remote'
            }
        }
    }

    stage('DEV unit test') {
      when {branch "k8s-dev"}
      steps{
         withCredentials([
            usernamePassword(credentialsId:'readonly', usernameVariable: 'PIP_USERNAME', passwordVariable: 'PIP_PASSWORD'),
            string(credentialsId:'VAULT_TOKEN', variable: 'VAULT_TOKEN'),
            string(credentialsId:'VAULT_URL', variable: 'VAULT_URL'),
            file(credentialsId:'VAULT_CRT', variable: 'VAULT_CRT')
          ]) {      
            sh """
            export CONFIG_CENTER_ENABLED='true'
            export VAULT_TOKEN=${VAULT_TOKEN}
            export VAULT_URL=${VAULT_URL}
            export VAULT_CRT=${VAULT_CRT}        
            pip3 install virtualenv
            /home/indoc/.local/bin/virtualenv -p python3 venv
            . venv/bin/activate
            PIP_USERNAME=${PIP_USERNAME} PIP_PASSWORD=${PIP_PASSWORD} pip3 install -r requirements.txt -r tests/test_requirements.txt -r internal_requirements.txt
            pytest -c tests/pytest.ini
            """
          }
      }
    }

    stage('DEV Build and push image') {
      when {branch "k8s-dev"}
      steps {
        script {
          withCredentials([usernamePassword(credentialsId:'readonly', usernameVariable: 'PIP_USERNAME', passwordVariable: 'PIP_PASSWORD')]) {        
            docker.withRegistry('https://registry-gitlab.indocresearch.org', registryCredential) {
                customImage = docker.build("registry-gitlab.indocresearch.org/platform/service_notification:$commit", "--build-arg pip_username=${PIP_USERNAME} --build-arg pip_password=${PIP_PASSWORD} --add-host git.indocresearch.org:10.4.3.151 .")
                customImage.push()
            }
          }
        }
      }
    }

    stage('DEV Remove image') {
      when {branch "k8s-dev"}
      steps{
        sh "docker rmi $imagename_dev:$commit"
      }
    }

    stage('DEV Deploy') {
      when {branch "k8s-dev"}
      steps{
        sh "sed -i 's/<VERSION>/$commit/g' kubernetes/dev-deployment.yaml"
        sh "kubectl config use-context dev"
        sh "kubectl apply -f kubernetes/dev-deployment.yaml"
      }
    }

    stage('Git clone staging') {
        when {branch "k8s-staging"}
        steps{
          script {
          git branch: "k8s-staging",
              url: 'https://git.indocresearch.org/platform/service_notification.git',
              credentialsId: 'lzhao'
            sh 'printenv'
            sh 'git submodule update --recursive --init --remote'
            }
        }
    }

    stage('STAGING Building and push image') {
      when {branch "k8s-staging"}
      steps {
        script {
            withCredentials([usernamePassword(credentialsId:'readonly', usernameVariable: 'PIP_USERNAME', passwordVariable: 'PIP_PASSWORD')]) {        
              docker.withRegistry('https://registry-gitlab.indocresearch.org', registryCredential) {
                  customImage = docker.build("registry-gitlab.indocresearch.org/platform/service_notification:$commit", "--build-arg pip_username=${PIP_USERNAME} --build-arg pip_password=${PIP_PASSWORD} --add-host git.indocresearch.org:10.4.3.151 .")
                  customImage.push()
              }
            }
          }
        }
      }
    }

    stage('STAGING Remove image') {
      when {branch "k8s-staging"}
      steps{
        sh "docker rmi $imagename_staging:$commit"
      }
    }

    stage('STAGING Deploy') {
      when {branch "k8s-staging"}
      steps{
        sh "sed -i 's/<VERSION>/$commit/g' kubernetes/staging-deployment.yaml"
        sh "kubectl config use-context staging"
        sh "kubectl apply -f kubernetes/staging-deployment.yaml"
      }
    }
  }
  post {
      failure {
        slackSend color: '#FF0000', message: "Build Failed! - ${env.JOB_NAME} $commit  (<${env.BUILD_URL}|Open>)", channel: 'jenkins-dev-staging-monitor'
      }
  }

}
