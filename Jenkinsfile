// ==============================================================================
// Jenkins CI/CD Declarative Pipeline: Jenkinsfile
// Project: CLOUD INFRASTRUCTURE MONITORING AND AUTOMATED ALERT SYSTEM
// Flow: Checkout -> Docker Build -> Pytest (in Docker) -> Deploy with Ansible
// ==============================================================================

pipeline {
    agent any

    environment {
        IMAGE_NAME     = "cloud-monitoring-ci"
        CONTAINER_NAME = "cloud-monitoring-ansible"
        HOST_PORT      = "5002"
        CONTAINER_PORT = "5000"
        VOLUME_NAME    = "cloud_monitoring_data"
        PLAYBOOK_FILE  = "cloud-monitoring-deploy.yml"
        INVENTORY_FILE = "inventory.ini"
    }

    options {
        timestamps()
        timeout(time: 20, unit: 'MINUTES')
        ansiColor('xterm')
    }

    stages {
        // Stage 1: Source Code Checkout
        stage('Stage 1 — Checkout') {
            steps {
                echo "============================================================"
                echo " [CI/CD] STAGE 1: Checking out latest source code repository"
                echo "============================================================"
                checkout scm
                script {
                    echo "[*] Git Commit: ${env.GIT_COMMIT ?: 'Local/Workspace'}"
                    echo "[*] Git Branch: ${env.GIT_BRANCH ?: 'main'}"
                }
            }
        }

        // Stage 2: Docker Image Build
        stage('Stage 2 — Build') {
            steps {
                echo "============================================================"
                echo " [CI/CD] STAGE 2: Building Docker image '${IMAGE_NAME}'"
                echo "============================================================"
                script {
                    // Build container image using Dockerfile
                    sh "docker build -t ${IMAGE_NAME} ."
                }
            }
        }

        // Stage 3: Automated Pytest in Built Image
        stage('Stage 3 — Test') {
            steps {
                echo "============================================================"
                echo " [CI/CD] STAGE 3: Running automated tests inside Docker container"
                echo "============================================================"
                script {
                    // Run pytest test suite inside newly built Docker image
                    sh "docker run --rm ${IMAGE_NAME} python -m pytest test_app.py -v"
                }
            }
        }

        // Stage 4: Deploy with Ansible
        stage('Stage 4 — Deploy with Ansible') {
            steps {
                echo "============================================================"
                echo " [CI/CD] STAGE 4: Deploying container via Ansible Playbook"
                echo "============================================================"
                script {
                    // Invoke configured Ansible playbook for idempotent deployment
                    echo "[*] Executing: ansible-playbook -i ${INVENTORY_FILE} ${PLAYBOOK_FILE}"
                    sh "ansible-playbook -i ${INVENTORY_FILE} ${PLAYBOOK_FILE}"
                }
            }
        }
    }

    post {
        success {
            echo "============================================================"
            echo " [CI/CD] SUCCESS: Pipeline completed all stages successfully!"
            echo " [*] Image:     ${IMAGE_NAME}"
            echo " [*] Container: ${CONTAINER_NAME}"
            echo " [*] URL:       http://localhost:${HOST_PORT}/dashboard"
            echo " [*] Health:    http://localhost:${HOST_PORT}/health"
            echo " [*] Storage:   Docker Volume '${VOLUME_NAME}' (/app/data)"
            echo "============================================================"
        }
        failure {
            echo "============================================================"
            echo " [CI/CD] FAILURE: Pipeline execution encountered an error."
            echo " Check the console log above for step failure diagnostics."
            echo "============================================================"
        }
        always {
            echo "[*] Jenkins pipeline execution concluded."
        }
    }
}
